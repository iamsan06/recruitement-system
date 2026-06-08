import json
import os

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv(
        "GROQ_API_KEY"
    )
)


def parse_job_description(
    description: str
):

    prompt = f"""
You are an expert technical recruiter.

Extract job requirements.

Return ONLY valid JSON.

Schema:

{{
    "skills": [],
    "experience_years": 0,
    "certifications": []
}}
Extract ONLY concrete technical skills.

Examples:

AWS
Docker
Kubernetes
Terraform
Jenkins
Linux
Python
FastAPI

Do NOT return generic concepts like:

Cloud Computing
Software Development
Programming
Deployment
Engineering

Skills must be technologies, tools, frameworks,
platforms, languages, or certifications.

Job Description:

{description}
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

    content = (
        response
        .choices[0]
        .message
        .content
    )

    content = content.replace(
        "```json",
        ""
    )

    content = content.replace(
        "```",
        ""
    )

    return json.loads(
        content.strip()
    )