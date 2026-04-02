import io

from PIL import Image

from ..llm.groq_client import run_vision_ocr


def extract_text_from_image_bytes(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))
    image_format = (image.format or "PNG").lower()
    mime_type = f"image/{'jpeg' if image_format == 'jpg' else image_format}"
    return run_vision_ocr(image_bytes, mime_type)
