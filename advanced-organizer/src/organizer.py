import os
import shutil
import logging
from typing import Dict
from tenacity import retry, stop_after_attempt, wait_exponential
from strategies import BaseStrategy, TypeStrategy, ImpostoStrategy, CompanyNameStrategy

# Configuração de Logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FileOrganizer:
    def __init__(self, base_path: str = r"C:\Users\ANDERSON\Desktop", dry_run: bool = True):
        self.dry_run = dry_run
        self.base_path = os.path.abspath(base_path)
        self.paths_and_strategies: Dict[str, BaseStrategy] = {
            os.path.join(self.base_path, "Impostos"): ImpostoStrategy(),
            os.path.join(self.base_path, "Notas"): CompanyNameStrategy(),
            self.base_path: TypeStrategy(),
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

    def organize(self):
        logger.info(f"Iniciando organização no diretório: {self.base_path} (Modo Simulação: {self.dry_run})")
        
        for root_path, strategy in self.paths_and_strategies.items():
            if not os.path.exists(root_path):
                logger.warning(f"Caminho não encontrado: {root_path}")
                continue

            logger.info(f"Processando diretório: {root_path}")
            
            # Lista apenas os arquivos no diretório atual (não recursivo para o Desktop geral)
            for item in os.listdir(root_path):
                source_path = os.path.join(root_path, item)
                
                if os.path.isfile(source_path):
                    sub_path = strategy.get_destination_subpath(source_path)
                    
                    if sub_path:
                        dest_path = os.path.join(root_path, sub_path, item)
                        
                        # Evita mover para dentro de si mesmo se já estiver na pasta certa
                        if os.path.abspath(source_path) == os.path.abspath(dest_path):
                            continue
                            
                        try:
                            self._move_file(source_path, dest_path)
                        except Exception as e:
                            logger.error(f"Erro ao mover {item}: {e}")

if __name__ == "__main__":
    import argparse
    import tkinter as tk
    from tkinter import filedialog

    parser = argparse.ArgumentParser(description="Organizador Avançado de Arquivos")
    parser.add_argument("--path", type=str, default=None, help="Caminho da pasta a ser organizada")
    parser.add_argument("--real", action="store_true", help="Executa a movimentação real dos arquivos (caso contrário, apenas simula)")
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
    organizer.organize()
