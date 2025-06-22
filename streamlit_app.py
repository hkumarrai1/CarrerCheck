import streamlit as st
from file_parser import extract_text
from keyword_matcher import extract_keywords, calculate_overlap
from semantic_matcher import compute_semantic_similarity
import difflib
import pyperclip
import os
from advanced_section_extractor import extract_skills_nlp, extract_education_nlp, extract_experience_nlp
from streamlit_option_menu import option_menu
import glob
import time

# --- Modern UI Layout ---

st.set_page_config(page_title="Resume ATS Checker", page_icon=":mag_right:", layout="wide")

# Sidebar with navigation and info
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/resume.png", width=80)
    st.title("ATS Resume Checker")
    st.markdown("""
    **Instructions:**
    1. Upload your resume and job description.
    2. Use the tabs to edit, compare, and get suggestions.
    3. For OCR, install Tesseract (see link below).
    """)
    st.markdown(
        '🔗 <b>Download Tesseract OCR:</b> '
        '<a href="https://github.com/UB-Mannheim/tesseract/wiki" target="_blank">Windows</a> | '
        '<a href="https://github.com/tesseract-ocr/tesseract/releases" target="_blank">All Platforms</a>',
        unsafe_allow_html=True
    )
    st.markdown('---')
    st.info('Made with ❤️ using Streamlit')

# --- Auto-cleanup uploaded files older than 30 minutes ---
def cleanup_old_uploads(patterns=["uploaded_resume_*", "uploaded_jd_*"]):
    now = time.time()
    for pattern in patterns:
        for file in glob.glob(pattern):
            try:
                if os.path.isfile(file):
                    mtime = os.path.getmtime(file)
                    if now - mtime > 1800:  # 1800 seconds = 30 minutes
                        os.remove(file)
            except Exception:
                pass
cleanup_old_uploads()

# Main UI with tabs
selected = option_menu(
    menu_title=None,
    options=["Resume", "Job Description", "Results"],
    icons=["file-earmark-person", "file-earmark-text", "bar-chart"],
    orientation="horizontal"
)

if selected == "Resume":
    st.header("Upload & Edit Resume")
    resume_file = st.file_uploader("Upload your resume (PDF, DOCX, or TXT)", type=["pdf", "docx", "txt"], key="resume_upload")
    resume_text = None
    if resume_file:
        resume_filename = resume_file.name
        resume_path = f"uploaded_resume_{resume_filename}"
        with open(resume_path, "wb") as f:
            f.write(resume_file.read())
        try:
            resume_text = extract_text(resume_path)
        except Exception as e:
            st.error(f"Could not extract text from resume: {e}")
    resume_editor_text = st.text_area(
        "Edit your resume here (or start from uploaded file):",
        value=resume_text if resume_text else "",
        height=300,
        key="resume_editor_tab"
    )
    st.session_state["resume_editor_text"] = resume_editor_text

