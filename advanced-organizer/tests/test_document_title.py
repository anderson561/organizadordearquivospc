"""Testes da classificacao por titulo do documento.

Usam PDFs gerados de verdade (pdf_fixtures) em vez de mocks de extract_text,
porque a extracao de titulo depende do metadado /Title e do layout da primeira
pagina - exatamente o que um mock esconderia.
"""
import os
import sys
import shutil
import tempfile
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
sys.path.append(os.path.dirname(__file__))

from pdf_fixtures import build_pdf
from document_terms import folder_case, match_term, normalize_for_match, pluralize_pt
from strategies import (DocumentTitleStrategy, TitleRegion, _clean_line,
                        _looks_like_title, extract_title_region, filename_hint)
from organizer import FileOrganizer


class TestPluralizePt(unittest.TestCase):

    def test_acronimo_recebe_s_minusculo(self):
        self.assertEqual(pluralize_pt("DARF"), "DARFs")
        self.assertEqual(pluralize_pt("IPTU"), "IPTUs")

    def test_terminacao_ao(self):
        self.assertEqual(pluralize_pt("certidão"), "certidões")
        self.assertEqual(pluralize_pt("procuração"), "procurações")

    def test_terminacao_l(self):
        self.assertEqual(pluralize_pt("edital"), "editais")
        self.assertEqual(pluralize_pt("fiscal"), "fiscais")

    def test_terminacao_r_e_z(self):
        self.assertEqual(pluralize_pt("parecer"), "pareceres")
        self.assertEqual(pluralize_pt("aviz"), "avizes")

    def test_terminacao_m(self):
        self.assertEqual(pluralize_pt("armazem"), "armazens")

    def test_vogal(self):
        self.assertEqual(pluralize_pt("recibo"), "recibos")
        self.assertEqual(pluralize_pt("alvará"), "alvarás")

    def test_excecao_irregular(self):
        self.assertEqual(pluralize_pt("pão"), "pães")

    def test_termo_composto_pluraliza_cada_palavra(self):
        self.assertEqual(pluralize_pt("nota fiscal"), "notas fiscais")

    def test_folder_case(self):
        self.assertEqual(folder_case("notas fiscais"), "Notas Fiscais")
        self.assertEqual(folder_case("DARFs"), "DARFs")
        # conectivo permanece minusculo
        self.assertEqual(folder_case("guias de recolhimento"), "Guias de Recolhimento")


class TestNormalizeForMatch(unittest.TestCase):

    def test_remove_acento_preservando_caixa(self):
        self.assertEqual(normalize_for_match("RELATÓRIO"), "RELATORIO")
        self.assertEqual(normalize_for_match("Certidão"), "Certidao")

    def test_colapsa_espacos(self):
        self.assertEqual(normalize_for_match("  nota   fiscal \n"), "nota fiscal")


class TestMatchTerm(unittest.TestCase):
    """O casamento acontece com limite de palavra, na regiao de titulo."""

    def _folder(self, title):
        entry = match_term(title)
        return entry.folder_name if entry else None

    def test_regressao_vendas_nao_e_das(self):
        # A versao anterior classificava isto como "DAS - Simples Nacional",
        # porque procurava a substring "DAS" no texto inteiro.
        self.assertEqual(self._folder("RELATORIO DE VENDAS MENSAIS"), "Relatórios")
        self.assertIsNone(self._folder("TOTAL DAS VENDAS DO MES"))
        self.assertIsNone(self._folder("TODAS AS MEDIDAS FORAM TOMADAS"))

    def test_preposicao_das_minuscula_nao_casa_acronimo(self):
        self.assertIsNone(self._folder("Relação das contribuições"))

    def test_das_exige_corroboracao(self):
        self.assertIsNone(self._folder("Guia DAS do mes"))
        self.assertEqual(self._folder("DAS - Simples Nacional"), "DASs")

    def test_acronimo_no_singular_e_no_plural(self):
        for titulo in ("DARF de janeiro", "DARFs de 2026", "DARFS pagos"):
            self.assertEqual(self._folder(titulo), "DARFs", titulo)

    def test_termo_com_acento_e_caixa_indiferentes(self):
        for titulo in ("RELATÓRIO", "relatorio", "Relatórios"):
            self.assertEqual(self._folder(titulo), "Relatórios", titulo)

    def test_precedencia_termo_mais_especifico(self):
        # "nota fiscal" vem antes de termos genericos no vocabulario
        self.assertEqual(self._folder("NOTA FISCAL DE SERVICOS"), "Notas Fiscais")

    def test_titulo_vazio(self):
        self.assertIsNone(self._folder(""))
        self.assertIsNone(self._folder("   "))


