import numpy as np
from .loader import load_pdf
from .chunker import chunk_text
from .embedder import embed_texts
from .vector_store import create_faiss_index, add_embeddings_to_index

# --- MODULE INITIALIZATION ---
# Load, Chunk, Embed, and Index PDF once on module load.
try:
    # 1. Load PDF
    raw_text = load_pdf()
    
    # 2. Chunk text (150 words per chunk)
    CHUNKS = chunk_text(raw_text, words_per_chunk=150)
    print(f"RAG Initialized: {len(CHUNKS)} chunks created")
    
    if CHUNKS:
        # 3. Create embeddings
        embeddings = embed_texts(CHUNKS)
        
        # 4. Build FAISS index
        dimension = embeddings.shape[1]
        INDEX = create_faiss_index(dimension)
        add_embeddings_to_index(INDEX, embeddings)
    else:
        INDEX = None

except Exception as e:
    print(f"RAG Initialization Error: {e}")
    CHUNKS = []
    INDEX = None


def retrieve_context(question: str, top_k: int = 3) -> str:
    """
    Finds the top_k most relevant chunks for the question using FAISS.
    Returns the joined chunks as a single string.
    """
    if INDEX is None or not CHUNKS:
        return ""

    try:
        # 1. Convert question to embedding (float32)
        question_embedding = embed_texts([question])
        question_embedding = question_embedding.astype("float32")
        
        # 2. Perform similarity search
        distances, indices = INDEX.search(question_embedding, top_k)
        
        # 3. Debug Print
        print("\n[DEBUG] Debugging retrieval precision:")
        for i, idx in enumerate(indices[0]):
            if 0 <= idx < len(CHUNKS):
                print(f" - Chunk {idx}: {CHUNKS[idx][:200]}...")
            else:
                print(f" - Chunk {idx}: (Index out of range)")
        
        # 4. Join top chunks
        relevant_chunks = []
        for idx in indices[0]:
            if 0 <= idx < len(CHUNKS):
                relevant_chunks.append(CHUNKS[idx])
        
        return "\n".join(relevant_chunks) if relevant_chunks else ""

    except Exception as e:
        print(f"RAG Retrieval Error: {e}")
        return ""