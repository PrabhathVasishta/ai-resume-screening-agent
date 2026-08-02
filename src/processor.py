# src/processor.py

import os
import re


class ResumeProcessor:
    """
    Cleans extracted text and extracts useful information.
    """

    def __init__(self, skills_file: str):

        if not os.path.exists(skills_file):
            raise FileNotFoundError(
                f"Skills file not found: {skills_file}"
            )

        self.skills = self.load_skills(skills_file)

    def load_skills(self, skills_file: str) -> set:
        """
        Load skills from skills.txt
        """

        with open(skills_file, "r", encoding="utf-8") as file:

            return {
                skill.strip().lower()
                for skill in file
                if skill.strip()
            }

    def clean_text(self, text: str) -> str:
        """
        Clean extracted resume text.
        """

        text = text.lower()

        text = re.sub(r"[^a-z0-9\s]", " ", text)

        text = re.sub(r"\s+", " ", text)

        return text.strip()

    def extract_skills(self, cleaned_text: str) -> list:
        """
        Extract matching skills.
        """

        extracted_skills = []

        for skill in self.skills:

            if skill in cleaned_text:
                extracted_skills.append(skill)

        return sorted(extracted_skills)

    def preprocess(self, text: str) -> dict:
        """
        Complete preprocessing pipeline.
        """

        cleaned_text = self.clean_text(text)

        skills = self.extract_skills(cleaned_text)

        return {
            "cleaned_text": cleaned_text,
            "skills": skills
        }