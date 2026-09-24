from app.extensions import db
from app.models.base import BaseModel


class Contract(BaseModel):
    __tablename__ = "contracts"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    job_id = db.Column(
        db.Integer,
        db.ForeignKey("jobs.id"),
        nullable=False
    )

    application_id = db.Column(
        db.Integer,
        db.ForeignKey("job_applications.id"),
        nullable=False,
        unique=True
    )

    client_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    freelancer_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    agreed_amount = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    start_date = db.Column(
        db.Date,
        nullable=True
    )

    end_date = db.Column(
        db.Date,
        nullable=True
    )

    status = db.Column(
        db.String(30),
        default="Active",
        nullable=False
    )

    job = db.relationship(
        "Job",
        backref=db.backref(
            "contracts",
            lazy=True
        )
    )

    application = db.relationship(
        "JobApplication",
        backref=db.backref(
            "contract",
            uselist=False
        )
    )

    client = db.relationship(
        "User",
        foreign_keys=[client_id],
        backref=db.backref(
            "client_contracts",
            lazy=True
        )
    )

    freelancer = db.relationship(
        "User",
        foreign_keys=[freelancer_id],
        backref=db.backref(
            "freelancer_contracts",
            lazy=True
        )
    )