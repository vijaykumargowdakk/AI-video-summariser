import streamlit as st
import os
import time
import tempfile
from pathlib import Path
import google.generativeai as genai

# Detect if running in Google Colab
try:
    from google.colab import drive
    IN_COLAB = True
except ImportError:
    IN_COLAB = False

# Set API Key
if IN_COLAB:
    API_KEY = "Paste_your_google_api_key"  # Replace with a valid API key
else:
    from dotenv import load_dotenv
    load_dotenv()
    API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure API Key
if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    st.error("API key not found. Please set it manually in Colab or in a .env file locally.")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="Multimodal AI Agent - Video Summarizer",
    page_icon="🎥",
    layout="wide"
)

st.title("Phidata Video AI Summarizer Agent 🎥🎤🖬")
st.header("Powered by Gemini 2.0 Flash Exp")

# File uploader
video_file = st.file_uploader("Upload a video file", type=['mp4', 'mov', 'avi'])

if video_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video:
        temp_video.write(video_file.read())
        video_path = temp_video.name

    st.video(video_path)

    user_query = st.text_area("What insights are you seeking from the video?")

    if st.button("🔍 Analyze Video"):
        if not user_query:
            st.warning("Please enter a question or insight to analyze the video.")
        else:
            try:
                with st.spinner("Processing video and gathering insights..."):
                    model = genai.GenerativeModel("gemini-1.0-pro")
                    response = model.generate_content(user_query)
                
                st.subheader("Analysis Result")
                st.markdown(response.text)
            except Exception as error:
                st.error(f"An error occurred during analysis: {error}")
            finally:
                Path(video_path).unlink(missing_ok=True)
else:
    st.info("Upload a video file to begin analysis.")
