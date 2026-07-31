from app.extensions import db

from app.models.job import Job
from app.models.company import Company
from app.models.job_category import JobCategory



# ==========================
# Create Job
# ==========================

def create_job(data):

    company = Company.query.get(
        data["company_id"]
    )

    if not company:
        return None, "Company not found"

    category = JobCategory.query.get(
        data["category_id"]
    )

    if not category:
        return None, "Job category not found"

    job = Job(

        company_id=data["company_id"],

        category_id=data["category_id"],

        title=data["title"],

        description=data["description"],

        location=data.get("location"),

        job_type=data["job_type"],

        work_mode=data["work_mode"],

        salary_min=data.get("salary_min"),

        salary_max=data.get("salary_max"),

        experience_required=data.get(
            "experience_required",
            0
        ),

        vacancies=data.get(
            "vacancies",
            1
        ),

        application_deadline=data.get(
            "application_deadline"
        )

    )

    db.session.add(job)
    db.session.commit()

    return job, None


# ==========================
# Create Job Category
# ==========================

def create_job_category(data):

    existing = JobCategory.query.filter_by(
        name=data["name"]
    ).first()

    if existing:
        return None, "Job category already exists"

    category = JobCategory(
        name=data["name"],
        description=data.get("description")
    )

    db.session.add(category)
    db.session.commit()

    return category, None


# ==========================
# Create Company
# ==========================

def create_company(owner_id, data):

    existing = Company.query.filter_by(
        name=data["name"]
    ).first()

    if existing:
        return None, "Company already exists"

    company = Company(

        owner_id=owner_id,

        name=data["name"],

        description=data.get("description"),

        website=data.get("website"),

        logo=data.get("logo"),

        industry=data.get("industry")

    )

    db.session.add(company)
    db.session.commit()

    return company, None


# ==========================
# Get All Jobs
# ==========================

def get_all_jobs():

    return Job.query.filter_by(
        is_active=True
    ).all()


# ==========================
# Get Job By ID
# ==========================

def get_job_by_id(job_id):

    job = Job.query.filter_by(
        id=job_id,
        is_active=True
    ).first()

    if not job:
        return None

    return job


# ==========================
# Update Job
# ==========================

def update_job(job_id, data):

    job = Job.query.filter_by(
        id=job_id,
        is_active=True
    ).first()

    if not job:
        return None, "Job not found"

    for key, value in data.items():

        if hasattr(job, key):
            setattr(job, key, value)

    db.session.commit()

    return job, None


# ==========================
# Delete Job (Soft Delete)
# ==========================

def delete_job(job_id):

    job = Job.query.filter_by(
        id=job_id,
        is_active=True
    ).first()

    if not job:
        return False, "Job not found"

    job.is_active = False

    db.session.commit()

    return True, None