class TestLooksLikeTitle(unittest.TestCase):

    def test_rejeita_nome_de_arquivo_e_placeholder(self):
        for ruim in ("Microsoft Word - nf.docx", "relatorio.pdf", "untitled",
                     "documento", "12345", "ab", "a3f9c1b2e4d5f6a7b8c9d0e1f2a3b4c5"):
            self.assertFalse(_looks_like_title(ruim), ruim)

    def test_aceita_titulo_real(self):
        for bom in ("Relatório Trimestral", "DARF - Arrecadacao", "Nota Fiscal 123"):
            self.assertTrue(_looks_like_title(bom), bom)


class TestExtractTitleRegion(unittest.TestCase):

    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.dir, ignore_errors=True)

    def _pdf(self, name, lines, title=None):
        return build_pdf(os.path.join(self.dir, name), lines, title=title)

    def test_usa_metadado_quando_plausivel(self):
        p = self._pdf("a.pdf", ["Corpo qualquer"], title="Relatório Trimestral")
        region = extract_title_region(p)
        self.assertEqual(region.metadata, "Relatório Trimestral")
        self.assertEqual(region.display, "Relatório Trimestral")

    def test_ignora_metadado_lixo_e_usa_o_cabecalho(self):
        p = self._pdf("b.pdf", ["NOTA FISCAL DE SERVICOS", "Prestador X"],
                      title="Microsoft Word - nf.docx")
        region = extract_title_region(p)
        self.assertEqual(region.metadata, "")
        self.assertEqual(region.display, "NOTA FISCAL DE SERVICOS")

    def test_sem_metadado_usa_primeiras_linhas(self):
        p = self._pdf("c.pdf", ["DARF", "Documento de Arrecadacao"])
        region = extract_title_region(p)
        self.assertEqual(region.display, "DARF")
        self.assertIn("Documento de Arrecadacao", region.text)

    def test_limita_o_numero_de_linhas(self):
        p = self._pdf("d.pdf", [f"linha {i}" for i in range(20)])
        region = extract_title_region(p, max_lines=3)
        self.assertEqual(len(region.heading.splitlines()), 3)

    def test_preserva_acentos_extraidos(self):
        p = self._pdf("e.pdf", ["CERTIDÃO NEGATIVA"])
        self.assertIn("CERTIDÃO", extract_title_region(p).text)


class TestDocumentTitleStrategy(unittest.TestCase):

    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.dir, ignore_errors=True)
        self.strategy = DocumentTitleStrategy()

    def _pdf(self, name, lines, title=None):
        return build_pdf(os.path.join(self.dir, name), lines, title=title)

    def test_classifica_pdf_por_titulo(self):
        casos = [
            (["DARF", "Arrecadacao"], "DARFs"),
            (["RELATÓRIO DE VENDAS"], "Relatórios"),
            (["DAS - Simples Nacional"], "DASs"),
            (["IPTU 2026"], "IPTUs"),
            (["NOTA FISCAL ELETRONICA"], "Notas Fiscais"),
            (["CONTRATO DE LOCACAO"], "Contratos"),
        ]
        for i, (linhas, esperado) in enumerate(casos):
            p = self._pdf(f"doc{i}.pdf", linhas)
            self.assertEqual(self.strategy.get_destination_subpath(p), esperado, linhas)

    def test_pdf_sem_termo_cai_na_pasta_por_extensao(self):
        p = self._pdf("x.pdf", ["Documento generico sem palavra-chave"])
        self.assertEqual(self.strategy.get_destination_subpath(p), "PDF")

    def test_nao_pdf_usa_a_estrategia_de_reserva(self):
        for nome, esperado in (("foto.jpg", "JPG"), ("planilha.xlsx", "XLSX"), ("dados", "Outros")):
            caminho = os.path.join(self.dir, nome)
            open(caminho, "w").close()
            self.assertEqual(self.strategy.get_destination_subpath(caminho), esperado)

    def test_pdf_ilegivel_vai_para_pasta_de_erro(self):
        caminho = os.path.join(self.dir, "corrompido.pdf")
        with open(caminho, "wb") as handle:
            handle.write(b"isto nao e um PDF")
        self.assertEqual(self.strategy.get_destination_subpath(caminho),
                         DocumentTitleStrategy.ERROR_FOLDER)

    def test_classify_devolve_titulo_e_pasta(self):
        p = self._pdf("y.pdf", ["DARF"], title="DARF Janeiro 2026")
        folder, region = self.strategy.classify(p)
        self.assertEqual(folder, "DARFs")
        self.assertEqual(region.display, "DARF Janeiro 2026")
        self.assertIsInstance(region, TitleRegion)

    def test_termo_no_corpo_nao_classifica(self):
        """O termo precisa estar no titulo, nao em qualquer lugar do texto."""
        linhas = ["CONTRATO DE PRESTACAO DE SERVICOS"] + [f"clausula {i}" for i in range(6)]
        linhas.append("O pagamento sera feito via DARF proprio")
        p = self._pdf("z.pdf", linhas)
        self.assertEqual(self.strategy.get_destination_subpath(p), "Contratos")


