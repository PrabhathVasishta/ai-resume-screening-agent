# app.py

import os
import shutil
import streamlit as st
import pandas as pd

from src.pipeline import ResumeScreeningPipeline
from src.parser import ResumeParser


st.set_page_config(
    page_title="AI Resume Screening Agent",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Resume Screening Agent")
st.markdown(
    "Upload **one Job Description** and **multiple resumes** for intelligent screening."
)

# -----------------------------
# Upload Files
# -----------------------------

jd_file = st.file_uploader(
    "Upload Job Description",
    type=["pdf", "docx", "txt"]
)

resume_files = st.file_uploader(
    "Upload Resumes",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True
)

# -----------------------------
# Start Screening
# -----------------------------

if st.button("Start Screening"):

    if jd_file is None:
        st.warning("Please upload a Job Description.")
        st.stop()

    if not resume_files:
        st.warning("Please upload at least one Resume.")
        st.stop()

    temp_folder = "temp"

    os.makedirs(temp_folder, exist_ok=True)

    try:

        # -------------------------
        # Save JD
        # -------------------------

        jd_path = os.path.join(
            temp_folder,
            jd_file.name
        )

        with open(jd_path, "wb") as file:
            file.write(jd_file.getbuffer())

        parser = ResumeParser()

        job_description = parser.extract_text(
            jd_path
        )

        # -------------------------
        # Save Resumes
        # -------------------------

        resume_folder = os.path.join(
            temp_folder,
            "resumes"
        )

        os.makedirs(
            resume_folder,
            exist_ok=True
        )

        for resume in resume_files:

            resume_path = os.path.join(
                resume_folder,
                resume.name
            )

            with open(resume_path, "wb") as file:

                file.write(
                    resume.getbuffer()
                )

        pipeline = ResumeScreeningPipeline()

        with st.spinner(
            "Analyzing resumes..."
        ):

            results = pipeline.process(
                job_description,
                resume_folder
            )

        if len(results) == 0:

            st.error(
                "No resumes were processed."
            )

            st.stop()

        dataframe = pd.DataFrame(results)
        average_score = round(
        dataframe["Overall Score"].mean(),
        2
        )

        best_candidate = dataframe.iloc[0]["Resume"]

        # -------------------------
        # Ranking
        # -------------------------

        dataframe.insert(
            0,
            "Rank",
            range(
                1,
                len(dataframe) + 1
            )
        )

        st.success(
            "Screening Completed Successfully!"
        )
        st.balloons()
        st.subheader("📊 Dashboard")

        c1, c2, c3 = st.columns(3)

        with c1:
                        st.metric(
                            "Total Candidates",
                            len(dataframe)
                        )

        with c2:
                        st.metric(
                            "Average Score",
                            f"{average_score}%"
                        )

        with c3:
                        st.metric(
                            "Best Candidate",
                            best_candidate
                        )

        st.divider()

        st.subheader(
            "🏆 Candidate Ranking"
        )

        st.dataframe(
            dataframe,
            use_container_width=True
        )

        # -------------------------
        # Candidate Details
        # -------------------------

        st.subheader(
            "Candidate Details"
        )

        for candidate in results:

                recommendation = "🔴 Not Recommended"

                if candidate["Overall Score"] >= 70:
                    recommendation = "🟢 Highly Recommended"

                elif candidate["Overall Score"] >= 50:
                    recommendation = "🟡 Recommended"

                elif candidate["Overall Score"] >= 30:
                    recommendation = "🟠 Consider"
                with st.expander(
                    f"{recommendation} | {candidate['Resume']}"
                ):

                    st.metric(
                        "Overall Score",
                        f"{candidate['Overall Score']}%"
                    )

                    st.progress(candidate["Overall Score"] / 100)

                    col1, col2, col3 = st.columns(3)

                    with col1:

                        st.metric(
                            "Skill Score",
                            f"{candidate['Skill Score']}%"
                        )

                        st.metric(
                            "Skills Matched",
                            f"{candidate['matched_skill_count']} / {candidate['total_skill_count']}"
                        )

                    with col2:

                        if candidate["Project Score"] > 0:

                            st.metric(
                                "Projects",
                                f"{candidate['Project Score']}%"
                            )

                        if candidate["Experience Score"] > 0:

                            st.metric(
                                "Experience",
                                f"{candidate['Experience Score']}%"
                            )

                    with col3:

                        st.metric(
                            "Similarity",
                            f"{candidate['Similarity']}%"
                        )

                    st.markdown("### ✅ Matched Skills")

                    skills = candidate["Matched Skills"].split(",")

                    for skill in skills:

                        if skill.strip():

                            st.success(skill.strip())

                    st.markdown("### ❌ Missing Skills")

                    skills = candidate["Missing Skills"].split(",")

                    for skill in skills:

                        if skill.strip():

                            st.error(skill.strip())

                    st.markdown("### 🤖 AI Feedback")

                    st.info(candidate["Feedback"])
        # -------------------------
        # Export
        # -------------------------

        csv_path, json_path = pipeline.export_results(
            results
        )

        col1, col2 = st.columns(2)

        with col1:

            with open(csv_path, "rb") as file:

                st.download_button(
                    "⬇ Download CSV",
                    file,
                    "screening_results.csv",
                    "text/csv"
                )

        with col2:

            with open(json_path, "rb") as file:

                st.download_button(
                    "⬇ Download JSON",
                    file,
                    "screening_results.json",
                    "application/json"
                )

    except Exception as error:

        st.error(error)

    finally:

        if os.path.exists(temp_folder):

            shutil.rmtree(temp_folder)