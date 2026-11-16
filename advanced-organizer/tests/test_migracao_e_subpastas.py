"""Migracao das pastas de versoes anteriores e leitura opcional de subpastas.

Usam o filesystem real: o que importa aqui e o que sobra no disco depois -
que pasta foi esvaziada, qual foi preservada, para onde cada arquivo foi.
"""
import os
import shutil
import sys
import tempfile
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from organizer import FileOrganizer, ORGANIZED_ROOT_NAME, _is_legacy_folder  # noqa: E402
from pdf_fixtures import build_pdf  # noqa: E402


class _Base(unittest.TestCase):
    def setUp(self):
        self.base = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.base, ignore_errors=True)

    def touch(self, *parts, content="x"):
        path = os.path.join(self.base, *parts)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(content)
        return path

    def pdf(self, *parts, lines=("Relatorio qualquer",)):
        path = os.path.join(self.base, *parts)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        return build_pdf(path, list(lines))

    def organized(self, *parts):
        return os.path.join(self.base, ORGANIZED_ROOT_NAME, *parts)


class TestDeteccaoDePastaLegada(_Base):

    def test_pasta_do_vocabulario_e_legada(self):
        self.touch("DARFs", "a.pdf")
        self.assertTrue(_is_legacy_folder(os.path.join(self.base, "DARFs")))

    def test_pasta_de_extensao_com_todos_os_arquivos_da_extensao(self):
        self.touch("PDF", "a.pdf")
        self.touch("PDF", "b.PDF")
        self.assertTrue(_is_legacy_folder(os.path.join(self.base, "PDF")))

    def test_pasta_de_extensao_misturada_nao_e_legada(self):
        self.touch("PDF", "a.pdf")
        self.touch("PDF", "anotacao.txt")
        self.assertFalse(_is_legacy_folder(os.path.join(self.base, "PDF")))

    def test_pasta_com_subpasta_nao_e_legada(self):
        self.touch("DARFs", "2026", "a.pdf")
        self.touch("DARFs", "b.pdf")
        self.assertFalse(_is_legacy_folder(os.path.join(self.base, "DARFs")))

    def test_pasta_do_usuario_nao_e_legada(self):
        for nome in ("ABR", "Documentos", "xml", "Outros"):
            self.touch(nome, "a.pdf")
            self.assertFalse(_is_legacy_folder(os.path.join(self.base, nome)), nome)

    def test_pasta_vazia_nao_e_legada(self):
        os.makedirs(os.path.join(self.base, "DARFs"))
        self.assertFalse(_is_legacy_folder(os.path.join(self.base, "DARFs")))


class TestMigracaoDeVersoesAnteriores(_Base):

    def test_pastas_antigas_vao_para_o_guarda_chuva_e_somem(self):
        self.pdf("DARFs", "guia.pdf", lines=("Texto sem categoria",))
        self.touch("JPG", "foto.jpg")

        FileOrganizer(base_path=self.base, dry_run=False).organize()

        self.assertTrue(os.path.isfile(self.organized("DARFs", "guia.pdf")))
        self.assertTrue(os.path.isfile(self.organized("JPG", "foto.jpg")))
        self.assertFalse(os.path.exists(os.path.join(self.base, "DARFs")))
        self.assertFalse(os.path.exists(os.path.join(self.base, "JPG")))

    def test_reclassifica_so_para_cima(self):
        # Em PDF/ (pasta por extensao), um DAM reconhecido sobe de categoria;
        # em DARFs/, um PDF sem termo NAO e rebaixado para PDF.
        self.pdf("PDF", "dam.pdf", lines=("DOCUMENTO DE ARRECADACAO MUNICIPAL - DAM",))
        self.pdf("DARFs", "sem_termo.pdf", lines=("Texto sem categoria",))

        plans = {p.name: p for p in FileOrganizer(base_path=self.base).classify_all()}

        self.assertEqual(plans["dam.pdf"].folder, "DAMs")
        self.assertEqual(plans["sem_termo.pdf"].folder, "DARFs")
        self.assertTrue(plans["sem_termo.pdf"].legacy)

    def test_pasta_do_usuario_fica_intacta(self):
        self.touch("ABR", "nota.pdf")
        FileOrganizer(base_path=self.base, dry_run=False).organize()
        self.assertTrue(os.path.isfile(os.path.join(self.base, "ABR", "nota.pdf")))

    def test_simulacao_nao_remove_pasta_antiga(self):
        self.touch("JPG", "foto.jpg")
        FileOrganizer(base_path=self.base, dry_run=True).organize()
        self.assertTrue(os.path.isfile(os.path.join(self.base, "JPG", "foto.jpg")))

    def test_guarda_chuva_existente_nao_e_relido(self):
        self.touch(ORGANIZED_ROOT_NAME, "JPG", "foto.jpg")
        self.assertEqual(FileOrganizer(base_path=self.base).classify_all(), [])


class TestSubpastas(_Base):

    def test_desligado_por_padrao(self):
        self.touch("ABR", "fundo", "a.txt")
        self.assertEqual(FileOrganizer(base_path=self.base).classify_all(), [])

    def test_ligado_le_qualquer_profundidade_e_mostra_a_origem(self):
        self.touch("ABR", "fundo", "a.txt")
        plans = FileOrganizer(base_path=self.base, include_subfolders=True).classify_all()
        self.assertEqual(len(plans), 1)
        self.assertEqual(plans[0].folder, "TXT")
        self.assertEqual(plans[0].display_name, os.path.join("ABR", "fundo", "a.txt"))

    def test_ignora_guarda_chuva_e_pastas_ocultas(self):
        self.touch(ORGANIZED_ROOT_NAME, "TXT", "ja.txt")
        self.touch(".git", "config.txt")
        plans = FileOrganizer(base_path=self.base, include_subfolders=True).classify_all()
        self.assertEqual(plans, [])

    def test_pasta_do_usuario_esvaziada_nao_e_removida(self):
        self.touch("ABR", "a.txt")
        FileOrganizer(base_path=self.base, dry_run=False, include_subfolders=True).organize()
        self.assertTrue(os.path.isfile(self.organized("TXT", "a.txt")))
        self.assertTrue(os.path.isdir(os.path.join(self.base, "ABR")))

    def test_nomes_iguais_em_subpastas_diferentes_nao_se_sobrescrevem(self):
        self.touch("A", "x.txt", content="um")
        self.touch("B", "x.txt", content="dois")
        FileOrganizer(base_path=self.base, dry_run=False, include_subfolders=True).organize()
        conteudos = sorted(
            open(os.path.join(self.organized("TXT"), n), encoding="utf-8").read()
            for n in os.listdir(self.organized("TXT"))
        )
        self.assertEqual(conteudos, ["dois", "um"])


if __name__ == "__main__":
    unittest.main()
