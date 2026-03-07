import sys
try:
    import audioop
except ImportError:
    import audioop_lts as audioop
    sys.modules["audioop"] = audioop

import os
from pydub import AudioSegment

def create_somatic_clips(audio_path, topic_map):
    """
    audio_path: Path to your raw mp3
    topic_map: The JSON list from processor.py (e.g., [{'title': '...', 'start': 0, 'end': 60, 'category': '...'}])
    """
    # Load the heavy audio file once into memory
    print(f"   Loading audio for slicing: {audio_path}")
    full_audio = AudioSegment.from_file(audio_path)
    total_duration_ms = len(full_audio)
    padding_ms = 1000  # 1 second on each side so clips don't sound chopped

    for clip in topic_map['clips']:
        # Pydub uses milliseconds; pad start/end, ensure start never below 0
        start_ms = max(0, clip['start'] * 1000 - padding_ms)
        end_ms = min(total_duration_ms, clip['end'] * 1000 + padding_ms)

        # Extract the segment
        print(f"   → Cutting: {clip['title']} ({clip['category']})")
        segment = full_audio[start_ms:end_ms]
        
        # Create the category folder if it doesn't exist
        folder_path = f"library/{clip['category'].replace(' ', '_')}"
        os.makedirs(folder_path, exist_ok=True)
        
        # Save the file
        filename = f"{folder_path}/{clip['title'].replace(' ', '_')}.mp3"
        segment.export(filename, format="mp3")
        
    print("   Audio snippets saved to library/.")