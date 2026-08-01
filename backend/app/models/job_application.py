from app.extensions import db
from app.models.base import BaseModel


class JobApplication(BaseModel):

    __tablename__ = "job_applications"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    job_id = db.Column(
        db.Integer,
        db.ForeignKey("jobs.id"),
        nullable=False
    )

    applicant_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    cover_letter = db.Column(
        db.Text,
        nullable=True
    )

    resume_url = db.Column(
        db.String(500),
        nullable=True
    )

    status = db.Column(
        db.String(30),
        default="Pending"
    )

    job = db.relationship(
        "Job",
        backref=db.backref(
            "applications",
            lazy=True
        )
    )

    applicant = db.relationship(
        "User",
        backref=db.backref(
            "applications",
            lazy=True
        )
    )