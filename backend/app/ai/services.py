from app.models.resume import Resume

from app.ai.parser import extract_resume_text
from app.ai.extractor import extract_resume_data

from app.models.job import Job
from app.ai.matcher import match_resume_with_job


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