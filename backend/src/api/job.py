from fastapi import (
    APIRouter,
    HTTPException
)

from backend.src.schemas.job_schema import (
    JobCreate,
    JobResponse
)

from backend.src.services.job_service import (
    create_job,
    get_all_jobs,
    get_job_by_id,
    delete_job
)

from backend.src.services.matching_service import (
    match_job
)

from backend.src.services.result_service import (
    get_results
)

router = APIRouter()


@router.post(
    "/",
    response_model=JobResponse
)
def create_new_job(
    job: JobCreate
):

    return create_job(job)


@router.get(
    "/",
    response_model=list[JobResponse]
)
def get_jobs():

    return get_all_jobs()


@router.get(
    "/{job_id}",
    response_model=JobResponse
)
def get_job(
    job_id: int
):

    job = get_job_by_id(
        job_id
    )

    if not job:

        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    return job


@router.delete(
    "/{job_id}"
)
def remove_job(
    job_id: int
):

    deleted = delete_job(
        job_id
    )

    if not deleted:

        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    return {
        "message":
        "Job deleted successfully"
    }


@router.post(
    "/{job_id}/match"
)
def match_candidates(
    job_id: int
):

    job = get_job_by_id(
        job_id
    )

    if not job:

        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    matches = match_job(
        job
    )

    return {
        "job_id": job.id,
        "job_title": job.title,
        "matches": matches
    }
@router.get(
    "/{job_id}/results"
)
def job_results(
    job_id: int
):

    return get_results(
        job_id
    )