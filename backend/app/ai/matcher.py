import re
from datetime import datetime

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


def calculate_resume_experience(resume_data):
    """
    Calculate total experience in years
    from internship durations.
    """

    total_months = 0

    internships = resume_data.get(
        "internships",
        []
    )

    if not internships:
        return 0

    for internship in internships:

        duration = internship.get(
            "duration",
            ""
        )

        if not duration:
            continue

        duration = duration.lower().strip()

        # Example:
        # sept-oct 25
        # sept-oct' 25

        match = re.search(
            r"(jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*"
            r"\s*[-–]\s*"
            r"(jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*"
            r"['’]?\s*(\d{2,4})",
            duration
        )

        if match:

            start_month = match.group(1)
            end_month = match.group(2)
            year = match.group(3)

            month_map = {
                "jan": 1,
                "feb": 2,
                "mar": 3,
                "apr": 4,
                "may": 5,
                "jun": 6,
                "jul": 7,
                "aug": 8,
                "sep": 9,
                "sept": 9,
                "oct": 10,
                "nov": 11,
                "dec": 12
            }

            start_month_num = month_map.get(
                start_month[:4]
            )

            end_month_num = month_map.get(
                end_month[:4]
            )

            if not start_month_num or not end_month_num:
                continue

            if len(year) == 2:
                year = 2000 + int(year)
            else:
                year = int(year)

            months = (
                end_month_num
                - start_month_num
                + 1
            )

            if months <= 0:
                months += 12

            total_months += months

    return round(
        total_months / 12,
        2
    )


def calculate_weighted_job_match(
    resume_data,
    required_skills,
    required_experience=0
):
    # Existing skill-based matching
    skill_result = calculate_job_match(
        resume_data,
        required_skills
    )

    skill_score = skill_result["match_score"]

    resume_experience = calculate_resume_experience(
        resume_data
    )

    # Experience score
    if required_experience <= 0:
        experience_score = 100
    elif resume_experience >= required_experience:
        experience_score = 100
    else:
        experience_score = round(
            (resume_experience / required_experience) * 100,
            2
        )

    # Weighted final score
    final_score = round(
        (skill_score * 0.8) +
        (experience_score * 0.2),
        2
    )

    return {
        "match_score": final_score,
        "skill_score": skill_score,
        "experience_score": experience_score,
        "matching_skills": skill_result[
            "matching_skills"
        ],
        "missing_skills": skill_result[
            "missing_skills"
        ]
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