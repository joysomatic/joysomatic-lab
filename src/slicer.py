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
    start_padding_ms = 1500  # 1.5 seconds so we never miss the first word
    end_padding_ms = 1500
    min_duration_ms = 3000   # segments < 3 sec get expanded to capture full sentence

    for clip in topic_map['clips']:
        start_ms = clip['start'] * 1000
        end_ms = clip['end'] * 1000
        duration_ms = end_ms - start_ms

        # If segment < 3 sec, expand to capture the full sentence
        if duration_ms < min_duration_ms:
            expand = (min_duration_ms - duration_ms) / 2
            start_ms = max(0, start_ms - expand)
            end_ms = min(total_duration_ms, end_ms + expand)

        # Aggressive padding: 1.5s on start, ensure start never below 0
        start_ms = max(0, start_ms - start_padding_ms)
        end_ms = min(total_duration_ms, end_ms + end_padding_ms)

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