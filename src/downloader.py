import yt_dlp

def download_audio(url):
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