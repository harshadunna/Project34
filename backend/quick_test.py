# quick_test.py

import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

print("Loaded Key:", api_key)  # check if it prints

genai.configure(api_key=api_key)

for m in genai.list_models():
    print(m.name)