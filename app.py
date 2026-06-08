import json
import requests
import pandas as pd
import gradio as gr

import os
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

def upload_resume(pdf):

    if pdf is None:
        return "Please select a PDF file."

    with open(pdf, "rb") as f:

        response = requests.post(
            f"{BACKEND_URL}/resume/upload",
            files={
                "file": (
                    pdf.split("/")[-1],
                    f,
                    "application/pdf"
                )
            }
        )

    data = response.json()
    lines = []
    for key, value in data.items():
        lines.append(f"{key.replace('_', ' ').title()}: {value}")
    return "\n".join(lines)


def load_candidates():

    response = requests.get(
        f"{BACKEND_URL}/resume"
    )

    data = response.json()

    if not data:
        return pd.DataFrame()

    return pd.DataFrame(data)


def get_candidate(candidate_id):

    response = requests.get(
        f"{BACKEND_URL}/resume/{int(candidate_id)}"
    )

    data = response.json()
    lines = []
    for key, value in data.items():
        label = key.replace('_', ' ').title()
        if isinstance(value, list):
            value = ", ".join(str(v) for v in value)
        lines.append(f"{label}: {value}")
    return "\n".join(lines)


# -------------------------
# Job Functions
# -------------------------

def create_job(title, description):

    payload = {
        "title": title,
        "description": description
    }

    response = requests.post(
        f"{BACKEND_URL}/jobs",
        json=payload
    )

    data = response.json()
    lines = []
    for key, value in data.items():
        lines.append(f"{key.replace('_', ' ').title()}: {value}")
    return "\n".join(lines)


def load_jobs():

    response = requests.get(
        f"{BACKEND_URL}/jobs"
    )

    data = response.json()

    if not data:
        return pd.DataFrame()

    return pd.DataFrame(data)


def get_job(job_id):

    response = requests.get(
        f"{BACKEND_URL}/jobs/{int(job_id)}"
    )

    data = response.json()
    lines = []
    for key, value in data.items():
        label = key.replace('_', ' ').title()
        if isinstance(value, list):
            value = ", ".join(str(v) for v in value)
        lines.append(f"{label}: {value}")
    return "\n".join(lines)


# -------------------------
# Matching
# -------------------------

def format_match_results(data):
    """Convert match result data to readable plain text."""
    if isinstance(data, list):
        lines = []
        for i, item in enumerate(data, 1):
            lines.append(f"--- Match #{i} ---")
            for key, value in item.items():
                label = key.replace('_', ' ').title()
                if isinstance(value, list):
                    value = ", ".join(str(v) for v in value)
                lines.append(f"  {label}: {value}")
        return "\n".join(lines) if lines else "No matches found."
    elif isinstance(data, dict):
        lines = []
        for key, value in data.items():
            label = key.replace('_', ' ').title()
            if isinstance(value, list):
                if value and isinstance(value[0], dict):
                    lines.append(f"{label}:")
                    for i, item in enumerate(value, 1):
                        lines.append(f"  --- Match #{i} ---")
                        for k, v in item.items():
                            lines.append(f"    {k.replace('_', ' ').title()}: {v}")
                else:
                    value = ", ".join(str(v) for v in value)
                    lines.append(f"{label}: {value}")
            else:
                lines.append(f"{label}: {value}")
        return "\n".join(lines)
    return str(data)


def match_job(job_id):

    response = requests.post(
        f"{BACKEND_URL}/jobs/{int(job_id)}/match"
    )

    return format_match_results(response.json())


def get_results(job_id):

    response = requests.get(
        f"{BACKEND_URL}/jobs/{int(job_id)}/results"
    )

    return format_match_results(response.json())


# -------------------------
# Theme
# -------------------------

css = """
html {
    overflow-y: scroll !important;
}

body {
    overflow-x: hidden !important;
    min-width: 0 !important;
}

.gradio-container {
    max-width: 1250px !important;
    margin: auto !important;
    width: 100% !important;
    box-sizing: border-box !important;
}

.block {
    border-radius: 14px !important;
}

footer {
    display:none !important;
}

h1 {
    font-weight:600;
}

.section-card {
    padding:20px;
    border:1px solid #e5e5e5;
    border-radius:14px;
}

input[type=number] {
    -moz-appearance: textfield !important;
}
input[type=number]::-webkit-outer-spin-button,
input[type=number]::-webkit-inner-spin-button {
    -webkit-appearance: none !important;
    margin: 0 !important;
}

.tabitem {
    min-height: 600px !important;
}

* {
    transition: none !important;
    animation: none !important;
}
"""

