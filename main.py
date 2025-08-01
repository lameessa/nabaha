import whisper
import json
import datetime
import joblib
from sentence_transformers import SentenceTransformer
import soundfile as sf
import traceback
import numpy as np

# Load models once
model = whisper.load_model("large")
encoder = SentenceTransformer("asafaya/bert-base-arabic")
clf = joblib.load("vishing_classifier.pkl")

def process_audio_file(file_path):
    try:
        # Load audio
        audio_data, sr = sf.read(file_path, dtype='float32')
        if sr != 16000:
            raise ValueError("Sample rate must be 16kHz")

        # Transcribe
        result = model.transcribe(file_path, language='ar')
        text = result["text"].strip()

        if text.strip() == "":
            return {"text": "", "prediction": "No speech detected."}

        # Encode transcript
        features = encoder.encode([text])

        # Predict
        preds = clf.predict(features)[0]              # Array of 0/1
        probs = clf.predict_proba(features)           # List of arrays
        max_index = int(np.argmax(preds))             # Which class got "1"
        max_prob = float(np.max(probs[max_index]))    # Max confidence

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

    except Exception as e:
        return {"error": traceback.format_exc()}
