import os
import sys
from custom_exception import CustomException
from langchain_huggingface.embeddings import HuggingFaceEmbeddings

from app.utils import EMBEDDING_MODEL_NAME

"""
    This is a helper class which creates Embedding model
    and returns the embedding model
"""
class EmbeddingModel:
    def __init__(self):
        self.embedding_model = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL_NAME
        )

    def get_embedding_model(self):
        return self.embedding_model