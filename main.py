from src.downloader import download_audio
from src.processor import transcribe_and_map
from src.writer import create_wisdom_pdf
import os

def run_lab(youtube_url):
    print("🚀 Starting JoySomatic Lab...")
    
    # 1. Download
    audio_file = download_audio(youtube_url)
    
    # 2. Process (Transcription + Wisdom)
    wisdom_data = transcribe_and_map(audio_file)
    
    # 3. Create PDF
    create_wisdom_pdf("Somatic Session Insights", wisdom_data, "Latest_Session")
    
    # 4. Cleanup
    if os.path.exists(audio_file):
        os.remove(audio_file)
        print("🧹 Cleaned up temporary audio.")

if __name__ == "__main__":
    url = input("Enter YouTube URL: ")
    run_lab(url)