

from functools import lru_cache

from keybert import KeyBERT
from sentence_transformers import SentenceTransformer


@lru_cache(maxsize=1)
def get_keybert_model():
    """
    Loads the KeyBERT model once and caches it.
    This function will be called by FastAPI's dependency injection system.
    """
    print("Loading KeyBERT model...") # Add print for demonstration of one-time load
    return KeyBERT('distilbert-base-nli-mean-tokens')

def extract_main_keyword(query: str, model_instance: KeyBERT):
    """
    Extracts the main keyword from a query using a provided KeyBERT model instance.
    """
    keywords = model_instance.extract_keywords(query)
    if keywords:
        return keywords[0][0]
    return None




@lru_cache(maxsize=1)
def get_embeddings_model():
    """
    Loads the miniLM-L6 model
    """
    print("Loading miniLM model...") # Add print for demonstration of one-time load
    return SentenceTransformer('all-MiniLM-L6-v2')

def add_embeddings(article_chunks, sentence_model):
    """
    input: list of article chunks
    output: chunks with embeddings
    """
    for chunk in article_chunks:
        embedding = sentence_model.encode(chunk.content)
        chunk.embed(embedding)
    return # the output of this is the ArticleChunk object gets embedded



