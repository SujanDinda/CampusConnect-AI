from app.ai.parser import extract_resume_text

text = extract_resume_text(
    "uploads/resumes/1_e3efba6f23164b2dad92e566ae5d1401.pdf"
)

print(text)