import os
import sys

from custom_exception import CustomException

from app.ingestion.config_loader import PathLoaderConfig, PathLoader
from app.ingestion.pdf_loader import PDFLoader
from app.ingestion.chunking import DocumentChunker
from app.ingestion.chroma_store import ChromaConfig

"""
Creates Vectorstore and save it locally
"""
class IngestionPipeline:
    def run_ingestion_pipeline(self):
        try:
            ''' Path Loader '''
            path_loader_config = PathLoaderConfig()
            path_loader = PathLoader(path_loader_config)
            file_paths = path_loader.load_pdf()
            print("Files Paths", file_paths)

            ''' PDF Loader'''
            pdf_loader = PDFLoader()
            documents = pdf_loader.load_pdf(file_paths)
            print("Documents:", len(documents))

            ''' Chunking '''
            chunker = DocumentChunker()
            chunked_docs = chunker.chunk_document(documents)
            print("Chunked Documents:", len(chunked_docs))
            
            ''' Chroma DB '''
            chroma_config = ChromaConfig()
            collection_name = chroma_config.add_documents(chunked_docs)
            print("Collection Name:", collection_name)

            return "Database Created Successfully..."
            
        except Exception as e:
            raise CustomException(e, sys)

if __name__=="__main__":
    ingestion_pipeline = IngestionPipeline()
    print(ingestion_pipeline.run_ingestion_pipeline())