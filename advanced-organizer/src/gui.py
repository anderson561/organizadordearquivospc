"""Interface grafica do Organizador Avancado.

Fluxo deliberadamente em duas etapas: "Analisar" nunca move nada e "Mover
arquivos" so habilita depois de uma analise, com confirmacao declarando a
quantidade. Isso remove pela estrutura o problema do modo simulacao silencioso,
em que a pessoa escolhia a pasta, via texto passando e nada acontecia.

Regra de concorrencia: a leitura dos PDFs roda numa thread de trabalho e os
widgets sao tocados APENAS pela thread principal. A comunicacao passa inteira
por uma fila drenada com root.after().
"""
import os
import queue
import threading
import tkinter as tk
from collections import Counter
from tkinter import filedialog, messagebox, ttk

from organizer import FileOrganizer

POLL_MS = 100          # intervalo de drenagem da fila de eventos
SYSTEM_DIRS = ("windows", "program files", "program files (x86)", "system32")


class OrganizerApp:
    """Janela unica: escolher pasta, analisar, revisar, mover."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.events: "queue.Queue[tuple]" = queue.Queue()
        self.cancel_event = threading.Event()
        self.worker = None
        self.plans = []

        root.title("Organizador Avançado de Arquivos")
        root.minsize(880, 520)
        self._build_widgets()
        self._set_state("inicial")
        # Foco no campo de pasta: dá para digitar ou colar o caminho de imediato.
        self.path_entry.focus_set()
        self.root.after(POLL_MS, self._pump)

    # ------------------------------------------------------------------ UI --
    def _build_widgets(self):
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(2, weight=1)

        top = ttk.Frame(self.root, padding=(12, 12, 12, 6))
        top.grid(row=0, column=0, sticky="ew")
        top.columnconfigure(1, weight=1)

        ttk.Label(top, text="Pasta:").grid(row=0, column=0, padx=(0, 8))
        self.path_var = tk.StringVar()
        self.path_entry = ttk.Entry(top, textvariable=self.path_var)
        self.path_entry.grid(row=0, column=1, sticky="ew")
        # Enter no campo dispara a análise, que é sempre a ação segura.
        self.path_entry.bind("<Return>", lambda _event: self._start_analysis())
        self.browse_btn = ttk.Button(top, text="Procurar...", command=self._choose_folder)
        self.browse_btn.grid(row=0, column=2, padx=(8, 0))

        actions = ttk.Frame(self.root, padding=(12, 0, 12, 6))
        actions.grid(row=1, column=0, sticky="ew")
        self.analyze_btn = ttk.Button(actions, text="Analisar", command=self._start_analysis)
        self.analyze_btn.grid(row=0, column=0)
        self.cancel_btn = ttk.Button(actions, text="Cancelar", command=self._request_cancel)
        self.cancel_btn.grid(row=0, column=1, padx=(8, 0))
        ttk.Label(actions, text="A análise não move nenhum arquivo.").grid(
            row=0, column=2, padx=(16, 0))

        table = ttk.Frame(self.root, padding=(12, 0))
        table.grid(row=2, column=0, sticky="nsew")
        table.columnconfigure(0, weight=1)
        table.rowconfigure(0, weight=1)

        columns = ("arquivo", "titulo", "pasta")
        self.tree = ttk.Treeview(table, columns=columns, show="headings")
        for key, label, width in (("arquivo", "ARQUIVO", 320),
                                  ("titulo", "TÍTULO DETECTADO", 330),
                                  ("pasta", "PASTA", 170)):
            self.tree.heading(key, text=label)
            self.tree.column(key, width=width, anchor="w")
        self.tree.grid(row=0, column=0, sticky="nsew")

        scroll = ttk.Scrollbar(table, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        scroll.grid(row=0, column=1, sticky="ns")
        # Destaca o que nao foi reconhecido pelo vocabulario.
        self.tree.tag_configure("sem_termo", foreground="#8a6d00")

        bottom = ttk.Frame(self.root, padding=(12, 6, 12, 12))
        bottom.grid(row=3, column=0, sticky="ew")
        bottom.columnconfigure(0, weight=1)

        self.summary_var = tk.StringVar(value="Escolha uma pasta e clique em Analisar.")
        ttk.Label(bottom, textvariable=self.summary_var).grid(row=0, column=0, sticky="w")

        self.progress = ttk.Progressbar(bottom, mode="determinate")
        self.progress.grid(row=1, column=0, sticky="ew", pady=(6, 0))
        self.progress_var = tk.StringVar(value="")
        ttk.Label(bottom, textvariable=self.progress_var).grid(row=1, column=1, padx=(8, 0))

        self.move_btn = ttk.Button(bottom, text="Mover arquivos", command=self._start_move)
        self.move_btn.grid(row=2, column=0, sticky="e", pady=(10, 0))

    def _set_state(self, state: str):
        """Habilita apenas o que faz sentido em cada momento."""
        self.state = state
        rodando = state in ("analisando", "movendo")
        self.analyze_btn.state(["disabled"] if rodando else ["!disabled"])
        self.browse_btn.state(["disabled"] if rodando else ["!disabled"])
        self.cancel_btn.state(["!disabled"] if rodando else ["disabled"])
        pode_mover = state == "analisado" and any(p.folder for p in self.plans)
        self.move_btn.state(["!disabled"] if pode_mover else ["disabled"])

    # -------------------------------------------------------------- acoes --
    def _choose_folder(self):
        escolhida = filedialog.askdirectory(title="Selecione a pasta a ser organizada")
        if escolhida:
            self.path_var.set(os.path.normpath(escolhida))
            self._clear_table()

    def _validate_folder(self):
        caminho = self.path_var.get().strip()
        if not caminho:
            messagebox.showwarning("Pasta não informada", "Informe a pasta a ser organizada.")
            return None
        if not os.path.isdir(caminho):
            messagebox.showerror("Pasta inválida", f"A pasta não existe:\n{caminho}")
            return None
        return os.path.abspath(caminho)

    def _clear_table(self):
        self.tree.delete(*self.tree.get_children())
        self.plans = []
        self.summary_var.set("")
        self.progress["value"] = 0
        self.progress_var.set("")

    def _start_analysis(self):
        caminho = self._validate_folder()
        if not caminho:
            return
        self._clear_table()
        self._set_state("analisando")
        self.summary_var.set("Lendo os documentos...")
        self._run_in_worker(self._work_analyze, caminho)

    def _start_move(self):
        movimentaveis = [p for p in self.plans if p.folder]
        caminho = self._validate_folder()
        if not caminho or not movimentaveis:
            return

        if self._is_system_dir(caminho) and not messagebox.askyesno(
            "Pasta de sistema",
            f"{caminho}\n\nEsta parece ser uma pasta de sistema. "
            "Mover arquivos aqui pode quebrar programas instalados.\n\nContinuar?",
        ):
            return

        destinos = len({p.folder for p in movimentaveis})
        if not messagebox.askyesno(
            "Confirmar movimentação",
            f"{len(movimentaveis)} arquivo(s) serão movidos para {destinos} pasta(s) "
            f"dentro de:\n{caminho}\n\nEsta ação move os arquivos de verdade. Continuar?",
        ):
            return

        self._set_state("movendo")
        self.summary_var.set("Movendo arquivos...")
        self._run_in_worker(self._work_move, caminho, movimentaveis)

    def _request_cancel(self):
        self.cancel_event.set()
        self.summary_var.set("Cancelando...")

    @staticmethod
    def _is_system_dir(caminho: str) -> bool:
        partes = {p.lower() for p in caminho.split(os.sep) if p}
        return bool(partes & set(SYSTEM_DIRS))

    # ------------------------------------------------- thread de trabalho --
    def _run_in_worker(self, target, *args):
        self.cancel_event.clear()
        self.worker = threading.Thread(target=target, args=args, daemon=True)
        self.worker.start()

    def _emit(self, *event):
        """Unico canal permitido entre a thread de trabalho e a interface."""
        self.events.put(event)

    def _work_analyze(self, caminho):
        try:
            organizer = FileOrganizer(base_path=caminho, dry_run=True)
            plans = organizer.classify_all(
                progress=lambda feitos, total, plan: self._emit("progresso", feitos, total, plan),
                cancel=self.cancel_event.is_set,
            )
            self._emit("analise_ok", plans, self.cancel_event.is_set())
        except Exception as exc:                     # noqa: BLE001 - a janela precisa reportar
            self._emit("erro", str(exc))

    def _work_move(self, caminho, plans):
        try:
            organizer = FileOrganizer(base_path=caminho, dry_run=False)
            summary = organizer.apply_plans(
                plans,
                progress=lambda feitos, total, plan: self._emit("progresso", feitos, total, plan),
                cancel=self.cancel_event.is_set,
            )
            self._emit("mover_ok", summary, self.cancel_event.is_set())
        except Exception as exc:                     # noqa: BLE001
            self._emit("erro", str(exc))

    # -------------------------------------------- ponte fila -> interface --
    def _pump(self):
        """Drena a fila na thread principal - onde tocar widgets e seguro."""
        try:
            while True:
                event = self.events.get_nowait()
                self._handle(event)
        except queue.Empty:
            pass
        finally:
            self.root.after(POLL_MS, self._pump)

    def _handle(self, event):
        kind = event[0]

        if kind == "progresso":
            feitos, total, plan = event[1], event[2], event[3]
            self.progress["maximum"] = max(total, 1)
            self.progress["value"] = feitos
            self.progress_var.set(f"{feitos}/{total}")
            if self.state == "analisando":
                self._append_row(plan)

        elif kind == "analise_ok":
            self.plans, cancelado = event[1], event[2]
            self._set_state("analisado")
            self.summary_var.set(self._describe(self.plans, cancelado))

        elif kind == "mover_ok":
            summary, cancelado = event[1], event[2]
            self._set_state("inicial")
            prefixo = "Cancelado - " if cancelado else ""
            self.summary_var.set(
                f"{prefixo}{summary.movidos} arquivo(s) movido(s), "
                f"{summary.falhas} falha(s), de {summary.analisados} analisado(s)."
            )
            self.plans = []
            messagebox.showinfo("Concluído", self.summary_var.get())

        elif kind == "erro":
            self._set_state("inicial")
            self.summary_var.set(f"Falhou: {event[1]}")
            messagebox.showerror("Erro", event[1])

    def _append_row(self, plan):
        tags = () if plan.recognized else ("sem_termo",)
        self.tree.insert("", "end", tags=tags,
                         values=(plan.name, plan.title, plan.folder or ""))

    @staticmethod
    def _describe(plans, cancelado: bool) -> str:
        if not plans:
            return "Nenhum arquivo encontrado nesta pasta."
        contagem = Counter(p.folder for p in plans if p.folder)
        destaque = " · ".join(f"{qtd} {pasta}" for pasta, qtd in contagem.most_common(4))
        sem_termo = sum(1 for p in plans if not p.recognized)
        partes = [f"{len(plans)} arquivo(s)"]
        if destaque:
            partes.append(destaque)
        if sem_termo:
            partes.append(f"{sem_termo} sem termo reconhecido")
        prefixo = "Análise cancelada - " if cancelado else ""
        return prefixo + " · ".join(partes)


def main(initial_path: str = ""):
    root = tk.Tk()
    app = OrganizerApp(root)
    if initial_path:
        app.path_var.set(os.path.normpath(initial_path))
    root.mainloop()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Organizador Avançado - interface gráfica")
    parser.add_argument("--path", type=str, default="", help="Pré-preenche a pasta")
    main(parser.parse_args().path)
