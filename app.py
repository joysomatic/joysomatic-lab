import yt_dlp
import os

def download_audio(link):
    print(f"--- Starting JoySomatic Ingestion ---")
    
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
        }],
        'outtmpl': 'somatic_input.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])
    
    print(f"\nSuccess! 'somatic_input.m4a' is now in your Lab.")

if __name__ == "__main__":
    url = input("Paste the Podcast or YouTube link here: ")
    download_audio(url)