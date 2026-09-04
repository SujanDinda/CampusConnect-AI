import re
import spacy

from app.ai.skills import build_unified_skills

from app.ai.scorer import calculate_resume_score

nlp = spacy.load("en_core_web_sm")

def extract_email(text):

    pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

    match = re.search(
        pattern,
        text
    )

    if match:
        return match.group()

    return None


def extract_phone(text):

    pattern = (
        r"(\+?\d{1,3}[- ]?)?"
        r"\d{10}"
    )

    match = re.search(
        pattern,
        text
    )

    if match:
        return match.group()

    return None


SKILLS = [
    "Python",
    "Flask",
    "Django",
    "FastAPI",
    "Java",
    "C",
    "C++",
    "SQL",
    "MySQL",
    "PostgreSQL",
    "MongoDB",
    "Git",
    "GitHub",
    "Docker",
    "Linux",
    "AWS",
    "Azure",
    "TensorFlow",
    "PyTorch",
    "Pandas",
    "NumPy",
    "Scikit-learn",
    "HTML",
    "CSS",
    "JavaScript",
    "React",
    "Node.js"
]


def extract_skills(text):

    found_skills = []

    for skill in SKILLS:

        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(
            pattern,
            text,
            re.IGNORECASE
        ):

            found_skills.append(skill)

    return sorted(
        list(set(found_skills))
    )


def extract_resume_data(text):

    sections = split_resume_sections(text)

    resume_data = {

        "name": extract_name(text),

        "email": extract_email(text),

        "phone": extract_phone(text),

        "education": extract_education(
            sections.get("education", [])
        ),

        "technical_skills": extract_technical_skills(
            sections.get("technical_skills", [])
        ),

        "projects": extract_projects(
            sections.get("projects", [])
        ),

        "internships": extract_internships(
            sections.get("internship", [])
        ),

        "skills": extract_skills(text)
    }

    resume_data["unified_skills"] = build_unified_skills(
        resume_data
    )
    resume_data["resume_score"] = calculate_resume_score(
        resume_data
    )
    return resume_data


def clean_text(text):

    text = text.strip()

    text = re.sub(
        r"^[•●◦o]\s*",
        "",
        text
    )

    return text


def extract_name(text):

    lines = text.splitlines()

    for line in lines[:5]:

        line = line.strip()

        if (
            line
            and len(line.split()) <= 4
            and "@" not in line
            and not any(char.isdigit() for char in line)
        ):
            return line

    doc = nlp(text)

    for entity in doc.ents:

        if entity.label_ == "PERSON":
            return entity.text

    return None



SECTION_HEADERS = {
    "CAREER OBJECTIVE": "career_objective",
    "OBJECTIVE": "career_objective",

    "EDUCATION": "education",
    "ACADEMIC QUALIFICATION": "education",
    "ACADEMIC QUALIFICATIONS": "education",

    "TECHNICAL SKILLS": "technical_skills",
    "TECHNICAL SKILL": "technical_skills",
    "SKILLS": "technical_skills",

    "SOFT SKILLS": "soft_skills",

    "PROJECT WORK": "projects",
    "PROJECT": "projects",
    "PROJECTS": "projects",

    "INTERNSHIP": "internship",
    "INTERNSHIPS": "internship",

    "WORK EXPERIENCE": "experience",
    "EXPERIENCE": "experience",

    "CERTIFICATION": "certifications",
    "CERTIFICATIONS": "certifications",

    "LANGUAGE PREFERENCE": "languages",
    "LANGUAGE PREFERENCES": "languages",
    "LANGUAGES": "languages",

    "ADDITIONAL INFORMATION": "additional_information",
    "HOBBIES": "additional_information",
    "INTERESTS": "additional_information"
}


def split_resume_sections(text):

    sections = {
        "header": []
    }

    current_section = "header"

    for line in text.splitlines():

        line = line.strip()

        if not line:
            continue

        upper_line = line.upper()

        section_found = False

        for heading, key in SECTION_HEADERS.items():

            if upper_line.startswith(heading):

                current_section = key

                if current_section not in sections:
                    sections[current_section] = []

                section_found = True
                break

        if not section_found:
            sections[current_section].append(line)

    return sections


def extract_education(education_lines):

    education = []

    current = {}

    for line in education_lines:

        line = clean_text(line)

        if not line:
            continue

        # Degree
        if any(
            degree in line.lower()
            for degree in [
                "b.tech",
                "bachelor",
                "b.sc",
                "m.tech",
                "mca",
                "mba",
                "secondary",
                "higher secondary"
            ]
        ):

            if current:
                education.append(current)

            current = {
                "degree": clean_text(line)
            }

        # Institution
        elif (
            "university" in line.lower()
            or
            "school" in line.lower()
            or
            "college" in line.lower()
        ):

            current["institution"] = clean_text(line)

        # CGPA
        elif "cgpa" in line.lower():

            match = re.search(
                r"(\d+(\.\d+)?)",
                line
            )

            if match:

                current["cgpa"] = match.group()

        # Percentage
        elif "percentage" in line.lower():

            match = re.search(
                r"(\d+(\.\d+)?)",
                line
            )

            if match:

                current["percentage"] = match.group()

        # Year
        elif "202" in line:

            match = re.search(
                r"(20\d\d)",
                line
            )

            if match:

                current["year"] = match.group()

    if current:

        education.append(current)

    return education


def extract_projects(project_lines):

    projects = []

    current = None

    for line in project_lines:

        line = clean_text(line)

        if not line:
            continue

        # Project Title
        if "|" in line:

            if current:
                projects.append(current)

            title, duration = line.split("|", 1)

            current = {
                "title": title.strip(),
                "duration": duration.strip(),
                "description": "",
                "skills": []
            }

        elif current:

            current["description"] += line + " "

    if current:
        projects.append(current)

    for project in projects:

        project["skills"] = extract_skills(
            project["description"]
        )

    return projects


def extract_internships(internship_lines):

    internships = []

    current = None

    for line in internship_lines:

        line = clean_text(line)

        if not line:
            continue

        # New internship entry
        if "|" in line:

            if current:
                internships.append(current)

            title, duration = line.split("|", 1)

            current = {
                "title": title.strip(),
                "duration": duration.strip(),
                "description": "",
                "skills": []
            }

        elif current:

            current["description"] += line + " "

    if current:
        internships.append(current)

    for internship in internships:

        internship["skills"] = extract_skills(
            internship["description"]
        )

    return internships


def extract_technical_skills(skill_lines):

    technical_skills = {

        "languages": [],

        "web_technologies": [],

        "core_subjects": []

    }

    current_section = None

    for line in skill_lines:

        line = clean_text(line)

        if not line:
            continue

        lower = line.lower()

        # Languages
        if lower.startswith("languages"):

            current_section = "languages"

            skills = line.split(":", 1)[1]

            technical_skills[current_section] = [

                skill.strip()

                for skill in skills.split(",")

                if skill.strip()

            ]

        # Web Technologies
        elif lower.startswith("web technologies"):

            current_section = "web_technologies"

            skills = line.split(":", 1)[1]

            technical_skills[current_section] = [

                skill.strip()

                for skill in skills.split(",")

                if skill.strip()

            ]

        # Core Subjects
        elif lower.startswith("core subjects"):

            current_section = "core_subjects"

        elif current_section == "core_subjects":

            technical_skills[current_section].append(
                line
            )

    return technical_skills