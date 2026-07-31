def validate_skill_data(data):

    errors = {}

    if not data.get("name"):
        errors["name"] = "Skill name is required"

    if len(data.get("name", "")) > 100:
        errors["name"] = "Skill name is too long"

    if data.get("category") and len(data["category"]) > 100:
        errors["category"] = "Category is too long"

    return errors


# ==========================
# User Skill Validation
# ==========================

ALLOWED_PROFICIENCY_LEVELS = [
    "Beginner",
    "Intermediate",
    "Advanced",
    "Expert"
]


def validate_user_skill_data(data):

    errors = {}

    # Skill ID
    if not data.get("skill_id"):
        errors["skill_id"] = "Skill ID is required"

    # Proficiency Level
    proficiency = data.get("proficiency_level")

    if not proficiency:
        errors["proficiency_level"] = \
            "Proficiency level is required"

    elif proficiency not in ALLOWED_PROFICIENCY_LEVELS:

        errors["proficiency_level"] = (
            f"Must be one of: "
            f"{', '.join(ALLOWED_PROFICIENCY_LEVELS)}"
        )

    # Years of Experience
    years = data.get("years_of_experience")

    if years is None:

        errors["years_of_experience"] = \
            "Years of experience is required"

    else:

        try:

            years = float(years)

            if years < 0:

                errors["years_of_experience"] = \
                    "Cannot be negative"

            elif years > 50:

                errors["years_of_experience"] = \
                    "Invalid years of experience"

        except (TypeError, ValueError):

            errors["years_of_experience"] = \
                "Must be a number"

    return errors