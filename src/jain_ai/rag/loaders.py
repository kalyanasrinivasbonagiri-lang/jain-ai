import os

from langchain_community.document_loaders import PyMuPDFLoader

from ..config import PROCESSED_FILES_PATH
from ..utils.logging_utils import get_logger


logger = get_logger("jain_ai.rag.loaders")


def list_pdf_files(folder_path):
    if not os.path.isdir(folder_path):
        logger.warning("Data folder not found: %s", folder_path)
        return []

    try:
        pdf_files = [
            file_name for file_name in os.listdir(folder_path)
            if file_name.lower().endswith(".pdf")
        ]
    except OSError as exc:
        logger.exception("Could not read data folder '%s': %s", folder_path, exc)
        return []

    return sorted(pdf_files)


def load_processed_files():
    if not os.path.exists(PROCESSED_FILES_PATH):
        return set()

    try:
        with open(PROCESSED_FILES_PATH, "r", encoding="utf-8") as file_obj:
            return {line.strip() for line in file_obj if line.strip()}
    except OSError as exc:
        logger.exception("Could not read processed files tracker '%s': %s", PROCESSED_FILES_PATH, exc)
        return set()


def save_processed_files(processed_files):
    try:
        with open(PROCESSED_FILES_PATH, "w", encoding="utf-8") as file_obj:
            for filename in sorted(processed_files):
                file_obj.write(filename + "\n")
    except OSError as exc:
        logger.exception("Could not write processed files tracker '%s': %s", PROCESSED_FILES_PATH, exc)


def load_pdfs_by_name(folder_path, file_names):
    loaded_docs = []

    for file_name in sorted(file_names):
        full_path = os.path.join(folder_path, file_name)

        try:
            loader = PyMuPDFLoader(full_path)
            file_docs = loader.load()
        except Exception as exc:
            logger.warning("Skipping unreadable PDF '%s': %s", file_name, exc)
            continue

        for index, doc in enumerate(file_docs):
            doc.metadata["source"] = file_name
            doc.metadata["file_path"] = full_path
            doc.metadata["page_number"] = doc.metadata.get("page", index)

        loaded_docs.extend(file_docs)

    return loaded_docs


def load_new_pdfs(folder_path, processed_files):
    all_pdf_files = list_pdf_files(folder_path)
    new_pdf_files = [file_name for file_name in all_pdf_files if file_name not in processed_files]

    if not new_pdf_files:
        return [], processed_files

    new_docs = load_pdfs_by_name(folder_path, new_pdf_files)
    successfully_loaded_files = {doc.metadata["source"] for doc in new_docs}

    if successfully_loaded_files:
        processed_files = set(processed_files)
        processed_files.update(successfully_loaded_files)
        save_processed_files(processed_files)

    for file_name in sorted(set(new_pdf_files) - successfully_loaded_files):
        logger.warning("PDF was not marked as processed because it could not be loaded: %s", file_name)

    return new_docs, processed_files


def load_all_pdfs(folder_path):
    return load_pdfs_by_name(folder_path, list_pdf_files(folder_path))
