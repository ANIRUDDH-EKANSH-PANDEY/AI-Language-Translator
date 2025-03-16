import streamlit as st
import requests
import av
import numpy as np
import speech_recognition as sr
from streamlit_webrtc import webrtc_streamer, WebRtcMode, AudioProcessorBase

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
    </style>
""", unsafe_allow_html=True)

# Initialize Session State
if "webrtc_ctx" not in st.session_state:
    st.session_state.webrtc_ctx = None
if "input_text" not in st.session_state:
    st.session_state.input_text = ""
if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""
if "speech_text" not in st.session_state:
    st.session_state.speech_text = ""
if "audio_frames" not in st.session_state:
    st.session_state.audio_frames = []  # Store audio frames

# 🎤 Define an Audio Processor Class
class AudioProcessor(AudioProcessorBase):
    def _init_(self):
        self.audio_frames = []  # Initialize empty buffer

    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        """Receive and store an audio frame."""
        audio_data = frame.to_ndarray().tobytes()
        self.audio_frames.append(audio_data)  # Store audio frames
        return frame  # Pass through unmodified

    def get_audio_data(self):
        """Return recorded audio as bytes."""
        return b"".join(self.audio_frames) if self.audio_frames else None

# 🎤 Speech Recognition Function
def recognize_speech():
    st.info("🎙 Click 'Start' and speak...")

    # Start WebRTC Stream
    if "webrtc_ctx" not in st.session_state or st.session_state.webrtc_ctx is None:
        st.session_state.webrtc_ctx = webrtc_streamer(
            key="speech",
            mode=WebRtcMode.SENDONLY,
            audio_processor_factory=AudioProcessor,
            media_stream_constraints={"audio": True, "video": False},
        )

    webrtc_ctx = st.session_state.webrtc_ctx  # Retrieve session

    if webrtc_ctx.audio_processor:
        audio_processor = webrtc_ctx.audio_processor

        # Wait for speech input
        st.info("🔊 Capturing audio... Speak now.")
        import time
        time.sleep(3)  # Wait for 3 seconds

        audio_data = audio_processor.get_audio_data()
        if not audio_data:
            st.error("❌ No valid audio recorded.")
            return

        # Save to temporary WAV file
        audio_path = "temp_audio.wav"
        with open(audio_path, "wb") as f:
            f.write(audio_data)

        # Recognize Speech
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_path) as source:
            audio = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio)
            st.session_state.speech_text = text  # Store recognized text
            st.success(f"Recognized: {text}")
        except sr.UnknownValueError:
            st.error("❌ Could not understand speech.")
        except sr.RequestError:
            st.error("❌ Speech recognition service unavailable.")

# ✅ Only One st.text_area()
text = st.text_area(
    "Enter text to translate:",
    value=st.session_state.speech_text if st.session_state.speech_text else st.session_state.input_text,
    key="input_text"
)

# 🎤 "Start Recording" Button (Keeps WebRTC Active)
if st.button("🎙 Start Recording"):
    recognize_speech()

# Callback to Clear Text
def clear_text():
    st.session_state.input_text = ""
    st.session_state.translated_text = ""
    st.session_state.speech_text = ""

# 🌍 Language Selection Dropdown
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
            response = requests.post("https://ai-language-translator.onrender.com/translate", json={"text": text, "target_language": languages[target_language]})
            if response.status_code == 200:
                st.session_state.translated_text = response.json().get("translated_text", "Translation failed")
            else:
                st.session_state.translated_text = "Error in translation."

with col3:
    st.button("Clear", on_click=clear_text)

# Display Translated Text
if st.session_state.translated_text:
    st.write("### Translated Text:")
    st.success(st.session_state.translated_text)