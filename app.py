<<<<<<< HEAD
import streamlit as st
from pytubefix import YouTube
import os
import uuid
import logging
logging.basicConfig(level=logging.DEBUG)

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

        try:
            # Get highest resolution progressive stream (video + audio)
            stream = yt.streams.filter(progressive=True, file_extension='mp4')\
                            .order_by('resolution').desc().first()

            if not stream:
                st.error("No compatible video streams found.")
            else:
                # Proceed with downloading
                ...
        except Exception as e:
            st.error(f"Stream selection error: {e}")


    except Exception as e:
        st.error(f"Error: {e}")
=======
from flask import Flask, render_template, request, send_from_directory, flash
import yt_dlp
import os
import time
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# Output folder
DOWNLOAD_FOLDER = os.path.join('static', 'downloads')
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
    
# Updated path
cookie_path = os.path.abspath(os.path.join('static', 'instagram_cookies.txt'))
print(f"Using cookie file at: {cookie_path}")

# DEBUG: Check if file exists
if not os.path.exists(cookie_path):
    print("❌ Cookie file not found at:", cookie_path)
else:
    print("✅ Cookie file found:", cookie_path)


ydl_opts = {
    'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(webpage_url_basename)s.%(ext)s'),
    'format': 'bestvideo+bestaudio/best',
    'merge_output_format': 'mp4',
    'quiet': False,
    'verbose': True,  # Add this
    'noplaylist': True,
    'cookiefile': cookie_path,
}


@app.route('/', methods=['GET', 'POST'])
def index():
    download_link = None
    if request.method == 'POST':
        url = request.form.get('url', '').strip()
        if not url:
            flash('❌ Please enter a valid URL.')
            return render_template('index.html')

        try:
            # yt-dlp options
            ydl_opts = {
                'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(webpage_url_basename)s.%(ext)s'),
                'format': 'bestvideo+bestaudio/best',
                'merge_output_format': 'mp4',
                'quiet': False,
                'noplaylist': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                filename = os.path.basename(filename)
                download_link = f'/static/downloads/{filename}'

            flash('✅ Download successful!')
        except Exception as e:
            flash(f'❌ Failed to download: {str(e)}')

    return render_template('index.html', download_link=download_link)

if __name__ == '__main__':
    app.run(debug=True)
>>>>>>> origin/yt
