from app.extensions import db
from flask_jwt_extended import get_jwt_identity
from app.models.skill import (
    Skill,
    UserSkill
)

from app.models.user import User

def create_skill(data):

    existing_skill = Skill.query.filter_by(
        name=data["name"]
    ).first()

    if existing_skill:
        return None, "Skill already exists"

    skill = Skill(
        name=data["name"],
        category=data.get("category"),
        description=data.get("description"),
        icon=data.get("icon")
    )

    db.session.add(skill)
    db.session.commit()

    return skill, None


def get_all_skills():

    return Skill.query.filter_by(
        is_active=True
    ).order_by(
        Skill.name
    ).all()


# ==========================
# Add Skill to User
# ==========================

def add_skill_to_user(user_id, data):

    # Check User
    user = User.query.get(user_id)

    if not user:
        return None, "User not found"

    # Check Skill
    skill = Skill.query.get(data["skill_id"])

    if not skill:
        return None, "Skill not found"

    # Prevent Duplicate Skill
    existing = UserSkill.query.filter_by(
        user_id=user_id,
        skill_id=data["skill_id"]
    ).first()

    if existing:
        return None, "Skill already added"

    # Only One Primary Skill
    if data.get("is_primary"):

        UserSkill.query.filter_by(
            user_id=user_id,
            is_primary=True
        ).update(
            {
                "is_primary": False
            }
        )

    # Create User Skill
    user_skill = UserSkill(

        user_id=user_id,

        skill_id=data["skill_id"],

        proficiency_level=data["proficiency_level"],

        years_of_experience=data["years_of_experience"],

        is_primary=data.get(
            "is_primary",
            False
        )

    )

    db.session.add(user_skill)

    db.session.commit()

    return user_skill, None


# ==========================
# Get User Skills
# ==========================

def get_user_skills(user_id):

    user_skills = UserSkill.query.filter_by(
        user_id=user_id
    ).all()

    return user_skills


# ==========================
# Remove User Skill
# ==========================

def remove_user_skill(user_id, skill_id):

    user_skill = UserSkill.query.filter_by(
        user_id=user_id,
        skill_id=skill_id
    ).first()

    if not user_skill:
        return "Skill not found"

    db.session.delete(user_skill)
    db.session.commit()

    return None