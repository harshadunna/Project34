from .prompt_builder import build_prompt
from .gemini_client import call_gemini

def generate_answer(question: str, persona: str, mode: str, context: str) -> str:
    """
    Main entry point for generating responses for the Airport Ground Operations bot.
    Ties together prompt building and Gemini API calls.
    """
    # 1. Build the prompt
    prompt = build_prompt(question, persona, mode, context)
    
    # 2. Call Gemini
    response = call_gemini(prompt)
    
    return response

# Usage example for FastAPI integration:
# @app.post("/ask")
# async def ask_airport_bot(request: QuestionRequest):
#     return generate_answer(
#         question=request.question,
#         persona=request.persona,
#         mode=request.mode,
#         context=fetch_relevant_context(request.question)
#     )
