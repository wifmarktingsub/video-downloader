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

ydl_opts = {
    'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(webpage_url_basename)s.%(ext)s'),
    'format': 'bestvideo+bestaudio/best',
    'merge_output_format': 'mp4',
    'quiet': False,
    'noplaylist': True,
    'cookiefile': 'instagram_cookies.txt',  # <-- Add this line
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
