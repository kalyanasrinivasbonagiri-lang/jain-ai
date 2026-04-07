import os

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.documents import Document

from ..config import PROCESSED_FILES_PATH
from ..utils.logging_utils import get_logger


logger = get_logger("jain_ai.rag.loaders")


SUPPORTED_SOURCE_EXTENSIONS = (".pdf", ".txt")
IGNORED_SOURCE_KEYWORDS = ("template", "example", "sample")


def should_index_source_file(file_name):
    lower_name = file_name.lower()
    if not lower_name.endswith(SUPPORTED_SOURCE_EXTENSIONS):
        return False
    return not any(keyword in lower_name for keyword in IGNORED_SOURCE_KEYWORDS)


def list_source_files(folder_path):
    if not os.path.isdir(folder_path):
        logger.warning("Data folder not found: %s", folder_path)
        return []

    try:
        source_files = []
        for root, _, files in os.walk(folder_path):
            for file_name in files:
                if not should_index_source_file(file_name):
                    continue
                full_path = os.path.join(root, file_name)
                relative_path = os.path.relpath(full_path, folder_path)
                source_files.append(relative_path)
    except OSError as exc:
        logger.exception("Could not read data folder '%s': %s", folder_path, exc)
        return []

    return sorted(source_files)


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


def load_texts_by_name(folder_path, file_names):
    loaded_docs = []

    for file_name in sorted(file_names):
        full_path = os.path.join(folder_path, file_name)

        try:
            with open(full_path, "r", encoding="utf-8") as file_obj:
                content = file_obj.read()
        except OSError as exc:
            logger.warning("Skipping unreadable text file '%s': %s", file_name, exc)
            continue

        if not content.strip():
            logger.warning("Skipping empty text file '%s'", file_name)
            continue

        loaded_docs.append(
            Document(
                page_content=content,
                metadata={
                    "source": file_name,
                    "file_path": full_path,
                    "page_number": 0,
                },
            )
        )

    return loaded_docs


def load_documents_by_name(folder_path, file_names):
    pdf_files = [file_name for file_name in file_names if file_name.lower().endswith(".pdf")]
    text_files = [file_name for file_name in file_names if file_name.lower().endswith(".txt")]
    return load_pdfs_by_name(folder_path, pdf_files) + load_texts_by_name(folder_path, text_files)


def load_new_documents(folder_path, processed_files):
    all_source_files = list_source_files(folder_path)
    new_source_files = [file_name for file_name in all_source_files if file_name not in processed_files]

    if not new_source_files:
        return [], processed_files

    new_docs = load_documents_by_name(folder_path, new_source_files)
    successfully_loaded_files = {doc.metadata["source"] for doc in new_docs}

    if successfully_loaded_files:
        processed_files = set(processed_files)
        processed_files.update(successfully_loaded_files)
        save_processed_files(processed_files)

    for file_name in sorted(set(new_source_files) - successfully_loaded_files):
        logger.warning("Source file was not marked as processed because it could not be loaded: %s", file_name)

    return new_docs, processed_files


def load_all_documents(folder_path):
    return load_documents_by_name(folder_path, list_source_files(folder_path))
