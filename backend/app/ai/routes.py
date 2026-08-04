from flask import Blueprint

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from app.ai.services import parse_latest_resume
from app.utils.api_response import (
    success_response,
    error_response
)

ai_bp = Blueprint(
    "ai",
    __name__
)


@ai_bp.route(
    "/resumes/parse",
    methods=["POST"]
)
@jwt_required()
def parse_resume():

    user_id = get_jwt_identity()

    data, error = parse_latest_resume(
        user_id
    )

    if error:

        return error_response(
            message=error,
            status_code=404
        )

    return success_response(
        message="Resume parsed successfully",
        data=data
    )