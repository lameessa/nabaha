from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from main import process_audio_file
from pydub import AudioSegment
import io
app = FastAPI()

# Allow cross-origin requests (useful for frontend like Lovable)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict to your frontend later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Nabaha API is running!"}

@app.post("/analyze")
async def analyze_audio(file: UploadFile = File(...)):
    contents = await file.read()

    # Try to detect and convert it using pydub
    audio = AudioSegment.from_file(io.BytesIO(contents))
    audio = audio.set_frame_rate(16000).set_channels(1)
    audio.export("uploaded.wav", format="wav")

    # Run prediction using your model
    result = process_audio_file("uploaded.wav")

    return result
