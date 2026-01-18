import os
import sys

from custom_exception import CustomException

from app.ingestion.config_loader import PathLoaderConfig, PathLoader
from app.ingestion.pdf_loader import PDFLoader
from app.ingestion.chunking import DocumentChunker
from app.ingestion.chroma_store import ChromaConfig

if __name__=="__main__":
    path_loader_config = PathLoaderConfig()
    path_loader = PathLoader(path_loader_config)

    file_paths = path_loader.load_pdf()

    pdf_loader = PDFLoader()

    documents = pdf_loader.load_pdf(file_paths)

    print(len(documents))
    print(documents[1].metadata)
    print("_______________________________________________________________")
    chunker = DocumentChunker()
    chunked_docs = chunker.chunk_document(documents=documents)
    print(len(chunked_docs))
    print("Chunked:",chunked_docs[1].metadata)

    chroma_config = ChromaConfig()
    print("_______________________________________________________________")
    print("Adding data to chroma db...")
    collection_name = chroma_config.add_documents(chunked_docs)
    print("collection_name:",collection_name)
    print("_______________________________________________________________")
    store = chroma_config.get_store()
    print("Store:",store._collection.count())
    print("_______________________________________________________________")    
    results = store.similarity_search(
    "What documents are required for Atal Pension Yojana?",
    k=1)
    print(results[0].page_content[:200])
    print(results[0].metadata)