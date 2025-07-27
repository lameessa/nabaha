import sounddevice as sd
import numpy as np
import whisper
import threading
import queue
import json
import datetime
import signal
import sys

# === Configuration ===
SAMPLE_RATE = 16000
CHUNK_DURATION = 2  # seconds
OUTPUT_FILE = "transcripts.json"

# === Initialize Whisper Model ===
model = whisper.load_model("large")  # You can use "small", "medium", "large" if needed

# === Shared resources ===
audio_queue = queue.Queue()
transcripts = []

# === Recording audio callback ===
def audio_callback(indata, frames, time, status):
    if status:
        print("⚠️", status)
    audio_queue.put(indata.copy())

# === Transcription logic ===
def transcribe_audio():
    while True:
        audio_chunk = audio_queue.get()

        # Flatten to 1D float32 array for Whisper
        audio_data = audio_chunk.flatten().astype(np.float32)

        try:
            result = model.transcribe(audio_data, language='ar')
            text = result["text"].strip()
            if text:
                print("📝", result["text"][::-1])
                transcripts.append({
                    "timestamp": datetime.datetime.now().isoformat(),
                    "text": text
                })

                # Save to JSON
                with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
                    json.dump(transcripts, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print("❌ Error during transcription:", e)

# === Graceful shutdown handler ===
def signal_handler(sig, frame):
    print("\n👋 Exiting and saving transcripts...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(transcripts, f, ensure_ascii=False, indent=2)
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# === Start recording ===
def main():
    print("🎤 Starting live Arabic transcription... Press Ctrl+C to stop.")
    threading.Thread(target=transcribe_audio, daemon=True).start()

    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, callback=audio_callback,
                        blocksize=int(SAMPLE_RATE * CHUNK_DURATION)):
        signal.pause()

if __name__ == "__main__":
    main()
