from email_validator import validate_email, EmailNotValidError


def validate_profile_data(data):

    errors = {}

    # ==========================
    # Full Name
    # ==========================

    full_name = data.get("full_name")

    if not full_name:
        errors["full_name"] = "Full name is required"

    elif len(full_name.strip()) < 2:
        errors["full_name"] = (
            "Full name must be at least 2 characters"
        )

    # ==========================
    # Headline
    # ==========================

    headline = data.get("headline")

    if headline and len(headline) > 255:
        errors["headline"] = (
            "Headline must not exceed 255 characters"
        )

    # ==========================
    # Bio
    # ==========================

    bio = data.get("bio")

    if bio and len(bio) > 2000:
        errors["bio"] = (
            "Bio must not exceed 2000 characters"
        )

    # ==========================
    # Phone
    # ==========================

    phone = data.get("phone")

    if phone and len(phone) > 20:
        errors["phone"] = (
            "Phone number is too long"
        )

    # ==========================
    # Graduation Year
    # ==========================

    graduation_year = data.get(
        "graduation_year"
    )

    if graduation_year:

        if not isinstance(
            graduation_year,
            int
        ):

            errors["graduation_year"] = (
                "Graduation year must be a number"
            )

    # ==========================
    # Hourly Rate
    # ==========================

    hourly_rate = data.get(
        "hourly_rate"
    )

    if hourly_rate is not None:

        try:

            if float(hourly_rate) < 0:

                errors["hourly_rate"] = (
                    "Hourly rate cannot be negative"
                )

        except (
            ValueError,
            TypeError
        ):

            errors["hourly_rate"] = (
                "Hourly rate must be a valid number"
            )

    # ==========================
    # Availability Status
    # ==========================

    availability_status = data.get(
        "availability_status"
    )

    allowed_statuses = [
        "available",
        "busy",
        "not_available"
    ]

    if availability_status:

        if availability_status not in allowed_statuses:

            errors["availability_status"] = (
                "Invalid availability status"
            )

    return errors