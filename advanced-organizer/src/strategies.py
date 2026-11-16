import os
import re
from abc import ABC, abstractmethod
from typing import NamedTuple, Optional, Tuple
from pdfminer.high_level import extract_text
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from document_terms import match_term, strip_accents

def sanitize_path_component(name: str) -> str:
    """Remove caracteres inválidos para nomes de pastas no Windows."""
    # Remove: \ / : * ? " < > |
    sanitized = re.sub(r'[\\/:*?"<>|]', '', name)
    # Remove espaços extras e quebras de linha
    sanitized = sanitized.replace('\n', ' ').strip()
    # Limita o tamanho para evitar caminhos muito longos
    return sanitized[:60]

class BaseStrategy(ABC):
    @abstractmethod
    def get_destination_subpath(self, file_path: str) -> Optional[str]:
        pass

class TypeStrategy(BaseStrategy):
    """Organiza puramente por extensão de arquivo."""
    def get_destination_subpath(self, file_path: str) -> Optional[str]:
        ext = os.path.splitext(file_path)[1].lower().strip('.')
        if not ext:
            return "Outros"
        return sanitize_path_component(ext.upper())

def _decode_pdf_string(raw) -> str:
    """Decodifica uma string de metadado PDF (bytes latin-1 ou UTF-16 com BOM)."""
    if isinstance(raw, bytes):
        if raw[:2] in (b"\xfe\xff", b"\xff\xfe"):
            return raw.decode("utf-16", "ignore")
        return raw.decode("latin-1", "ignore")
    return str(raw or "")


def _looks_like_title(candidate: str) -> bool:
    """Descarta metadados /Title que não são titulo de verdade.

    Geradores de PDF costumam preencher /Title com o nome do arquivo de origem
    ('Microsoft Word - doc1.docx'), com placeholders ou com hashes.
    """
    text = candidate.strip()
    if len(text) < 3:
        return False
    low = text.lower()
    if low.startswith(("microsoft word -", "microsoft excel -", "microsoft powerpoint -")):
        return False
    if low.endswith((".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx")):
        return False
    if low in {"untitled", "document", "documento", "sem titulo", "sem título"}:
        return False
    if not re.search(r"[^\W\d_]{3}", text):      # precisa conter letras, não só números
        return False
    if re.fullmatch(r"[0-9a-f]{16,}", low):      # hash / uuid
        return False
    return True


def _pdf_metadata_title(file_path: str) -> str:
    """Título declarado nos metadados do PDF, ou string vazia."""
    try:
        with open(file_path, "rb") as handle:
            document = PDFDocument(PDFParser(handle))
            for info in document.info or []:
                candidate = _decode_pdf_string(info.get("Title"))
                if _looks_like_title(candidate):
                    return candidate.strip()
    except Exception:
        pass       # metadado ausente ou ilegível não impede a leitura do cabeçalho
    return ""


_CAMEL_BOUNDARY = re.compile(r"(?<=[a-z0-9])(?=[A-Z])")


def filename_hint(file_path: str) -> str:
    """O nome do arquivo como sinal de classificação.

    Costuma ser o sinal mais confiável na prática: um DARF emitido pela Receita
    não traz a sigla 'DARF' em lugar nenhum do conteúdo (o cabeçalho diz
    'Documento de Arrecadação'), mas o nome do arquivo quase sempre traz.

    Separadores viram espaço e limites camelCase são quebrados, para que
    'NotaFiscalNFSe_01.xml' também possa casar.
    """
    stem = os.path.splitext(os.path.basename(file_path))[0]
    spaced = re.sub(r"[_\-.]+", " ", stem)
    spaced = _CAMEL_BOUNDARY.sub(" ", spaced)
    return re.sub(r"\s+", " ", spaced).strip()


class TitleRegion(NamedTuple):
    """Os lugares de um documento onde o título pode estar."""
    metadata: str      # /Title, se plausível
    heading: str       # primeiras linhas da página 1
    filename: str      # nome do arquivo, normalizado

    @property
    def text(self) -> str:
        """Trecho usado para casar o vocabulário."""
        return "\n".join(part for part in (self.metadata, self.heading, self.filename) if part)

    @property
    def display(self) -> str:
        """Título legível, para relatórios."""
        if self.metadata:
            return self.metadata
        if self.heading:
            return self.heading.splitlines()[0]
        return self.filename


# Marcador que o pdfminer emite quando a fonte embutida nao traz mapa
# ToUnicode. Varios DAMs de prefeitura sao assim: o cabecalho sai como
# "(cid:0)(cid:1)(cid:2)..." em vez de texto.
_CID_NOISE = re.compile(r"\(cid:\d+\)")


def _clean_line(line: str) -> str:
    """Limpa uma linha da regiao de titulo, devolvendo '' se nada restar.

    Descartar as linhas que sobram vazias e o que importa: a janela tem apenas
    5 linhas, e sem isso o ruido de (cid:N) ocupava todas elas e escondia o
    cabecalho legivel que vinha logo abaixo.
    """
    return re.sub(r"\s+", " ", _CID_NOISE.sub(" ", line)).strip()


def extract_title_region(file_path: str, max_lines: int = 5) -> TitleRegion:
    """Extrai a região de título de um PDF.

    Lê apenas a primeira página: o casamento acontece no título, não no corpo,
    e isso também torna a classificação bem mais rápida que ler o documento
    inteiro.
    """
    text = extract_text(file_path, maxpages=1) or ""
    lines = [clean for clean in map(_clean_line, text.splitlines()) if clean][:max_lines]
    return TitleRegion(
        _pdf_metadata_title(file_path),
        "\n".join(lines),
        filename_hint(file_path),
    )


