import os
import sys

from typing import List
from app.utils import BASE_DIR
from custom_exception import CustomException

from langchain_community.document_loaders import PyPDFLoader, UnstructuredPDFLoader
from langchain_core.documents import Document

"""
    Responsible for loading PDF files and converting them into LangChain
    Document objects with enriched metadata.

    - Accepts absolute PDF file paths
    - Uses PyPDFLoader for text-based PDFs
    - Falls back to UnstructuredPDFLoader if Using PyPDFLoader not possible
    - Adds standardized metadata for downstream RAG processing
"""
class PDFLoader:
        
    def load_pdf(self, file_paths: List[str]) -> List[Document]:
        try:
            all_docs = []

            for path in file_paths:

                docs = self.load_single_pdf(path)

                file_name = os.path.splitext(os.path.basename(path))[0]

                for doc in docs:
                    doc.metadata.update({
                        "source":file_name,
                        "file_name":file_name
                    })

                all_docs.extend(docs)
            
            return all_docs

        except Exception as e:
            raise CustomException(e, sys)

    def load_single_pdf(self, path):
        try:
            # First try PyPDF (fast)
            loader = PyPDFLoader(path)
            return loader.load()

        except Exception:
            # Fallback for govt / scanned PDFs
            loader = UnstructuredPDFLoader(
                path,
                mode="elements",
                strategy="fast"
            )
            return loader.load()