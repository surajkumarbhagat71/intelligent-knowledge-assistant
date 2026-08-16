from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from .models import KnowledgeDocument, DocumentChunk
from .embedding import generate_embedding


def process_document(document: KnowledgeDocument):
    """
    PDF ko read karta hai, page-wise text extract karta hai,
    text ko smaller chunks me divide karta hai,
    embedding generate karta hai
    aur DocumentChunk table me save karta hai.
    """

    pdf_path = document.file.path

    reader = PdfReader(pdf_path)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    chunks = []
    chunk_index = 0

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        if not text.strip():
            continue

        page_chunks = splitter.split_text(text)

        for chunk_text in page_chunks:

            embedding = generate_embedding(chunk_text)

            chunks.append(
                DocumentChunk(
                    document=document,
                    content=chunk_text,
                    chunk_index=chunk_index,
                    page_number=page_number,
                    embedding=embedding,
                )
            )

            chunk_index += 1

    DocumentChunk.objects.bulk_create(chunks)

    return len(chunks)