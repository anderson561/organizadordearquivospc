"""Vocabulario de termos de documentos e regras de nome de pasta.

O casamento acontece sobre a REGIAO DE TITULO do documento (metadado /Title
e primeiras linhas), nunca sobre o texto inteiro. Casar contra o corpo inteiro
produzia falsos positivos graves: a versao anterior classificava qualquer
documento com a palavra "VENDAS" como guia do Simples Nacional, porque
procurava a substring "DAS".
"""
import re
import unicodedata
from typing import Iterable, NamedTuple, Optional, Tuple

# Palavras que nao recebem maiuscula no nome da pasta.
_MINOR_WORDS = {"de", "da", "do", "das", "dos", "e"}

# Plurais irregulares ou com mudanca de acento. A regra geral cobre o resto.
_PLURAL_EXCEPTIONS = {
    "mao": "maos",
    "mão": "mãos",
    "irmao": "irmaos",
    "irmão": "irmãos",
    "pao": "paes",
    "pão": "pães",
    "cidadao": "cidadaos",
    "cidadão": "cidadãos",
    "fossil": "fosseis",
    "fóssil": "fósseis",
    "papel": "papéis",
    "farol": "faróis",
}


def strip_accents(text: str) -> str:
    """Remove acentos preservando a caixa das letras."""
    decomposed = unicodedata.normalize("NFKD", text)
    return "".join(ch for ch in decomposed if not unicodedata.combining(ch))


def normalize_for_match(text: str) -> str:
    """Forma canonica para casamento: sem acento e com espacos colapsados.

    A caixa e PRESERVADA de proposito - acronimos ambiguos (DAS) dependem dela
    para se distinguir da preposicao homografa.
    """
    return re.sub(r"\s+", " ", strip_accents(text)).strip()


def _plural_word(word: str) -> str:
    """Pluraliza uma unica palavra em portugues."""
    if word.lower() in _PLURAL_EXCEPTIONS:
        plural = _PLURAL_EXCEPTIONS[word.lower()]
        return plural.upper() if word.isupper() else plural

    # Acronimo (DARF, IPTU): recebe apenas o 's' minusculo -> DARFs
    if word.isupper() and len(word) > 1:
        return word + "s"

    low = word.lower()
    if low.endswith("ão"):
        return word[:-2] + "ões"
    if low.endswith("ao"):
        return word[:-2] + "oes"
    if low.endswith("m"):
        return word[:-1] + "ns"
    if low.endswith(("al", "el", "ol", "ul")):
        vowel = low[-2]
        accented = {"a": "a", "e": "é", "o": "ó", "u": "u"}[vowel]
        return word[:-2] + accented + "is"
    if low.endswith("il"):
        return word[:-2] + "is"
    if low.endswith(("r", "z")):
        return word + "es"
    if low.endswith("s"):
        # Monossilabo tonico (mes -> meses); demais ficam inalterados.
        return word + "es" if len(word) <= 4 else word
    return word + "s"


def pluralize_pt(term: str) -> str:
    """Pluraliza um termo, palavra por palavra ('nota fiscal' -> 'notas fiscais')."""
    return " ".join(_plural_word(w) for w in term.split())


def folder_case(term: str) -> str:
    """Formata o termo como nome de pasta ('notas fiscais' -> 'Notas Fiscais')."""
    words = term.split()
    out = []
    for i, word in enumerate(words):
        if word.isupper():          # preserva acronimos: DARFs, IPTUs
            out.append(word)
        elif i > 0 and word.lower() in _MINOR_WORDS:
            out.append(word.lower())
        else:
            out.append(word[:1].upper() + word[1:])
    return " ".join(out)


class Term(NamedTuple):
    """Uma entrada do vocabulario.

    term      termo no singular, como aparece no documento
    acronym   se True, exige caixa alta no titulo (evita casar 'das'/'DAS')
    requires  ao menos um destes trechos deve estar no titulo (corroboracao
              para termos ambiguos)
    folder    sobrescreve o nome de pasta derivado por pluralizacao
    """
    term: str
    acronym: bool = False
    requires: Tuple[str, ...] = ()
    folder: Optional[str] = None

    @property
    def folder_name(self) -> str:
        return self.folder or folder_case(pluralize_pt(self.term))


