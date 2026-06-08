def skill_match_score(
    candidate_skills,
    required_skills
):

    if not required_skills:
        return 100

    candidate = {
        s.lower()
        for s in candidate_skills
    }

    required = {
        s.lower()
        for s in required_skills
    }

    matched = (
        candidate & required
    )

    return (
        len(matched)
        / len(required)
    ) * 100


def experience_score(
    candidate_years,
    required_years
):

    if required_years == 0:
        return 100

    return min(
        candidate_years /
        required_years,
        1
    ) * 100


def certification_score(
    candidate_certs,
    required_certs
):

    if not required_certs:
        return 100

    candidate = {
        str(c).lower()
        for c in candidate_certs
    }

    required = {
        str(c).lower()
        for c in required_certs
    }

    matched = (
        candidate & required
    )

    return (
        len(matched)
        / len(required)
    ) * 100