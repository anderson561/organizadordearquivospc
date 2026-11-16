import os
import unittest
from unittest.mock import patch
import sys

# Adiciona o diretório src ao path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from strategies import sanitize_path_component, TypeStrategy, CompanyNameStrategy

class TestStrategies(unittest.TestCase):

    def test_sanitize_path_component(self):
        self.assertEqual(sanitize_path_component("Pasta: Teste/123?"), "Pasta Teste123")
        self.assertEqual(sanitize_path_component("Nome\nCom\nQuebra"), "Nome Com Quebra")
        self.assertEqual(sanitize_path_component("a" * 100), "a" * 60)

    def test_type_strategy(self):
        strategy = TypeStrategy()
        self.assertEqual(strategy.get_destination_subpath("document.pdf"), "PDF")
        self.assertEqual(strategy.get_destination_subpath("IMAGE.PNG"), "PNG")
        self.assertEqual(strategy.get_destination_subpath(".gitignore"), "Outros")
        self.assertEqual(strategy.get_destination_subpath("no_extension"), "Outros")

    @patch('strategies.extract_text')
    def test_company_name_strategy(self, mock_extract):
        strategy = CompanyNameStrategy()

        # Test non-PDF fallback
        self.assertEqual(strategy.get_destination_subpath("nota.xml"), "XML")

        # Test PDF with date and Razão Social on same line
        mock_extract.return_value = "Emissão: 15/04/2026\nRazão Social: Empresa Teste LTDA\nValor: R$ 100,00"
        subpath = strategy.get_destination_subpath("nota.pdf")
        self.assertEqual(subpath, os.path.join("2026", "04 - Abril", "Empresa Teste LTDA"))

        # Test PDF with Emitente on next line
        mock_extract.return_value = "Data: 20/12/2025\nEmitente\nMinha Empresa S/A\nCNPJ: 00.000.000/0001-00"
        subpath = strategy.get_destination_subpath("nota.pdf")
        self.assertEqual(subpath, os.path.join("2025", "12 - Dezembro", "Minha Empresa SA"))

        # Sem data valida: "Sem Data", nunca o mes corrente (seria um mes inventado)
        mock_extract.return_value = "Nome/Razão Social: Outra Empresa\nOutras informações"
        subpath = strategy.get_destination_subpath("nota.pdf")
        self.assertEqual(subpath, os.path.join("Sem Data", "Outra Empresa"))

        # Sem rotulo de razao social: "Desconhecido", nunca a primeira linha
        # (que costuma ser "NOTA FISCAL" ou o nome da prefeitura)
        mock_extract.return_value = "NOTA FISCAL\nEmissao 05/03/2026\nEMPRESA TESTE LTDA"
        subpath = strategy.get_destination_subpath("nota.pdf")
        self.assertEqual(subpath, os.path.join("2026", "03 - Março", "Desconhecido"))

        # Test Exception handling
        mock_extract.side_effect = Exception("Erro ao ler PDF")
        self.assertEqual(strategy.get_destination_subpath("nota.pdf"), "Notas - Erro na Leitura")

class TestCompanyNameConservadora(unittest.TestCase):
    """Casos que a versao anterior resolvia inventando um valor."""

    def setUp(self):
        self.strategy = CompanyNameStrategy()

    def _subpath(self, texto):
        with patch('strategies.extract_text', return_value=texto):
            return self.strategy.get_destination_subpath("nota.pdf")

    def test_rotulo_sem_acento_e_reconhecido(self):
        self.assertEqual(self._subpath("RAZAO SOCIAL: ALFA SERVICOS LTDA\nEmissao: 10/07/2026"),
                         os.path.join("2026", "07 - Julho", "ALFA SERVICOS LTDA"))

    def test_prefere_a_data_de_emissao(self):
        """Vencimento antes da emissao no texto: vale a emissao."""
        texto = "Vencimento 30/09/2026\nRazão Social: Beta LTDA\nData de Emissão\n15/08/2026"
        self.assertEqual(self._subpath(texto), os.path.join("2026", "08 - Agosto", "Beta LTDA"))

    def test_data_impossivel_e_ignorada(self):
        texto = "Protocolo 45/13/2026\nRazão Social: Gama SA\nEmitida em 02/01/2026"
        self.assertEqual(self._subpath(texto), os.path.join("2026", "01 - Janeiro", "Gama SA"))

    def test_rotulo_de_secao_seguido_de_rotulo_de_campo(self):
        """'EMITENTE' seguido de 'Razão Social: X' devolve X, nao a linha do rotulo."""
        texto = "DADOS DO EMITENTE\nRazão Social: Delta ME\n01/02/2026"
        self.assertEqual(self._subpath(texto), os.path.join("2026", "02 - Fevereiro", "Delta ME"))


if __name__ == '__main__':
    unittest.main()
