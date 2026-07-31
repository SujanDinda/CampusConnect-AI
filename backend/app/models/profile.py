from datetime import datetime

from app.extensions import db


class Profile(db.Model):

    __tablename__ = "profiles"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # ==========================
    # User Relationship
    # ==========================

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        unique=True,
        nullable=False
    )

    # ==========================
    # Basic Information
    # ==========================

    full_name = db.Column(
        db.String(150),
        nullable=False
    )

    headline = db.Column(
        db.String(255),
        nullable=True
    )

    bio = db.Column(
        db.Text,
        nullable=True
    )

    phone = db.Column(
        db.String(20),
        nullable=True
    )

    profile_image = db.Column(
        db.String(500),
        nullable=True
    )

    # ==========================
    # Location
    # ==========================

    location = db.Column(
        db.String(255),
        nullable=True
    )

    city = db.Column(
        db.String(100),
        nullable=True
    )

    state = db.Column(
        db.String(100),
        nullable=True
    )

    country = db.Column(
        db.String(100),
        nullable=True
    )

    # ==========================
    # Education
    # ==========================

    department = db.Column(
        db.String(150),
        nullable=True
    )

    graduation_year = db.Column(
        db.Integer,
        nullable=True
    )

    # ==========================
    # Freelancer Information
    # ==========================

    hourly_rate = db.Column(
        db.Numeric(10, 2),
        nullable=True
    )

    availability_status = db.Column(
        db.String(50),
        default="available",
        nullable=False
    )

    # ==========================
    # Professional Links
    # ==========================

    resume_url = db.Column(
        db.String(500),
        nullable=True
    )

    portfolio_url = db.Column(
        db.String(500),
        nullable=True
    )

    github_url = db.Column(
        db.String(500),
        nullable=True
    )

    linkedin_url = db.Column(
        db.String(500),
        nullable=True
    )

    website_url = db.Column(
        db.String(500),
        nullable=True
    )

    # ==========================
    # Timestamps
    # ==========================

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # ==========================
    # Relationship
    # ==========================

    user = db.relationship(
        "User",
        backref=db.backref(
            "profile",
            uselist=False
        )
    )