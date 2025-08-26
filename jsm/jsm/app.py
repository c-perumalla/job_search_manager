import streamlit as st
import requests
import os
from pathlib import Path
from datetime import datetime
import sys
sys.path.append("/Users/calvinperumalla/personal/git/job_search_manager/jsm")

# Import your custom function
# Assuming your function is in a module named my_library and is called fine_tune_resume
from tailor_resume_lib import fine_tune_resume  

# --- Settings ---
DOWNLOAD_DIR = "/Users/calvinperumalla/personal/git/job_search_manager/jsm/jsm/job_descriptions"
Path(DOWNLOAD_DIR).mkdir(exist_ok=True)  # Ensure download folder exists

# --- Streamlit UI ---
st.title("Resume Fine-Tuning Tool")

# Input: URL for HTML download
url = st.text_input("Enter a website URL to download HTML:")

if url:
    try:
        # Fetch HTML
        response = requests.get(url)
        response.raise_for_status()  # Raise error for bad responses

        # Save HTML to file
        fname = f"downloaded_page_{datetime.now().strftime("%Y%m%d_%H%M")}.html"
        job_description_filename = os.path.join(DOWNLOAD_DIR, fname)
        with open(job_description_filename, "w", encoding="utf-8") as f:
            f.write(response.text)

        st.success(f"HTML downloaded successfully to {job_description_filename}")
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to download HTML: {e}")

# Button: Fine Tune Resume
if st.button("Fine Tune Resume"):
    try:
        result = fine_tune_resume(job_description_filename, url)
        st.success("Fine-tune process completed!")
        st.write("Result:", result)
    except Exception as e:
        st.error(f"Error during fine-tuning: {e}")
