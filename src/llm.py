# src/llm.py

from openai import OpenAI
from config import Config


class LLMReviewer:
    """
    Generates recruiter feedback.
    Falls back to rule-based feedback if no API key is available.
    """

    def __init__(self):

        if Config.API_KEY:
            self.client = OpenAI(
                api_key=Config.API_KEY,
                base_url=Config.BASE_URL
            )
        else:
            self.client = None

    def _recommendation(self, score):

        if score >= 85:
            return "Accept"

        elif score >= 65:
            return "Consider"

        return "Reject"

    def _fallback_feedback(self, match_result):

        recommendation = self._recommendation(
            match_result["overall_score"]
        )

        matched = (
            ", ".join(match_result["matched_skills"])
            if match_result["matched_skills"]
            else "None"
        )

        missing = (
            ", ".join(match_result["missing_skills"])
            if match_result["missing_skills"]
            else "None"
        )

        return f"""
SUMMARY
Overall Resume Score : {match_result['overall_score']}%

SECTION SCORES

Skills : {match_result['skill_match_score']}%

Projects : {match_result['project_score']}%

Education : {match_result['education_score']}%

Experience : {match_result['experience_score']}%

Similarity : {match_result['similarity_score']}%

MATCHED SKILLS

{matched}

MISSING SKILLS

{missing}

FINAL RECOMMENDATION

{recommendation}
"""

    def generate_feedback(self, match_result):

        if self.client is None:
            return self._fallback_feedback(match_result)

        prompt = f"""
You are an experienced Technical Recruiter.

Analyze the candidate using the scores below.

Overall Score:
{match_result['overall_score']}%

Skill Match:
{match_result['skill_match_score']}%

Project Match:
{match_result['project_score']}%

Education Match:
{match_result['education_score']}%

Experience Match:
{match_result['experience_score']}%

Resume Similarity:
{match_result['similarity_score']}%

Matched Skills:
{", ".join(match_result["matched_skills"])}

Missing Skills:
{", ".join(match_result["missing_skills"])}

Return exactly this format.

Summary

Strengths

Weaknesses

Recommendation

Reason

Suggested Learning Path
"""

        try:

            response = self.client.chat.completions.create(

                model=Config.MODEL_NAME,

                messages=[

                    {
                        "role": "system",
                        "content": "You are a Senior Technical Recruiter."
                    },

                    {
                        "role": "user",
                        "content": prompt
                    }

                ],

                temperature=Config.TEMPERATURE

            )

            return response.choices[0].message.content.strip()

        except Exception:

            return self._fallback_feedback(match_result)