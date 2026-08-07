def calculate_resume_score(resume_data):

    score = 0
    breakdown = {}

    # -------------------------
    # Technical Skills - 30
    # -------------------------

    technical = resume_data.get(
        "technical_skills",
        {}
    )

    skill_count = (
        len(technical.get("languages", []))
        + len(technical.get("web_technologies", []))
    )

    technical_score = min(
        skill_count * 10,
        30
    )

    score += technical_score

    breakdown["technical_skills"] = technical_score

    # -------------------------
    # Projects - 25
    # -------------------------

    projects = resume_data.get(
        "projects",
        []
    )

    project_score = min(
        len(projects) * 12.5,
        25
    )

    score += project_score

    breakdown["projects"] = project_score

    # -------------------------
    # Internship - 20
    # -------------------------

    internships = resume_data.get(
        "internships",
        []
    )

    internship_score = min(
        len(internships) * 20,
        20
    )

    score += internship_score

    breakdown["internships"] = internship_score

    # -------------------------
    # Education - 15
    # -------------------------

    education = resume_data.get(
        "education",
        []
    )

    education_score = 15 if education else 0

    score += education_score

    breakdown["education"] = education_score

    # -------------------------
    # Completeness - 10
    # -------------------------

    completeness_score = 0

    if resume_data.get("name"):
        completeness_score += 2

    if resume_data.get("email"):
        completeness_score += 2

    if resume_data.get("phone"):
        completeness_score += 2

    if resume_data.get("projects"):
        completeness_score += 2

    if resume_data.get("technical_skills"):
        completeness_score += 2

    score += completeness_score

    breakdown["completeness"] = completeness_score

    # -------------------------
    # Final Score
    # -------------------------

    return {
        "overall_score": round(score, 2),
        "breakdown": breakdown
    }