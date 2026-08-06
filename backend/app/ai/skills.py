from collections import defaultdict


def build_unified_skills(resume_data):

    skill_map = defaultdict(set)

    # Technical Skills
    technical = resume_data.get(
        "technical_skills",
        {}
    )

    for skill in technical.get(
        "languages",
        []
    ):

        skill_map[skill].add(
            "TECHNICAL_SKILLS"
        )

    for skill in technical.get(
        "web_technologies",
        []
    ):

        skill_map[skill].add(
            "TECHNICAL_SKILLS"
        )

    # Projects
    for project in resume_data.get(
        "projects",
        []
    ):

        for skill in project.get(
            "skills",
            []
        ):

            skill_map[skill].add(
                "PROJECT"
            )

    # Internships
    for internship in resume_data.get(
        "internships",
        []
    ):

        for skill in internship.get(
            "skills",
            []
        ):

            skill_map[skill].add(
                "INTERNSHIP"
            )

    unified = []

    for skill, sources in sorted(skill_map.items()):

        unified.append({

            "name": skill,

            "sources": sorted(list(sources))

        })

    return unified