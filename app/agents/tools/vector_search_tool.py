import os
import sys

from typing import List
from custom_exception import CustomException
from app.ingestion.chroma_store import ChromaConfig

class VectorSearchTool:
    def __init__(self):
        self.store = ChromaConfig().get_store()
    
    def run(self, query : str, k: int = 5, score_threshold: float = 0.3) -> List[str]:
        try:
            results = self.store.similarity_search_with_relevance_scores(
                query,
                k,
            )

            # Filter out low quality match
            filtered = [
                doc.page_content
                for doc, score in results
                if score >= score_threshold
            ]

            return filtered
        except Exception as e:
            raise CustomException(e, sys)