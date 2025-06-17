# ffmpeg_auto_installer

🔧 A lightweight Python utility to auto-install and configure **FFmpeg** on Windows — with retries, detailed logging, and dynamic PATH updates. Perfect for audio transcription and video processing pipelines using tools like Hugging Face Transformers or Whisper.

---

## 💡 Why use this?

Many AI audio workflows (like speech-to-text using `transformers.pipeline("automatic-speech-recognition")`) require `ffmpeg` to decode audio files like MP3, WAV, or FLAC. This package ensures that `ffmpeg` is installed and available — even in clean or CI environments.

---

## ✅ Features

- 🔍 Detects if `ffmpeg` is already installed
- ⏬ Downloads the latest build from [Gyan.dev](https://www.gyan.dev/ffmpeg/builds/)
- 📦 Extracts zip and updates `PATH` dynamically at runtime
- 🔁 Retries downloads on failure
- 🪵 Detailed logging

---

## 🚀 Installation

```bash
pip install ffmpeg_auto_installer

**## Usage**
from ffmpeg_auto_installer import ensure_ffmpeg

# Automatically install and configure ffmpeg if not present
ensure_ffmpeg()

# Now you can use libraries like transformers without ffmpeg errors
from transformers import pipeline

asr = pipeline("automatic-speech-recognition")
result = asr("sample.mp3")  # will now work
