import streamlit as st
import openai
import PyPDF2

# ---- SETUP ----
st.set_page_config(page_title="AI Resume Analyzer", layout="centered")
st.title("📄 AI Resume Analyzer with GPT")
st.write("Upload your resume (PDF), and let AI provide professional feedback!")

# ---- OPENAI API ----
# Replace this with your actual API key from https://platform.openai.com/account/api-keys
openai.api_key = "#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"

# ---- FUNCTIONS ----
def extract_text_from_pdf(uploaded_file):
    try:
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
        return text
    except Exception as e:
        st.error("❌ Error reading the PDF: " + str(e))
        return ""

def get_resume_feedback(resume_text):
    try:
        prompt = f"""
        You are an expert career coach. Analyze the following resume text and provide:
        - 3 strengths of the candidate
        - 3 areas for improvement
        - Suggestions to make the resume more attractive for AI/ML or GenAI jobs.

        Resume Text:
        {resume_text}
        """

        response = openai.ChatCompletion.create(
            model="gpt-4",  # You can also use "gpt-3.5-turbo" if GPT-4 is not available
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {e}"

# ---- FILE UPLOAD ----
uploaded_file = st.file_uploader("📤 Upload your resume PDF", type=["pdf"])

if uploaded_file:
    with st.spinner("⏳ Reading your resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)

    if resume_text:
        st.success("✅ Resume loaded successfully!")
        if st.button("🔍 Analyze with AI"):
            with st.spinner("🧠 Analyzing with GPT..."):
                feedback = get_resume_feedback(resume_text)
            st.subheader("📊 AI Feedback:")
            st.markdown(feedback)
    else:
        st.warning("⚠️ No text found in the uploaded PDF.")


            
