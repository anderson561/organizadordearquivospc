import os
import re
import shutil
import logging
from typing import Dict, Iterable, List, NamedTuple, Optional
from tenacity import retry, stop_after_attempt, wait_exponential
from document_terms import TERMS
from strategies import (BaseStrategy, DocumentTitleStrategy, CompanyNameStrategy,
                        sanitize_path_component)
from version import __version__

# Configuração de Logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# Todo arquivo reconhecido vai para dentro desta pasta unica, e nao direto
# na raiz escolhida. Antes cada categoria (DARFs, Notas Fiscais, JPG...)
# nascia solta ali, misturada com o que ja existia na pasta - em Downloads,
# uma dezena de pastas novas ao lado de tudo que ja estava la. Com a pasta
# guarda-chuva, a raiz ganha uma unica entrada nova.
ORGANIZED_ROOT_NAME = "Arquivos Organizados"


class FilePlan(NamedTuple):
    """O destino decidido para um arquivo, antes de qualquer movimentação."""
    name: str
    path: str
    title: str                  # título detectado (vazio para não-PDF)
    folder: Optional[str]       # subpasta de destino
    recognized: bool            # True se um termo do vocabulário casou
    origin: str = ""            # subpasta de origem, relativa a pasta escolhida
    legacy: bool = False        # veio de uma pasta criada por versao anterior

    @property
    def display_name(self) -> str:
        """Nome com a subpasta de origem, quando houver."""
        return os.path.join(self.origin, self.name) if self.origin else self.name


# Pastas de categoria que as versoes anteriores a 1.6.0 criavam soltas na
# raiz: os nomes do vocabulario, a pasta de erro de leitura e as pastas por
# extensao (PDF, JPG...). Sao migradas para dentro de ORGANIZED_ROOT_NAME.
_LEGACY_TERM_FOLDERS = frozenset(
    {sanitize_path_component(t.folder_name) for t in TERMS} | {DocumentTitleStrategy.ERROR_FOLDER}
)
_EXTENSION_FOLDER = re.compile(r"[A-Z0-9]{1,10}")


def _is_legacy_folder(dir_path: str) -> bool:
    """True se a pasta tem a forma exata de uma pasta criada pelo programa.

    Conservador de proposito - uma pasta do usuario nunca pode ser esvaziada
    por engano. Exige: nenhuma subpasta, pelo menos um arquivo e
      - nome identico a uma categoria do vocabulario ("DARFs", "Certidões"), ou
      - nome de extensao em maiusculas ("PDF") com TODOS os arquivos daquela
        extensao. Uma pasta "Documentos" ou "ABR" nunca casa.
    """
    name = os.path.basename(dir_path)
    try:
        entries = os.listdir(dir_path)
    except OSError:
        return False
    if any(os.path.isdir(os.path.join(dir_path, e)) for e in entries) or not entries:
        return False
    if name in _LEGACY_TERM_FOLDERS:
        return True
    if not _EXTENSION_FOLDER.fullmatch(name):
        return False
    return all(os.path.splitext(e)[1].lower() == "." + name.lower() for e in entries)


class Summary(NamedTuple):
    """O que aconteceu numa execução."""
    analisados: int
    movidos: int
    falhas: int

