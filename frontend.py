import streamlit as st
import requests
import speech_recognition as sr

# Set Page Configuration
st.set_page_config(page_title="AI Translator", layout="centered")

# Title
st.title("🌍 AI-Based Language Translator")

# Subheader Below Title
st.subheader("Enter Text Below or Use Microphone 🎤")

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

        /* Change cursor to pointer when hovering over the dropdown */
        div[data-baseweb="select"] > div {
            cursor: pointer !important;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State
if "input_text" not in st.session_state:
    st.session_state.input_text = ""
if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""
if "speech_text" not in st.session_state:
    st.session_state.speech_text = ""  # Temporary storage for speech input

# Function to Capture Speech and Convert to Text
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙 Speak now...")
        try:
            audio = recognizer.listen(source, timeout=5)  # 5-second timeout
            text = recognizer.recognize_google(audio)  # Convert speech to text
            st.session_state.speech_text = text  # Store in temporary key
        except sr.UnknownValueError:
            st.error("❌ Could not understand the speech.")
        except sr.RequestError:
            st.error("❌ Speech service error.")

# **✅ Keep Only One st.text_area()**
text = st.text_area(
    "Enter text to translate:",
    value=st.session_state.speech_text if st.session_state.speech_text else st.session_state.input_text, 
    key="input_text"
)

# 🎤 Add Microphone Button
if st.button("🎙 Speak"):
    recognize_speech()
    st.rerun()  # ✅ Force UI refresh to update text area

# Callback Function to Clear Text
def clear_text():
    st.session_state.input_text = ""
    st.session_state.translated_text = ""
    st.session_state.speech_text = ""  # Also clear speech input

# Language Selection Dropdown (Below Text Area)
languages = {
    "English": "en",
    "Hindi": "hi",
    "French": "fr",
    "German": "de",
    "Russian": "ru",
    "Spanish": "es",
    "Chinese (Simplified)": "zh-cn",
    "Japanese": "ja",
    "Korean": "ko",
    "Italian": "it",
    "Portuguese": "pt",
    "Arabic": "ar",
    "Dutch": "nl",
    "Greek": "el",
    "Turkish": "tr",
    "Hebrew": "he",
    "Thai": "th",
    "Bengali": "bn",
    "Urdu": "ur",
    "Tamil": "ta"
}
target_language = st.selectbox("Select Target Language:", list(languages.keys()))

# Buttons
col1, col2, col3 = st.columns([1, 0.2, 1])

with col1:
    if st.button("Translate"):
        if text.strip():
            response = requests.post("http://127.0.0.1:8000/translate", json={"text": text, "target_language": languages[target_language]})
            if response.status_code == 200:
                st.session_state.translated_text = response.json().get("translated_text", "Translation failed")
            else:
                st.session_state.translated_text = "Error in translation."

with col3:
    st.button("Clear", on_click=clear_text)  # ✅ Properly clearing session state using a callback function

# Display Translated Text
if st.session_state.translated_text:
    st.write("### Translated Text:")
    st.success(st.session_state.translated_text)