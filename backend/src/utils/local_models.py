from functools import lru_cache

# from keybert import KeyBERT
from sentence_transformers import SentenceTransformer


# @lru_cache(maxsize=1)
# def get_keybert_model():
#     """
#     Loads the KeyBERT model once and caches it.
#     This function will be called by FastAPI's dependency injection system.
#     """
#     print("Loading KeyBERT model...")  # Add print for demonstration of one-time load
#     return KeyBERT("distilbert-base-nli-mean-tokens")
#
#
# def extract_main_keyword(query: str, model_instance: KeyBERT):
#     """
#     Extracts the main keyword from a query using a provided KeyBERT model instance.
#     """
#     keywords = model_instance.extract_keywords(query)
#     if keywords:
#         return keywords[0][0]
#     return None


@lru_cache(maxsize=1)
def get_embeddings_model():
    """
    Loads the miniLM-L6 model
    """
    print("Loading miniLM model...")  # Add print for demonstration of one-time load
    return SentenceTransformer("all-MiniLM-L6-v2")


# def add_embeddings(article_chunks, sentence_model):
#     """
#     input: list of article chunks
#     output: chunks with embeddings
#     """
#     embeddings = sentence_model.encode(article_chunks, convert_to_numpy=True)
#     # Convert the NumPy array of embeddings to a standard Python list of lists.
#     return embeddings.tolist()


def chunkify(text: str, max_chunk_size: int = 300) -> list[str]:
    """
    Splits a single string of text into chunks of a maximum size.

    Args:
        text (str): The text to chunk.
        max_chunk_size (int): The maximum number of words per chunk.

    Returns:
        List[str]: A list of text chunks.
    """
    if not text or len(text.split()) == 0:
        return []

    words = text.split()
    chunks = []

    # Check if the text is already small enough
    if len(words) < max_chunk_size:
        chunks.append(" ".join(words))
        return chunks

    # Chunk the text
    for i in range(0, len(words), max_chunk_size):
        chunk = " ".join(words[i : i + max_chunk_size])
        chunks.append(chunk)

    return chunks


# This is an example of what your add_embeddings() might look like
def add_embeddings(chunks: list[str], model: SentenceTransformer) -> list[list[float]]:
    """
    Generates embeddings for a list of text chunks using a pre-trained model.

    Args:
        chunks (List[str]): A list of text chunks.
        model (SentenceTransformer): The pre-trained model to use for embeddings.

    Returns:
        List[List[float]]: A list of embeddings, where each embedding is a list of floats.
    """
    if not chunks:
        return []

    embeddings = model.encode(chunks, convert_to_tensor=False)
    # Convert embeddings to a list of lists for easy storage
    return embeddings.tolist()
