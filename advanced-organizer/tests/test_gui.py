"""Testes da interface grafica.

Dois niveis:

1. A camada de dados que a interface consome (classify_all / apply_plans), que
   nao depende de widget algum - e onde vive a garantia de que "Analisar" nao
   move nada e de que cancelar interrompe.
2. Um smoke test de construcao da janela, que so roda se houver display. Ele
   nao substitui teste manual de interacao; garante que a montagem dos widgets
   e o estado inicial dos botoes nao quebraram.
"""
import os
import shutil
import sys
import tempfile
import threading
import unittest
import unittest.mock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
sys.path.append(os.path.dirname(__file__))

from pdf_fixtures import build_pdf
from organizer import FileOrganizer, FilePlan, Summary, ORGANIZED_ROOT_NAME


def _criar_root():
    """Cria o unico root do Tk do processo, ou None se nao houver Tk usavel.

    Neste ambiente (Python da Microsoft Store dentro de venv) apenas UM
    interpretador Tcl pode ser criado por processo: o segundo falha com
    "Can't find a usable init.tcl". Por isso o root e criado uma vez, nunca
    destruido, e compartilhado por todos os testes de janela.
    """
    try:
        import tkinter
        root = tkinter.Tk()
        root.withdraw()
        return root
    except Exception:
        return None


_ROOT = _criar_root()


class TestCamadaDeDados(unittest.TestCase):
    """O que a interface chama nas threads de trabalho."""

    def setUp(self):
        self.base = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.base, ignore_errors=True)
        build_pdf(os.path.join(self.base, "guia darf.pdf"), ["Documento de Arrecadação"])
        build_pdf(os.path.join(self.base, "rel.pdf"), ["RELATÓRIO MENSAL"])
        build_pdf(os.path.join(self.base, "outro.pdf"), ["Documento generico"])

    def _organizer(self, dry_run=True):
        return FileOrganizer(base_path=self.base, dry_run=dry_run)

    def test_classify_all_nao_move_nada(self):
        antes = sorted(os.listdir(self.base))
        plans = self._organizer().classify_all()
        self.assertEqual(sorted(os.listdir(self.base)), antes)
        self.assertEqual(len(plans), 3)
        self.assertTrue(all(isinstance(p, FilePlan) for p in plans))

    def test_classify_all_reporta_progresso(self):
        eventos = []
        plans = self._organizer().classify_all(
            progress=lambda feitos, total, plan: eventos.append((feitos, total, plan.name))
        )
        self.assertEqual(len(eventos), len(plans))
        self.assertEqual([e[0] for e in eventos], [1, 2, 3])
        self.assertTrue(all(e[1] == 3 for e in eventos))

    def test_classify_all_respeita_cancelamento(self):
        cancelar = threading.Event()
        cancelar.set()
        plans = self._organizer().classify_all(cancel=cancelar.is_set)
        self.assertEqual(plans, [])

    def test_cancelamento_no_meio_interrompe(self):
        vistos = []
        cancelar = threading.Event()

        def progresso(feitos, total, plan):
            vistos.append(plan.name)
            if feitos == 1:
                cancelar.set()

        plans = self._organizer().classify_all(progress=progresso, cancel=cancelar.is_set)
        self.assertEqual(len(plans), 1, "deveria parar no arquivo seguinte ao cancelamento")
        self.assertEqual(len(vistos), 1)

    def test_marca_o_que_nao_foi_reconhecido(self):
        por_nome = {p.name: p for p in self._organizer().classify_all()}
        self.assertTrue(por_nome["guia darf.pdf"].recognized)
        self.assertEqual(por_nome["guia darf.pdf"].folder, "DARFs")
        self.assertFalse(por_nome["outro.pdf"].recognized)
        self.assertEqual(por_nome["outro.pdf"].folder, "PDF")

    def test_apply_plans_move_sem_reler_os_pdfs(self):
        plans = self._organizer().classify_all()
        summary = self._organizer(dry_run=False).apply_plans(plans)

        self.assertIsInstance(summary, Summary)
        self.assertEqual(summary.movidos, 3)
        self.assertEqual(summary.falhas, 0)
        raiz = os.path.join(self.base, ORGANIZED_ROOT_NAME)
        self.assertEqual(os.listdir(os.path.join(raiz, "DARFs")), ["guia darf.pdf"])
        self.assertEqual(os.listdir(os.path.join(raiz, "Relatórios")), ["rel.pdf"])

    def test_apply_plans_em_dry_run_nao_move(self):
        plans = self._organizer().classify_all()
        antes = sorted(os.listdir(self.base))
        summary = self._organizer(dry_run=True).apply_plans(plans)
        self.assertEqual(sorted(os.listdir(self.base)), antes)
        self.assertEqual(summary.analisados, 3)

    def test_apply_plans_move_apenas_o_subconjunto_recebido(self):
        """A interface envia so os planos com pasta definida."""
        plans = [p for p in self._organizer().classify_all() if p.recognized]
        self._organizer(dry_run=False).apply_plans(plans)
        self.assertIn("outro.pdf", os.listdir(self.base))


