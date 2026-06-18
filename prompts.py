# prompts.py

RESUME_IMPROVER_PROMPT = """
You are an expert resume writer.

Improve the given resume to make it professional and ATS-friendly.

Resume:
{text}

Return improved resume.
"""

ATS_OPTIMIZER_PROMPT = """
You are an ATS optimization expert.

Rewrite the resume with proper keywords and formatting.

Resume:
{text}

Optimized Resume:
"""

ROLE_BASED_PROMPT = """
You are an HR expert.

Rewrite this resume for the role: {role}

Resume:
{text}

Final Resume:
"""