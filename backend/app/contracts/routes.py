from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.contracts.schemas import (
    validate_contract_data,
    validate_contract_status_data
)

from app.contracts.services import (
    create_contract,
    get_contract,
    update_contract_status
)

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


@contract_bp.route("/<int:contract_id>", methods=["GET"])
@jwt_required()
def get_contract_details(contract_id):

    current_user = get_jwt_identity()

    contract, error = get_contract(
        contract_id
    )

    if error:
        return error_response(
            error,
            status_code=404
        )

    # Only client or freelancer involved in the contract can view it
    if (
        contract.client_id != int(current_user)
        and contract.freelancer_id != int(current_user)
    ):
        return error_response(
            "Permission denied",
            status_code=403
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
            "start_date": contract.start_date,
            "end_date": contract.end_date,
            "status": contract.status
        },
        message="Contract retrieved successfully",
        status_code=200
    )


@contract_bp.route("/<int:contract_id>/status", methods=["PUT"])
@jwt_required()
def update_contract_status_route(contract_id):

    current_user = get_jwt_identity()

    # Only CLIENT can update contract status
    if not has_role(
        current_user,
        "CLIENT"
    ):
        return error_response(
            "Permission denied",
            status_code=403
        )

    data = request.get_json() or {}

    errors = validate_contract_status_data(data)

    if errors:
        return error_response(
            "Validation failed",
            errors=errors,
            status_code=400
        )

    contract, error = update_contract_status(
        contract_id=contract_id,
        client_id=current_user,
        status=data["status"]
    )

    if error:
        return error_response(
            error,
            status_code=404
            if error == "Contract not found"
            else 403
        )

    return success_response(
        data={
            "contract_id": contract.id,
            "status": contract.status
        },
        message="Contract status updated successfully",
        status_code=200
    )