elif selected == "Job Description":
    st.header("Provide Job Description")
    jd_file = st.file_uploader("Upload the job description (PDF, DOCX, or TXT)", type=["pdf", "docx", "txt"], key="jd_upload")
    jd_clipboard = st.button("Paste Job Description from Clipboard", key="jd_clipboard_btn")
    jd_clipboard_text = None
    if jd_clipboard:
        try:
            jd_clipboard_text = pyperclip.paste()
            st.success("Job description pasted from clipboard!")
        except Exception as e:
            st.error(f"Clipboard error: {e}")
    jd_manual = st.text_area("Or paste/type the job description here:", key="jd_manual_tab")
    jd_screen = st.button("Capture Job Description from Screen (screenshot + OCR)", key="jd_screen_btn")
    jd_screen_text = None
    if jd_screen:
        import platform
        import sys
        running_on_cloud = False
        if "STREMLIT_SERVER_HEADLESS" in os.environ or "SPACE_ID" in os.environ:
            running_on_cloud = True
        if running_on_cloud:
            st.error("OCR screenshot feature is not supported on this platform. To use this feature, please run the app locally.\n\nYou can download and run the full app from GitHub: [https://github.com/yourusername/resume-ats-checker](https://github.com/yourusername/resume-ats-checker)")
            st.stop()
        # --- Move these imports here ---
        import pyautogui
        from PIL import Image
        import pytesseract
        # ---
        st.info("After clicking OK, select the region of your screen with the job description.")
        st.warning("Make sure this Streamlit window is not covering the job description!")
        st.write("You have 3 seconds to switch to the target window.")
        import time
        time.sleep(3)
        screenshot = pyautogui.screenshot()
        st.image(screenshot, caption="Full screenshot. Please crop manually if needed.")
        screenshot_path = "jd_screenshot.png"
        screenshot.save(screenshot_path)
        try:
            jd_screen_text = pytesseract.image_to_string(Image.open(screenshot_path))
            st.success("Text extracted from screenshot!")
            st.text_area("Extracted Job Description (editable)", value=jd_screen_text, key="ocr_jd_tab")
        except Exception as e:
            st.error(f"OCR error: {e}")
        os.remove(screenshot_path)
    # Save job description text in session state for Results tab
    job_desc_text = None
    if jd_file:
        jd_filename = jd_file.name
        jd_path = f"uploaded_jd_{jd_filename}"
        with open(jd_path, "wb") as f:
            f.write(jd_file.read())
        try:
            job_desc_text = extract_text(jd_path)
        except Exception as e:
            st.error(f"Could not extract text from job description: {e}")
    elif jd_clipboard_text:
        job_desc_text = jd_clipboard_text
    elif jd_screen_text:
        job_desc_text = jd_screen_text
    elif jd_manual.strip():
        job_desc_text = jd_manual
    st.session_state["job_desc_text"] = job_desc_text

elif selected == "Results":
    st.header("ATS Match Results & Suggestions")
    resume_editor_text = st.session_state.get("resume_editor_text", "")
    job_desc_text = st.session_state.get("job_desc_text", "")
    if resume_editor_text and job_desc_text:
        resume_keywords = extract_keywords(resume_editor_text)
        jd_keywords = extract_keywords(job_desc_text)
        num_matched, total_jd, score, missing = calculate_overlap(resume_keywords, jd_keywords)
        st.write(f"**Match score:** {score*100:.1f}%")
        st.write(f"**Missing keywords:** {', '.join(sorted(missing)) if missing else 'None!'}")
        if missing:
            st.write("\n**Suggestions to improve your resume:**")
            st.write("- Add these missing keywords/skills from the job description:")
            for kw in sorted(missing):
                st.write(f"  - {kw}")
            similar = suggest_similar_keywords(missing, resume_keywords)
            if similar:
                st.write("\nYou have similar words in your resume for some missing keywords:")
                for kw, matches in similar.items():
                    st.write(f"  - {kw}: similar in your resume -> {', '.join(matches)}")
        semantic_score = compute_semantic_similarity(resume_editor_text, job_desc_text)
        st.write(f"\n**Semantic similarity score:** {semantic_score:.2f}")
        st.subheader("Extracted Resume Sections (NLP)")
        skills = extract_skills_nlp(resume_editor_text)
        education = extract_education_nlp(resume_editor_text)
        experience = extract_experience_nlp(resume_editor_text)
        st.write(f"**Skills (NLP):** {', '.join(skills) if skills else 'None found'}")
        st.write(f"**Education Entities (NLP):** {', '.join(education) if education else 'None found'}")
        st.write("**Experience Sentences (NLP):**")
        if experience:
            for sent in experience:
                st.write(f"- {sent}")
        else:
            st.write("None found")
    else:
        st.info("Please upload your resume and provide a job description (file, clipboard, screenshot, or text box) in the previous tabs to begin.")
