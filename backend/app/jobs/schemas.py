# Allowed values
ALLOWED_JOB_TYPES = [
    "Full Time",
    "Part Time",
    "Internship",
    "Freelance",
    "Contract"
]

ALLOWED_WORK_MODES = [
    "Remote",
    "Hybrid",
    "On-site"
]


def validate_job_data(data):

    errors = {}

    required_fields = [
        "company_id",
        "category_id",
        "title",
        "description",
        "job_type",
        "work_mode"
    ]

    for field in required_fields:

        if not data.get(field):

            errors[field] = f"{field} is required"

    if (
        data.get("job_type")
        and
        data["job_type"] not in ALLOWED_JOB_TYPES
    ):

        errors["job_type"] = "Invalid job type"

    if (
        data.get("work_mode")
        and
        data["work_mode"] not in ALLOWED_WORK_MODES
    ):

        errors["work_mode"] = "Invalid work mode"

    salary_min = data.get("salary_min")
    salary_max = data.get("salary_max")

    if (
        salary_min is not None
        and
        salary_max is not None
        and
        salary_min > salary_max
    ):

        errors["salary"] = (
            "salary_min cannot be greater than salary_max"
        )

    return errors


def validate_company_data(data):

    errors = {}

    if not data.get("name"):
        errors["name"] = "Company name is required"

    website = data.get("website")

    if website and not (
        website.startswith("http://")
        or
        website.startswith("https://")
    ):
        errors["website"] = (
            "Website must start with http:// or https://"
        )

    return errors