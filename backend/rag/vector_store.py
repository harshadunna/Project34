import faiss
import numpy as np

def create_faiss_index(dimension: int) -> faiss.Index:
    """
    Creates a FAISS IndexFlatL2 with the given dimension.
    """
    return faiss.IndexFlatL2(dimension)

def add_embeddings_to_index(index: faiss.Index, embeddings: np.ndarray) -> None:
    """
    Adds embeddings to the FAISS index.
    Embeddings are assumed to be float32 already.
    """
    # Ensure it's float32 for FAISS
    if not isinstance(embeddings, np.ndarray):
        embeddings = np.array(embeddings)
    
    embeddings = embeddings.astype("float32")
    index.add(embeddings)