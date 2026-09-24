from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.contracts.schemas import validate_contract_data
from app.contracts.services import create_contract

from app.permissions.services import has_role

from app.utils.api_response import success_response, error_response


contract_bp = Blueprint(
    "contracts",
    __name__,
    url_prefix="/api/v1/contracts"
)


@contract_bp.route("/", methods=["POST"])
@jwt_required()
def create_new_contract():

    current_user = get_jwt_identity()

    if not has_role(
        current_user,
        "CLIENT"
    ):
        return error_response(
            "Permission denied",
            status_code=403
        )

    data = request.get_json() or {}

    errors = validate_contract_data(data)

    if errors:
        return error_response(
            "Validation failed",
            errors=errors,
            status_code=400
        )

    contract, error = create_contract(
        application_id=data["application_id"],
        client_id=current_user
    )

    if error:
        return error_response(
            error,
            status_code=403
            if error == "Permission denied"
            else 400
        )

    return success_response(
        data={
            "contract_id": contract.id,
            "job_id": contract.job_id,
            "application_id": contract.application_id,
            "client_id": contract.client_id,
            "freelancer_id": contract.freelancer_id,
            "agreed_amount": float(
                contract.agreed_amount
            ),
            "status": contract.status
        },
        message="Contract created successfully",
        status_code=201
    )