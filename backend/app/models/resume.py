from app.extensions import db
from app.models.base import BaseModel


class Resume(BaseModel):

    __tablename__ = "resumes"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    file_name = db.Column(
        db.String(255),
        nullable=False
    )

    file_path = db.Column(
        db.String(500),
        nullable=False
    )

    file_size = db.Column(
        db.Integer,
        nullable=False
    )

    mime_type = db.Column(
        db.String(100),
        nullable=False
    )

    user = db.relationship(
        "User",
        backref=db.backref(
            "resumes",
            lazy=True
        )
    )