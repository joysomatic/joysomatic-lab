# Wisdom Synthesis Engine

A **professional, local-first tool for personal research**. Turn podcasts and long-form audio into structured insights and high-fidelity clips—without sending your data to the cloud.

---

## Data Sovereignty: 100% Local

Your audio and transcripts **never leave your machine**. The Wisdom Synthesis Engine is designed for **data sovereignty**:

- **No API keys** — no OpenAI, no cloud transcription, no external LLM calls.
- **Local transcription** — [Whisper](https://github.com/openai/whisper) runs on your CPU/GPU.
- **Local summarization** — [Ollama](https://ollama.ai) runs [Llama 3.2](https://ollama.com/library/llama3.2) on your machine.
- **Local outputs** — PDFs and audio snippets are written to `library/` on disk.

Everything runs in your environment. You own the pipeline and the data.

---

## Signal over Noise Pipeline

When you run the engine, it executes the full **Signal over Noise** workflow:

1. **Download** — Fetch audio from a YouTube URL (via `yt-dlp`).
2. **Transcribe** — Convert speech to text with local Whisper.
3. **Summarize** — Extract **High-Signal Insights** and **Actionable Somatic Wisdom** with local Ollama (Llama 3.2).
4. **PDF** — Generate a structured Wisdom Synthesis Engine report in `library/wisdom_pdfs/`.
5. **Snippets** — Slice the original audio into high-fidelity clips by segment and save them under `library/`.
6. **Cleanup** — Remove the temporary full-length audio file.

---

## Requirements

- **Python 3.x**
- **FFmpeg** (for audio conversion and slicing)
- **Ollama** with **Llama 3.2** pulled (`ollama pull llama3.2`)

Install Python dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

From the project root:

```bash
python main.py
```

Enter a YouTube URL when prompted. Outputs appear in:

- `library/wisdom_pdfs/Latest_Session.pdf` — structured summary and wisdom
- `library/High-Signal_Insight/` and `library/Somatic_Wisdom/` — audio clips

---

## Project Layout

- `main.py` — Entry point; runs the full Signal over Noise pipeline.
- `src/downloader.py` — Downloads audio from URLs.
- `src/processor.py` — Whisper transcription + Ollama extraction (High-Signal Insights, Actionable Somatic Wisdom) + clip list.
- `src/writer.py` — Builds the Wisdom Synthesis Engine PDF.
- `src/slicer.py` — Cuts audio into snippets from the segment map.

---

## Why Local-First?

- **Privacy** — Sensitive or personal content stays on your device.
- **Control** — No rate limits or dependency on third-party APIs.
- **Offline** — Once models are installed, you can run without internet (after download).
- **Cost** — No per-request or subscription fees for transcription or summarization.

The Wisdom Synthesis Engine is built for researchers, coaches, and anyone who wants to turn audio into actionable wisdom while keeping full control of their data.