theme = gr.themes.Soft(
    radius_size="lg"
)


# -------------------------
# UI
# -------------------------

with gr.Blocks(
    theme=theme,
    css=css,
    title="Resume Analysing Platform"
) as demo:

    gr.Markdown(
        """
        # Resume Analysing Platform

        RAG Intelligence • GROQ LLM • BAAI/bge-small-en-v1.5
        """
    )

    with gr.Tabs():

        # --------------------------------
        # Resume Management
        # --------------------------------

        with gr.Tab("Candidates"):

            with gr.Row():

                with gr.Column(scale=1):

                    pdf_file = gr.File(
                        label="Upload Resume",
                        file_types=[".pdf"]
                    )

                    upload_btn = gr.Button(
                        "Upload",
                        variant="primary"
                    )

                    upload_result = gr.Textbox(
                        label="Response",
                        lines=6,
                        interactive=False
                    )

                with gr.Column(scale=2):

                    candidate_table = gr.Dataframe(
                        label="Candidates",
                        interactive=False
                    )

                    refresh_candidates = gr.Button(
                        "Refresh"
                    )

            gr.Markdown("---")

            with gr.Row():

                candidate_id = gr.Textbox(
                    label="Candidate ID",
                    placeholder="Enter candidate ID",
                    scale=1
                )

                get_candidate_btn = gr.Button(
                    "Load Candidate",
                    scale=0
                )

            candidate_json = gr.Textbox(
                label="Candidate Details",
                lines=10,
                interactive=False
            )

            upload_btn.click(
                upload_resume,
                pdf_file,
                upload_result
            )

            refresh_candidates.click(
                load_candidates,
                outputs=candidate_table
            )

            get_candidate_btn.click(
                get_candidate,
                candidate_id,
                candidate_json
            )

        # --------------------------------
        # Job Management
        # --------------------------------

        with gr.Tab("Jobs"):

            with gr.Row():

                with gr.Column(scale=1):

                    job_title = gr.Textbox(
                        label="Job Title"
                    )

                    job_desc = gr.Textbox(
                        label="Job Description",
                        lines=10
                    )

                    create_job_btn = gr.Button(
                        "Create Job",
                        variant="primary"
                    )

                    create_job_result = gr.Textbox(
                        label="Response",
                        lines=6,
                        interactive=False
                    )

                with gr.Column(scale=2):

                    jobs_table = gr.Dataframe(
                        label="Jobs",
                        interactive=False
                    )

                    refresh_jobs = gr.Button(
                        "Refresh Jobs"
                    )

            gr.Markdown("---")

            with gr.Row():

                job_id_view = gr.Textbox(
                    label="Job ID",
                    placeholder="Enter job ID"
                )

                load_job_btn = gr.Button(
                    "Load Job"
                )

            job_json = gr.Textbox(
                label="Job Details",
                lines=10,
                interactive=False
            )

            create_job_btn.click(
                create_job,
                [job_title, job_desc],
                create_job_result
            )

            refresh_jobs.click(
                load_jobs,
                outputs=jobs_table
            )

            load_job_btn.click(
                get_job,
                job_id_view,
                job_json
            )

        # --------------------------------
        # Matching
        # --------------------------------

        with gr.Tab("Matching"):

            with gr.Row():

                with gr.Column(scale=1):

                    match_job_id = gr.Textbox(
                        label="Job ID",
                        placeholder="Enter job ID"
                    )

                    match_btn = gr.Button(
                        "Run Matching",
                        variant="primary"
                    )

                with gr.Column(scale=2):

                    match_output = gr.Textbox(
                        label="Match Results",
                        lines=15,
                        interactive=False
                    )

            gr.Markdown("---")

            with gr.Row():

                result_job_id = gr.Textbox(
                    label="Job ID",
                    placeholder="Enter job ID"
                )

                results_btn = gr.Button(
                    "Load Stored Results"
                )

            stored_results = gr.Textbox(
                label="Stored Results",
                lines=15,
                interactive=False
            )

            match_btn.click(
                match_job,
                match_job_id,
                match_output
            )

            results_btn.click(
                get_results,
                result_job_id,
                stored_results
            )

demo.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", 7860))
)