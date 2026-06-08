from collections import defaultdict
import json

from sqlalchemy import text

from src.database import SessionLocal
from src.models import Candidate
from src.services.embedding_service import generate_embedding
from src.services.explanation_service import generate_match_explanation
from src.services.scoring_service import (
    skill_match_score,
    experience_score,
    certification_score
)
from src.services.result_service import save_results


def match_job(job):

    db = SessionLocal()

    try:
        job_embedding = generate_embedding(job.description)

        embedding_str = (
            "[" + ",".join(str(x) for x in job_embedding) + "]"
        )

        query = text(
            """
            SELECT
                candidate_id,
                section,
                chunk_text,
                1 - (
                    embedding <=>
                    CAST(:embedding AS vector)
                ) AS similarity

            FROM resume_chunks

            ORDER BY
                embedding <=>
                CAST(:embedding AS vector)

            LIMIT 50
            """
        )

        result = db.execute(query, {"embedding": embedding_str})
        rows = result.fetchall()

        if not rows:
            return []

        candidate_matches = defaultdict(list)

        for row in rows:
            candidate_matches[row.candidate_id].append(
                {
                    "section": row.section,
                    "text": row.chunk_text,
                    "similarity": float(row.similarity)
                }
            )

        ranked = []
        seen_emails = set()

        for candidate_id, matches in candidate_matches.items():

            candidate = (
                db.query(Candidate)
                .filter(Candidate.id == candidate_id)
                .first()
            )

            if not candidate:
                continue

            if candidate.email:
                email = candidate.email.strip().lower()

                if email in seen_emails:
                    continue

                seen_emails.add(email)

            matches.sort(key=lambda x: x["similarity"], reverse=True)
            top_matches = matches[:3]

            vector_score = (
                sum(m["similarity"] for m in top_matches) / len(top_matches)
            ) * 100

            skill_score = skill_match_score(
                candidate.skills or [],
                job.skills or []
            )

            experience_score_value = experience_score(
                candidate.experience_years or 0,
                job.experience_years or 0
            )

            cert_score = certification_score(
                candidate.certifications or [],
                job.certifications or []
            )

            # -----------------------------
            # HARD FILTERS
            # -----------------------------

            if vector_score < 50:
                continue

            if job.skills and skill_score < 30:
                continue

            # -----------------------------
            # DYNAMIC WEIGHTS
            # -----------------------------

            weights = {"vector": 0.40}

            if job.skills:
                weights["skills"] = 0.35

            if job.experience_years and job.experience_years > 0:
                weights["experience"] = 0.15

            if job.certifications:
                weights["certifications"] = 0.10

            total_weight = sum(weights.values())

            for key in weights:
                weights[key] /= total_weight

            final_score = (
                vector_score * weights.get("vector", 0)
                + skill_score * weights.get("skills", 0)
                + experience_score_value * weights.get("experience", 0)
                + cert_score * weights.get("certifications", 0)
            )

            candidate_skills = {
                str(skill).lower() for skill in (candidate.skills or [])
            }

            required_skills = {
                str(skill).lower() for skill in (job.skills or [])
            }

            matched_skills = sorted(list(candidate_skills & required_skills))
            missing_skills = sorted(list(required_skills - candidate_skills))

            score_breakdown = {"vector": round(vector_score, 2)}

            if job.skills:
                score_breakdown["skills"] = round(skill_score, 2)

            if job.experience_years and job.experience_years > 0:
                score_breakdown["experience"] = round(experience_score_value, 2)

            if job.certifications:
                score_breakdown["certifications"] = round(cert_score, 2)

            ranked.append(
                {
                    "candidate_id": candidate.id,
                    "candidate_name": candidate.name,
                    "score": round(final_score, 2),
                    "score_breakdown": score_breakdown,
                    "matched_skills": matched_skills,
                    "missing_skills": missing_skills,
                    "top_matches": top_matches
                }
            )

        ranked.sort(key=lambda x: x["score"], reverse=True)
        ranked = ranked[:5]

        final_results = []

        for candidate in ranked:

            evidence_texts = [match["text"] for match in candidate["top_matches"]]

            try:
                explanation = generate_match_explanation(
                    job.description,
                    evidence_texts
                )

                if isinstance(explanation, str):
                    try:
                        cleaned = (
                            explanation
                            .replace("```json", "")
                            .replace("```", "")
                            .strip()
                        )
                        explanation = json.loads(cleaned)

                    except Exception:
                        explanation = {
                            "summary": explanation,
                            "strengths": [],
                            "weaknesses": []
                        }

            except Exception as e:
                explanation = {
                    "summary": "Failed to generate explanation",
                    "strengths": [],
                    "weaknesses": [str(e)]
                }

            final_results.append(
                {
                    "candidate_id": candidate["candidate_id"],
                    "candidate_name": candidate["candidate_name"],
                    "score": candidate["score"],
                    "score_breakdown": candidate["score_breakdown"],
                    "matched_skills": candidate["matched_skills"],
                    "missing_skills": candidate["missing_skills"],
                    "explanation": explanation,
                    "evidence": [
                        {
                            "section": match["section"],
                            "similarity": round(match["similarity"], 4),
                            "text": (
                                match["text"][:250] + "..."
                                if len(match["text"]) > 250
                                else match["text"]
                            )
                        }
                        for match in candidate["top_matches"]
                    ]
                }
            )

        save_results(job.id, final_results)

        return final_results

    finally:
        db.close()