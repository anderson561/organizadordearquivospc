import os
import shutil
import logging
from typing import Dict, Iterable, List, NamedTuple, Optional
from tenacity import retry, stop_after_attempt, wait_exponential
from strategies import BaseStrategy, DocumentTitleStrategy, CompanyNameStrategy

# Configuração de Logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class FilePlan(NamedTuple):
    """O destino decidido para um arquivo, antes de qualquer movimentação."""
    name: str
    path: str
    title: str                  # título detectado (vazio para não-PDF)
    folder: Optional[str]       # subpasta de destino
    recognized: bool            # True se um termo do vocabulário casou


class Summary(NamedTuple):
    """O que aconteceu numa execução."""
    analisados: int
    movidos: int
    falhas: int

class FileOrganizer:
    def __init__(self, base_path: str = r"C:\Users\ANDERSON\Desktop", dry_run: bool = True):
        self.dry_run = dry_run
        self.base_path = os.path.abspath(base_path)
        self.paths_and_strategies: Dict[str, BaseStrategy] = {
            os.path.join(self.base_path, "Impostos"): DocumentTitleStrategy(),
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

    def _iter_files(self):
        """Percorre (pasta, estrategia, caminho) de cada arquivo elegivel."""
        for root_path, strategy in self.paths_and_strategies.items():
            if not os.path.exists(root_path):
                continue
            for item in sorted(os.listdir(root_path)):
                source_path = os.path.join(root_path, item)
                if os.path.isfile(source_path):
                    yield root_path, strategy, source_path

    def _plan_for(self, strategy: BaseStrategy, source_path: str) -> FilePlan:
        """Decide o destino de um arquivo, sem mover nada."""
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
            destination = folder or strategy.fallback.get_destination_subpath(source_path)
        else:
            destination = strategy.get_destination_subpath(source_path)

        return FilePlan(name, source_path, title, destination, recognized)

    def classify_all(self, progress=None, cancel=None) -> List[FilePlan]:
        """Classifica todos os arquivos e devolve os planos, sem mover nada.

        'progress(feitos, total, plano)' e chamado a cada arquivo e 'cancel()'
        e consultado antes de cada um - e assim que a interface grafica mostra
        andamento e permite interromper sem travar a janela.
        """
        files = list(self._iter_files())
        total = len(files)
        plans: List[FilePlan] = []

        for index, (_, strategy, source_path) in enumerate(files, start=1):
            if cancel and cancel():
                break
            plan = self._plan_for(strategy, source_path)
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
                root_path = os.path.dirname(plan.path)
                dest_path = os.path.join(root_path, plan.folder, plan.name)

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

        summary = Summary(len(plans), movidos, falhas)
        self._log_summary(*summary)
        return summary

    def report(self):
        """Imprime a classificacao de cada arquivo sem mover nada (uso no CLI)."""
        plans = self.classify_all()
        unrecognized = [p for p in plans if not p.recognized]

        width = max((len(p.name) for p in plans), default=8)
        print(f"\nClassificacao de {len(plans)} arquivo(s) em {self.base_path}\n")
        print(f"{'ARQUIVO'.ljust(width)}  {'TITULO DETECTADO'.ljust(40)}  PASTA")
        print(f"{'-' * width}  {'-' * 40}  {'-' * 20}")
        for plan in plans:
            print(f"{plan.name.ljust(width)}  {plan.title[:40].ljust(40)}  {plan.folder}")

        if unrecognized:
            print(f"\n{len(unrecognized)} arquivo(s) sem termo reconhecido "
                  f"(caem na pasta por extensao):")
            for plan in unrecognized:
                print(f"  - {plan.name}: {plan.title[:60]!r}")
            print("\nPara classificar estes, acrescente o termo em src/document_terms.py")

        return plans

    def organize(self, progress=None, cancel=None) -> Summary:
        logger.info(f"Iniciando organização no diretório: {self.base_path} (Modo Simulação: {self.dry_run})")

        for root_path in self.paths_and_strategies:
            if not os.path.exists(root_path):
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
                "(ou use o atalho executar_real.bat)."
            )
        else:
            logger.info(
                f"CONCLUIDO: {analisados} arquivo(s) analisado(s), "
                f"{movidos} movido(s), {falhas} falha(s)."
            )

if __name__ == "__main__":
    import argparse
    import tkinter as tk
    from tkinter import filedialog

    parser = argparse.ArgumentParser(description="Organizador Avançado de Arquivos")
    parser.add_argument("--path", type=str, default=None, help="Caminho da pasta a ser organizada")
    parser.add_argument("--real", action="store_true", help="Executa a movimentação real dos arquivos (caso contrário, apenas simula)")
    parser.add_argument("--report", action="store_true", help="Apenas lista o título detectado e a pasta de destino de cada arquivo, sem mover nada")
    args = parser.parse_args()

    # If no path provided, open a folder selection dialog
    if not args.path:
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        selected_path = filedialog.askdirectory(title="Selecione a pasta a ser organizada")
        if not selected_path:
            logger.error("Nenhum caminho selecionado. Encerrando.")
            exit(1)
        args.path = selected_path

    organizer = FileOrganizer(base_path=args.path, dry_run=not args.real)
    if args.report:
        organizer.report()
    else:
        organizer.organize()
