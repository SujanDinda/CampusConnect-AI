from flask import request, jsonify

from app.auth import auth_bp

from app.auth.schemas import (
    validate_registration_data
)

from app.auth.services import (
    register_user,
    login_user
)

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    create_access_token,
    get_jwt
)

from app.models.user import User

from app.models.token_blocklist import TokenBlocklist
from app.extensions import db


@auth_bp.route(
    "/register",
    methods=["POST"]
)
def register():

    data = request.get_json()

    if not data:

        return jsonify({
            "status": "error",
            "message": "Request body is required"
        }), 400

    errors = validate_registration_data(
        data
    )

    if errors:

        return jsonify({
            "status": "error",
            "errors": errors
        }), 400

    email = data.get("email")

    password = data.get("password")

    role = data.get(
        "role",
        "STUDENT"
    )

    user, error = register_user(
        email=email,
        password=password,
        role_name=role
    )

    if error:

        return jsonify({
            "status": "error",
            "message": error
        }), 400

    return jsonify({

        "status": "success",

        "message": "User registered successfully",

        "data": {

            "user_id": user.id,

            "email": user.email,

            "role": role

        }

    }), 201


@auth_bp.route(
    "/login",
    methods=["POST"]
)
def login():

    data = request.get_json()

    if not data:

        return jsonify({
            "status": "error",
            "message": "Request body is required"
        }), 400

    email = data.get("email")

    password = data.get("password")

    if not email or not password:

        return jsonify({
            "status": "error",
            "message": "Email and password are required"
        }), 400

    result, error = login_user(
        email=email,
        password=password
    )

    if error:

        return jsonify({
            "status": "error",
            "message": error
        }), 401

    user = result["user"]

    return jsonify({

        "status": "success",

        "message": "Login successful",

        "data": {

            "user": {
                "id": user.id,
                "email": user.email
            },

            "access_token": result[
                "access_token"
            ],

            "refresh_token": result[
                "refresh_token"
            ]

        }

    }), 200


@auth_bp.route(
    "/me",
    methods=["GET"]
)
@jwt_required()
def me():

    current_user_id = get_jwt_identity()

    user = User.query.get(current_user_id)

    if not user:

        return jsonify({
            "status": "error",
            "message": "User not found"
        }), 404

    roles = [
        role.name
        for role in user.roles
    ]

    return jsonify({

        "status": "success",

        "data": {

            "id": user.id,

            "email": user.email,

            "is_active": user.is_active,

            "is_verified": user.is_verified,

            "roles": roles

        }

    }), 200


@auth_bp.route(
    "/refresh",
    methods=["POST"]
)
@jwt_required(refresh=True)
def refresh():

    current_user = get_jwt_identity()

    access_token = create_access_token(
        identity=current_user
    )

    return jsonify({
        "status": "success",
        "access_token": access_token
    }), 200


@auth_bp.route(
    "/logout",
    methods=["POST"]
)
@jwt_required()
def logout():

    token = get_jwt()

    jti = token["jti"]

    blocked_token = TokenBlocklist(
        jti=jti
    )

    db.session.add(blocked_token)
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "Logout successful"
    }), 200