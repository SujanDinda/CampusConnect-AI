from app.extensions import db
from app.models.contract import Contract
from app.models.milestone import Milestone


def create_milestone(
    contract_id,
    client_id,
    title,
    description,
    amount,
    due_date
):
    contract = Contract.query.get(contract_id)

    if not contract:
        return None, "Contract not found"

    # Only the client who owns the contract can create milestones
    if contract.client_id != int(client_id):
        return None, "Permission denied"

    # Prevent milestone creation for cancelled contracts
    if contract.status == "Cancelled":
        return None, "Cannot create milestone for a cancelled contract"

    milestone = Milestone(
        contract_id=contract_id,
        title=title,
        description=description,
        amount=amount,
        due_date=due_date,
        status="Pending"
    )

    db.session.add(milestone)
    db.session.commit()

    return milestone, None


def get_milestone(milestone_id, user_id):
    milestone = Milestone.query.get(milestone_id)

    if not milestone:
        return None, "Milestone not found"

    contract = milestone.contract

    if (
        contract.client_id != int(user_id)
        and contract.freelancer_id != int(user_id)
    ):
        return None, "Permission denied"

    return milestone, None


def update_milestone_status(
    milestone_id,
    user_id,
    status
):
    milestone = Milestone.query.get(
        milestone_id
    )

    if not milestone:
        return None, "Milestone not found"

    contract = milestone.contract

    current_status = milestone.status

    # Client workflow
    if contract.client_id == int(user_id):

        allowed_transitions = {
            "Pending": ["In Progress"],
            "Submitted": ["Approved", "Rejected"],
            "Approved": ["Completed"],
            "Rejected": ["In Progress"]
        }

        allowed_statuses = allowed_transitions.get(
            current_status,
            []
        )

        if status not in allowed_statuses:
            return None, (
                f"Cannot change milestone status "
                f"from {current_status} to {status}"
            )

    # Freelancer workflow
    elif contract.freelancer_id == int(user_id):

        if current_status != "In Progress":
            return None, (
                "Freelancer can submit only "
                "an In Progress milestone"
            )

        if status != "Submitted":
            return None, (
                "Freelancer can only change "
                "In Progress to Submitted"
            )

    else:
        return None, "Permission denied"

    milestone.status = status

    db.session.commit()

    return milestone, None