class FileOrganizer:
    def __init__(self, base_path: str, dry_run: bool = True, include_subfolders: bool = False):
        # base_path e obrigatorio: um padrao embutido apontava para a Area de
        # Trabalho de uma maquina especifica - caminho pessoal num repositorio
        # publico, e uma pasta que nao existe em nenhum outro computador.
        self.dry_run = dry_run
        self.base_path = os.path.abspath(base_path)
        # Subpastas do usuario so sao lidas quando pedido: em Downloads elas
        # incluem projetos e instaladores que ninguem quer ver espalhados.
        self.include_subfolders = include_subfolders
        # <base>/Impostos saiu: usava a mesma estrategia que a propria raiz e
        # so gerava um aviso de "caminho nao encontrado" a cada execucao.
        self.paths_and_strategies: Dict[str, BaseStrategy] = {
            os.path.join(self.base_path, "Notas"): CompanyNameStrategy(),
            self.base_path: DocumentTitleStrategy(),
        }

    @staticmethod
    def _free_name(candidate: str, suffix_builder) -> str:
        """Retorna o primeiro nome livre a partir de 'candidate'.

        'suffix_builder(n)' recebe o numero da tentativa (1, 2, 3...) e devolve
        o nome alternativo. Necessario porque o destino "desambiguado" tambem
        pode ja existir - checar apenas uma vez causava sobrescrita silenciosa.
        """
        if not os.path.exists(candidate):
            return candidate

        attempt = 1
        while True:
            alternative = suffix_builder(attempt)
            if not os.path.exists(alternative):
                return alternative
            attempt += 1

    def _resolve_conflicts(self, dest_dir: str):
        """Renomeia arquivos que ocupam o lugar de pastas no caminho de destino."""
        # No Windows, removemos o drive para iterar nas pastas
        drive, path_parts = os.path.splitdrive(dest_dir)
        path_acc = drive + os.sep

        for part in path_parts.strip(os.sep).split(os.sep):
            path_acc = os.path.join(path_acc, part)
            if os.path.exists(path_acc) and os.path.isfile(path_acc):
                # Conflito fatal: existe um arquivo onde deveria ser uma pasta.
                # O nome de quarentena precisa ser unico: se '_CONFLITO_F_P' ja
                # existisse, o os.rename falhava e o arquivo nunca era movido.
                blocked = path_acc
                quarantine = self._free_name(
                    blocked + "_CONFLITO_F_P",
                    lambda n, b=blocked: f"{b}_CONFLITO_F_P_{n}",
                )
                logger.warning(f"CONFLITO DETECTADO: O arquivo '{blocked}' impede a criacao da pasta. Renomeando para '{os.path.basename(quarantine)}' para prosseguir.")
                os.rename(blocked, quarantine)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def _move_file(self, source: str, destination: str):
        # Garantir caminhos absolutos
        abs_source = os.path.abspath(source)
        abs_dest = os.path.abspath(destination)

        if self.dry_run:
            logger.info(f"[DRY RUN] Moveria: {abs_source} -> {abs_dest}")
            return

        dest_dir = os.path.dirname(abs_dest)

        try:
            # Validacao de conflitos (arquivo bloqueando pasta)
            self._resolve_conflicts(dest_dir)

            os.makedirs(dest_dir, exist_ok=True)

            # Evita sobrescrever: desambigua com o mtime e, se preciso, com um
            # contador. shutil.move sobrescreve o destino no Windows, entao o
            # nome final precisa estar garantidamente livre.
            base, ext = os.path.splitext(abs_dest)

            def alternative(attempt: int) -> str:
                # O mtime so e lido quando existe colisao de verdade.
                stamp = int(os.path.getmtime(abs_source))
                if attempt == 1:
                    return f"{base}_{stamp}{ext}"
                return f"{base}_{stamp}_{attempt - 1}{ext}"

            abs_dest = self._free_name(abs_dest, alternative)

            # Ultima barreira contra perda de dados: nunca sobrescrever.
            if os.path.exists(abs_dest):
                raise FileExistsError(f"Destino ja existe, movimentacao abortada: {abs_dest}")

            shutil.move(abs_source, abs_dest)
            logger.info(f"MOVIDO: {os.path.basename(abs_source)} -> {abs_dest}")
        except Exception as e:
            logger.error(f"FALHA AO MOVER '{os.path.basename(abs_source)}': {str(e)}")
            raise # Relanca para o retry se necessario

    @staticmethod
    def _files_in(dir_path: str) -> List[str]:
        return [os.path.join(dir_path, item) for item in sorted(os.listdir(dir_path))
                if os.path.isfile(os.path.join(dir_path, item))]

    def _subfolders(self) -> List[str]:
        """Subpastas diretas da raiz que podem conter arquivos a organizar."""
        reserved = {ORGANIZED_ROOT_NAME} | {os.path.basename(p) for p in self.paths_and_strategies
                                            if p != self.base_path}
        return [os.path.join(self.base_path, name) for name in sorted(os.listdir(self.base_path))
                if name not in reserved and not name.startswith((".", "$"))
                and os.path.isdir(os.path.join(self.base_path, name))
                and not os.path.islink(os.path.join(self.base_path, name))]

    def _iter_files(self):
        """Percorre (estrategia, caminho, pasta legada) de cada arquivo elegivel.

        Ordem: arquivos soltos da raiz e de Notas; depois as pastas de categoria
        de versoes anteriores (sempre migradas); por fim, se pedido, as demais
        subpastas, em qualquer profundidade.
        """
        for root_path, strategy in self.paths_and_strategies.items():
            if os.path.exists(root_path):
                for source_path in self._files_in(root_path):
                    yield strategy, source_path, None

        if not os.path.exists(self.base_path):
            return
        title_strategy = self.paths_and_strategies.get(self.base_path) or DocumentTitleStrategy()
        others = []
        for sub in self._subfolders():
            if _is_legacy_folder(sub):
                for source_path in self._files_in(sub):
                    yield title_strategy, source_path, os.path.basename(sub)
            else:
                others.append(sub)

        if self.include_subfolders:
            for sub in others:
                for dir_path, dir_names, file_names in os.walk(sub):
                    dir_names[:] = sorted(d for d in dir_names if not d.startswith((".", "$")))
                    for file_name in sorted(file_names):
                        yield title_strategy, os.path.join(dir_path, file_name), None

    def _plan_for(self, strategy: BaseStrategy, source_path: str,
                  legacy_folder: Optional[str] = None) -> FilePlan:
        """Decide o destino de um arquivo, sem mover nada.

        Arquivo de pasta legada so e reclassificado "para cima": se o
        vocabulario o reconhece, ganha a categoria nova; senao, mantem a pasta
        em que ja estava - nunca e rebaixado para a pasta por extensao.
        """
        name = os.path.basename(source_path)
        title = ""
        recognized = True

        if isinstance(strategy, DocumentTitleStrategy):
            try:
                folder, region = strategy.classify(source_path)
                title = region.display
            except Exception as exc:
                folder, title = None, f"<falha na leitura: {exc}>"
            recognized = folder is not None
            destination = (folder or legacy_folder
                           or strategy.fallback.get_destination_subpath(source_path))
        else:
            destination = strategy.get_destination_subpath(source_path)

        origin = os.path.relpath(os.path.dirname(source_path), self.base_path)
        return FilePlan(name, source_path, title, destination, recognized,
                        "" if origin == os.curdir else origin, legacy_folder is not None)

    def classify_all(self, progress=None, cancel=None) -> List[FilePlan]:
        """Classifica todos os arquivos e devolve os planos, sem mover nada.

        'progress(feitos, total, plano)' e chamado a cada arquivo e 'cancel()'
        e consultado antes de cada um - e assim que a interface grafica mostra
        andamento e permite interromper sem travar a janela.
        """
        files = list(self._iter_files())
        total = len(files)
        plans: List[FilePlan] = []

        for index, (strategy, source_path, legacy_folder) in enumerate(files, start=1):
            if cancel and cancel():
                break
            plan = self._plan_for(strategy, source_path, legacy_folder)
            plans.append(plan)
            if progress:
                progress(index, total, plan)

        return plans

    def apply_plans(self, plans: Iterable[FilePlan], progress=None, cancel=None) -> Summary:
        """Executa a movimentacao de planos ja classificados.

        Separado de classify_all para que a interface nao precise reler os PDFs
        depois da analise - com centenas de arquivos, reler dobraria a espera.
        """
        plans = list(plans)
        movidos = falhas = 0

        for index, plan in enumerate(plans, start=1):
            if cancel and cancel():
                break

            if plan.folder:
                # Destino ancorado na pasta ESCOLHIDA, nao na pasta do arquivo:
                # arquivos de <base>/Notas tambem vao para o unico
                # <base>/Arquivos Organizados, em vez de criar um segundo
                # guarda-chuva dentro da subpasta.
                dest_path = os.path.join(self.base_path, ORGANIZED_ROOT_NAME, plan.folder, plan.name)

                # Evita mover para dentro de si mesmo se já estiver na pasta certa
                if os.path.abspath(plan.path) != os.path.abspath(dest_path):
                    try:
                        self._move_file(plan.path, dest_path)
                        movidos += 1
                    except Exception as e:
                        falhas += 1
                        logger.error(f"Erro ao mover {plan.name}: {e}")

            if progress:
                progress(index, len(plans), plan)

        if not self.dry_run:
            self._remove_emptied_legacy_folders(plans)
        summary = Summary(len(plans), movidos, falhas)
        self._log_summary(*summary)
        return summary

    @staticmethod
    def _remove_emptied_legacy_folders(plans: List[FilePlan]):
        """Remove as pastas legadas que a migracao deixou vazias.

        So pastas legadas, e so se vazias (os.rmdir recusa pasta com conteudo):
        uma pasta de onde algum arquivo falhou ao sair continua la.
        """
        for folder in sorted({os.path.dirname(p.path) for p in plans if p.legacy}):
            try:
                if not os.listdir(folder):
                    os.rmdir(folder)
                    logger.info(f"Pasta antiga vazia removida: {folder}")
            except OSError as exc:
                logger.warning(f"Pasta antiga mantida ({folder}): {exc}")

    def report(self):
        """Imprime a classificacao de cada arquivo sem mover nada (uso no CLI)."""
        plans = self.classify_all()
        unrecognized = [p for p in plans if not p.recognized]

        width = max((len(p.display_name) for p in plans), default=8)
        print(f"\nClassificacao de {len(plans)} arquivo(s) em {self.base_path}\n")
        print(f"Os reconhecidos vao para dentro de {ORGANIZED_ROOT_NAME!r}, na subpasta indicada em PASTA.\n")
        print(f"{'ARQUIVO'.ljust(width)}  {'TITULO DETECTADO'.ljust(40)}  PASTA")
        print(f"{'-' * width}  {'-' * 40}  {'-' * 20}")
        for plan in plans:
            print(f"{plan.display_name.ljust(width)}  {plan.title[:40].ljust(40)}  {plan.folder}")

        if unrecognized:
            print(f"\n{len(unrecognized)} arquivo(s) sem termo reconhecido "
                  f"(caem na pasta por extensao):")
            for plan in unrecognized:
                print(f"  - {plan.display_name}: {plan.title[:60]!r}")
            print("\nPara classificar estes, acrescente o termo em src/document_terms.py")

        return plans

    def organize(self, progress=None, cancel=None) -> Summary:
        logger.info(f"Iniciando organização no diretório: {self.base_path} (Modo Simulação: {self.dry_run})")

        for root_path in self.paths_and_strategies:
            if not os.path.exists(root_path):
                # Notas e opcional: a ausencia dela nao e problema.
                if root_path == self.base_path:
                    logger.warning(f"Caminho não encontrado: {root_path}")
            else:
                logger.info(f"Processando diretório: {root_path}")

        plans = self.classify_all(cancel=cancel)
        return self.apply_plans(plans, progress=progress, cancel=cancel)

    def _log_summary(self, analisados: int, movidos: int, falhas: int):
        """Fecha a execucao dizendo o que de fato aconteceu.

        Sem isso, uma simulacao parece uma execucao que nao funcionou: o padrao
        e dry_run, entao quem roda pelo atalho ou pelo seletor de pasta ve um
        monte de log e nenhum arquivo movido.
        """
        if self.dry_run:
            logger.warning(
                f"SIMULACAO CONCLUIDA: {analisados} arquivo(s) analisado(s), "
                f"{movidos} seriam movidos. NENHUM arquivo foi movido de verdade."
            )
            logger.warning(
                "Para mover os arquivos, rode novamente com --real "
                "(ou use a interface grafica, que mostra a tabela antes de mover)."
            )
        else:
            logger.info(
                f"CONCLUIDO: {analisados} arquivo(s) analisado(s), "
                f"{movidos} movido(s), {falhas} falha(s)."
            )