class TestFilenameHint(unittest.TestCase):
    """O nome do arquivo e um sinal de primeira classe."""

    def test_separadores_viram_espaco(self):
        self.assertEqual(filename_hint("andre_darf-irrf.052026.pdf"), "andre darf irrf 052026")

    def test_quebra_camelcase(self):
        self.assertEqual(filename_hint("NotaFiscalNFSe.xml"), "Nota Fiscal NFSe")

    def test_ignora_diretorio_e_extensao(self):
        self.assertEqual(filename_hint(r"C:\tmp\Sub\contrato final.pdf"), "contrato final")


class TestClassificacaoPeloNomeDoArquivo(unittest.TestCase):
    """Casos observados no acervo real do usuario."""

    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.dir, ignore_errors=True)
        self.strategy = DocumentTitleStrategy()

    def _pdf(self, name, lines, title=None):
        return build_pdf(os.path.join(self.dir, name), lines, title=title)

    def test_darf_da_receita_sem_a_sigla_no_conteudo(self):
        """O DARF impresso pela Receita nao contem a sigla 'DARF'."""
        p = self._pdf("guia.pdf", ["Documento de Arrecadação", "de Receitas Federais", "CNPJ"])
        self.assertEqual(self.strategy.get_destination_subpath(p), "DARFs")

    def test_darf_reconhecido_pelo_nome_do_arquivo(self):
        p = self._pdf("andre darf irrf crf 052026.pdf", ["Conteudo sem termo algum"])
        self.assertEqual(self.strategy.get_destination_subpath(p), "DARFs")

    def test_danfse_vai_para_notas_fiscais(self):
        p = self._pdf("2307304125.pdf", ["DANFSe v1.0", "Documento Auxiliar da NFS-e"])
        self.assertEqual(self.strategy.get_destination_subpath(p), "Notas Fiscais")

    def test_perdcomp(self):
        p = self._pdf("13245811.pdf", ["Receita Federal do Brasil",
                                       "PEDIDO DE RESTITUIÇÃO", "PERDCOMP  8.33"])
        self.assertEqual(self.strategy.get_destination_subpath(p), "PERDCOMPs")

    def test_declaracao(self):
        p = self._pdf("Banco Elos.pdf", ["Anexo: Declaração de Titularidade de Conta Corrente"])
        self.assertEqual(self.strategy.get_destination_subpath(p), "Declarações")

    def test_xml_classificado_pelo_nome_camelcase(self):
        caminho = os.path.join(self.dir, "0838335000183_NotaFiscaldeServicoEletronicaNFSe_000103.xml")
        open(caminho, "w").close()
        self.assertEqual(self.strategy.get_destination_subpath(caminho), "Notas Fiscais")

    def test_nao_pdf_sem_termo_no_nome_continua_por_extensao(self):
        caminho = os.path.join(self.dir, "IMG_2026.jpg")
        open(caminho, "w").close()
        self.assertEqual(self.strategy.get_destination_subpath(caminho), "JPG")


