from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    Text,
    JSON,
    ForeignKey
)

from sqlalchemy.orm import declarative_base

from pgvector.sqlalchemy import Vector

Base = declarative_base()


class Candidate(Base):

    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)

    email = Column(String)

    phone = Column(String)

    linkedin = Column(String)

    github = Column(String)

    skills = Column(JSON)

    experience_years = Column(Integer)

    education = Column(JSON)

    experience = Column(JSON)

    projects = Column(JSON)

    certifications = Column(JSON)

    resume_text = Column(Text)

    filename = Column(String)

    pdf_url = Column(String)


class Job(Base):

    __tablename__ = "jobs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    title = Column(String)

    description = Column(Text)

    skills = Column(JSON)

    experience_years = Column(
        Integer,
        default=0
    )

    certifications = Column(JSON)


class ResumeChunk(Base):

    __tablename__ = "resume_chunks"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    candidate_id = Column(
        Integer,
        ForeignKey("candidates.id", ondelete="CASCADE"),
        nullable=False
    )

    section = Column(
        String,
        nullable=False
    )

    chunk_text = Column(
        Text,
        nullable=False
    )

    embedding = Column(
        Vector(384)
    )


class JobCandidate(Base):

    __tablename__ = "job_candidates"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    job_id = Column(
        Integer,
        ForeignKey(
            "jobs.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    candidate_id = Column(
        Integer,
        ForeignKey(
            "candidates.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    score = Column(Float)          # Fixed: was Integer, scores are floats e.g. 72.43

    explanation = Column(JSON)

    matched_skills = Column(JSON)

    missing_skills = Column(JSON)

    score_breakdown = Column(JSON)