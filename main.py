from src.downloader import download_audio
from src.processor import transcribe_and_map
from src.writer import create_wisdom_pdf
from src.slicer import create_somatic_clips
import os

def run_pipeline(youtube_url):
    print("🚀 Wisdom Synthesis Engine — Signal over Noise pipeline")
    print("   (100% local: Whisper → Ollama Llama 3.2 → PDF + audio snippets)\n")

    # 1. Download audio
    print("--- 1. Downloading audio ---")
    audio_file = download_audio(youtube_url)

    # 2. Transcribe (local Whisper) + extract wisdom (local Ollama) + build clips
    print("\n--- 2. Transcribing & extracting wisdom (local) ---")
    wisdom_data = transcribe_and_map(audio_file)

    # 3. Generate structured PDF
    print("\n--- 3. Generating PDF ---")
    pdf_sections = {k: v for k, v in wisdom_data.items() if k != "clips"}
    create_wisdom_pdf("Session Insights", pdf_sections, "Latest_Session")

    # 4. Create high-fidelity audio snippets (slicer)
    if wisdom_data.get("clips"):
        print("\n--- 4. Creating audio snippets ---")
        create_somatic_clips(audio_file, wisdom_data)
    else:
        print("\n--- 4. No clips to slice (skipping) ---")

    # 5. Cleanup temporary audio
    if os.path.exists(audio_file):
        os.remove(audio_file)
        print("\n🧹 Temporary audio removed.")

    print("\n✅ Wisdom Synthesis Engine — pipeline complete.")
    print("   Check library/wisdom_pdfs/ and library/ for outputs.")


if __name__ == "__main__":
    url = input("Enter YouTube URL: ")
    run_pipeline(url)
