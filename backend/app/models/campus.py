from app.extensions import db

# Campus - User Many-to-Many Association Table
campus_members = db.Table(
    "campus_members",
    db.Column(
        "user_id",
        db.Integer,
        db.ForeignKey("users.id"),
        primary_key=True
    ),
    db.Column(
        "campus_id",
        db.Integer,
        db.ForeignKey("campuses.id"),
        primary_key=True
    )
)


class Campus(db.Model):
    __tablename__ = "campuses"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(255),
        nullable=False
    )

    email_domain = db.Column(
        db.String(255),
        unique=True,
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

    is_verified = db.Column(
        db.Boolean,
        default=False
    )