if __name__ == "__main__":
    import argparse
    import sys
    import tkinter as tk
    from tkinter import filedialog

    parser = argparse.ArgumentParser(description="Organizador Avançado de Arquivos")
    parser.add_argument("--version", action="version", version=f"Organizador Avançado de Arquivos {__version__}")
    parser.add_argument("--path", type=str, default=None, help="Caminho da pasta a ser organizada")
    parser.add_argument("--real", action="store_true", help="Executa a movimentação real dos arquivos (caso contrário, apenas simula)")
    parser.add_argument("--report", action="store_true", help="Apenas lista o título detectado e a pasta de destino de cada arquivo, sem mover nada")
    parser.add_argument("--subpastas", action="store_true", help="Inclui os arquivos das subpastas, em qualquer profundidade")
    args = parser.parse_args()

    # If no path provided, open a folder selection dialog
    if not args.path:
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        selected_path = filedialog.askdirectory(title="Selecione a pasta a ser organizada")
        if not selected_path:
            logger.error("Nenhum caminho selecionado. Encerrando.")
            sys.exit(1)
        args.path = selected_path

    organizer = FileOrganizer(base_path=args.path, dry_run=not args.real,
                              include_subfolders=args.subpastas)
    if args.report:
        organizer.report()
    else:
        organizer.organize()
