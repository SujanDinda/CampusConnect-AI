from app.extensions import db
from app.models.base import BaseModel


class Milestone(BaseModel):
    __tablename__ = "milestones"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    contract_id = db.Column(
        db.Integer,
        db.ForeignKey("contracts.id"),
        nullable=False
    )

    title = db.Column(
        db.String(255),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    amount = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    due_date = db.Column(
        db.Date,
        nullable=True
    )

    status = db.Column(
        db.String(30),
        default="Pending",
        nullable=False
    )

    contract = db.relationship(
        "Contract",
        backref=db.backref(
            "milestones",
            lazy=True
        )
    )