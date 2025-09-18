import streamlit as st
import subprocess
import os
import uuid
from dotenv import load_dotenv

# Load environment variables if needed
load_dotenv()
PO_TOKEN = os.getenv("PO_TOKEN")
VISITOR_DATA = os.getenv("VISITOR_DATA")

# Folder setup
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

st.set_page_config(page_title="YouTube Video Downloader", layout="centered")
st.title("📥 YouTube Video Downloader")
st.markdown("Paste a YouTube link below and download the video.")

url = st.text_input("Enter YouTube Video URL")

if url:
    st.video(url)

    # Show video metadata (optional, using yt-dlp --dump-json)
    try:
        result = subprocess.run(
            ["yt-dlp", "--dump-json", url],
            capture_output=True, text=True, check=True
        )
        import json
        metadata = json.loads(result.stdout)

        st.write(f"**Title:** {metadata.get('title', 'Unknown')}")
        st.write(f"**Length:** {int(metadata.get('duration', 0)) // 60} minutes")
        st.write(f"**Author:** {metadata.get('uploader', 'Unknown')}")

        if st.button("Download Video"):
            st.info("Downloading video... Please wait.")
            unique_filename = f"{uuid.uuid4()}.mp4"
            output_path = os.path.join(DOWNLOAD_FOLDER, unique_filename)

            try:
                # Download the best mp4 format using yt-dlp
                subprocess.run([
                    "yt-dlp",
                    "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
                    "-o", output_path,
                    url
                ], check=True)

                st.success("Download complete!")

                with open(output_path, "rb") as f:
                    st.download_button(
                        label="📥 Click here to download the video",
                        data=f,
                        file_name=metadata.get('title', 'video') + ".mp4",
                        mime="video/mp4"
                    )

                # Optional: delete file after download button is shown
                # os.remove(output_path)

            except subprocess.CalledProcessError as e:
                st.error("❌ Download failed. Check the URL or try again later.")
                st.text(f"Error details:\n{e}")

    except subprocess.CalledProcessError as e:
        st.error("❌ Failed to fetch video metadata.")
        st.text(f"Error details:\n{e}")