class TestLogicaSemJanela(unittest.TestCase):
    """Metodos estaticos da interface: testaveis sem criar widget algum."""

    def test_resumo_agrupa_por_pasta(self):
        from gui import OrganizerApp
        plans = [
            FilePlan("a.pdf", "a", "DARF", "DARFs", True),
            FilePlan("b.pdf", "b", "DARF", "DARFs", True),
            FilePlan("c.pdf", "c", "", "PDF", False),
        ]
        texto = OrganizerApp._describe(plans, cancelado=False)
        self.assertIn("3 arquivo(s)", texto)
        self.assertIn("2 DARFs", texto)
        self.assertIn("1 sem termo reconhecido", texto)

    def test_resumo_sinaliza_cancelamento(self):
        from gui import OrganizerApp
        texto = OrganizerApp._describe([FilePlan("a", "a", "", "PDF", False)], cancelado=True)
        self.assertIn("cancelada", texto.lower())

    def test_resumo_de_pasta_vazia(self):
        from gui import OrganizerApp
        self.assertIn("Nenhum arquivo", OrganizerApp._describe([], cancelado=False))

    def test_detecta_pasta_de_sistema(self):
        from gui import OrganizerApp
        self.assertTrue(OrganizerApp._is_system_dir(r"C:\Windows\System32"))
        self.assertTrue(OrganizerApp._is_system_dir(r"C:\Program Files\App"))
        self.assertFalse(OrganizerApp._is_system_dir(r"C:\Users\ANDERSON\Downloads"))


@unittest.skipUnless(_ROOT is not None, "sem Tk utilizavel neste ambiente")
class TestJanela(unittest.TestCase):
    """Smoke test dos widgets, sobre o root compartilhado do modulo."""

    def setUp(self):
        from gui import OrganizerApp
        self.root = _ROOT
        # Limpa os widgets do teste anterior antes de remontar a janela.
        for child in self.root.winfo_children():
            child.destroy()
        self.app = OrganizerApp(self.root)

    def test_estado_inicial_bloqueia_movimentacao(self):
        self.assertEqual(self.app.state, "inicial")
        self.assertIn("disabled", self.app.move_btn.state())
        self.assertIn("disabled", self.app.cancel_btn.state())
        self.assertNotIn("disabled", self.app.analyze_btn.state())

    def test_mover_continua_bloqueado_sem_analise(self):
        self.app.plans = []
        self.app._set_state("analisado")
        self.assertIn("disabled", self.app.move_btn.state())

    def test_mover_libera_apos_analise_com_resultado(self):
        self.app.plans = [FilePlan("a.pdf", "/tmp/a.pdf", "DARF", "DARFs", True)]
        self.app._set_state("analisado")
        self.assertNotIn("disabled", self.app.move_btn.state())

    def test_durante_execucao_bloqueia_reentrancia(self):
        self.app._set_state("analisando")
        self.assertIn("disabled", self.app.analyze_btn.state())
        self.assertIn("disabled", self.app.browse_btn.state())
        self.assertNotIn("disabled", self.app.cancel_btn.state())

    def test_fluxo_completo_analisar_e_mover(self):
        """Analisa e move de verdade, drenando a fila como o mainloop faria.

        Os dialogos modais sao neutralizados: sem isso o messagebox final trava
        o teste para sempre, esperando um clique que nunca vem.
        """
        import gui
        base = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, base, ignore_errors=True)
        build_pdf(os.path.join(base, "guia darf.pdf"), ["Documento de Arrecadação"])
        build_pdf(os.path.join(base, "rel.pdf"), ["RELATÓRIO MENSAL"])

        with unittest.mock.patch.object(gui.messagebox, "showinfo"), \
             unittest.mock.patch.object(gui.messagebox, "askyesno", return_value=True):
            self.app.path_var.set(base)

            self.app._start_analysis()
            self._drain(lambda: self.app.state == "analisando")
            self.assertEqual(len(self.app.plans), 2)
            self.assertEqual(sorted(os.listdir(base)), ["guia darf.pdf", "rel.pdf"],
                             "a analise nao pode mover nada")

            self.app._start_move()
            self._drain(lambda: self.app.state == "movendo")

        raiz = os.path.join(base, ORGANIZED_ROOT_NAME)
        self.assertEqual(os.listdir(os.path.join(raiz, "DARFs")), ["guia darf.pdf"])
        self.assertEqual(os.listdir(os.path.join(raiz, "Relatórios")), ["rel.pdf"])
        self.assertIn("2 arquivo(s) movido(s)", self.app.summary_var.get())

    def _drain(self, still_running, timeout=60):
        import time
        limite = time.time() + timeout
        while still_running() and time.time() < limite:
            self.root.update()
            self.app._pump()
            time.sleep(0.01)
        self.assertFalse(still_running(), "a operacao nao terminou no tempo esperado")

    def test_fila_alimenta_a_tabela(self):
        plan = FilePlan("guia.pdf", "g", "Documento de Arrecadação", "DARFs", True)
        self.app._handle(("progresso", 1, 1, plan))
        filhos = self.app.tree.get_children()
        self.assertEqual(len(filhos), 0, "linhas so entram durante a analise")

        self.app._set_state("analisando")
        self.app._handle(("progresso", 1, 1, plan))
        filhos = self.app.tree.get_children()
        self.assertEqual(len(filhos), 1)
        self.assertEqual(self.app.tree.item(filhos[0], "values")[2], "DARFs")


if __name__ == '__main__':
    unittest.main()
