def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100):
    paragraphs = text.split("\n\n")
    chunks = []

    for para in paragraphs:
        if len(para.strip()) > 50:
            chunks.append(para.strip())

    return chunks