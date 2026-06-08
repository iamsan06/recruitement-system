from src.database import SessionLocal
from src.models import Candidate


def get_all_candidates():

    db = SessionLocal()

    try:
        return db.query(Candidate).all()

    finally:
        db.close()


def get_candidate_by_id(candidate_id):

    db = SessionLocal()

    try:
        return db.query(Candidate).filter(
            Candidate.id == candidate_id
        ).first()

    finally:
        db.close()


def delete_candidate(candidate_id):

    db = SessionLocal()

    try:

        candidate = db.query(Candidate).filter(
            Candidate.id == candidate_id
        ).first()

        if not candidate:
            return False

        db.delete(candidate)

        db.commit()

        return True

    finally:
        db.close()