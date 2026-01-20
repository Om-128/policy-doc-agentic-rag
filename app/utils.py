import os

BASE_DIR = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
) 

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

CHROMA_DB_DIR = os.path.join(BASE_DIR, 'data', 'vectorstore')

COLLECTION_NAME = "software_faq"