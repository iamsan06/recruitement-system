from src.database import SessionLocal

from src.models import (
    JobCandidate
)


def save_results(
    job_id,
    results
):

    db = SessionLocal()

    try:

        db.query(
            JobCandidate
        ).filter(
            JobCandidate.job_id
            == job_id
        ).delete()

        for result in results:

            row = JobCandidate(

                job_id=job_id,

                candidate_id=result[
                    "candidate_id"
                ],

                score=result[
                    "score"
                ],

                explanation=result[
                    "explanation"
                ],

                matched_skills=result[
                    "matched_skills"
                ],

                missing_skills=result[
                    "missing_skills"
                ],

                score_breakdown=result[
                    "score_breakdown"
                ]
            )

            db.add(row)

        db.commit()

    finally:

        db.close()


def get_results(
    job_id
):

    db = SessionLocal()

    try:

        rows = db.query(
            JobCandidate
        ).filter(
            JobCandidate.job_id
            == job_id
        ).order_by(
            JobCandidate.score.desc()
        ).all()

        # Serialize to dicts so FastAPI can return them properly
        return [
            {
                "id": row.id,
                "job_id": row.job_id,
                "candidate_id": row.candidate_id,
                "score": row.score,
                "explanation": row.explanation,
                "matched_skills": row.matched_skills,
                "missing_skills": row.missing_skills,
                "score_breakdown": row.score_breakdown
            }
            for row in rows
        ]

    finally:

        db.close()