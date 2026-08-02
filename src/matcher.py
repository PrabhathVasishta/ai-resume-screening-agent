# src/matcher.py

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class ResumeMatcher:
    """
    Compare Resume with Job Description using
    Skills + Projects + Education + Experience + Text Similarity.
    """

    SKILL_WEIGHT = 0.40
    PROJECT_WEIGHT = 0.20
    EDUCATION_WEIGHT = 0.10
    EXPERIENCE_WEIGHT = 0.10
    TEXT_WEIGHT = 0.20

    def calculate_similarity(self, text1, text2):
        """
        Calculate cosine similarity using TF-IDF.
        """

        if not text1.strip() or not text2.strip():
            return 0.0

        vectorizer = TfidfVectorizer()

        matrix = vectorizer.fit_transform([text1, text2])

        similarity = cosine_similarity(
            matrix[0:1],
            matrix[1:2]
        )[0][0]

        return round(similarity * 100, 2)

    def skill_score(self, jd_skills, resume_skills):

        jd = {
            skill.lower().strip()
            for skill in jd_skills
            if skill.strip()
        }

        resume = {
            skill.lower().strip()
            for skill in resume_skills
            if skill.strip()
        }

        matched = sorted(jd.intersection(resume))

        missing = sorted(jd.difference(resume))

        total = len(jd)

        if total == 0:
            score = 0
        else:
            score = round((len(matched) / total) * 100, 2)

        return {
            "score": score,
            "matched": matched,
            "missing": missing,
            "matched_count": len(matched),
            "total_count": total
        }

    def section_score(self, jd_section, resume_section):
        """
        Compare individual sections using TF-IDF.
        """

        return self.calculate_similarity(
            jd_section,
            resume_section
        )

    def match(self, jd_data, resume_data):
        """
        Complete Resume Matching.
        """

        skill_result = self.skill_score(
                jd_data["skills"],
                resume_data["skills"]
            )

        skill_match_score = skill_result["score"]

        matched_skills = skill_result["matched"]

        missing_skills = skill_result["missing"]

        project_score = self.section_score(
            jd_data["sections"]["projects"],
            resume_data["sections"]["projects"]
        )

        education_score = self.section_score(
            jd_data["sections"]["education"],
            resume_data["sections"]["education"]
        )

        experience_score = self.section_score(
            jd_data["sections"]["experience"],
            resume_data["sections"]["experience"]
        )

        text_similarity = self.calculate_similarity(
            jd_data["cleaned_text"],
            resume_data["cleaned_text"]
        )

        overall_score = (

            skill_match_score * self.SKILL_WEIGHT +

            project_score * self.PROJECT_WEIGHT +

            education_score * self.EDUCATION_WEIGHT +

            experience_score * self.EXPERIENCE_WEIGHT +

            text_similarity * self.TEXT_WEIGHT

        )

        overall_score = round(overall_score, 2)

        return {

                "overall_score": overall_score,

                "skill_match_score": skill_match_score,

                "project_score": project_score,

                "education_score": education_score,

                "experience_score": experience_score,

                "similarity_score": text_similarity,

                "matched_skills": matched_skills,

                "missing_skills": missing_skills,

                "matched_skill_count": skill_result["matched_count"],

                "total_skill_count": skill_result["total_count"]

            }