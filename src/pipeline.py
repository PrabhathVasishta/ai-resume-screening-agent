# src/pipeline.py

import os

from src.parser import ResumeParser
from src.processor import ResumeProcessor
from src.section_parser import ResumeSectionParser
from src.matcher import ResumeMatcher
from src.llm import LLMReviewer
from src.exporter import ResultExporter


class ResumeScreeningPipeline:

    def __init__(self):

        self.parser = ResumeParser()

        self.processor = ResumeProcessor(
            "data/skills.txt"
        )

        self.section_parser = ResumeSectionParser()

        self.matcher = ResumeMatcher()

        self.llm = LLMReviewer()

        self.exporter = ResultExporter()

    def process(
        self,
        job_description,
        resume_folder
    ):

        results = []

        # -------------------------
        # Process Job Description
        # -------------------------

        jd_data = self.processor.preprocess(
            job_description
        )

        jd_data["sections"] = self.section_parser.extract_sections(
            job_description
        )

        # -------------------------
        # Process Every Resume
        # -------------------------

        for file_name in os.listdir(resume_folder):

            file_path = os.path.join(
                resume_folder,
                file_name
            )

            if not os.path.isfile(file_path):
                continue

            try:

                # Read Resume
                resume_text = self.parser.extract_text(
                    file_path
                )

                # Clean Resume
                resume_data = self.processor.preprocess(
                    resume_text
                )

                # Extract Resume Sections
                resume_data["sections"] = self.section_parser.extract_sections(
                    resume_text
                )

                # Match Resume
                match_result = self.matcher.match(
                    jd_data,
                    resume_data
                )

                # AI Feedback
                feedback = self.llm.generate_feedback(
                    match_result
                )

                # Final Result
                results.append({

                    "Resume": file_name,

                    "Overall Score":
                        match_result["overall_score"],

                    "Skill Score":
                        match_result["skill_match_score"],
                    "matched_skill_count":
                        match_result["matched_skill_count"],

                    "total_skill_count":
                        match_result["total_skill_count"],

                    "Project Score":
                        match_result["project_score"],

                    "Education Score":
                        match_result["education_score"],

                    "Experience Score":
                        match_result["experience_score"],

                    "Similarity":
                        match_result["similarity_score"],

                    "Matched Skills":
                        ", ".join(
                            match_result["matched_skills"]
                        ),

                    "Missing Skills":
                        ", ".join(
                            match_result["missing_skills"]
                        ),

                    "Feedback":
                        feedback

                })

            except Exception as error:

                results.append({

                    "Resume": file_name,

                    "Overall Score": 0,

                    "Skill Score": 0,

                    "Project Score": 0,

                    "Education Score": 0,

                    "Experience Score": 0,

                    "Similarity": 0,

                    "Matched Skills": "",

                    "Missing Skills": "",

                    "Feedback": str(error)

                })

        results.sort(

            key=lambda x: x["Overall Score"],

            reverse=True

        )

        return results

    def export_results(
        self,
        results
    ):

        csv_path = self.exporter.export_csv(results)

        json_path = self.exporter.export_json(results)

        return csv_path, json_path