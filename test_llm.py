from backend.llm.service import generate_answer
from backend.llm.prompt_builder import build_prompt

def test_prompt_generation():
    print("Testing Prompt Generation...")
    question = "How do I check in for my flight?"
    persona = "First-time traveler"
    mode = "Checklist"
    context = "Passengers can check in at self-service kiosks or counters in the departures hall."
    
    prompt = build_prompt(question, persona, mode, context)
    print("--- GENERATED PROMPT ---")
    print(prompt)
    print("------------------------")
    assert "First-time traveler" in prompt
    assert "Checklist" in prompt
    assert "self-service kiosks" in prompt
    print("Prompt Generation Test Passed!\n")

def test_service_failure_handling():
    print("Testing Service Failure Handling (Missing API Key scenario)...")
    # This will likely return an error message since no API key is set in the environment
    response = generate_answer("Test question", "Student", "Simple", "Test context")
    print(f"Response: {response}")
    assert "Error" in response or "Information not available" in response
    print("Failure Handling Test Passed!\n")

if __name__ == "__main__":
    test_prompt_generation()
    test_service_failure_handling()
