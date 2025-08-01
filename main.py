from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from linkapi import check_link_safety
import whisper
import joblib
import traceback
import numpy as np
import soundfile as sf
import librosa
from sentence_transformers import SentenceTransformer

# ✅ Create FastAPI app
app = FastAPI()

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
# Lazy-load models for faster startup
@app.post("/analyze-audio")
async def analyze_audio(audio: UploadFile = File(...)):
    try:
        # Load models when needed
        model = whisper.load_model("tiny")
        encoder = SentenceTransformer("asafaya/bert-base-arabic")
        clf = joblib.load("vishing_classifier.pkl")

        # Save uploaded file
        with open(audio.filename, "wb") as buffer:
            buffer.write(await audio.read())

        # Read & resample
        audio_data, sr = sf.read(audio.filename, dtype='float32')
        if sr != 16000:
            audio_data = librosa.resample(audio_data, orig_sr=sr, target_sr=16000)
            sf.write(audio.filename, audio_data, 16000)

        # Transcribe
        result = model.transcribe(audio.filename, language='ar')
        text = result["text"].strip()

        if not text:
            return {"text": "", "prediction": "No speech detected", "confidence": 0}

        # Encode & classify
        features = encoder.encode([text])
        preds = clf.predict(features)[0]
        probs = clf.predict_proba(features)
        max_prob = float(np.max(probs))

        labels = [
            "رمز تحقق", "بنك", "تهديد", "رقم بطاقة",
            "معلومات حساسة", "مكالمة عادية", "تخويف", "طلب تحويل"
        ]
        predicted_labels = [labels[i] for i, val in enumerate(preds) if val == 1]

        return {
            "text": text,
            "prediction": f"🔴 Detected: {', '.join(predicted_labels)}" if predicted_labels else "🟢 Normal Call",
            "confidence": round(max_prob * 100, 2)
        }

    except Exception:
        return {"error": traceback.format_exc()}
