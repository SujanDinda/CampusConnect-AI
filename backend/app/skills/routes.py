from flask import request, jsonify

from app.skills import skills_bp

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from app.skills.schemas import (
    validate_skill_data,
    validate_user_skill_data
)

from app.skills.services import (
    create_skill,
    get_all_skills,
    add_skill_to_user,
    get_user_skills,
    remove_user_skill
)


# ==========================
# Create Skill
# ==========================

@skills_bp.route(
    "",
    methods=["POST"]
)
def create_new_skill():

    data = request.get_json()

    if not data:

        return jsonify({
            "status": "error",
            "message": "Request body is required"
        }), 400

    errors = validate_skill_data(data)

    if errors:

        return jsonify({
            "status": "error",
            "errors": errors
        }), 400

    skill, error = create_skill(data)

    if error:

        return jsonify({
            "status": "error",
            "message": error
        }), 409

    return jsonify({

        "status": "success",

        "message": "Skill created successfully",

        "data": {

            "id": skill.id,

            "name": skill.name,

            "category": skill.category

        }

    }), 201


# ==========================
# Get All Skills
# ==========================

@skills_bp.route(
    "",
    methods=["GET"]
)
def list_skills():

    skills = get_all_skills()

    return jsonify({

        "status": "success",

        "count": len(skills),

        "data": [

            {

                "id": skill.id,

                "name": skill.name,

                "category": skill.category

            }

            for skill in skills

        ]

    }), 200


# ==========================
# Add Skill to Current User
# ==========================

@skills_bp.route(
    "/me",
    methods=["POST"]
)
@jwt_required()
def add_my_skill():

    current_user_id = get_jwt_identity()

    data = request.get_json()

    if not data:

        return jsonify({
            "status": "error",
            "message": "Request body is required"
        }), 400

    errors = validate_user_skill_data(data)

    if errors:

        return jsonify({
            "status": "error",
            "errors": errors
        }), 400

    user_skill, error = add_skill_to_user(
        current_user_id,
        data
    )

    if error:

        return jsonify({
            "status": "error",
            "message": error
        }), 400

    return jsonify({

        "status": "success",

        "message": "Skill added successfully",

        "data": {

            "skill_id": user_skill.skill_id,

            "proficiency_level":
                user_skill.proficiency_level,

            "years_of_experience":
                user_skill.years_of_experience,

            "is_primary":
                user_skill.is_primary

        }

    }), 201


# ==========================
# Get Current User Skills
# ==========================

@skills_bp.route(
    "/me",
    methods=["GET"]
)
@jwt_required()
def get_my_skills():

    current_user_id = get_jwt_identity()

    user_skills = get_user_skills(
        current_user_id
    )

    return jsonify({

        "status": "success",

        "count": len(user_skills),

        "data": [

            {

                "skill_id":
                    item.skill.id,

                "skill_name":
                    item.skill.name,

                "category":
                    item.skill.category,

                "proficiency_level":
                    item.proficiency_level,

                "years_of_experience":
                    item.years_of_experience,

                "is_primary":
                    item.is_primary

            }

            for item in user_skills

        ]

    }), 200


# ==========================
# Remove User Skill
# ==========================

@skills_bp.route(
    "/me/<int:skill_id>",
    methods=["DELETE"]
)
@jwt_required()
def delete_my_skill(skill_id):

    current_user_id = get_jwt_identity()

    error = remove_user_skill(
        current_user_id,
        skill_id
    )

    if error:

        return jsonify({
            "status": "error",
            "message": error
        }), 404

    return jsonify({
        "status": "success",
        "message": "Skill removed successfully"
    }), 200