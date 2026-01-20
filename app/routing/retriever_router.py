import os
import sys
from custom_exception import CustomException

from typing import List
from langchain_core.documents import Document

from app.ingestion.chroma_store import ChromaConfig


class RetrieverRouter:

    def __init__(self):
        self.store = ChromaConfig().get_store()

    def retreive(self, query: str, k: int = 4) -> List[Document]:

        # Else Search with metadata
        return self.store.similarity_search(
            query,
            k,
        )

if __name__=="__main__":
    router = RetrieverRouter()
    query = "Why can't I get the 'set SP4T switch' command to work via Ethernet? "
    docs = router.retreive(query, k=5)
    for d in docs:
        print("Answer:", d.page_content)
        print("__________________________________")
        print("Metadata:", d.metadata)