class TestGuiasPorJurisdicao(unittest.TestCase):
    """A familia 'documento de arrecadacao' se divide por jurisdicao.

    Todas as guias - municipal (DAM), estadual (DAE) e federal (DARF) -
    comecam com a mesma frase. Tratar a frase como termo generico mandava as
    tres para DARFs: foi assim que um DAM municipal foi arquivado como DARF.
    """

    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.dir, ignore_errors=True)
        self.strategy = DocumentTitleStrategy()

    def _pdf(self, name, lines, title=None):
        return build_pdf(os.path.join(self.dir, name), lines, title=title)

    # --- municipal ---------------------------------------------------------
    def test_dam_municipal_com_sigla_e_frase(self):
        """Cabecalho real de DAM de prefeitura, com metadado /Title 'DAM'."""
        p = self._pdf("INST MULHER - ISS.pdf",
                      ["12/08/2026, 14:25", "DAM",
                       "DOCUMENTO DE ARRECADAÇÃO MUNICIPAL - DAM",
                       "PAD - Parcelamento Administrativo de Débitos"],
                      title="DAM")
        self.assertEqual(self.strategy.get_destination_subpath(p), "DAMs")

    def test_dam_pela_frase_municipal_sem_a_sigla(self):
        p = self._pdf("guia.pdf", ["Documento de Arrecadação Municipal", "Prefeitura"])
        self.assertEqual(self.strategy.get_destination_subpath(p), "DAMs")

    def test_dam_reconhecido_so_pelo_nome_do_arquivo(self):
        """DAMs de prefeitura costumam vir com fonte sem mapa ToUnicode."""
        p = self._pdf("dam tff 2025.pdf", ["ESTADO DA BAHIA", "MUNICÍPIO DE CONCEIÇÃO"])
        self.assertEqual(self.strategy.get_destination_subpath(p), "DAMs")

    def test_dam_nunca_cai_em_darfs(self):
        """A regressao reportada: DAM detectado, arquivado em DARFs."""
        p = self._pdf("deltaline dam iss 102025.pdf", ["Documento de Arrecadação Municipal"])
        self.assertNotEqual(self.strategy.get_destination_subpath(p), "DARFs")

    # --- estadual ----------------------------------------------------------
    def test_dae_estadual_pelo_nome(self):
        p = self._pdf("Macedo Fl. 03 DAE 1145 09-2022.pdf", ["https://servicos.sefaz.ba.gov.br"])
        self.assertEqual(self.strategy.get_destination_subpath(p), "DAEs")

    def test_dae_pela_frase_estadual(self):
        p = self._pdf("guia.pdf", ["Documento de Arrecadação Estadual", "SEFAZ"])
        self.assertEqual(self.strategy.get_destination_subpath(p), "DAEs")

    # --- federal -----------------------------------------------------------
    def test_darf_federal_com_a_frase_quebrada_em_duas_linhas(self):
        """O PDF da Receita quebra o cabecalho; a frase casa atravessando a linha."""
        p = self._pdf("GuiaPagamento_60225957000168.pdf",
                      ["Documento de Arrecadação", "de Receitas Federais", "CNPJ"])
        self.assertEqual(self.strategy.get_destination_subpath(p), "DARFs")

    def test_darf_sobrevive_a_erro_de_digitacao_no_nome(self):
        """Nomes reais trazem 'daf', 'dar', 'darrf' - a frase e que salva."""
        for nome in ("boca daf irrf crf 062026.pdf", "sao pedro dar irrf crf 072026.pdf",
                     "tamp darrf irrf csrf 072026.pdf"):
            with self.subTest(nome=nome):
                p = self._pdf(nome, ["Documento de Arrecadação de Receitas Federais"])
                self.assertEqual(self.strategy.get_destination_subpath(p), "DARFs")

    def test_frase_truncada_sem_jurisdicao_nao_vira_darf(self):
        """Sem jurisdicao nao ha como saber: melhor nao classificar.

        'Documento de Arrecadacao' sozinho descreve as tres guias. Nos 540 PDFs
        reais conferidos, todo documento que dependia so da frase trazia
        'de Receitas Federais' junto - ninguem e perdido por essa escolha.
        """
        p = self._pdf("guia.pdf", ["Documento de Arrecadação", "Valor total"])
        self.assertEqual(self.strategy.get_destination_subpath(p), "PDF")

    def test_pastas_no_plural(self):
        self.assertEqual(match_term("DAM").folder_name, "DAMs")
        self.assertEqual(match_term("DAE").folder_name, "DAEs")
        self.assertEqual(match_term("DARF").folder_name, "DARFs")


