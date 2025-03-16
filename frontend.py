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

# Initialize Session State
if "webrtc_active" not in st.session_state:
    st.session_state.webrtc_active = False
if "webrtc_ctx" not in st.session_state:
    st.session_state.webrtc_ctx = None
if "speech_text" not in st.session_state:
    st.session_state.speech_text = ""

# 🎤 Define an Audio Processor Class
class AudioProcessor(AudioProcessorBase):
    def _init_(self):
        self.audio_frames = []

    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        """Receive an audio frame and store it."""
        self.audio_frames.append(frame.to_ndarray().tobytes())
        return frame  # Return unmodified

    def get_audio_data(self):
        """Return recorded audio as bytes."""
        return b"".join(self.audio_frames) if self.audio_frames else None

# 🎤 Speech Recognition Function
def recognize_speech():
    if not st.session_state.webrtc_active:
        st.session_state.webrtc_active = True  # ✅ Keep WebRTC Active

        # Start WebRTC Stream
        st.session_state.webrtc_ctx = webrtc_streamer(
            key="speech",
            mode=WebRtcMode.SENDONLY,
            audio_processor_factory=AudioProcessor,
            media_stream_constraints={"audio": True, "video": False},
        )

# 🎤 Stop Recording
def stop_recording():
    st.session_state.webrtc_active = False  # ✅ Stop WebRTC
    webrtc_ctx = st.session_state.webrtc_ctx

    if webrtc_ctx and webrtc_ctx.audio_processor:
        audio_processor = webrtc_ctx.audio_processor
        audio_data = audio_processor.get_audio_data()

        if audio_data:
            audio_path = "temp_audio.wav"
            with open(audio_path, "wb") as f:
                f.write(audio_data)

            # Recognize Speech
            recognizer = sr.Recognizer()
            with sr.AudioFile(audio_path) as source:
                audio = recognizer.record(source)

            try:
                text = recognizer.recognize_google(audio)
                st.session_state.speech_text = text
                st.success(f"Recognized: {text}")
            except sr.UnknownValueError:
                st.error("❌ Could not understand speech.")
            except sr.RequestError:
                st.error("❌ Speech recognition service unavailable.")

# 🎤 Show Start/Stop Buttons
if not st.session_state.webrtc_active:
    if st.button("🎙 Start Recording"):
        recognize_speech()
else:
    if st.button("🛑 Stop Recording"):
        stop_recording()

# ✅ Show Recognized Text
text = st.text_area(
    "Enter text to translate:",
    value=st.session_state.speech_text if st.session_state.speech_text else "",
    key="input_text"
)