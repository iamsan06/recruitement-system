from src.database import SessionLocal
from src.models import Candidate


def save_candidate(candidate_data):

    db = SessionLocal()

    try:

        candidate = Candidate(
            name=candidate_data.get("name"),
            email=candidate_data.get("email"),
            phone=candidate_data.get("phone"),
            linkedin=candidate_data.get("linkedin"),
            github=candidate_data.get("github"),
            skills=candidate_data.get("skills"),
            experience_years=candidate_data.get("experience_years"),
            education=candidate_data.get("education"),
            experience=candidate_data.get("experience"),
            projects=candidate_data.get("projects"),
            certifications=candidate_data.get("certifications"),
            resume_text=candidate_data.get("resume_text"),
            filename=candidate_data.get("filename"),
            pdf_url=candidate_data.get("pdf_url")
        )

        db.add(candidate)

        db.commit()

        db.refresh(candidate)

        return candidate

    finally:
        db.close()