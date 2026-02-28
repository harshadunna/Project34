from rag.retriever import retrieve_context

if __name__ == "__main__":
    question = "Can I carry a 150ml medicine bottle?"
    print(f"Question: {question}\n")
    
    context = retrieve_context(question)
    print("Retrieved Context:")
    print(context)
