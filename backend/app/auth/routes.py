from flask import request, jsonify

from app.auth import auth_bp

from app.auth.schemas import (
    validate_registration_data
)

from app.auth.services import (
    register_user,
    login_user
)


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