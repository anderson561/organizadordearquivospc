"""Gerador minimo de PDF de uma pagina, para os testes.

Escrito na mao em sintaxe PDF crua de proposito: valida a extracao contra
arquivos PDF de verdade sem introduzir dependencia de escrita (reportlab e
companhia) no projeto.
"""
from typing import Optional, Sequence


def _escape(text: str) -> str:
    """Escapa os caracteres especiais de uma string literal PDF."""
    return text.replace("\\", r"\\").replace("(", r"\(").replace(")", r"\)")


def _content_stream(lines: Sequence[str]) -> bytes:
    ops = ["BT", "/F1 12 Tf", "72 720 Td"]
    for i, line in enumerate(lines):
        if i:
            ops.append("0 -16 Td")
        ops.append(f"({_escape(line)}) Tj")
    ops.append("ET")
    # latin-1 casa com o WinAnsiEncoding declarado na fonte, o que preserva
    # os acentos na extracao.
    return "\n".join(ops).encode("latin-1", "replace")


def build_pdf(path: str, lines: Sequence[str], title: Optional[str] = None) -> str:
    """Grava um PDF de uma pagina com as linhas dadas e, opcionalmente, /Title."""
    content = _content_stream(lines)

    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        b"/Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>",
        b"<< /Length " + str(len(content)).encode() + b" >>\nstream\n" + content + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>",
    ]
    if title is not None:
        objects.append(b"<< /Title (" + _escape(title).encode("latin-1", "replace") + b") >>")

    out = bytearray(b"%PDF-1.4\n")
    offsets = []
    for number, body in enumerate(objects, start=1):
        offsets.append(len(out))
        out += f"{number} 0 obj\n".encode() + body + b"\nendobj\n"

    xref_at = len(out)
    total = len(objects) + 1
    out += f"xref\n0 {total}\n".encode()
    out += b"0000000000 65535 f \n"
    for off in offsets:
        out += f"{off:010d} 00000 n \n".encode()

    trailer = f"<< /Size {total} /Root 1 0 R"
    if title is not None:
        trailer += f" /Info {len(objects)} 0 R"
    trailer += " >>"
    out += f"trailer\n{trailer}\nstartxref\n{xref_at}\n%%EOF\n".encode()

    with open(path, "wb") as handle:
        handle.write(bytes(out))
    return path
