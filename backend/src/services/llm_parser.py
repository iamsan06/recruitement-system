import os
import json

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def parse_candidate_with_llm(
    resume_text: str
):

    prompt = f"""
You are an expert technical recruiter.

Extract information from the resume.

Return ONLY valid JSON.

Schema:

{{
    "name": "",
    "email": "",
    "phone": "",
    "linkedin": "",
    "github": "",

    "skills": [],

    "experience_years": 0,

    "education": [],

    "experience": [],

    "projects": [],

    "certifications": []
}}

Resume:

{resume_text}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    content = response.choices[0].message.content

    content = content.replace(
        "```json",
        ""
    )

    content = content.replace(
        "```",
        ""
    )

    return json.loads(content)