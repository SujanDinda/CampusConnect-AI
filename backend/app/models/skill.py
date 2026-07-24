from app.extensions import db

# User - Skill Many-to-Many Association Table
user_skills = db.Table(
    "user_skills",
    db.Column(
        "user_id",
        db.Integer,
        db.ForeignKey("users.id"),
        primary_key=True
    ),
    db.Column(
        "skill_id",
        db.Integer,
        db.ForeignKey("skills.id"),
        primary_key=True
    )
)


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