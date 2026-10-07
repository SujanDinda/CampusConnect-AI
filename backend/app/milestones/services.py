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