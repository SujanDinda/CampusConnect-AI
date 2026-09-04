from datetime import datetime

from app.extensions import db


class Skill(db.Model):

    __tablename__ = "skills"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    category = db.Column(
        db.String(100),
        nullable=True
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    icon = db.Column(
        db.String(255),
        nullable=True
    )

    is_active = db.Column(
        db.Boolean,
        default=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    user_skills = db.relationship(
        "UserSkill",
        back_populates="skill",
        cascade="all, delete-orphan"
    )

    jobs = db.relationship(
        "Job",
        secondary="job_skills",
        back_populates="required_skills"
    )


class UserSkill(db.Model):

    __tablename__ = "user_skills"

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        primary_key=True
    )

    skill_id = db.Column(
        db.Integer,
        db.ForeignKey("skills.id"),
        primary_key=True
    )

    proficiency_level = db.Column(
        db.String(30),
        default="Beginner"
    )

    years_of_experience = db.Column(
        db.Float,
        default=0
    )

    is_primary = db.Column(
        db.Boolean,
        default=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    user = db.relationship(
        "User",
        back_populates="user_skills"
    )

    skill = db.relationship(
        "Skill",
        back_populates="user_skills"
    )