from fastapi import FastAPI

from src.api.resume import router as resume_router
from src.api.job import router as job_router

app = FastAPI()


app.include_router(
    resume_router,
    prefix="/resume",
    tags=["Resume"]
)

app.include_router(
    job_router,
    prefix="/jobs",
    tags=["Jobs"]
)