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