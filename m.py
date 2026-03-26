
import streamlit as st
from agents.controller import generate_sop
from docx import Document
import io
import PyPDF2

st.set_page_config(page_title="SOP Generator AI", layout="centered")

# Hide Streamlit default UI
st.markdown("""
    <style>
        /* Hide top toolbar completely */
        div[data-testid="stToolbar"] {
            display: none !important;
        }

        /* Hide profile icon / avatar */
        button[kind="header"] {
            display: none !important;
        }

        /* Hide hamburger menu */
        #MainMenu {
            display: none !important;
        }

        /* Hide footer */
        footer {
            display: none !important;
        }

        /* Hide header area */
        header {
            display: none !important;
        }
    </style>
""", unsafe_allow_html=True)

# HEADER
st.markdown("<h1 style='text-align: center;'>🎓 Yes Germany</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: grey;'>AI SOP Generator for Students</p>", unsafe_allow_html=True)

st.divider()

# FORM SECTION
student_name = st.text_input("Student Full Name")
course = st.text_input("Course Name")
university = st.text_input("University Name")

mode = st.selectbox("Writing Style", ["Formal"])

uploaded_file = st.file_uploader("Upload CV (PDF only)", type=["pdf"])

def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# GENERATE BUTTON
if st.button("🚀 Generate SOP"):

    if student_name and course and university and uploaded_file:

        with st.spinner("Reading CV..."):
            cv_text = extract_text_from_pdf(uploaded_file)

        with st.spinner("Generating SOP..."):
            sop = generate_sop(student_name, course, university, cv_text, mode)

        st.success("✅ SOP Generated Successfully")

        # OUTPUT BOX
        st.text_area("Your SOP", sop, height=300)

        # DOWNLOAD
        doc = Document()
        doc.add_paragraph(sop)

        buffer = io.BytesIO()
        doc.save(buffer)
        buffer.seek(0)

        st.download_button(
            label="📄 Download SOP",
            data=buffer,
            file_name="SOP.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )

    else:
        st.warning("⚠️ Please fill all fields and upload CV.")
