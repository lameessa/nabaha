<<<<<<< HEAD
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from main import process_audio_file
from pydub import AudioSegment
import io
import os

app = FastAPI()

# CORS for Lovable frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to your frontend URL later
=======
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from main import process_audio_file, process_text_message
from pydub import AudioSegment
from pydantic import BaseModel
import io
import json

app = FastAPI()

# Enable CORS for frontend testing (e.g., Lovable)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Later, restrict to frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Nabaha API is running!"}

<<<<<<< HEAD
@app.post("/analyze-audio")
async def analyze_audio(audio: UploadFile = File(...)):  # Accept "audio" instead of "file"
    try:
        contents = await audio.read()

        # Convert any format to WAV @ 16kHz mono
        audio_segment = AudioSegment.from_file(io.BytesIO(contents))
        audio_segment = audio_segment.set_frame_rate(16000).set_channels(1)

        temp_filename = "uploaded.wav"
        audio_segment.export(temp_filename, format="wav")

        # Run prediction using ML pipeline
        result = process_audio_file(temp_filename)

        # Clean up
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

        # Format result for Lovable frontend
        if "error" in result:
            return {"status": "error", "details": result["error"]}

        return {
            "status": "danger" if "🔴" in result["prediction"] else "safe",
            "confidence": result.get("confidence", 0),
            "transcription": result.get("text", ""),
            "prediction": result.get("prediction", "")
        }

    except Exception as e:
        return {"status": "error", "details": str(e)}
=======
@app.post("/analyze")
async def analyze_audio(
    file: UploadFile = File(...),
    weights: Optional[str] = Form(None)  # Weights sent as JSON string from frontend
):
    try:
        # Read and preprocess the uploaded audio file
        contents = await file.read()
        audio = AudioSegment.from_file(io.BytesIO(contents))
        audio = audio.set_frame_rate(16000).set_channels(1)
        audio.export("uploaded.wav", format="wav")

        # Parse weights JSON string if provided
        try:
            label_weights = json.loads(weights) if weights else None
        except json.JSONDecodeError:
            label_weights = None

        # Run prediction
        result = process_audio_file("uploaded.wav", label_weights)
        print("✅ Received audio file")
        print("🪙 Weights:", label_weights)

        return result

    except Exception as e:
        return {"error": str(e)}

class TextInput(BaseModel):
    message: str

