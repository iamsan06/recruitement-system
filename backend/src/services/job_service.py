from src.database import SessionLocal
from src.models import Job
from src.services.job_parser import (
    parse_job_description
)

def create_job(job_data):

    db = SessionLocal()

    try:

        parsed = (
            parse_job_description(
                job_data.description
            )
        )

        job = Job(
            title=job_data.title,
            description=job_data.description,

            skills=parsed.get(
                "skills",
                []
            ),

            experience_years=parsed.get(
                "experience_years",
                0
            ),

            certifications=parsed.get(
                "certifications",
                []
            )
        )

        db.add(job)

        db.commit()

        db.refresh(job)

        return job

    finally:

        db.close()


def get_all_jobs():

    db = SessionLocal()

    try:
        return db.query(Job).all()

    finally:
        db.close()


def get_job_by_id(job_id):

    db = SessionLocal()

    try:
        return db.query(Job).filter(
            Job.id == job_id
        ).first()

    finally:
        db.close()


def delete_job(job_id):

    db = SessionLocal()

    try:

        job = db.query(Job).filter(
            Job.id == job_id
        ).first()

        if not job:
            return False

        db.delete(job)

        db.commit()

        return True

    finally:
        db.close()