# Wisdom Synthesis Engine

A **professional, local-first tool for personal research**. Turn podcasts and long-form audio into structured insights and high-fidelity clips—without sending your data to the cloud.

---

## Data Sovereignty: 100% Local

Your audio and transcripts **never leave your machine**. The Wisdom Synthesis Engine is designed for **data sovereignty**:

- **No API keys** — no OpenAI, no cloud transcription, no external LLM calls.
- **Local transcription** — [Whisper](https://github.com/openai/whisper) runs on your CPU/GPU.
- **Local summarization** — `llama-cpp-python` runs a local `.gguf` model (llama.cpp) on your machine.
- **Local outputs** — PDFs and audio snippets are written to `library/` on disk.

Everything runs in your environment. You own the pipeline and the data.

---

## Signal over Noise Pipeline

When you run the engine, it executes the full **Signal over Noise** workflow:

1. **Download** — Fetch audio from a YouTube URL (via `yt-dlp`).
2. **Transcribe** — Convert speech to text with local Whisper.
3. **Summarize** — Extract **High-Signal Insights** and **Actionable Somatic Wisdom** with local llama.cpp (`llama-cpp-python`) using a `.gguf` model in `models/`.
4. **PDF** — Generate a structured Wisdom Synthesis Engine report in `library/wisdom_pdfs/`.
5. **Snippets** — Slice the original audio into high-fidelity clips by segment and save them under `library/`.
6. **Cleanup** — Remove the temporary full-length audio file.

---

## Requirements

- **Python 3.x**
- A local **`.gguf` model** placed at `models/llama-3.2-1b.gguf` (or update the path in `src/processor.py`)

---

## System Requirements

### FFmpeg (required)

FFmpeg is required for audio conversion and slicing (used by `yt-dlp` postprocessing and `pydub`).

- **macOS (Homebrew)**:

```bash
brew install ffmpeg
```

- **Windows (Chocolatey)**:

```bash
choco install ffmpeg
```

- **Windows (manual download)**: get builds from [FFmpeg Downloads](https://ffmpeg.org/download.html) and ensure `ffmpeg` is on your `PATH`.

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
- `src/processor.py` — Whisper transcription + local GGUF inference via `llama-cpp-python` + clip list.
- `src/writer.py` — Builds the Wisdom Synthesis Engine PDF.
- `src/slicer.py` — Cuts audio into snippets from the segment map.

---

## Setup (Local `.gguf` Model)

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Download or copy a compatible `.gguf` model and place it here:

- `models/llama-3.2-1b.gguf`

3. macOS GPU acceleration (Metal):

```bash
CMAKE_ARGS="-DGGML_METAL=on" pip install llama-cpp-python
```

If you already installed `llama-cpp-python`, reinstall it with the command above to enable Metal acceleration.

---

## Troubleshooting

- **Python 3.13+ / 3.14: `ModuleNotFoundError: No module named 'audioop'`**
  - Install `audioop-lts` (included in `requirements.txt`).
  - This project also applies a small compatibility monkey-patch in `src/slicer.py` so `pydub` can import `audioop` on Python 3.13+.

- **Windows: building `llama-cpp-python` fails**
  - You may need **Visual Studio Build Tools** (C++ build tools) installed so pip can compile the native extension.

## Why Local-First?

- **Privacy** — Sensitive or personal content stays on your device.
- **Control** — No rate limits or dependency on third-party APIs.
- **Offline** — Once models are installed, you can run without internet (after download).
- **Cost** — No per-request or subscription fees for transcription or summarization.

The Wisdom Synthesis Engine is built for researchers, coaches, and anyone who wants to turn audio into actionable wisdom while keeping full control of their data.
