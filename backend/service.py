from rag.retriever import retrieve_context
from llm.prompt_builder import build_prompt
from llm.gemini_client import call_gemini

def generate_answer(question: str, persona: str, mode: str) -> str:
    """
    Main service function that connects RAG and LLM components.
    
    1. Retrieves relevant context from airport documentation.
    2. Builds a persona-based prompt with the retrieved context.
    3. Calls Gemini API to generate the final response.
    
    Args:
        question (str): The user's query about airport operations.
        persona (str): The traveler persona (e.g., First-time traveler, Business traveler).
        mode (str): The detail level of the response (e.g., Simple, Detailed, Checklist).
        
    Returns:
        str: The generated response or a clean error message.
    """
    try:
        # 1. Retrieve relevant context from RAG system
        context = retrieve_context(question)
        
        # 4. Clean error handling: If no documentation is found
        if not context or not context.strip():
            return "Information not available in airport documentation."
        
        # 2. Construct the specialized prompt
        prompt = build_prompt(question, persona, mode, context)
        
        # 3. Get response from Gemini
        response = call_gemini(prompt)
        
        # Double-check if the response is essentially an error or empty
        if not response or "Error:" in response:
             return "Information not available in airport documentation."
             
        return response

    except Exception:
        # 4. Gemini fails or any other unexpected error → safe fallback message
        return "Information not available in airport documentation."
