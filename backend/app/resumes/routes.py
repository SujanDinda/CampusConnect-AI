import os
from flask import request

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from app.resumes import resume_bp

from app.resumes.schemas import (
    allowed_file,
    MAX_FILE_SIZE
)

from app.resumes.services import save_resume

from app.utils.api_response import (
    success_response,
    error_response
)


@resume_bp.route(
    "/upload",
    methods=["POST"]
)
@jwt_required()
def upload_resume():

    if "resume" not in request.files:

        return error_response(
            message="Resume file is required",
            status_code=400
        )

    file = request.files["resume"]

    if file.filename == "":

        return error_response(
            message="No file selected",
            status_code=400
        )

    if not allowed_file(file.filename):

        return error_response(
            message="Only PDF and DOCX files are allowed",
            status_code=400
        )

    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)

    if size > MAX_FILE_SIZE:

        return error_response(
            message="File size exceeds 5 MB",
            status_code=400
        )

    user_id = get_jwt_identity()

    resume = save_resume(
        file,
        user_id
    )

    return success_response(
        message="Resume uploaded successfully",
        data={
            "resume_id": resume.id,
            "file_name": resume.file_name
        },
        status_code=201
    )