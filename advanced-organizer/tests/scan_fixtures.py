"""Gera PDFs "escaneados": so imagem, sem nenhuma camada de texto.

Parte de um PDF de texto gerado por pdf_fixtures, rasteriza a pagina com o
pdfium e grava um PDF novo contendo apenas essa imagem - exatamente o que um
scanner entrega. O pdfminer nao extrai nada dele; so o OCR le.
"""
import os
import tempfile

import pypdfium2 as pdfium

from pdf_fixtures import build_pdf


def build_scanned_pdf(path, lines, scale=3.0):
    with tempfile.TemporaryDirectory() as tmp:
        texto = build_pdf(os.path.join(tmp, "texto.pdf"), lines)
        origem = pdfium.PdfDocument(texto)
        try:
            pagina = origem[0]
            largura, altura = pagina.get_size()
            bitmap = pagina.render(scale=scale)
            pagina.close()

            destino = pdfium.PdfDocument.new()
            nova = destino.new_page(largura, altura)
            imagem = pdfium.PdfImage.new(destino)
            imagem.set_bitmap(bitmap)
            imagem.set_matrix(pdfium.PdfMatrix().scale(largura, altura))
            nova.insert_obj(imagem)
            nova.gen_content()
            destino.save(path)
            nova.close()
            destino.close()
        finally:
            origem.close()
    return path
