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
    apply_for_job,
    get_my_applications,
    get_job_applications,
    update_application_status,
    withdraw_application
)

from app.utils.api_response import (
    success_response,
    error_response
)

from app.permissions.decorators import (
    role_required,
    roles_required
)

from app.permissions.services import (
    is_job_owner,
    is_application_owner
)


@jobs_bp.route(
    "",
    methods=["POST"]
)
@jwt_required()
@role_required("CLIENT")
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
@role_required("ADMIN")
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
@role_required("CLIENT")
def create_company_route():

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
@role_required("CLIENT")
def edit_job(job_id):

    current_user = get_jwt_identity()

    if not is_job_owner(current_user, job_id):

        return error_response(
            message="Permission denied",
            status_code=403
        )

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
@role_required("CLIENT")
def remove_job(job_id):

    current_user = get_jwt_identity()

    if not is_job_owner(current_user, job_id):

        return error_response(
            message="Permission denied",
            status_code=403
        )

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
@roles_required([
    "STUDENT",
    "FREELANCER"
])
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


@jobs_bp.route(
    "/applications/me",
    methods=["GET"]
)
@jwt_required()
def my_applications():

    applicant_id = get_jwt_identity()

    applications = get_my_applications(
        applicant_id
    )

    return success_response(

        message="Applications fetched successfully",

        data=[

            {

                "application_id": app.id,

                "job_id": app.job.id,

                "job_title": app.job.title,

                "company": app.job.company.name,

                "status": app.status,

                "applied_at": app.created_at

            }

            for app in applications

        ]

    )


@jobs_bp.route(
    "/<int:job_id>/applications",
    methods=["GET"]
)
@jwt_required()
def list_job_applications(job_id):

    current_user = get_jwt_identity()

    if not is_job_owner(current_user, job_id):

        return error_response(
            message="Permission denied",
            status_code=403
        )

    applications = get_job_applications(job_id)

    return success_response(

        message="Applicants fetched successfully",

        data=[
            {
                "application_id": app.id,
                "applicant_id": app.applicant.id,
                "email": app.applicant.email,
                "status": app.status,
                "cover_letter": app.cover_letter,
                "resume_url": app.resume_url,
                "applied_at": app.created_at
            }
            for app in applications
        ]
    )


@jobs_bp.route(
    "/applications/<int:application_id>/status",
    methods=["PUT"]
)
@jwt_required()
def change_application_status(application_id):

    current_user = get_jwt_identity()

    if not is_application_owner(
        current_user,
        application_id
    ):

        return error_response(
            message="Permission denied",
            status_code=403
        )

    data = request.get_json()

    status = data.get("status")

    if not status:

        return error_response(
            message="Status is required",
            status_code=400
        )

    application, error = update_application_status(
        application_id,
        status
    )

    if error:

        return error_response(
            message=error,
            status_code=404
        )

    return success_response(

        message="Application status updated successfully",

        data={

            "application_id": application.id,

            "status": application.status

        }

    )


@jobs_bp.route(
    "/applications/<int:application_id>",
    methods=["DELETE"]
)
@jwt_required()
def withdraw_job_application(application_id):

    applicant_id = get_jwt_identity()

    success, error = withdraw_application(
        application_id,
        applicant_id
    )

    if error:

        return error_response(
            message=error,
            status_code=404
        )

    return success_response(
        message="Application withdrawn successfully"
    )