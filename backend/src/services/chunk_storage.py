from backend.src.database import SessionLocal
from backend.src.models import ResumeChunk


def save_chunks(
    candidate_id,
    chunks
):

    db = SessionLocal()

    try:

        for chunk in chunks:

            db_chunk = ResumeChunk(
                candidate_id=candidate_id,
                section=chunk["section"],
                chunk_text=chunk["text"],
                embedding=chunk["embedding"]
            )

            db.add(db_chunk)

        db.commit()

    finally:
        db.close()