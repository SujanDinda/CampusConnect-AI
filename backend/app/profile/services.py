from app.extensions import db

from app.models.profile import Profile


def get_profile_by_user_id(user_id):

    profile = Profile.query.filter_by(
        user_id=user_id
    ).first()

    return profile


def create_profile(
    user_id,
    data
):

    existing_profile = Profile.query.filter_by(
        user_id=user_id
    ).first()

    if existing_profile:

        return None, "Profile already exists"

    profile = Profile(

        user_id=user_id,

        full_name=data.get(
            "full_name"
        ),

        headline=data.get(
            "headline"
        ),

        bio=data.get(
            "bio"
        ),

        phone=data.get(
            "phone"
        ),

        profile_image=data.get(
            "profile_image"
        ),

        location=data.get(
            "location"
        ),

        city=data.get(
            "city"
        ),

        state=data.get(
            "state"
        ),

        country=data.get(
            "country"
        ),

        department=data.get(
            "department"
        ),

        graduation_year=data.get(
            "graduation_year"
        ),

        hourly_rate=data.get(
            "hourly_rate"
        ),

        availability_status=data.get(
            "availability_status",
            "available"
        ),

        resume_url=data.get(
            "resume_url"
        ),

        portfolio_url=data.get(
            "portfolio_url"
        ),

        github_url=data.get(
            "github_url"
        ),

        linkedin_url=data.get(
            "linkedin_url"
        ),

        website_url=data.get(
            "website_url"
        )
    )

    db.session.add(
        profile
    )

    db.session.commit()

    return profile, None


def update_profile(
    user_id,
    data
):

    profile = Profile.query.filter_by(
        user_id=user_id
    ).first()

    if not profile:
        return None, "Profile not found"

    allowed_fields = [
        "full_name",
        "headline",
        "bio",
        "phone",
        "profile_image",
        "location",
        "city",
        "state",
        "country",
        "department",
        "graduation_year",
        "hourly_rate",
        "availability_status",
        "resume_url",
        "portfolio_url",
        "github_url",
        "linkedin_url",
        "website_url"
    ]

    for field in allowed_fields:

        if field in data:

            setattr(
                profile,
                field,
                data[field]
            )

    db.session.commit()

    return profile, None