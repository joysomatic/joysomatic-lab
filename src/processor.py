import whisper
import ollama
import json
import re

def transcribe_and_map(audio_path):
    # 1. Local Transcription (Whisper is free)
    print("👂 Transcribing audio (Local Whisper)...")
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    full_text = result['text']
    
    # 2. Local Wisdom Extraction (Local Llama 3.2)
    print("🧠 Extracting wisdom (Ollama)...")
    prompt = f"""
    Return ONLY a raw JSON object based on this transcript. 
    Keys: "Summary", "Core_Insights", "Exercises".
    
    Instructions:
    - If no exercises are found in the text, generate 3 "Somatic Integration Prompts".
    - "Core_Insights" and "Exercises" must be LISTS of strings.
    - No conversational filler. No ```json markdown.
    
    Transcript: {full_text[:5000]}
    """
    
    response = ollama.chat(model='llama3.2', messages=[{'role': 'user', 'content': prompt}])
    raw_content = response['message']['content'].strip()

    # Find the JSON block to prevent the "JSONDecodeError"
    try:
        json_match = re.search(r'(\{.*\})', raw_content, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(1))
        return json.loads(raw_content)
    except Exception as e:
        print(f"⚠️ Clean-up needed: {e}")
        return {"Summary": "Error", "Core_Insights": [], "Exercises": ["Take a deep breath and retry."]}