def build_prompt(question: str, persona: str, mode: str, context: str) -> str:
    """
    Builds a structured prompt for the Gemini LLM based on persona and mode.
    """
    
    # System Rules
    system_rules = """
SYSTEM RULES:
- Only explain airport ground operations.
- Do NOT issue boarding passes.
- Do NOT modify flight details.
- Do NOT provide booking services.
- Use ONLY provided context.
- If answer not found in context, respond exactly with:
  "Information not available in airport documentation."
"""

    # Persona Logic
    persona_instructions = f"""
PERSONA LOGIC:
- Adapt tone and complexity for this persona: {persona}.
- Examples of how to behave:
    - First-time traveler: Simple, reassuring, very detailed on basics.
    - Student: Informative, concise, uses modern but professional language.
    - Elderly passenger: Patient, clear, large-print-style clarity, avoid jargon.
    - Business traveler: Efficient, bullet points, time-saving tips.
"""

    # Mode Logic
    mode_instructions = ""
    if mode == "Simple":
        mode_instructions = "MODE: Simple - Provide a short and easy explanation for quick understanding."
    elif mode == "Detailed":
        mode_instructions = "MODE: Detailed - Provide a comprehensive and in-depth explanation."
    elif mode == "Checklist":
        mode_instructions = "MODE: Checklist - Format the response as a clear, step-by-step checklist."

    # Response Format Rules
    format_rules = """
RESPONSE FORMAT RULES:
- Use Markdown formatting
- Use clear headings (###)
- Use bullet points for steps
- Always include:
    - Main explanation section
    - "Important Notes" section if applicable
"""

    # Final Prompt Assembly
    full_prompt = f"""
{system_rules}

{persona_instructions}

{mode_instructions}

{format_rules}

CONTEXT:
{context}

USER QUESTION:
{question}
"""
    return full_prompt.strip()
