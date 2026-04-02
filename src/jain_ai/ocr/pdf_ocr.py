import re

import fitz

from ..llm.groq_client import run_vision_ocr


def pdf_page_to_png_bytes(page):
    pixmap = page.get_pixmap(matrix=fitz.Matrix(2, 2))
    return pixmap.tobytes("png")


def extract_text_from_pdf_bytes(pdf_bytes):
    pdf = fitz.open(stream=pdf_bytes, filetype="pdf")
    direct_text = "\n".join(page.get_text("text") for page in pdf).strip()

    if len(re.sub(r"\s+", "", direct_text)) >= 80:
        return direct_text

    ocr_pages = []
    for page in pdf[:3]:
        ocr_text = run_vision_ocr(pdf_page_to_png_bytes(page), "image/png")
        if ocr_text and ocr_text != "NO_TEXT_FOUND":
            ocr_pages.append(ocr_text)

    return "\n\n".join(ocr_pages).strip()