class DocumentTitleStrategy(BaseStrategy):
    """Classifica documentos pelo termo encontrado no título.

    PDFs são lidos internamente; um termo reconhecido define a pasta no plural
    (DARF -> 'DARFs'). PDFs sem termo reconhecido e arquivos não-PDF caem na
    estratégia de reserva, preservando a organização por extensão.
    """
    ERROR_FOLDER = "Erro na Leitura"

    def __init__(self, max_title_lines: int = 5, fallback: Optional[BaseStrategy] = None):
        self.max_title_lines = max_title_lines
        self.fallback = fallback or TypeStrategy()

    def classify(self, file_path: str) -> Tuple[Optional[str], TitleRegion]:
        """Devolve (pasta, região de título) - usado pelo modo relatório."""
        if file_path.lower().endswith('.pdf'):
            region = extract_title_region(file_path, self.max_title_lines)
        else:
            # Não-PDF: só o nome do arquivo serve de sinal.
            region = TitleRegion("", "", filename_hint(file_path))

        entry = match_term(region.text)
        folder = sanitize_path_component(entry.folder_name) if entry else None
        return folder, region

    def get_destination_subpath(self, file_path: str) -> Optional[str]:
        try:
            folder, _ = self.classify(file_path)
        except Exception:
            if file_path.lower().endswith('.pdf'):
                return self.ERROR_FOLDER
            return self.fallback.get_destination_subpath(file_path)

        if folder:
            return folder
        # Sem termo reconhecido: mantém o comportamento por extensão.
        return self.fallback.get_destination_subpath(file_path)


_DATE =re.compile(r"(\d{2})/(\d{2})/(\d{4})")
# Rotulos comparados sem acento e em caixa alta: "RAZAO SOCIAL" sem til
# tambem e um rotulo valido, e e assim que muitos PDFs o trazem.
_COMPANY_LABELS = ("NOME/RAZAO SOCIAL", "RAZAO SOCIAL", "EMITENTE")


def _valid_date(match) -> Optional[Tuple[int, int]]:
    """(ano, mes) de um casamento dd/mm/aaaa, ou None se a data nao existe."""
    day, month, year = map(int, match.groups())
    if 1 <= day <= 31 and 1 <= month <= 12:
        return year, month
    return None


def _has_label(line: str) -> bool:
    upper = strip_accents(line).upper()
    return any(label in upper for label in _COMPANY_LABELS)


class CompanyNameStrategy(BaseStrategy):
    """Extrai Ano / Mes / Empresa de Notas Fiscais.

    Segue a regra do projeto: sem informacao confiavel, nao inventa. Sem data
    valida vai para "Sem Data", e nao para o mes corrente; sem rotulo de razao
    social vai para "Desconhecido", e nao para a primeira linha do documento -
    que costuma ser "NOTA FISCAL" ou o nome da prefeitura.
    """

    MONTHS = {
        1: "01 - Janeiro", 2: "02 - Fevereiro", 3: "03 - Março",
        4: "04 - Abril", 5: "05 - Maio", 6: "06 - Junho",
        7: "07 - Julho", 8: "08 - Agosto", 9: "09 - Setembro",
        10: "10 - Outubro", 11: "11 - Novembro", 12: "12 - Dezembro"
    }
    NO_DATE = "Sem Data"
    NO_COMPANY = "Desconhecido"

    @staticmethod
    def _find_date(lines) -> Optional[Tuple[int, int]]:
        """Prefere a data rotulada como emissao; senao, a primeira data valida."""
        for i, line in enumerate(lines):
            if "EMISS" in strip_accents(line).upper():
                for candidate in lines[i:i + 2]:
                    for match in _DATE.finditer(candidate):
                        found = _valid_date(match)
                        if found:
                            return found
        for line in lines:
            for match in _DATE.finditer(line):
                found = _valid_date(match)
                if found:
                    return found
        return None

    @staticmethod
    def _find_company(lines) -> Optional[str]:
        for i, line in enumerate(lines):
            if not _has_label(line):
                continue
            if ":" in line:
                potential = line.split(":")[-1].strip()
                if len(potential) > 3:
                    return potential
            # Sem valor na mesma linha: usa a seguinte, desde que ela nao seja
            # outro rotulo ("EMITENTE" seguido de "Razao Social: X" deve
            # devolver X, e nao a linha do rotulo).
            if i + 1 < len(lines) and not _has_label(lines[i + 1]):
                return lines[i + 1].strip()
        return None

    def get_destination_subpath(self, file_path: str) -> Optional[str]:
        if not file_path.lower().endswith('.pdf'):
            return TypeStrategy().get_destination_subpath(file_path)

        try:
            text = extract_text(file_path)
            lines = [ln.strip() for ln in text.splitlines() if ln.strip()]

            company = sanitize_path_component(self._find_company(lines) or self.NO_COMPANY)
            date = self._find_date(lines)
            if date is None:
                return os.path.join(self.NO_DATE, company)

            year, month = date
            return os.path.join(
                sanitize_path_component(str(year)),
                sanitize_path_component(self.MONTHS[month]),
                company,
            )

        except Exception:
            return "Notas - Erro na Leitura"
