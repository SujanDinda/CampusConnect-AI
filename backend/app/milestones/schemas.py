from datetime import datetime


ALLOWED_MILESTONE_STATUS = [
    "Pending",
    "In Progress",
    "Submitted",
    "Approved",
    "Rejected",
    "Completed"
]


def validate_milestone_data(data):
    errors = {}

    if not data.get("contract_id"):
        errors["contract_id"] = (
            "Contract ID is required"
        )

    if not data.get("title"):
        errors["title"] = (
            "Milestone title is required"
        )

    amount = data.get("amount")

    if amount is None:
        errors["amount"] = (
            "Milestone amount is required"
        )
    elif not isinstance(amount, (int, float)):
        errors["amount"] = (
            "Milestone amount must be a number"
        )
    elif amount <= 0:
        errors["amount"] = (
            "Milestone amount must be greater than 0"
        )

    due_date = data.get("due_date")

    if due_date:
        try:
            datetime.strptime(
                due_date,
                "%Y-%m-%d"
            ).date()
        except ValueError:
            errors["due_date"] = (
                "Due date must be in YYYY-MM-DD format"
            )

    return errors


def validate_milestone_status_data(data):
    errors = {}

    status = data.get("status")

    if not status:
        errors["status"] = (
            "Milestone status is required"
        )

    elif status not in ALLOWED_MILESTONE_STATUS:
        errors["status"] = (
            "Invalid milestone status"
        )

    return errors