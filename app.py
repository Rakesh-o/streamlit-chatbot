from gtts import gTTS
import streamlit as st
import base64
import speech_recognition as sr
from chat import get_response  # Ensure chat.py is correct!

# Initialize session state for chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Function for speech recognition
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            st.warning("Could not understand audio.")
        except sr.RequestError:
            st.warning("Could not request results.")
        return ""

# Function for text-to-speech (TTS)
def speak(text):
    if not text.strip():  # Prevent empty speech
        st.warning("No text to convert to speech.")
        return
    
    tts = gTTS(text=text, lang="en")
    tts.save("output.mp3")

    # Convert to base64 for Streamlit playback
    with open("output.mp3", "rb") as file:
        audio_bytes = file.read()
    
    st.audio(audio_bytes, format="audio/mp3")

# Set page layout
st.set_page_config(layout="wide")
st.title("🤖 SKYAIT ChatBot")

# Chat interface
st.markdown("---")
st.subheader("💬 Chat")

chat_container = st.container()

# Display chat history
with chat_container:
    for query, response in st.session_state.history:
        with st.chat_message("user"):
            st.markdown(f"**You:** {query}")

        with st.chat_message("assistant"):
            st.markdown(f"**Bot:** {response}")

# Input for new query
new_query = st.text_input("Ask something:", key="input")

# Buttons
col1, col2, col3 = st.columns([1, 1, 1])

# Button to send text input
with col1:
    if st.button("📩 Send", key="send"):
        if new_query.strip():  # Ensure input is not empty
            response = get_response(new_query)
            if response:
                st.session_state.history.append((new_query, response))
                print(f"User: {new_query}, Bot: {response}")  # Debugging
                st.rerun()
            else:
                st.warning("No response received from chatbot.")
        else:
            st.warning("Please enter a valid query.")

# Button for voice input
with col2:
    if st.button("🎤 Speak", key="voice"):
        spoken_query = recognize_speech()
        if spoken_query.strip():  # Ensure input is valid
            response = get_response(spoken_query)
            if response:
                st.session_state.history.append((spoken_query, response))
                print(f"User: {spoken_query}, Bot: {response}")  # Debugging
                st.rerun()
            else:
                st.warning("No response received from chatbot.")
        else:
            st.warning("Could not recognize speech.")

# Button to speak the last response
with col3:
    if st.button("🔊 Speak Response", key="speak"):
        if st.session_state.history:
            speak(st.session_state.history[-1][1])
        else:
            st.warning("No response to speak.")

# Debugging: Show chat history in UI
st.write("Chat History:", st.session_state.history)
