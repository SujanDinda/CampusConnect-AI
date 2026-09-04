def calculate_job_match(resume_data, required_skills):

    # Resume unified skills
    resume_skills = {
        skill["name"].lower()
        for skill in resume_data.get(
            "unified_skills",
            []
        )
    }

    # Normalize job skills
    job_skills = {
        skill.strip().lower()
        for skill in required_skills
    }

    matching_skills = sorted(
        resume_skills.intersection(job_skills)
    )

    missing_skills = sorted(
        job_skills.difference(resume_skills)
    )

    total_required = len(job_skills)

    if total_required == 0:
        match_score = 0
    else:
        match_score = round(
            (len(matching_skills) / total_required) * 100,
            2
        )

    return {
        "match_score": match_score,
        "matching_skills": matching_skills,
        "missing_skills": missing_skills
    }


def get_job_required_skills(job):

    return [
        skill.name
        for skill in job.required_skills
        if skill.is_active
    ]


from app.ai.parser import extract_resume_text
from app.ai.extractor import extract_resume_data


def match_resume_with_job(
    resume_file_path,
    job
):
    # -------------------------
    # Extract resume text
    # -------------------------

    text = extract_resume_text(
        resume_file_path
    )

    # -------------------------
    # Extract resume data
    # -------------------------

    resume_data = extract_resume_data(
        text
    )

    # -------------------------
    # Get Job Skills
    # -------------------------

    required_skills = get_job_required_skills(
        job
    )

    # -------------------------
    # Calculate Match
    # -------------------------

    match_result = calculate_job_match(
        resume_data,
        required_skills
    )

    # -------------------------
    # Return Result
    # -------------------------

    return {
        "job_id": job.id,
        "job_title": job.title,
        "match_score": match_result["match_score"],
        "matching_skills": match_result["matching_skills"],
        "missing_skills": match_result["missing_skills"]
    }