import streamlit as st
import spacy
import PyPDF2
import io

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def analyze_resume(resume_text, job_description):
    # Process the resume and job description
    resume_doc = nlp(resume_text)
    job_doc = nlp(job_description)
    
    # Extract relevant information (this is a simple example, you might want to expand this)
    resume_skills = [token.text.lower() for token in resume_doc if token.pos_ == "NOUN"]
    job_skills = [token.text.lower() for token in job_doc if token.pos_ == "NOUN"]
    
    # Calculate match score (simple overlap for this example)
    matching_skills = set(resume_skills) & set(job_skills)
    score = len(matching_skills) / len(set(job_skills)) * 100
    
    # Determine missing skills
    missing_skills = set(job_skills) - matching_skills
    
    return score, list(matching_skills), list(missing_skills)

# Streamlit app
st.title("Resume Analyzer")

# Job description input
job_description = st.text_area("Enter the job description:")

# Resume upload
uploaded_file = st.file_uploader("Choose a resume PDF", type="pdf")

if uploaded_file is not None and job_description:
    # Extract text from PDF
    resume_text = extract_text_from_pdf(uploaded_file)
    
    # Analyze resume
    score, matching_skills, missing_skills = analyze_resume(resume_text, job_description)
    
    # Display results
    st.subheader("Analysis Results")
    st.write(f"Resume match score: {score:.2f}%")
    st.write("Matching skills:")
    st.write(", ".join(matching_skills))
    
    st.subheader("Skills to Add")
    st.write("These skills are mentioned in the job description but missing from the resume:")
    st.write(", ".join(missing_skills))

    # The following line has been removed:
    # st.subheader("Extracted Resume Text")
    # st.text(resume_text)
