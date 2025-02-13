#!/bin/bash

# Install system dependencies for PyAudio
apt-get update && apt-get install -y portaudio19-dev pulseaudio alsa-utils

# Install Python dependencies
pip install --no-cache-dir -r requirements.txt

# Run the Streamlit app
streamlit run streamlit_app.py --server.port=$PORT
