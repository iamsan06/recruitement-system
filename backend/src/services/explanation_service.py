import os

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_match_explanation(
    job_description: str,
    evidence_chunks: list
):

    evidence_text = "\n\n".join(
        evidence_chunks
    )

    prompt = f"""
You are an expert technical recruiter.

Job Description:

{job_description}

Resume Evidence:

{evidence_text}

Explain:

1. Why this candidate matches
2. Relevant skills
3. Relevant experience/projects
4. Missing skills if any

You MUST ONLY use information present in the evidence.

Do not assume skills, projects, technologies, experience,
or achievements that are not explicitly mentioned.

If evidence is insufficient, say so.

Return JSON only.

Return concise recruiter feedback.

Maximum 150 words.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return (
        response
        .choices[0]
        .message
        .content
    )