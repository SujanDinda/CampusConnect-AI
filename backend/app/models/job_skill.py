from app.extensions import db


job_skills = db.Table(

    "job_skills",

    db.Column(
        "job_id",
        db.Integer,
        db.ForeignKey("jobs.id"),
        primary_key=True
    ),

    db.Column(
        "skill_id",
        db.Integer,
        db.ForeignKey("skills.id"),
        primary_key=True
    )

)