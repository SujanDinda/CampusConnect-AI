from app.ai.parser import extract_resume_text

from app.ai.extractor import split_resume_sections

from app.ai.parser import extract_resume_text

text = extract_resume_text(
    "uploads/resumes/1_a967eca41ee94f8cacf9b7f3fc945684.pdf"
)

print(text)


# sections = split_resume_sections(text)

# for section, content in sections.items():

#     print(section)

#     print("-" * 30)

#     print("\n".join(content))

#     print()


sections = split_resume_sections(text)

for section, content in sections.items():

    print(f"\n===== {section.upper()} =====")

    for line in content:
        print(line)