class TestRuidoDeFonteSemToUnicode(unittest.TestCase):
    """PDFs cuja fonte embutida nao traz mapa ToUnicode saem como (cid:N)."""

    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.dir, ignore_errors=True)

    def test_clean_line_remove_os_marcadores(self):
        self.assertEqual(_clean_line("(cid:0)(cid:1)(cid:2)"), "")
        self.assertEqual(_clean_line("(cid:12)DAM(cid:13)"), "DAM")
        self.assertEqual(_clean_line("  texto   normal  "), "texto normal")

    def test_linhas_de_ruido_nao_consomem_a_janela(self):
        """Sem a limpeza, o ruido ocupava as 5 linhas e escondia o cabecalho."""
        caminho = build_pdf(
            os.path.join(self.dir, "guia.pdf"),
            ["(cid:0)(cid:1)(cid:2)", "(cid:3)(cid:4)", "(cid:5)", "(cid:6)", "(cid:7)",
             "Documento de Arrecadação Municipal"],
        )
        region = extract_title_region(caminho)
        self.assertNotIn("cid:", region.heading)
        self.assertEqual(DocumentTitleStrategy().get_destination_subpath(caminho), "DAMs")


class TestOrganizerIntegration(unittest.TestCase):
    """Fluxo completo: classifica e move de verdade, no filesystem."""

    def setUp(self):
        self.base = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.base, ignore_errors=True)

    def test_move_para_pastas_pluralizadas(self):
        build_pdf(os.path.join(self.base, "d1.pdf"), ["DARF", "Janeiro"])
        build_pdf(os.path.join(self.base, "d2.pdf"), ["DARF", "Fevereiro"])
        build_pdf(os.path.join(self.base, "r1.pdf"), ["RELATÓRIO MENSAL"])
        open(os.path.join(self.base, "foto.jpg"), "w").close()

        FileOrganizer(base_path=self.base, dry_run=False).organize()

        self.assertEqual(sorted(os.listdir(os.path.join(self.base, "DARFs"))),
                         ["d1.pdf", "d2.pdf"])
        self.assertEqual(os.listdir(os.path.join(self.base, "Relatórios")), ["r1.pdf"])
        self.assertEqual(os.listdir(os.path.join(self.base, "JPG")), ["foto.jpg"])

    def test_pasta_contem_somente_os_arquivos_daquele_termo(self):
        build_pdf(os.path.join(self.base, "a.pdf"), ["DARF"])
        build_pdf(os.path.join(self.base, "b.pdf"), ["RELATÓRIO"])
        build_pdf(os.path.join(self.base, "c.pdf"), ["NOTA FISCAL"])

        FileOrganizer(base_path=self.base, dry_run=False).organize()

        self.assertEqual(os.listdir(os.path.join(self.base, "DARFs")), ["a.pdf"])
        self.assertEqual(os.listdir(os.path.join(self.base, "Relatórios")), ["b.pdf"])
        self.assertEqual(os.listdir(os.path.join(self.base, "Notas Fiscais")), ["c.pdf"])

    def test_muitos_arquivos_na_mesma_pasta_nenhum_sobrescrito(self):
        """Consolidar por termo aumenta a colisao de nomes: nada pode se perder."""
        conteudos = []
        for i in range(6):
            build_pdf(os.path.join(self.base, "guia.pdf"), ["DARF", f"parcela {i}"])
            conteudos.append(open(os.path.join(self.base, "guia.pdf"), "rb").read())
            os.utime(os.path.join(self.base, "guia.pdf"), (1700000000, 1700000000))
            FileOrganizer(base_path=self.base, dry_run=False).organize()

        destino = os.path.join(self.base, "DARFs")
        salvos = [open(os.path.join(destino, n), "rb").read() for n in os.listdir(destino)]
        self.assertEqual(len(salvos), 6, "algum arquivo foi sobrescrito")
        self.assertEqual(sorted(salvos), sorted(conteudos))

    def test_dry_run_nao_move_nada(self):
        build_pdf(os.path.join(self.base, "d.pdf"), ["DARF"])
        FileOrganizer(base_path=self.base, dry_run=True).organize()
        self.assertEqual(os.listdir(self.base), ["d.pdf"])

    def test_report_nao_move_e_lista_a_classificacao(self):
        build_pdf(os.path.join(self.base, "d.pdf"), ["DARF"])
        build_pdf(os.path.join(self.base, "sem_termo.pdf"), ["Documento generico"])

        plans = FileOrganizer(base_path=self.base, dry_run=True).report()

        self.assertEqual(sorted(os.listdir(self.base)), ["d.pdf", "sem_termo.pdf"])
        por_nome = {p.name: p for p in plans}
        self.assertEqual(por_nome["d.pdf"].folder, "DARFs")
        self.assertTrue(por_nome["d.pdf"].recognized)
        self.assertEqual(por_nome["sem_termo.pdf"].folder, "PDF")
        self.assertFalse(por_nome["sem_termo.pdf"].recognized)


