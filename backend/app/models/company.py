from app.extensions import db
from app.models.base import BaseModel


class Company(BaseModel):

    __tablename__ = "companies"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    owner_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    name = db.Column(
        db.String(255),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    website = db.Column(
        db.String(255),
        nullable=True
    )

    logo = db.Column(
        db.String(500),
        nullable=True
    )

    industry = db.Column(
        db.String(100),
        nullable=True
    )

    is_verified = db.Column(
        db.Boolean,
        default=False
    )

    owner = db.relationship(
        "User",
        backref="companies"
    )