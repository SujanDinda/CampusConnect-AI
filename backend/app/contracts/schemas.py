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