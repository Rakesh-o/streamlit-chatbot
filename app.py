import streamlit as st
import speech_recognition as sr
import pyttsx3
import time
from chat import get_response

# Initialize session state for chat history & recording status
if "history" not in st.session_state:
    st.session_state.history = []
if "listening" not in st.session_state:
    st.session_state.listening = False  # Track if the mic is active
if "query" not in st.session_state:
    st.session_state.query = ""  # Store current input

# Function for speech recognition with a stop button
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.session_state.listening = True  # Set listening to True
        st.info("🎤 Listening... Click 'Stop Listening' to cancel.")
        try:
            audio = recognizer.listen(source, timeout=10)  # Listen for 10 sec max
            text = recognizer.recognize_google(audio)
            st.session_state.listening = False  # Reset listening state
            return text
        except sr.UnknownValueError:
            st.warning("❌ Could not understand audio.")
        except sr.RequestError:
            st.warning("⚠️ Could not request results.")
        st.session_state.listening = False
        return ""

# Function for text-to-speech (TTS)
def speak(text):
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)
    engine.say(text)
    engine.runAndWait()

# Set page layout
st.set_page_config(layout="wide")
st.title("🤖 SKYAIT ChatBot")

# Chat interface
st.markdown("---")
st.subheader("💬 Chat History")

# Display chat history
for query, response in st.session_state.history:
    with st.chat_message("user"):
        st.markdown(f"**You:** {query}")
    with st.chat_message("assistant"):
        st.markdown(f"**Bot:** {response}")

# Input for new query (Stored in session state)
st.session_state.query = st.text_input("Ask something:", value=st.session_state.query, placeholder="Type your question here...")

# Buttons
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

with col1:
    if st.button("📩 Send"):
        if st.session_state.query:
            response = get_response(st.session_state.query)
            st.session_state.history.append((st.session_state.query, response))
            st.session_state.query = ""  # Clear input after sending
            st.rerun()  # Refresh UI

with col2:
    if st.button("🎤 Speak"):
        text = recognize_speech()
        if text:
            response = get_response(text)
            st.session_state.history.append((text, response))
            st.session_state.query = ""  # Clear input after voice input
            st.rerun()  # Refresh UI

with col3:
    if st.button("🔊 Speak Response"):
        if st.session_state.history:
            speak(st.session_state.history[-1][1])

with col4:
    if st.session_state.listening:
        if st.button("🛑 Stop Listening"):
            st.session_state.listening = False  # Stop listening
            st.rerun()  # Refresh UI
