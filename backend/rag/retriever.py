from rag.loader import load_pdf
from rag.chunker import chunk_text
from rag.embeddings import embed_texts, embed_query
from rag.vector_store import VectorStore

PDF_PATH = r"D:\aitam\Project34\airport.pdf"

# 1️⃣ Load PDF
text = load_pdf(PDF_PATH)

# 2️⃣ Chunk text
chunks = chunk_text(text, chunk_size=500, overlap=100)

# 3️⃣ Generate embeddings
embeddings = embed_texts(chunks)

# 4️⃣ Build FAISS index ONCE
dimension = len(embeddings[0])
vector_store = VectorStore(dimension)
vector_store.add_embeddings(embeddings, chunks)


def retrieve_context(question: str) -> str:
    query_embedding = embed_query(question)
    results = vector_store.search(query_embedding, k=5)
    return "\n\n".join(results)