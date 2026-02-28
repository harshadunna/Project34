from sentence_transformers import SentenceTransformer
import numpy as np

# Load model ONCE at module level
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_texts(texts: list[str]) -> np.ndarray:
    """
    Encodes a list of texts into embeddings using SentenceTransformer.
    Returns a numpy array of float32 embeddings.
    """
    embeddings = model.encode(texts, convert_to_numpy=True)
    return embeddings.astype("float32")
