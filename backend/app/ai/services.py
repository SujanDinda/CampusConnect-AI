from app.models.resume import Resume

from app.ai.parser import extract_resume_text
from app.ai.extractor import extract_resume_data

from app.models.job import Job
from app.ai.matcher import (
    match_resume_with_job,
    calculate_job_match
)


def parse_latest_resume(user_id):

    resume = (
        Resume.query
        .filter_by(user_id=user_id)
        .order_by(Resume.id.desc())
        .first()
    )

    if not resume:
        return None, "Resume not found"

    text = extract_resume_text(
        resume.file_path
    )

    data = extract_resume_data(text)

    return data, None


def match_latest_resume_with_job(user_id, job_id):

    # Get active job
    job = (
        Job.query
        .filter_by(
            id=job_id,
            is_active=True
        )
        .first()
    )

    if not job:
        return None, "Job not found"

    # Get latest resume
    resume = (
        Resume.query
        .filter_by(user_id=user_id)
        .order_by(Resume.id.desc())
        .first()
    )

    if not resume:
        return None, "Resume not found"

    # Match resume with job
    result = match_resume_with_job(
        resume.file_path,
        job
    )

    return result, None


def recommend_jobs_for_resume(user_id):

    # -------------------------
    # Get latest resume
    # -------------------------

    resume = (
        Resume.query
        .filter_by(user_id=user_id)
        .order_by(Resume.id.desc())
        .first()
    )

    if not resume:
        return None, "Resume not found"

    # -------------------------
    # Extract resume data ONCE
    # -------------------------

    text = extract_resume_text(
        resume.file_path
    )

    resume_data = extract_resume_data(
        text
    )

    # -------------------------
    # Get all active jobs
    # -------------------------

    jobs = (
        Job.query
        .filter_by(
            is_active=True
        )
        .all()
    )

    if not jobs:
        return [], None

    recommendations = []

    # -------------------------
    # Match resume with jobs
    # -------------------------

    for job in jobs:

        required_skills = [
            skill.name
            for skill in job.required_skills
            if skill.is_active
        ]

        match_result = calculate_job_match(
            resume_data,
            required_skills
        )

        recommendations.append({
            "job_id": job.id,
            "job_title": job.title,
            "match_score": match_result["match_score"],
            "matching_skills": match_result["matching_skills"],
            "missing_skills": match_result["missing_skills"]
        })

    # -------------------------
    # Sort by match score
    # -------------------------

    recommendations.sort(
        key=lambda job: job["match_score"],
        reverse=True
    )

    return recommendations, None