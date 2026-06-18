# utils.py

def fake_ai_response(prompt, resume_text):
    """
    Simulates AI output (since we are not using OpenAI API).
    This is enough for GenAI + Prompt Engineering project.
    """

    # Basic transformation simulation
    improved_text = resume_text.strip()

    # Simple enhancements (demo logic)
    improved_text = improved_text.replace("i ", "I ")
    improved_text = improved_text.replace("python", "Python")
    improved_text = improved_text.replace("ml", "Machine Learning")

    return f"""
=== AI GENERATED RESUME ===

{improved_text}

===========================
Improved using Prompt Engineering System
"""