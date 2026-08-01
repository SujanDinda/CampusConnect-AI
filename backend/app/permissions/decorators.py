from functools import wraps

from flask_jwt_extended import (
    get_jwt_identity
)

from app.utils.api_response import error_response

from app.permissions.services import (
    has_role,
    has_any_role
)


def role_required(role_name):

    def decorator(fn):

        @wraps(fn)
        def wrapper(*args, **kwargs):

            user_id = get_jwt_identity()

            if not has_role(
                user_id,
                role_name
            ):

                return error_response(
                    message="Permission denied",
                    status_code=403
                )

            return fn(
                *args,
                **kwargs
            )

        return wrapper

    return decorator


def roles_required(role_names):

    def decorator(fn):

        @wraps(fn)
        def wrapper(*args, **kwargs):

            user_id = get_jwt_identity()

            if not has_any_role(
                user_id,
                role_names
            ):

                return error_response(
                    message="Permission denied",
                    status_code=403
                )

            return fn(
                *args,
                **kwargs
            )

        return wrapper

    return decorator