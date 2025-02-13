#!/bin/bash

# Install PortAudio for PyAudio
apt-get update && apt-get install -y portaudio19-dev

# Run the Streamlit app
streamlit run streamlit_app.py --server.port=$PORT
