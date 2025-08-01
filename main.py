from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from linkapi import check_link_safety
import whisper
import joblib
import traceback
import numpy as np
import soundfile as sf
import librosa
from sentence_transformers import SentenceTransformer

# Load models once
model = whisper.load_model("tiny")
encoder = SentenceTransformer("asafaya/bert-base-arabic")
print("✅ SentenceTransformer loaded!")

print("🔄 Loading classifier...")
clf = joblib.load("vishing_classifier.pkl")
print("✅ Classifier loaded!")

# =====================
# Link Scan Endpoint
# =====================
class LinkRequest(BaseModel):
    url: str

@app.post("/check_link")
def check_link(data: LinkRequest):
    return check_link_safety(data.url)

# =====================
# Audio Scan Endpoint
# =====================
@app.post("/analyze")
async def analyze_audio(audio: UploadFile = File(...)):
    try:
        # Save uploaded file
        file_path = audio.filename
        with open(file_path, "wb") as buffer:
            buffer.write(await audio.read())

        # Read & resample
        audio_data, sr = sf.read(file_path, dtype='float32')
        if sr != 16000:
            audio_data = librosa.resample(audio_data, orig_sr=sr, target_sr=16000)
            sf.write(file_path, audio_data, 16000)

        # Transcribe using preloaded Whisper
        result = whisper_model.transcribe(file_path, language='ar')
        text = result.get("text", "").strip()
        if not text:
            return {"text": "", "prediction": "No speech detected", "confidence": 0}

        # Encode & classify
        features = encoder.encode([text])
        preds = clf.predict(features)[0]
        probs = clf.predict_proba(features)[0]
        confidence = round(float(np.max(probs)) * 100, 2)

        labels = [
            "رمز تحقق", "بنك", "تهديد", "رقم بطاقة",
            "معلومات حساسة", "مكالمة عادية", "تخويف", "طلب تحويل"
        ]
        detected = [labels[i] for i, val in enumerate(preds) if val == 1]
        prediction = (
            f"🔴 Detected: {', '.join(detected)}" if detected else "🟢 Normal Call"
        )

        return {"text": text, "prediction": prediction, "confidence": confidence}

    except Exception:
        return {"error": traceback.format_exc()}
