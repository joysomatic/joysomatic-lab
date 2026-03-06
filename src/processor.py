import whisper
import ollama
import json
import re

def transcribe_and_map(audio_path):
    # 1. Local transcription (Whisper — runs entirely on your machine)
    print("   Transcribing with local Whisper...")
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    full_text = result["text"]
    segments = result.get("segments", [])

    # 2. Local wisdom extraction (Ollama Llama 3.2 — no API keys)
    print("   Extracting High-Signal Insights & Actionable Somatic Wisdom (Ollama)...")
    prompt = f"""Return ONLY a raw JSON object. No markdown, no explanation.

Keys (use these exactly):
- "Summary": one short paragraph summarizing the main message.
- "High_Signal_Insights": a list of strings — the most important ideas, principles, or realizations from the transcript. Focus on clarity and signal over noise.
- "Actionable_Somatic_Wisdom": a list of strings — concrete practices, prompts, or body-based actions a listener can do (breath, movement, reflection prompts). If the transcript has few, suggest 2–3 that fit the themes.

Rules:
- All three keys must be present. "High_Signal_Insights" and "Actionable_Somatic_Wisdom" must be arrays of strings.
- No conversational filler. Output only the JSON object.

Transcript (excerpt):
{full_text[:5000]}
"""

    response = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": prompt}])
    raw_content = response["message"]["content"].strip()

    try:
        json_match = re.search(r"(\{.*\})", raw_content, re.DOTALL)
        data = json.loads(json_match.group(1)) if json_match else json.loads(raw_content)
    except Exception as e:
        print(f"   ⚠️ Parse fallback: {e}")
        data = {
            "Summary": "Extraction incomplete.",
            "High_Signal_Insights": [],
            "Actionable_Somatic_Wisdom": ["Pause and re-read the transcript with curiosity."],
        }

    # Normalize keys for PDF (allow legacy or alternate names from model)
    if "Core_Insights" in data and "High_Signal_Insights" not in data:
        data["High_Signal_Insights"] = data.pop("Core_Insights", [])
    if "Exercises" in data and "Actionable_Somatic_Wisdom" not in data:
        data["Actionable_Somatic_Wisdom"] = data.pop("Exercises", [])

    # Build clips for the slicer from Whisper segments (timestamped)
    clips = []
    for i, seg in enumerate(segments[:20]):  # cap at 20 clips
        text = (seg.get("text") or "").strip()
        if not text or len(text) < 10:
            continue
        start = int(seg.get("start", 0))
        end = int(seg.get("end", start + 30))
        title = (text[:50] + "…") if len(text) > 50 else text
        title = re.sub(r"[^\w\s\-\.]", "", title).strip() or f"Segment_{i+1}"
        category = "High-Signal Insight" if i % 2 == 0 else "Somatic Wisdom"
        clips.append({"title": title, "start": start, "end": end, "category": category})
    data["clips"] = clips

    return data
