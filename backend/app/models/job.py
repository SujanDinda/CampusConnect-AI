from app.extensions import db
from app.models.base import BaseModel
from app.models.job_skill import job_skills


class Job(BaseModel):

    __tablename__ = "jobs"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    company_id = db.Column(
        db.Integer,
        db.ForeignKey("companies.id"),
        nullable=False
    )

    category_id = db.Column(
        db.Integer,
        db.ForeignKey("job_categories.id"),
        nullable=False
    )

    title = db.Column(
        db.String(255),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    location = db.Column(
        db.String(255),
        nullable=True
    )

    job_type = db.Column(
        db.String(50),
        nullable=False
    )

    work_mode = db.Column(
        db.String(50),
        nullable=False
    )

    salary_min = db.Column(
        db.Integer,
        nullable=True
    )

    salary_max = db.Column(
        db.Integer,
        nullable=True
    )

    experience_required = db.Column(
        db.Float,
        default=0
    )

    vacancies = db.Column(
        db.Integer,
        default=1
    )

    application_deadline = db.Column(
        db.Date,
        nullable=True
    )

    is_active = db.Column(
        db.Boolean,
        default=True
    )

    company = db.relationship(
        "Company",
        backref=db.backref(
            "jobs",
            lazy=True
        )
    )

    required_skills = db.relationship(
        "Skill",
        secondary=job_skills,
        backref="jobs"
    )

    category = db.relationship(
        "JobCategory",
        backref=db.backref(
            "jobs",
            lazy=True
        )
    )