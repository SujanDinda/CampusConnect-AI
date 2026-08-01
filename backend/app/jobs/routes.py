from flask import request

from app.jobs import jobs_bp

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from app.jobs.schemas import (
    validate_job_data,
    validate_company_data,
    validate_job_application_data
)

from app.jobs.services import (
    create_job,
    create_job_category,
    create_company,
    get_all_jobs,
    get_job_by_id,
    update_job,
    delete_job,
    apply_for_job
)

from app.utils.api_response import (
    success_response,
    error_response
)


@jobs_bp.route(
    "",
    methods=["POST"]
)
@jwt_required()
def create_new_job():

    data = request.get_json()

    if not data:

        return error_response(
            message="Request body is required",
            status_code=400
        )

    errors = validate_job_data(data)

    if errors:

        return error_response(
            message="Validation failed",
            errors=errors,
            status_code=400
        )

    job, error = create_job(data)

    if error:

        return error_response(
            message=error,
            status_code=400
        )

    return success_response(

        message="Job created successfully",

        data={

            "id": job.id,

            "title": job.title,

            "company_id": job.company_id,

            "category_id": job.category_id

        },

        status_code=201
    )


@jobs_bp.route(
    "/categories",
    methods=["POST"]
)
@jwt_required()
def create_category():

    data = request.get_json()

    if not data or not data.get("name"):

        return error_response(
            message="Category name is required",
            status_code=400
        )

    category, error = create_job_category(data)

    if error:

        return error_response(
            message=error,
            status_code=400
        )

    return success_response(

        message="Job category created successfully",

        data={
            "id": category.id,
            "name": category.name
        },

        status_code=201
    )


@jobs_bp.route(
    "/companies",
    methods=["POST"]
)
@jwt_required()
def create_new_company():

    current_user_id = get_jwt_identity()

    data = request.get_json()

    if not data:

        return error_response(
            message="Request body is required",
            status_code=400
        )

    errors = validate_company_data(data)

    if errors:

        return error_response(
            message="Validation failed",
            errors=errors,
            status_code=400
        )

    company, error = create_company(
        current_user_id,
        data
    )

    if error:

        return error_response(
            message=error,
            status_code=400
        )

    return success_response(

        message="Company created successfully",

        data={
            "id": company.id,
            "name": company.name
        },

        status_code=201
    )


@jobs_bp.route(
    "",
    methods=["GET"]
)
def list_jobs():

    jobs = get_all_jobs()

    return success_response(

        message="Jobs fetched successfully",

        data=[

            {

                "id": job.id,

                "title": job.title,

                "company": job.company.name,

                "category": job.category.name,

                "location": job.location,

                "job_type": job.job_type,

                "work_mode": job.work_mode,

                "salary_min": job.salary_min,

                "salary_max": job.salary_max

            }

            for job in jobs

        ]

    )


@jobs_bp.route(
    "/<int:job_id>",
    methods=["GET"]
)
def get_job(job_id):

    job = get_job_by_id(job_id)

    if not job:

        return error_response(
            message="Job not found",
            status_code=404
        )

    return success_response(

        message="Job fetched successfully",

        data={

            "id": job.id,

            "title": job.title,

            "description": job.description,

            "company": job.company.name,

            "category": job.category.name,

            "location": job.location,

            "job_type": job.job_type,

            "work_mode": job.work_mode,

            "salary_min": job.salary_min,

            "salary_max": job.salary_max,

            "experience_required": job.experience_required,

            "vacancies": job.vacancies,

            "application_deadline": (
                str(job.application_deadline)
                if job.application_deadline
                else None
            )

        }

    )


@jobs_bp.route(
    "/<int:job_id>",
    methods=["PUT"]
)
@jwt_required()
def edit_job(job_id):

    data = request.get_json()

    if not data:

        return error_response(
            message="Request body is required",
            status_code=400
        )

    job, error = update_job(
        job_id,
        data
    )

    if error:

        return error_response(
            message=error,
            status_code=404
        )

    return success_response(

        message="Job updated successfully",

        data={

            "id": job.id,

            "title": job.title

        }

    )


@jobs_bp.route(
    "/<int:job_id>",
    methods=["DELETE"]
)
@jwt_required()
def remove_job(job_id):

    success, error = delete_job(job_id)

    if error:

        return error_response(
            message=error,
            status_code=404
        )

    return success_response(
        message="Job deleted successfully"
    )


@jobs_bp.route(
    "/apply",
    methods=["POST"]
)
@jwt_required()
def apply_job():

    applicant_id = get_jwt_identity()

    data = request.get_json()

    if not data:

        return error_response(
            message="Request body is required",
            status_code=400
        )

    errors = validate_job_application_data(data)

    if errors:

        return error_response(
            message="Validation failed",
            errors=errors,
            status_code=400
        )

    application, error = apply_for_job(
        applicant_id,
        data
    )

    if error:

        return error_response(
            message=error,
            status_code=400
        )

    return success_response(

        message="Application submitted successfully",

        data={

            "application_id": application.id,

            "job_id": application.job_id,

            "status": application.status

        },

        status_code=201
    )