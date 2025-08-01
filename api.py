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
    allow_origins=["*"],  # ⚠️ Replace with frontend origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Nabaha API is running!"}

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

@app.post("/analyze-text")
async def analyze_text(data: TextInput):
    result = process_text_message(data.message)
    return result
