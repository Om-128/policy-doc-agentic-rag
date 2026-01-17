import os
import sys

from typing import List
from utils import BASE_DIR
from custom_exception import CustomException

from langchain_community.document_loaders import PyPDFLoader, UnstructuredPDFLoader
from langchain_core.documents import Document

"""
    Responsible for loading PDF files and converting them into LangChain
    Document objects with enriched metadata.

    - Accepts absolute PDF file paths
    - Uses PyPDFLoader for text-based PDFs
    - Falls back to UnstructuredPDFLoader for scanned / govt PDFs
    - Adds standardized metadata for downstream RAG processing
"""
class PDFLoader:
        
    def load(self, file_paths: List[str]) -> List[Document]:
        """
        Load multiple PDFs and return a list of LangChain Documents.

        Args:
            file_paths (List[str]): List of absolute PDF file paths

        Returns:
            List[Document]: Loaded documents with metadata
        """
        try:
            all_docs = []

            for path in file_paths:

                docs = self.load_single_pdf(path)

                file_name = os.path.splitext(os.path.basename(path))[0]
                doc_type = self._get_type(path)

                for doc in docs:
                    doc.metadata.update({
                        "source":file_name,
                        "file_name":file_name,
                        "type":doc_type
                    })

                all_docs.extend(docs)
            
            return all_docs

        except Exception as e:
            raise CustomException(e, sys)

    def load_single_pdf(self, path):
                """
        Load a single PDF file.

        Attempts fast text extraction first using PyPDFLoader.
        Falls back to UnstructuredPDFLoader for PDFs with
        broken encodings or scanned content.

        Args:
            path (str): Absolute path to the PDF file

        Returns:
            List[Document]: Documents extracted from the PDF
        """
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


    def _get_type(self, path:str):
        return "policy" if "policies" in path.lower() else "document"