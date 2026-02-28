import faiss
import numpy as np


class VectorStore:
    def __init__(self, dimension):
        # Use Inner Product for cosine similarity
        self.index = faiss.IndexFlatIP(dimension)
        self.text_chunks = []

    def add_embeddings(self, embeddings, chunks):
        embeddings = np.array(embeddings).astype("float32")

        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(embeddings)

        self.index.add(embeddings)
        self.text_chunks.extend(chunks)

    def search(self, query_embedding, k=5):
        query_embedding = np.array([query_embedding]).astype("float32")

        # Normalize query embedding
        faiss.normalize_L2(query_embedding)

        distances, indices = self.index.search(query_embedding, k)

        results = []
        for idx in indices[0]:
            if idx < len(self.text_chunks):
                results.append(self.text_chunks[idx])

        return results