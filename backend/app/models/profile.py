from app.extensions import db


class Profile(db.Model):

    __tablename__ = "profiles"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        unique=True,
        nullable=False
    )

    full_name = db.Column(
        db.String(150),
        nullable=False
    )

    bio = db.Column(
        db.Text,
        nullable=True
    )

    profile_image = db.Column(
        db.String(500),
        nullable=True
    )

    location = db.Column(
        db.String(255),
        nullable=True
    )

    hourly_rate = db.Column(
        db.Numeric(10, 2),
        nullable=True
    )

    availability_status = db.Column(
        db.String(50),
        default="available"
    )

    user = db.relationship(
        "User",
        backref=db.backref(
            "profile",
            uselist=False
        )
    )