from flask import request, jsonify

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from app.profile import profile_bp

from app.profile.schemas import (
    validate_profile_data
)

from app.profile.services import (
    create_profile,
    get_profile_by_user_id,
    update_profile
)


# ==========================
# Create Profile
# ==========================

@profile_bp.route(
    "",
    methods=["POST"]
)
@jwt_required()
def create_user_profile():

    current_user_id = get_jwt_identity()

    data = request.get_json()

    if not data:

        return jsonify({
            "status": "error",
            "message": "Request body is required"
        }), 400

    errors = validate_profile_data(
        data
    )

    if errors:

        return jsonify({
            "status": "error",
            "errors": errors
        }), 400

    profile, error = create_profile(
        user_id=current_user_id,
        data=data
    )

    if error:

        return jsonify({
            "status": "error",
            "message": error
        }), 409

    return jsonify({

        "status": "success",

        "message": "Profile created successfully",

        "data": {

            "id": profile.id,

            "user_id": profile.user_id,

            "full_name": profile.full_name,

            "headline": profile.headline,

            "bio": profile.bio,

            "location": profile.location,

            "availability_status":
                profile.availability_status

        }

    }), 201


# ==========================
# Get My Profile
# ==========================

@profile_bp.route(
    "/me",
    methods=["GET"]
)
@jwt_required()
def get_my_profile():

    current_user_id = get_jwt_identity()

    profile = get_profile_by_user_id(
        current_user_id
    )

    if not profile:

        return jsonify({
            "status": "error",
            "message": "Profile not found"
        }), 404

    return jsonify({

        "status": "success",

        "data": {

            "id": profile.id,

            "user_id": profile.user_id,

            "full_name": profile.full_name,

            "headline": profile.headline,

            "bio": profile.bio,

            "phone": profile.phone,

            "profile_image":
                profile.profile_image,

            "location": profile.location,

            "city": profile.city,

            "state": profile.state,

            "country": profile.country,

            "department":
                profile.department,

            "graduation_year":
                profile.graduation_year,

            "hourly_rate":
                str(profile.hourly_rate)
                if profile.hourly_rate
                else None,

            "availability_status":
                profile.availability_status,

            "resume_url":
                profile.resume_url,

            "portfolio_url":
                profile.portfolio_url,

            "github_url":
                profile.github_url,

            "linkedin_url":
                profile.linkedin_url,

            "website_url":
                profile.website_url

        }

    }), 200


@profile_bp.route(
    "/me",
    methods=["PUT"]
)
@jwt_required()
def update_my_profile():

    current_user_id = get_jwt_identity()

    data = request.get_json()

    if not data:

        return jsonify({
            "status": "error",
            "message": "Request body is required"
        }), 400

    errors = validate_profile_data(
        data
    )

    if errors:

        return jsonify({
            "status": "error",
            "errors": errors
        }), 400

    profile, error = update_profile(
        user_id=current_user_id,
        data=data
    )

    if error:

        return jsonify({
            "status": "error",
            "message": error
        }), 404

    return jsonify({

        "status": "success",

        "message": "Profile updated successfully",

        "data": {

            "id": profile.id,

            "user_id": profile.user_id,

            "full_name": profile.full_name,

            "headline": profile.headline,

            "bio": profile.bio,

            "location": profile.location,

            "availability_status":
                profile.availability_status

        }

    }), 200