from app.extensions import db
from app.models.job_application import JobApplication
from app.models.contract import Contract


def create_contract(application_id, client_id):
    application = JobApplication.query.get(application_id)

    if not application:
        return None, "Application not found"

    # Contract can only be created from an accepted proposal
    if application.status != "Accepted":
        return None, "Only accepted applications can create a contract"

    # Verify that the logged-in client owns the job
    if application.job.company.owner_id != int(client_id):
        return None, "Permission denied"

    # Prevent duplicate contract
    existing_contract = Contract.query.filter_by(
        application_id=application_id
    ).first()

    if existing_contract:
        return None, "Contract already exists for this application"

    contract = Contract(
        job_id=application.job_id,
        application_id=application.id,
        client_id=client_id,
        freelancer_id=application.applicant_id,
        agreed_amount=application.proposed_amount,
        status="Active"
    )

    db.session.add(contract)
    db.session.commit()

    return contract, None