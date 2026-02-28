# test_llm.py

from llm.prompt_builder import build_prompt
from llm.gemini_client import call_gemini

question = "Explain boarding procedure"
persona = "First-time traveler"
mode = "Checklist"
context = "Boarding begins 30 minutes before departure..."

prompt = build_prompt(question, persona, mode, context)
response = call_gemini(prompt)

print(response)