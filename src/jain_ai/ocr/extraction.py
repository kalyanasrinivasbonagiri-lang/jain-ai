from PIL import UnidentifiedImageError
from werkzeug.utils import secure_filename

from ..constants.settings import IMAGE_EXTENSIONS, PDF_EXTENSIONS
from ..utils.logging_utils import get_logger
from ..utils.validators import allowed_file
from .image_ocr import extract_text_from_image_bytes
from .pdf_ocr import extract_text_from_pdf_bytes


logger = get_logger("jain_ai.ocr.extraction")


def extract_uploaded_text(file_storage):
    if not file_storage or not file_storage.filename:
        return "", "", None

    filename = secure_filename(file_storage.filename)
    extension = "." + filename.lower().rsplit(".", 1)[-1] if "." in filename else ""

    if not allowed_file(filename):
        return "", filename, "Unsupported file type. Please upload a PDF or image file."

    try:
        file_bytes = file_storage.read()
    except Exception:
        return "", filename, "I could not read the uploaded file."

    if not file_bytes:
        return "", filename, "The uploaded file is empty."

    try:
        if extension in PDF_EXTENSIONS:
            return extract_text_from_pdf_bytes(file_bytes), filename, None
        if extension in IMAGE_EXTENSIONS:
            return extract_text_from_image_bytes(file_bytes), filename, None
    except UnidentifiedImageError:
        logger.warning("Uploaded image could not be parsed: %s", filename)
        return "", filename, "The uploaded image could not be processed."
    except Exception as exc:
        logger.exception("File extraction failed for '%s': %s", filename, exc)
        return "", filename, "I ran into a problem while reading that file."

    return "", filename, "Unsupported file type. Please upload a PDF or image file."
