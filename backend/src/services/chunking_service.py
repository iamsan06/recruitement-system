import re


SECTION_HEADERS = {
    "education": [
        "education",
        "academic background",
        "qualifications"
    ],

    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "employment history"
    ],

    "projects": [
        "projects",
        "personal projects",
        "academic projects"
    ],

    "skills": [
        "skills",
        "technical skills",
        "core skills",
        "competencies"
    ],

    "certifications": [
        "certifications",
        "licenses",
        "licenses & certifications"
    ]
}


def normalize_header(text: str):

    text = text.lower().strip()

    text = re.sub(r"[:\-|]+$", "", text)

    return re.sub(r"\s+", " ", text)


def detect_section(line: str):

    normalized = normalize_header(line)

    for section, aliases in SECTION_HEADERS.items():

        for alias in aliases:

            if (
                normalized == alias
                or normalized.startswith(alias)
            ):
                return section

    return None


def split_hierarchical(section, text):

    if section == "experience":

        blocks = re.split(
            r"\n(?=[A-Z][^\n]*(Engineer|Developer|Intern|Manager|Analyst|Consultant))",
            text
        )

        return [
            {
                "section": f"experience_{i+1}",
                "text": block.strip()
            }
            for i, block in enumerate(blocks)
            if block.strip()
        ]

    if section == "projects":

        blocks = re.split(
            r"\n(?=[A-Z][^\n]*(Project|System|Platform|Application|App|Tool))",
            text
        )

        return [
            {
                "section": f"project_{i+1}",
                "text": block.strip()
            }
            for i, block in enumerate(blocks)
            if block.strip()
        ]

    return [
        {
            "section": section,
            "text": text.strip()
        }
    ]


def chunk_resume(text: str):

    lines = text.splitlines()

    chunks = []

    current_section = "general"

    buffer = []

    for raw_line in lines:

        line = raw_line.strip()

        if not line:
            continue

        detected = detect_section(line)

        if detected:

            if buffer:

                section_text = "\n".join(buffer)

                chunks.extend(
                    split_hierarchical(
                        current_section,
                        section_text
                    )
                )

            current_section = detected

            buffer = []

        else:

            buffer.append(line)

    if buffer:

        section_text = "\n".join(buffer)

        chunks.extend(
            split_hierarchical(
                current_section,
                section_text
            )
        )

    return chunks