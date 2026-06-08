import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)


def upload_pdf(
    pdf_bytes: bytes,
    storage_name: str
):

    supabase.storage.from_("resume").upload(
        path=storage_name,
        file=pdf_bytes,
        file_options={
            "content-type": "application/pdf"
        }
    )

    return storage_name