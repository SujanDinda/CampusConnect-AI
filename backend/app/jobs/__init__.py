from flask import Blueprint

jobs_bp = Blueprint(
    "jobs",
    __name__,
    url_prefix="/api/v1/jobs"
)