import os
import sys

from custom_exception import CustomException
from app.RAG.embedding import EmbeddingModel
from langchain_chroma import Chroma

from app.utils import CHROMA_DB_DIR, COLLECTION_NAME

"""
    This class creates Chroma DB inside CHROMA_DB_DIR
    take chunked_documents and extracts texts and metadata from them
    Apply Embedding on texts and store embedded_texts and metadata in collection 
"""
class ChromaConfig:
    
    def __init__(self):
        self.embedding_model = EmbeddingModel().get_embedding_model()

        self.store = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=self.embedding_model,
            persist_directory=CHROMA_DB_DIR
        )
    
    def add_documents(self, documents):
        try:
            texts = [doc.page_content for doc in documents]
            metadata = [doc.metadata for doc in documents]

            self.store.add_texts(
                texts=texts,
                metadatas=metadata
            )

            return self.store._collection_name
        except Exception as e:
            raise CustomException(e, sys)

    def get_store(self):
        return self.store