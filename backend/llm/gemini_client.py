import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def configure_gemini():
    """Configure the Gemini API using the API key from environment."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        # In a real production app, we might raise an error here
        # but the requirement says "Never crash if Gemini fails"
        # and "basic exceptions cleanly". 
        # We'll handle the missing key during the call.
        return False
    
    genai.configure(api_key=api_key)
    return True

def call_gemini(prompt: str) -> str:
    """
    Send prompt to Gemini and return the response text.
    Handles basic exceptions cleanly and never crashes.
    """
    try:
        # Attempt to configure if not already done
        if not configure_gemini():
            return "Error: Gemini API key not found in environment."

        model = genai.GenerativeModel("models/gemini-2.5-flash")
        response = model.generate_content(prompt)
        
        if response and response.text:
            return response.text
        return "Error: Received empty response from Gemini."

    except Exception as e:
        # Clean exception handling as per requirements
        # We don't print the API key or sensitive info
        # Log the error (in a real app) or return a safe message
        return f"Information not available in airport documentation. (Internal Error: {str(e)})"
