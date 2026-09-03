"""Testes de regressao para os dois bugs de perda/travamento de arquivos.

Ao contrario dos demais testes, estes usam o filesystem real (tmp_path), porque
os bugs originais estavam justamente no comportamento do os.rename/shutil.move
no Windows - que mocks nao reproduzem.
"""
import os
import sys
import unittest
import tempfile
import shutil

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from organizer import FileOrganizer, ORGANIZED_ROOT_NAME


class TestNoDataLoss(unittest.TestCase):
    """Bug: a desambiguacao por mtime acontecia uma unica vez. Na terceira
    colisao de nome+mtime, shutil.move sobrescrevia o arquivo anterior e o log
    ainda reportava 'MOVIDO' com sucesso."""

    def setUp(self):
        self.base = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.base, ignore_errors=True)

    def _drop_file(self, content, mtime):
        path = os.path.join(self.base, "arquivo.txt")
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(content)
        os.utime(path, (mtime, mtime))

    def test_colisoes_repetidas_preservam_todos_os_arquivos(self):
        mtime = 1700000000
        esperados = {"VERSAO-1", "VERSAO-2", "VERSAO-3", "VERSAO-4"}

        for versao in sorted(esperados):
            self._drop_file(versao, mtime)
            FileOrganizer(base_path=self.base, dry_run=False).organize()

        destino = os.path.join(self.base, ORGANIZED_ROOT_NAME, "TXT")
        encontrados = {
            open(os.path.join(destino, nome), encoding="utf-8").read()
            for nome in os.listdir(destino)
        }

        self.assertEqual(encontrados, esperados, "arquivo sobrescrito silenciosamente")

    def test_nunca_sobrescreve_destino_existente(self):
        os.makedirs(os.path.join(self.base, ORGANIZED_ROOT_NAME, "TXT"))
        preexistente = os.path.join(self.base, ORGANIZED_ROOT_NAME, "TXT", "unico.txt")
        with open(preexistente, "w", encoding="utf-8") as handle:
            handle.write("CONTEUDO-ORIGINAL")
        os.utime(preexistente, (1700000000, 1700000000))

        origem = os.path.join(self.base, "unico.txt")
        with open(origem, "w", encoding="utf-8") as handle:
            handle.write("CONTEUDO-NOVO")
        os.utime(origem, (1700000000, 1700000000))

        FileOrganizer(base_path=self.base, dry_run=False).organize()

        self.assertEqual(
            open(preexistente, encoding="utf-8").read(),
            "CONTEUDO-ORIGINAL",
            "o arquivo que ja estava no destino foi sobrescrito",
        )


class TestConflictResolutionIsIdempotent(unittest.TestCase):
    """Bug: o nome de quarentena era fixo ('_CONFLITO_F_P'). Se ja existisse,
    os.rename lancava FileExistsError, os 3 retries queimavam ~6s e o arquivo
    nunca era organizado."""

    def setUp(self):
        self.base = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.base, ignore_errors=True)

    def test_quarentena_ja_ocupada_nao_impede_a_organizacao(self):
        # A pasta de destino agora vive dentro do guarda-chuva.
        os.makedirs(os.path.join(self.base, ORGANIZED_ROOT_NAME))
        # 'TXT' e um arquivo bloqueando a pasta de destino...
        with open(os.path.join(self.base, ORGANIZED_ROOT_NAME, "TXT"), "w", encoding="utf-8") as handle:
            handle.write("bloqueador")
        # ...e o nome de quarentena padrao ja esta ocupado.
        with open(os.path.join(self.base, ORGANIZED_ROOT_NAME, "TXT_CONFLITO_F_P"), "w", encoding="utf-8") as handle:
            handle.write("conflito anterior")

        alvo = os.path.join(self.base, "doc.txt")
        with open(alvo, "w", encoding="utf-8") as handle:
            handle.write("meu documento")

        FileOrganizer(base_path=self.base, dry_run=False).organize()

        self.assertFalse(os.path.exists(alvo), "doc.txt ficou preso na raiz")
        self.assertTrue(
            os.path.isdir(os.path.join(self.base, ORGANIZED_ROOT_NAME, "TXT")),
            "a pasta de destino nao foi criada",
        )
        self.assertEqual(
            open(os.path.join(self.base, ORGANIZED_ROOT_NAME, "TXT", "doc.txt"), encoding="utf-8").read(),
            "meu documento",
        )


if __name__ == '__main__':
    unittest.main()
