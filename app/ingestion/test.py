import os
import sys

from custom_exception import CustomException

from app.ingestion.config_loader import PathLoaderConfig, PathLoader
from app.ingestion.pdf_loader import PDFLoader

if __name__=="__main__":
    path_loader_config = PathLoaderConfig()
    path_loader = PathLoader(path_loader_config)

    file_paths = path_loader.load_pdf()

    pdf_loader = PDFLoader()

    documents = pdf_loader.load(file_paths)

    print(len(documents))
    print(documents[0].metadata)
