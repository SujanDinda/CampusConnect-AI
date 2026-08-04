import re

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

    text = text.lower()

    for skill in SKILLS:

        if skill.lower() in text:

            found_skills.append(skill)

    return sorted(list(set(found_skills)))


def extract_resume_data(text):

    return {
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text)
    }