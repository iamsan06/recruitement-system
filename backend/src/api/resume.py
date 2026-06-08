from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException
)

from uuid import uuid4

from src.services.pdf_parser import extract_text

from src.services.llm_parser import (
    parse_candidate_with_llm
)

from src.services.storage import (
    save_candidate
)

from src.services.supabase_storage import (
    upload_pdf
)

from src.services.candidate_service import (
    get_all_candidates,
    get_candidate_by_id,
    delete_candidate
)

from src.services.chunking_service import (
    chunk_resume
)

from src.services.embedding_service import (
    generate_embedding
)

from src.services.chunk_storage import (
    save_chunks
)

router = APIRouter()


@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...)
):

    if not file.filename.lower().endswith(".pdf"):
        return {
            "success": False,
            "message": "Only PDF files allowed"
        }

    storage_filename = (
        f"{uuid4()}_{file.filename}"
    )

    pdf_bytes = await file.read()

    upload_pdf(
        pdf_bytes,
        storage_filename
    )

    resume_text = extract_text(
        pdf_bytes
    )

    candidate = parse_candidate_with_llm(
        resume_text
    )

    candidate["resume_text"] = resume_text
    candidate["filename"] = file.filename
    candidate["pdf_url"] = storage_filename

    saved_candidate = save_candidate(
        candidate
    )

    chunks = chunk_resume(
        resume_text
    )

    for chunk in chunks:

        chunk["embedding"] = (
            generate_embedding(
                chunk["text"]
            )
        )

    save_chunks(
        saved_candidate.id,
        chunks
    )

    return {
        "success": True,
        "candidate_id": saved_candidate.id,
        "chunks_created": len(chunks)
    }


@router.get("/")
def get_candidates():

    return get_all_candidates()


@router.get("/{candidate_id}")
def get_candidate(candidate_id: int):

    candidate = get_candidate_by_id(
        candidate_id
    )

    if not candidate:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found"
        )

    return candidate


@router.delete("/{candidate_id}")
def remove_candidate(candidate_id: int):

    deleted = delete_candidate(
        candidate_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found"
        )

    return {
        "message": "Candidate deleted successfully"
    }