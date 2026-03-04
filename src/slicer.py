import os
from pydub import AudioSegment

def create_somatic_clips(audio_path, topic_map):
    """
    audio_path: Path to your raw mp3
    topic_map: The JSON list from processor.py (e.g., [{'title': '...', 'start': 0, 'end': 60, 'category': '...'}])
    """
    # Load the heavy audio file once into memory
    print(f"✂️ Loading audio for slicing: {audio_path}")
    full_audio = AudioSegment.from_file(audio_path)
    
    for clip in topic_map['clips']:
        # Pydub calculates in milliseconds
        start_ms = clip['start'] * 1000
        end_ms = clip['end'] * 1000
        
        # Extract the segment
        print(f"  → Cutting: {clip['title']} ({clip['category']})")
        segment = full_audio[start_ms:end_ms]
        
        # Create the category folder if it doesn't exist
        folder_path = f"library/{clip['category'].replace(' ', '_')}"
        os.makedirs(folder_path, exist_ok=True)
        
        # Save the file
        filename = f"{folder_path}/{clip['title'].replace(' ', '_')}.mp3"
        segment.export(filename, format="mp3")
        
    print("✅ Library update complete!")