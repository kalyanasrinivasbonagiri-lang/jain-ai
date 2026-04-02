from langchain_text_splitters import RecursiveCharacterTextSplitter


splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)


def split_documents_with_ids(documents_to_split):
    if not documents_to_split:
        return [], []

    split_docs = splitter.split_documents(documents_to_split)
    chunk_counts = {}
    chunk_ids = []

    for doc in split_docs:
        source = doc.metadata.get("source", "unknown")
        page_number = doc.metadata.get("page_number", doc.metadata.get("page", 0))
        chunk_key = f"{source}:{page_number}"
        chunk_index = chunk_counts.get(chunk_key, 0)
        chunk_counts[chunk_key] = chunk_index + 1

        doc.metadata["chunk_index"] = chunk_index
        chunk_ids.append(f"{source}:{page_number}:{chunk_index}")

    return split_docs, chunk_ids
