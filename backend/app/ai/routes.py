from flask import Blueprint

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from app.ai.services import (
    parse_latest_resume,
    match_latest_resume_with_job
)
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


@ai_bp.route(
    "/jobs/<int:job_id>/match",
    methods=["POST"]
)
@jwt_required()
def match_job(job_id):

    user_id = get_jwt_identity()

    data, error = match_latest_resume_with_job(
        user_id,
        job_id
    )

    if error:

        return error_response(
            message=error,
            status_code=404
        )

    return success_response(
        message="Resume matched successfully",
        data=data
    )