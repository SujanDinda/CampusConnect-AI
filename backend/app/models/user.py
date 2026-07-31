from datetime import datetime
from app.extensions import db
from app.models.role import user_roles
from app.models.campus import campus_members
from app.models.skill import UserSkill


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    email = db.Column(
        db.String(255),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    is_active = db.Column(
        db.Boolean,
        default=True
    )

    is_verified = db.Column(
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

    # Many-to-Many relationship with Role model
    roles = db.relationship(
        "Role",
        secondary=user_roles,
        backref="users"
    )

    campuses = db.relationship(
        "Campus",
        secondary=campus_members,
        backref="members"
    )

    user_skills = db.relationship(
        "UserSkill",
        back_populates="user",
        cascade="all, delete-orphan"
    )