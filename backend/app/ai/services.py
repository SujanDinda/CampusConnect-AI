from app.models.resume import Resume

from app.ai.parser import extract_resume_text
from app.ai.extractor import extract_resume_data


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