# Ordem = precedencia. O primeiro termo que casar vence, entao os mais
# especificos vem antes dos mais genericos.
TERMS: Tuple[Term, ...] = (
    # --- Notas fiscais de servico eletronicas -------------------------------
    Term("nota fiscal", folder="Notas Fiscais"),
    Term("DANFSe", acronym=True, folder="Notas Fiscais"),
    Term("NFS-e", folder="Notas Fiscais"),
    Term("NFSe", acronym=True, folder="Notas Fiscais"),

    # --- Guias de arrecadacao: a JURISDICAO decide a pasta ------------------
    # A frase "documento de arrecadacao" descreve a familia inteira - a guia
    # municipal, a estadual e a federal comecam todas assim. Usa-la como termo
    # generico mandava as tres para DARFs. Cada jurisdicao tem entrada propria,
    # e a frase federal precisa vir COMPLETA.
    #
    # Municipal (ISS, TFF): "DOCUMENTO DE ARRECADACAO MUNICIPAL - DAM".
    Term("DAM", acronym=True),
    Term("documento de arrecadação municipal", folder="DAMs"),
    # Estadual (ICMS na Bahia): DAE.
    Term("DAE", acronym=True),
    Term("documento de arrecadação estadual", folder="DAEs"),
    # Federal. O DARF impresso pela Receita nao traz a sigla, so o cabecalho
    # "Documento de Arrecadacao de Receitas Federais", quebrado em duas linhas.
    Term("DARF", acronym=True),
    Term("documento de arrecadação de receitas federais", folder="DARFs"),
    Term("IPTU", acronym=True),
    Term("IPVA", acronym=True),
    Term("GRERJ", acronym=True),
    # A guia do Simples sai do PGDASD (Programa Gerador do Documento de
    # Arrecadacao do Simples Nacional Declaratorio). Em varios PDFs o bloco
    # do CNPJ vem antes do cabecalho e empurra a frase 'Documento de
    # Arrecadacao do Simples Nacional' para fora da janela de cinco linhas,
    # entao a corroboracao exigida por 'DAS' nunca chega. O nome do arquivo,
    # porem, sempre traz o prefixo do emissor: PGDASD-DAS-<cnpj><periodo>.
    # Vem antes de 'DAS' e dos termos genericos para nao perder a guia para
    # 'declaracao' ou 'extrato' - o mesmo programa gera esses outros papeis,
    # e so o segmento depois de PGDASD separa um do outro.
    Term("PGDASD DAS", acronym=True, folder="DASs"),
    # "DAS" e homografo da preposicao "das": exige corroboracao explicita.
    Term("DAS", acronym=True, requires=("SIMPLES NACIONAL", "ARRECADACAO DO SIMPLES")),

    # --- Demais documentos --------------------------------------------------
    Term("PERDCOMP", acronym=True),
    Term("relatório"),
    Term("contrato"),
    Term("declaração"),
    Term("certidão"),
    Term("recibo"),
    Term("boleto"),
    Term("extrato"),
    Term("comprovante"),
    Term("procuração"),
    Term("alvará"),
)


def _pattern_for(entry: Term) -> "re.Pattern[str]":
    """Regex que casa o termo no singular ou no plural, com limite de palavra."""
    if entry.acronym:
        body = re.escape(normalize_for_match(entry.term))
        # Acronimos ambiguos (os que exigem corroboracao) casam apenas em caixa
        # alta: e o que separa a guia "DAS" da preposicao "das". Os demais nao
        # sao palavras do portugues, entao podem casar em qualquer caixa - o que
        # e essencial para reconhecer nomes de arquivo, sempre minusculos
        # ('andre darf irrf 052026.pdf').
        flags = 0 if entry.requires else re.IGNORECASE
        return re.compile(rf"\b{body}s?\b", flags)

    forms = {
        normalize_for_match(entry.term),
        normalize_for_match(pluralize_pt(entry.term)),
    }
    alternatives = "|".join(
        re.escape(f).replace(r"\ ", r"\s+") for f in sorted(forms, key=len, reverse=True)
    )
    return re.compile(rf"\b(?:{alternatives})\b", re.IGNORECASE)


_PATTERNS: Tuple[Tuple[Term, "re.Pattern[str]"], ...] = tuple(
    (entry, _pattern_for(entry)) for entry in TERMS
)


def match_term(title: str, terms: Optional[Iterable[Term]] = None) -> Optional[Term]:
    """Retorna a entrada do vocabulario que casa com o titulo, ou None."""
    if not title or not title.strip():
        return None

    normalized = normalize_for_match(title)
    upper = normalized.upper()

    candidates = _PATTERNS if terms is None else ((e, _pattern_for(e)) for e in terms)
    for entry, pattern in candidates:
        if not pattern.search(normalized):
            continue
        # Termo ambiguo: so vale com corroboracao no titulo.
        if entry.requires and not any(req in upper for req in entry.requires):
            continue
        return entry
    return None
