from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from service import generate_answer
import uvicorn

app = FastAPI(
    title="Airport Operations Explainer API",
    description="Backend for the Airport Ground Operations & Passenger Flow Explainer Bot",
    version="1.0.0"
)

# 2. Enable CORS (allow all origins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Pydantic request model
class QueryRequest(BaseModel):
    question: str
    persona: str
    mode: str

# 5. GET /health endpoint
@app.get("/health")
async def health_check():
    """
    Check if the API service is running.
    """
    return {"status": "running"}

# 4. POST /ask endpoint
@app.post("/ask")
async def ask_question(request: QueryRequest):
    """
    Accepts a question, persona, and mode, and returns the AI-generated answer 
    using the RAG-enhanced service layer.
    """
    try:
        # 4. Call generate_answer()
        result = generate_answer(
            question=request.question,
            persona=request.persona,
            mode=request.mode
        )
        
        # 4. Return the result in requested format
        return {"answer": result}
        
    except Exception as e:
        # 6. Basic error handling
        raise HTTPException(
            status_code=500, 
            detail=f"An error occurred while processing your request: {str(e)}"
        )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
