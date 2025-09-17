import streamlit as st
from pytubefix import YouTube
import os
import uuid

# Folder to store downloads
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

st.set_page_config(page_title="YouTube Video Downloader", layout="centered")

st.title("📥 YouTube Video Downloader")
st.markdown("Paste a YouTube link below and download the video.")

# User input
url = st.text_input("Enter YouTube Video URL")

if url:
    try:
        yt = YouTube(url)
        st.video(url)

        st.write(f"**Title:** {yt.title}")
        st.write(f"**Length:** {yt.length // 60} minutes")
        st.write(f"**Author:** {yt.author}")
        
        if st.button("Download Video"):
            st.info("Downloading video... Please wait.")

            # Filter for 720p mp4 (or best available)
            stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

            # Unique filename to avoid duplicates
            unique_filename = f"{uuid.uuid4()}.mp4"
            output_path = os.path.join(DOWNLOAD_FOLDER, unique_filename)

            stream.download(output_path=DOWNLOAD_FOLDER, filename=unique_filename)

            st.success("Download complete!")

            with open(output_path, "rb") as f:
                st.download_button(
                    label="📥 Click here to download the video",
                    data=f,
                    file_name=yt.title + ".mp4",
                    mime="video/mp4"
                )
    except Exception as e:
        st.error(f"Error: {e}")
