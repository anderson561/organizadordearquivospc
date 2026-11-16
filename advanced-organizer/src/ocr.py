"""OCR da primeira pagina de PDFs escaneados, com o OCR nativo do Windows.

Por que o OCR do Windows, e nao Tesseract: o produto e um .exe de clique duplo
que nao pode exigir instalacao de nada. O motor do Windows (Windows.Media.Ocr)
ja vem no sistema, com o idioma pt-BR presente em toda instalacao em portugues.
O Tesseract exigiria instalar um programa a parte em cada maquina.

A pagina e rasterizada com o pdfium (pypdfium2), que traz o binario embutido.

Tudo aqui e opcional por construcao: se o Windows nao tiver OCR, se o idioma
nao estiver instalado ou se as bibliotecas faltarem, `ocr_first_page` devolve
lista vazia e a classificacao segue como antes - pelo nome do arquivo. OCR que
falha nunca pode virar classificacao errada nem travar a analise.
"""
import asyncio
import logging
from functools import lru_cache
from typing import List, Optional

logger = logging.getLogger(__name__)

# Escala de renderizacao: 2.0 = 144 dpi. Abaixo disso o OCR erra letras de
# corpo pequeno; acima, so gasta tempo - a regiao de titulo usa letras grandes.
RENDER_SCALE = 2.0
PREFERRED_LANGUAGES = ("pt-BR", "pt")


@lru_cache(maxsize=1)
def _engine():
    """Cria o motor de OCR uma vez por processo, ou None se indisponivel."""
    try:
        from winrt.windows.globalization import Language
        from winrt.windows.media.ocr import OcrEngine
    except Exception as exc:  # bibliotecas ausentes ou fora do Windows
        logger.debug("OCR indisponivel: %s", exc)
        return None

    for tag in PREFERRED_LANGUAGES:
        try:
            language = Language(tag)
            if OcrEngine.is_language_supported(language):
                engine = OcrEngine.try_create_from_language(language)
                if engine is not None:
                    return engine
        except Exception as exc:
            logger.debug("OCR: idioma %s indisponivel: %s", tag, exc)

    # Sem portugues: o idioma do perfil do usuario ainda le siglas e numeros.
    try:
        return OcrEngine.try_create_from_user_profile_languages()
    except Exception as exc:
        logger.debug("OCR: nenhum idioma disponivel: %s", exc)
        return None


def is_available() -> bool:
    return _engine() is not None


def _render_first_page(file_path: str):
    """Pagina 1 como (bytes BGRA, largura, altura), ou None."""
    import pypdfium2 as pdfium
    import pypdfium2.raw as pdfium_c

    pdf = pdfium.PdfDocument(file_path)
    try:
        if len(pdf) == 0:
            return None
        page = pdf[0]
        try:
            bitmap = page.render(scale=RENDER_SCALE, force_bitmap_format=pdfium_c.FPDFBitmap_BGRA)
            width, height, stride = bitmap.width, bitmap.height, bitmap.stride
            raw = bytes(bitmap.buffer)
            if stride != width * 4:
                # SoftwareBitmap exige linhas contiguas; remove o preenchimento.
                raw = b"".join(raw[row * stride:row * stride + width * 4] for row in range(height))
            return raw, width, height
        finally:
            page.close()
    finally:
        pdf.close()


async def _recognize(engine, raw: bytes, width: int, height: int):
    from winrt.windows.graphics.imaging import BitmapPixelFormat, SoftwareBitmap
    from winrt.windows.storage.streams import DataWriter

    writer = DataWriter()
    writer.write_bytes(raw)
    buffer = writer.detach_buffer()
    bitmap = SoftwareBitmap.create_copy_from_buffer(buffer, BitmapPixelFormat.BGRA8, width, height)
    return await engine.recognize_async(bitmap)


def ocr_first_page(file_path: str) -> List[str]:
    """Linhas de texto da pagina 1, na ordem de leitura; [] se nao der."""
    engine = _engine()
    if engine is None:
        return []
    try:
        rendered = _render_first_page(file_path)
        if rendered is None:
            return []
        raw, width, height = rendered
        limit: Optional[int] = getattr(engine, "max_image_dimension", None)
        if limit and (width > limit or height > limit):
            logger.debug("OCR: pagina maior que o limite do motor (%s)", limit)
            return []
        result = asyncio.run(_recognize(engine, raw, width, height))
        return [line.text.strip() for line in result.lines if line.text.strip()]
    except Exception as exc:
        logger.debug("OCR falhou em %s: %s", file_path, exc)
        return []
