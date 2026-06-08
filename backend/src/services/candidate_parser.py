import re

SKILLS = [
    "Python",
    "Java",
    "C++",
    "FastAPI",
    "React",
    "Docker",
    "AWS",
    "PostgreSQL",
    "MongoDB",
    "Git"
]

def parse_candidate(text: str):

    email_pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

    phone_pattern = r"(\+?\d[\d\s\-]{8,15})"

    emails = re.findall(email_pattern, text)
    phones = re.findall(phone_pattern, text)

    found_skills = []

    lower_text = text.lower()

    for skill in SKILLS:
        if skill.lower() in lower_text:
            found_skills.append(skill)

    return {
        "email": emails[0] if emails else None,
        "phone": phones[0] if phones else None,
        "skills": found_skills,
        "resume_text": text
    }