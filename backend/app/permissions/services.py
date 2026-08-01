from app.models.user import User
from app.models.job import Job
from app.models.job_application import JobApplication

def has_role(user_id, role_name):

    user = User.query.get(user_id)

    if not user:
        return False

    return any(
        role.name == role_name
        for role in user.roles
    )


def has_any_role(user_id, role_names):

    user = User.query.get(user_id)

    if not user:
        return False

    user_roles = {
        role.name
        for role in user.roles
    }

    return bool(
        user_roles.intersection(
            set(role_names)
        )
    )


def is_job_owner(user_id, job_id):
    """
    Check whether the current user owns the job.
    """

    job = Job.query.get(job_id)

    if not job:
        return False

    return job.company.owner_id == user_id


def is_application_owner(user_id, application_id):
    """
    Check whether the current user owns
    the job related to this application.
    """

    application = JobApplication.query.get(application_id)

    if not application:
        return False

    return application.job.company.owner_id == user_id