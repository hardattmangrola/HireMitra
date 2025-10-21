import streamlit as st
from src.helper import extract_text_from_pdf,ask_groq
from src.job_api import fetch_linkedin_jobs,fetch_naukri_jobs
st.set_page_config(page_title="Job Recommendation System", layout="wide")
st.title("AI Job Recommender")
st.markdown("Upload your resume and get personalized job recommendations on Linked and Naukri!")

uploaded_file=st.file_uploader("Upload your Resume(PDF)", type=["pdf"])
if uploaded_file:
    with st.spinner("Extracting text from resume..."):
        resume_text=extract_text_from_pdf(uploaded_file)
    with st.spinner("Summarizing your resume..."):
        summary=ask_groq(f"Summarize my resume highlighting skills,education and experience:\n{resume_text}",max_tokens=500)
    with st.spinner("Finding skill gaps..."):
        gaps=ask_groq(f"Analyze this resume and highlight missing skills,certifications and experiences needed for bettwer job opportunities:\n{resume_text}",max_tokens=400)

    with st.spinner("Creating Future Roadmap..."):
        roadmap=ask_groq(f"Based on this resume, suggest a future roadmap to improve this person career prospect:\n{resume_text}")
    # Display nicely formatted results
    st.markdown("---")
    st.header("📑 Resume Summary")
    st.markdown(f"<div style='background-color: #000000; padding: 15px; border-radius: 10px; font-size:16px; color:white;'>{summary}</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.header("🛠️ Skill Gaps & Missing Areas")
    st.markdown(f"<div style='background-color: #000000; padding: 15px; border-radius: 10px; font-size:16px; color:white;'>{gaps}</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.header("🚀 Future Roadmap & Preparation Strategy")
    st.markdown(f"<div style='background-color: #000000; padding: 15px; border-radius: 10px; font-size:16px; color:white;'>{roadmap}</div>", unsafe_allow_html=True)

    st.success("✅ Analysis Completed Successfully!")


    if st.button("🔎Get Job Recommendations"):
        with st.spinner("Fetching job recommendations..."):
            keywords = ask_groq(
                f"Based on this resume summary, suggest the best job titles and keywords for searching jobs. Give a comma-separated list only, no explanation.\n\nSummary: {summary}",
                max_tokens=100
            )

            search_keywords_clean = keywords.replace("\n", "").strip()

        st.success(f"Extracted Job Keywords: {search_keywords_clean}")

        with st.spinner("Fetching jobs from LinkedIn and Naukri..."):
            linkedin_jobs = fetch_linkedin_jobs(search_keywords_clean, rows=5)
            naukri_jobs = fetch_naukri_jobs(search_keywords_clean, rows=5)


        st.markdown("---")
        st.header("💼 Top 5 LinkedIn Jobs")

        if linkedin_jobs and len(linkedin_jobs) > 0:
            for i, job in enumerate(linkedin_jobs, 1):
                with st.container():
                    st.markdown(f"### {i}. {job.get('title', 'N/A')}")
                    st.markdown(f"**Company:** {job.get('companyName', 'N/A')}")
                    
                    # Handle location with fallback
                    location = job.get('location') or job.get('locationName') or 'Location not specified'
                    st.markdown(f"**📍 Location:** {location}")
                    
                    # Handle job link with fallback
                    job_link = job.get('link') or job.get('url') or job.get('jobUrl')
                    if job_link:
                        st.markdown(f"**🔗 [View Job]({job_link})**")
                    else:
                        st.markdown("**🔗 Link not available**")
                    
                    # Add job description if available
                    if job.get('description'):
                        with st.expander("View Job Description"):
                            st.markdown(job.get('description', 'No description available'))
                    
                    st.markdown("---")
        else:
            st.warning("No LinkedIn jobs found.")

        st.markdown("---")
        st.header("💼 Top 5 Naukri Jobs (India)")

        if naukri_jobs and len(naukri_jobs) > 0:
            for i, job in enumerate(naukri_jobs, 1):
                with st.container():
                    st.markdown(f"### {i}. {job.get('title', 'N/A')}")
                    st.markdown(f"**Company:** {job.get('companyName', 'N/A')}")
                    
                    # Handle location with fallback
                    location = job.get('location') or job.get('locationName') or 'Location not specified'
                    st.markdown(f"**📍 Location:** {location}")
                    
                    # Handle job link with fallback
                    job_link = job.get('url') or job.get('link') or job.get('jobUrl')
                    if job_link:
                        st.markdown(f"**🔗 [View Job]({job_link})**")
                    else:
                        st.markdown("**🔗 Link not available**")
                    
                    # Add job description if available
                    if job.get('description'):
                        with st.expander("View Job Description"):
                            st.markdown(job.get('description', 'No description available'))
                    
                    st.markdown("---")
        else:
            st.warning("No Naukri jobs found.")



