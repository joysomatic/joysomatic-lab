import whisper
import json
import re
import os

from llama_cpp import Llama


DEFAULT_GGUF_MODEL_PATH = "./models/llama-3.2-1b.gguf"


class WisdomProcessor:
    def __init__(
        self,
        model_path: str = DEFAULT_GGUF_MODEL_PATH,
        n_ctx: int = 4096,
        n_gpu_layers: int = -1,
        verbose: bool = False,
    ):
        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Missing local model file at '{model_path}'. "
                "Place your .gguf model under ./models/ (see README)."
            )
        self.llm = Llama(
            model_path=model_path,
            n_ctx=n_ctx,
            n_gpu_layers=n_gpu_layers,
            verbose=verbose,
        )

    def _rescue_bullets(self, raw_content: str) -> list:
        """When JSON fails, extract bullet-like lines from model output."""
        rescued = []
        bullet_start = re.compile(r"^(\s*[-*•]\s*|\s*\d+\.\s*)\s*")
        for line in raw_content.splitlines():
            line = line.strip()
            if not line or len(line) < 3:
                continue
            line = bullet_start.sub("", line).strip()
            if not line:
                continue
            # Remove markdown code fences or leading/trailing junk
            line = re.sub(r"^```\w*\s*", "", line).strip()
            line = re.sub(r"\s*```\s*$", "", line).strip()
            if line and line not in ("{", "}", "json"):
                rescued.append(line)
        return rescued[:50]  # cap for safety

    def generate_wisdom(self, transcript_text: str) -> dict:
        prompt = f"""Output ONLY a raw JSON object with two keys: "insights" and "somatic_wisdom", both containing lists of strings. Do not include any introductory text, markdown formatting, or explanations.

Transcript (excerpt):
{transcript_text[:5000]}
"""

        # llama.cpp local inference (no server, no API keys)
        result = self.llm.create_chat_completion(
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=2048,
        )
        raw_content = (
            (result.get("choices", [{}])[0].get("message", {}) or {}).get("content", "") or ""
        ).strip()

        data = None
        try:
            json_match = re.search(r"(\{.*\})", raw_content, re.DOTALL)
            blob = json_match.group(1) if json_match else raw_content
            data = json.loads(blob)
        except Exception as e:
            print(f"   ⚠️ JSON parse failed ({e}); rescuing bullet points from model output.")
            rescued = self._rescue_bullets(raw_content)
            data = {
                "Summary": "",
                "High_Signal_Insights": rescued if rescued else [],
                "Actionable_Somatic_Wisdom": [],
            }

        # Map strict keys to pipeline keys (insights -> High_Signal_Insights, somatic_wisdom -> Actionable_Somatic_Wisdom)
        if data is not None and isinstance(data, dict):
            if "insights" in data and isinstance(data["insights"], list):
                data["High_Signal_Insights"] = data.pop("insights", [])
            if "somatic_wisdom" in data and isinstance(data["somatic_wisdom"], list):
                data["Actionable_Somatic_Wisdom"] = data.pop("somatic_wisdom", [])
            # Tolerate legacy/alternate keys
            if "Core_Insights" in data and "High_Signal_Insights" not in data:
                data["High_Signal_Insights"] = data.pop("Core_Insights", [])
            if "Exercises" in data and "Actionable_Somatic_Wisdom" not in data:
                data["Actionable_Somatic_Wisdom"] = data.pop("Exercises", [])
            data.setdefault("Summary", data.get("Summary", ""))
            data.setdefault("High_Signal_Insights", [])
            data.setdefault("Actionable_Somatic_Wisdom", [])
        else:
            data = {"Summary": "", "High_Signal_Insights": [], "Actionable_Somatic_Wisdom": []}

        return data


def transcribe_and_map(audio_path):
    # 1. Local transcription (Whisper — runs entirely on your machine)
    print("   Transcribing with local Whisper...")
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    full_text = result["text"]
    segments = result.get("segments", [])

    # 2. Local wisdom extraction (llama-cpp-python, .gguf in ./models/)
    print("   Extracting High-Signal Insights & Actionable Somatic Wisdom (llama.cpp)...")
    processor = WisdomProcessor()
    data = processor.generate_wisdom(full_text)

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
