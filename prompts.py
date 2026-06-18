# prompts.py

RESUME_IMPROVER_PROMPT = """
You are an expert resume editor.

TASK:
Rewrite the resume into a fully professional, grammatically correct version.

STRICT RULES:
- Fix ALL grammar and spelling mistakes
- Correct capitalization (e.g., Raj Kumar, Python, Machine Learning)
- Rewrite sentences in formal professional English
- DO NOT copy original sentences exactly
- DO NOT repeat input text as-is
- Maintain original meaning
- Make it structured and ATS-friendly
- Remove informal language like "little bit", "dont know", etc.

OUTPUT RULE:
Return ONLY the final improved resume.
No explanations. No original text.

Resume:
{text}

Final Resume:
"""


ATS_OPTIMIZER_PROMPT = """
You are an ATS optimization expert.

TASK:
Rewrite resume for ATS systems.

STRICT RULES:
- Fully rewrite all sentences
- Improve grammar and structure
- Add professional wording
- Improve keyword richness
- DO NOT fabricate new experience

OUTPUT:
Only final ATS-friendly resume.

Resume:
{text}

ATS Resume:
"""


ROLE_BASED_PROMPT = """
You are a senior HR resume writer.

TASK:
Rewrite resume for role: {role}

STRICT RULES:
- Fully rewrite entire resume
- Fix grammar and capitalization
- Make it role-specific and professional
- Improve clarity and structure
- DO NOT invent experience

Resume:
{text}

Final Resume for {role}:
"""
