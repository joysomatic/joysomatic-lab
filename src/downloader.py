import os
import yt_dlp

def download_audio(url):
    """Download audio from URL; returns path to local file (e.g. data/raw_audio.mp3)."""
    os.makedirs("data", exist_ok=True)
    options = {
        'format': 'bestaudio/best',
        'outtmpl': 'data/raw_audio.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])
    return "data/raw_audio.mp3"