class TestGuiaDoSimplesPeloPGDASD(unittest.TestCase):
    """A guia do Simples nem sempre mostra o cabecalho na janela de titulo.

    O PGDASD gera quatro papeis diferentes com o mesmo prefixo de nome: a
    guia (DAS), a declaracao, o extrato e o recibo de entrega. Em parte dos
    PDFs da guia o bloco do CNPJ vem antes do cabecalho e empurra a frase
    "Documento de Arrecadacao do Simples Nacional" para fora das cinco
    primeiras linhas, entao a corroboracao exigida pelo acronimo "DAS" nunca
    chega e a guia caia na organizacao por extensao.
    """

    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.dir, ignore_errors=True)
        self.strategy = DocumentTitleStrategy()

    def _pdf(self, name, lines, title=None):
        return build_pdf(os.path.join(self.dir, name), lines, title=title)

    def test_guia_sem_o_cabecalho_na_janela_de_titulo(self):
        """O caso que falhava: o CNPJ empurra o cabecalho para fora."""
        p = self._pdf("PGDASD-DAS-20547819202511001.pdf",
                      ["CNPJ", "20.547.819/0001-80 BOTECO 27 BAR E RESTAURANTE LTDA.",
                       "Razão Social", "Período de Apuração", "Data de Vencimento"])
        self.assertEqual(self.strategy.get_destination_subpath(p), "DASs")

    def test_guia_com_o_cabecalho_visivel_continua_em_dass(self):
        p = self._pdf("PGDASD-DAS-60225957000168.pdf",
                      ["Documento de Arrecadação", "do Simples Nacional",
                       "CNPJ", "60.225.957/0001-68"])
        self.assertEqual(self.strategy.get_destination_subpath(p), "DASs")

    def test_declaracao_do_mesmo_programa_nao_vira_guia(self):
        """O prefixo PGDASD sozinho nao decide: o segmento seguinte decide."""
        p = self._pdf("PGDASD-DECLARACAO-60225957202511002.pdf",
                      ["Declaração Anual", "Simples Nacional"])
        self.assertEqual(self.strategy.get_destination_subpath(p), "Declarações")

    def test_extrato_do_mesmo_programa_nao_vira_guia(self):
        p = self._pdf("PGDASD-EXTRATO-60225957202511002.pdf",
                      ["Extrato da Apuração", "Simples Nacional"])
        self.assertEqual(self.strategy.get_destination_subpath(p), "Extratos")

    def test_nome_em_caixa_baixa_tambem_reconhece(self):
        """Nome de arquivo renomeado a mao chega minusculo."""
        p = self._pdf("pgdasd-das-60225957000168.pdf", ["CNPJ", "60.225.957/0001-68"])
        self.assertEqual(self.strategy.get_destination_subpath(p), "DASs")

    def test_a_preposicao_das_nao_ativa_a_guia(self):
        """A protecao contra o homografo continua valendo."""
        p = self._pdf("relatorio.pdf", ["Relatório das vendas do mês"])
        self.assertEqual(self.strategy.get_destination_subpath(p), "Relatórios")


if __name__ == '__main__':
    unittest.main()
