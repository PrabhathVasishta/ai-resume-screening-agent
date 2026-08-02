# src/section_parser.py

class ResumeSectionParser:

    def __init__(self):

        self.headings = {
            "skills": [
                "skills",
                "technical skills",
                "core skills",
                "key skills"
            ],
            "projects": [
                "projects",
                "project"
            ],
            "education": [
                "education",
                "qualification",
                "academic qualification"
            ],
            "experience": [
                "experience",
                "work experience",
                "professional experience"
            ],
            "certifications": [
                "certifications",
                "certification"
            ]
        }

    def extract_sections(self, text):

        sections = {
            "skills": "",
            "projects": "",
            "education": "",
            "experience": "",
            "certifications": ""
        }

        current = None

        for line in text.split("\n"):

            line = line.strip()

            if not line:
                continue

            lower = line.lower()

            for section, names in self.headings.items():

                if lower in names:
                    current = section
                    break
            else:
                if current:
                    sections[current] += line + "\n"

        return sections