from email_validator import validate_email, EmailNotValidError


def validate_registration_data(data):

    errors = {}

    email = data.get("email")
    password = data.get("password")

    if not email:
        errors["email"] = "Email is required"

    else:
        try:
            validate_email(email)

        except EmailNotValidError:
            errors["email"] = "Invalid email address"

    if not password:
        errors["password"] = "Password is required"

    elif len(password) < 8:
        errors["password"] = (
            "Password must be at least 8 characters"
        )

    return errors