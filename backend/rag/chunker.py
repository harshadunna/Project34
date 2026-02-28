def chunk_text(text: str, words_per_chunk: int = 150) -> list[str]:
    """
    Splits text into chunks of ~150 words each.
    Ignores empty chunks, strips whitespace, and normalizes characters.
    """
    # Basic normalization for common PDF extraction artifacts
    # (e.g., ligatures or mis-encoded characters)
    text = text.replace("Ɵ", "ti")  # Common in some PDF fonts for 'ti'
    text = text.replace("ﬁ", "fi")
    text = text.replace("ﬂ", "fl")
    text = text.replace("Ō", "ft")  # Common for 'ft' like in 'aircraft'
    
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), words_per_chunk):
        chunk = " ".join(words[i : i + words_per_chunk])
        chunk = chunk.strip()
        if chunk:
            chunks.append(chunk)
            
    return chunks