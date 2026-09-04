from app import create_app
from app.models.job import Job

from app.ai.matcher import match_resume_with_job


app = create_app()


resume_path = (
    "uploads/resumes/"
    "1_a967eca41ee94f8cacf9b7f3fc945684.pdf"
)


with app.app_context():

    job = Job.query.filter_by(
        id=1
    ).first()

    if not job:

        print("Job not found")

    else:

        result = match_resume_with_job(
            resume_path,
            job
        )

        print("\nJOB:")
        print(
            result["job_title"]
        )

        print(
            "\nMATCH SCORE:",
            result["match_score"],
            "%"
        )

        print(
            "\nMATCHING SKILLS:"
        )

        for skill in result[
            "matching_skills"
        ]:
            print(
                "-",
                skill
            )

        print(
            "\nMISSING SKILLS:"
        )

        for skill in result[
            "missing_skills"
        ]:
            print(
                "-",
                skill
            )