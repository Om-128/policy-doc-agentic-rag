import os
import sys

from custom_exception import CustomException

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List

"""
    This Class Takes List[Documents] which we will get by using
    our PDF loader
    Then we will split doc and get List[chunks]
    Then we add the same metadata to each chunk in the list[chunks]
    append the chunk to chunked_list
    Return the chunked_list
"""
class DocumentChunker:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=150,
            separators=["\n\n", "\n", ".", " "]
        )
    
    def chunk_document(self, documents: List[Document]) -> List[Document]:
        try:
            chunked_docs = []

            for doc in documents:
                chunks = self.text_splitter.split_text(doc.page_content)

                for i, chunk in enumerate(chunks):
                    chunked_docs.append(
                        Document(
                            page_content=chunk,
                            metadata={
                                **doc.metadata,
                                "chunk_id": i
                            }
                        )
                    )

            return chunked_docs
        except Exception as e:
            raise CustomException(e, sys)