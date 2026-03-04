import yt_dlp
import whisper
import os

def download_audio(link):
    print(f"--- 1. Ingesting Audio ---")
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'outtmpl': 'somatic_input.m4a',
        'overwrites': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])
    return "somatic_input.m4a"

def process_audio(filename):
    print(f"--- 2. Synthesizing Wisdom (This may take a minute) ---")
    model = whisper.load_model("base")
    
    # We ask for 'verbose' to get timestamps
    result = model.transcribe(filename)
    
    # Create the Summary with Timestamps
    with open("somatic_summary.txt", "w", encoding="utf-8") as f:
        f.write("JOYSOMATIC SUMMARY & TIMESTAMPS\n")
        f.write("="*30 + "\n\n")
        
        for segment in result['segments']:
            start = int(segment['start'])
            # Format seconds into MM:SS
            timestamp = f"{start // 60:02d}:{start % 60:02d}"
            f.write(f"[{timestamp}] {segment['text'].strip()}\n")
    
    print("--- 3. Transcription Complete ---")

def cleanup(filename):
    if os.path.exists(filename):
        os.remove(filename)
        print(f"--- 4. Lab Cleaned: {filename} deleted ---")

if __name__ == "__main__":
    url = input("Paste the Podcast/YouTube link here: ")
    audio_file = download_audio(url)
    process_audio(audio_file)
    cleanup(audio_file) # This fulfills your request to keep the Lab tidy!
    print("\nCheck 'somatic_summary.txt' on the left for your results.")