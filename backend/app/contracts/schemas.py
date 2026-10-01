ALLOWED_CONTRACT_STATUS = [
    "Active",
    "Completed",
    "Cancelled"
]


def validate_contract_data(data):
    errors = {}

    if not data.get("application_id"):
        errors["application_id"] = "Application ID is required"

    return errors


def validate_contract_status_data(data):
    errors = {}

    status = data.get("status")

    if not status:
        errors["status"] = "Contract status is required"

    elif status not in ALLOWED_CONTRACT_STATUS:
        errors["status"] = "Invalid contract status"

    return errors


from datetime import datetime


def validate_contract_dates_data(data):
    errors = {}

    start_date = data.get("start_date")
    end_date = data.get("end_date")

    parsed_start_date = None
    parsed_end_date = None

    if start_date:
        try:
            parsed_start_date = datetime.strptime(
                start_date,
                "%Y-%m-%d"
            ).date()
        except ValueError:
            errors["start_date"] = (
                "Start date must be in YYYY-MM-DD format"
            )

    if end_date:
        try:
            parsed_end_date = datetime.strptime(
                end_date,
                "%Y-%m-%d"
            ).date()
        except ValueError:
            errors["end_date"] = (
                "End date must be in YYYY-MM-DD format"
            )

    if (
        parsed_start_date
        and parsed_end_date
        and parsed_end_date < parsed_start_date
    ):
        errors["end_date"] = (
            "End date cannot be before start date"
        )

    return errors