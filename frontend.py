import streamlit as st
import requests
import os
from io import BytesIO
from PyPDF2 import PdfReader
from docx import Document

# Set Page Configuration
st.set_page_config(page_title="AI Translator", layout="centered")

# Title
st.title("🌍 AI-Based Language Translator")

# Subheader Below Title
st.subheader("Enter Text or Upload a File for Translation 📄")

# Custom CSS for Styling
st.markdown("""
    <style>
        .stTextArea textarea {
            background-color: black !important;
            color: white !important;
            font-size: 16px !important;
            border-radius: 8px !important;
            padding: 10px !important;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State
if "input_text" not in st.session_state:
    st.session_state.input_text = ""
if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""
if "uploaded_filename" not in st.session_state:
    st.session_state.uploaded_filename = ""

# ✅ *Text Area for Manual Input*
text = st.text_area(
    "Enter text to translate:",
    value=st.session_state.input_text,
    key="input_text"
)

# ✅ *File Upload for Text Extraction*
uploaded_file = st.file_uploader("Upload a file (TXT, PDF, DOCX)", type=["txt", "pdf", "docx"])

# 📄 *Extract Text from Uploaded File*
if uploaded_file:
    file_ext = uploaded_file.name.split(".")[-1]
    extracted_text = ""

    if file_ext == "txt":
        extracted_text = uploaded_file.getvalue().decode("utf-8")
    elif file_ext == "pdf":
        pdf_reader = PdfReader(uploaded_file)
        extracted_text = "\n".join(page.extract_text() for page in pdf_reader.pages if page.extract_text())
    elif file_ext == "docx":
        doc = Document(uploaded_file)
        extracted_text = "\n".join(para.text for para in doc.paragraphs)

    # Store extracted text in session state
    st.session_state.input_text = extracted_text

    # Show extracted text in text area
    st.text_area("Extracted Text:", value=extracted_text, height=200, key="extracted_text", disabled=True)

# 🌍 *Language Selection Dropdown*
languages = {
    "English": "en", "Hindi": "hi", "French": "fr", "German": "de",
    "Russian": "ru", "Spanish": "es", "Chinese (Simplified)": "zh-cn",
    "Japanese": "ja", "Korean": "ko", "Italian": "it", "Portuguese": "pt",
    "Arabic": "ar", "Dutch": "nl", "Greek": "el", "Turkish": "tr",
    "Hebrew": "he", "Thai": "th", "Bengali": "bn", "Urdu": "ur", "Tamil": "ta"
}
target_language = st.selectbox("Select Target Language:", list(languages.keys()))

# 🎯 *Translate Button*
if st.button("Translate"):
    if st.session_state.input_text.strip():
        response = requests.post("https://ai-language-translator.onrender.com/translate",
                                 json={"text": st.session_state.input_text, "target_language": languages[target_language]})
        if response.status_code == 200:
            st.session_state.translated_text = response.json().get("translated_text", "Translation failed")
        else:
            st.session_state.translated_text = "Error in translation."

# ✅ *Show Translated Text*
if st.session_state.translated_text:
    st.write("### Translated Text:")
    st.success(st.session_state.translated_text)

    # 📝 *Download Translated File*
    file_format = uploaded_file.name.split(".")[-1] if uploaded_file else "txt"
    translated_filename = f"translated.{file_format}"

    if file_format == "txt":
        translated_bytes = st.session_state.translated_text.encode("utf-8")
    elif file_format == "docx":
        translated_doc = BytesIO()
        doc = Document()
        doc.add_paragraph(st.session_state.translated_text)
        doc.save(translated_doc)
        translated_doc.seek(0)
        translated_bytes = translated_doc.read()
    elif file_format == "pdf":
        translated_bytes = st.session_state.translated_text.encode("utf-8")  # Simple text-based PDF handling

    st.download_button(
        label="📥 Download Translated File",
        data=translated_bytes,
        file_name=translated_filename,
        mime="text/plain" if file_format == "txt" else "application/octet-stream"
    )

# 🔄 *Clear Button*
def clear_text():
    st.session_state.input_text = ""
    st.session_state.translated_text = ""
    st.session_state.uploaded_filename = ""

st.button("Clear", on_click=clear_text)