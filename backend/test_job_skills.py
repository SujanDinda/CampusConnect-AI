from app import create_app
from app.extensions import db
from app.models.job import Job
from sqlalchemy import text

from app.ai.matcher import get_job_required_skills


app = create_app()

with app.app_context():

    db.engine.echo = True

    print("DATABASE:")
    print(db.engine.url)

    print("\nJOB SKILLS FROM DATABASE:")

    result = db.session.execute(
        text("""
            SELECT
                js.job_id,
                s.id,
                s.name
            FROM job_skills js
            JOIN skills s
                ON js.skill_id = s.id
            WHERE js.job_id = 1
        """)
    )

    for row in result:
        print(row)

    print("\nRELATIONSHIP SQL:")

    print(
        Job.required_skills.property.primaryjoin
    )

    print(
        Job.required_skills.property.secondaryjoin
    )

    print("\nSQLALCHEMY RELATIONSHIP:")

    job = Job.query.filter_by(id=1).first()

    if job:

        print("Job:")
        print(job.title)

        print("\nRequired Skills:")

        for skill in job.required_skills:
            print("-", skill.name)