import bcrypt
from app.extensions import db
from app.models.role import Role
from app.models.user import User

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token
)


def hash_password(password):

    password_bytes = password.encode("utf-8")

    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(
        password_bytes,
        salt
    )

    return hashed_password.decode("utf-8")


def verify_password(password, hashed_password):

    password_bytes = password.encode("utf-8")

    hashed_password_bytes = hashed_password.encode("utf-8")

    return bcrypt.checkpw(
        password_bytes,
        hashed_password_bytes
    )


def register_user(email, password, role_name="STUDENT"):

    existing_user = User.query.filter_by(
        email=email
    ).first()

    if existing_user:

        return None, "User with this email already exists"

    hashed_password = hash_password(password)

    user = User(
        email=email,
        password_hash=hashed_password
    )

    role = Role.query.filter_by(
        name=role_name
    ).first()

    if not role:

        return None, "Invalid role"

    user.roles.append(role)

    db.session.add(user)

    db.session.commit()

    return user, None

def login_user(email, password):

    user = User.query.filter_by(
        email=email
    ).first()

    if not user:
        return None, "Invalid email or password"

    if not user.is_active:
        return None, "User account is inactive"

    password_valid = verify_password(
        password,
        user.password_hash
    )

    if not password_valid:
        return None, "Invalid email or password"

    access_token = create_access_token(
        identity=str(user.id)
    )

    refresh_token = create_refresh_token(
        identity=str(user.id)
    )

    return {
        "user": user,
        "access_token": access_token,
        "refresh_token": refresh_token
    }, None