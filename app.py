import yt_dlp
import whisper # This is the new AI Ear!

def download_audio(link):
    print(f"--- Starting JoySomatic Ingestion ---")
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'outtmpl': 'somatic_input.m4a',
        'overwrites': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])

def transcribe_audio():
    print("\n--- AI is now listening to your somatic input ---")
    model = whisper.load_model("base") # "base" is fast and good for most podcasts
    result = model.transcribe("somatic_input.m4a")
    
    # Save the text so we can read it
    with open("transcription.txt", "w") as f:
        f.write(result["text"])
    
    print("Success! Read 'transcription.txt' in your sidebar to see what was said.")

if __name__ == "__main__":
    url = input("Paste the link here: ")
    download_audio(url)
    transcribe_audio()