from app import create_app

from app.permissions.services import is_job_owner


app = create_app()


with app.app_context():

    user_id = 3
    job_id = 5

    result = is_job_owner(
        user_id,
        job_id
    )

    print("User ID:", user_id)
    print("Job ID:", job_id)
    print("Is Job Owner:", result)