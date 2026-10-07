from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.milestones.schemas import (
    validate_milestone_data
)

from app.milestones.services import (
    create_milestone,
    get_milestone
)

from app.permissions.services import has_role

from app.utils.api_response import (
    success_response,
    error_response
)


milestone_bp = Blueprint(
    "milestones",
    __name__,
    url_prefix="/api/v1/milestones"
)


@milestone_bp.route("/", methods=["POST"])
@jwt_required()
def create_new_milestone():

    current_user = get_jwt_identity()

    # Only CLIENT can create milestones
    if not has_role(
        current_user,
        "CLIENT"
    ):
        return error_response(
            "Permission denied",
            status_code=403
        )

    data = request.get_json() or {}

    errors = validate_milestone_data(
        data
    )

    if errors:
        return error_response(
            "Validation failed",
            errors=errors,
            status_code=400
        )

    milestone, error = create_milestone(
        contract_id=data["contract_id"],
        client_id=current_user,
        title=data["title"],
        description=data.get("description"),
        amount=data["amount"],
        due_date=data.get("due_date")
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
            "milestone_id": milestone.id,
            "contract_id": milestone.contract_id,
            "title": milestone.title,
            "description": milestone.description,
            "amount": float(
                milestone.amount
            ),
            "due_date": str(
                milestone.due_date
            )
            if milestone.due_date
            else None,
            "status": milestone.status
        },
        message="Milestone created successfully",
        status_code=201
    )


@milestone_bp.route("/<int:milestone_id>", methods=["GET"])
@jwt_required()
def get_milestone_details(milestone_id):

    current_user = get_jwt_identity()

    milestone, error = get_milestone(
        milestone_id,
        current_user
    )

    if error:
        return error_response(
            error,
            status_code=404
            if error == "Milestone not found"
            else 403
        )

    return success_response(
        data={
            "milestone_id": milestone.id,
            "contract_id": milestone.contract_id,
            "title": milestone.title,
            "description": milestone.description,
            "amount": float(
                milestone.amount
            ),
            "due_date": str(
                milestone.due_date
            )
            if milestone.due_date
            else None,
            "status": milestone.status
        },
        message="Milestone retrieved successfully",
        status_code=200
    )