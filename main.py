<<<<<<< HEAD
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from linkapi import check_link_safety
import whisper
=======
import whisperx
>>>>>>> 959b12203e61c1b804bfbeba8829a82d27639536
import joblib
import traceback
import numpy as np
import soundfile as sf
<<<<<<< HEAD
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
=======
import re
import whisper

# Load models once
model = whisper.load_model("large")
clf = joblib.load("vishing_classifier.pkl")

FEATURE_NAMES = [
    "request_passwords",
    "request_code",
    "request_money_transfer",
    "request_banking_info",
    "request_personal_info",
    "used_threat",
    "is_urgent",
    "good_offers"
]

DEFAULT_WEIGHTS = {
    "request_passwords": 1.0,
    "request_code": 0.9,
    "request_money_transfer": 1.3,
    "request_banking_info": 0.8,
    "request_personal_info": 0.7,
    "used_threat": 1.2,
    "is_urgent": 1.0,
    "good_offers": 0.4
}

def extract_features_from_text(text: str) -> dict:
    return {
        "request_passwords": int(bool(re.search(r"كلمة مرور|الرقم السري|رمز المرور", text))),
        "request_code": int(bool(re.search(r"رمز التحقق|OTP|رمز", text))),
        "request_money_transfer": int(bool(re.search(r"تحويل|أرسل|مبلغ|فلوس", text))),
        "request_banking_info": int(bool(re.search(r"حساب بنكي|رقم حساب|بنك", text))),
        "request_personal_info": int(bool(re.search(r"الهوية|تاريخ ميلاد|عنوان|معلومات شخصية", text))),
        "used_threat": int(bool(re.search(r"سحب القضية|شرطة|سجن|تهديد", text))),
        "is_urgent": int(bool(re.search(r"فورا|مستعجل|الآن|ضروري", text))),
        "good_offers": int(bool(re.search(r"عرض|هدية|فرصة|مجانا", text)))
    }

def process_audio_file(file_path, label_weights=None):
    try:
        # Step 1: Load and validate audio
        audio_data, sr = sf.read(file_path, dtype='float32')
>>>>>>> 959b12203e61c1b804bfbeba8829a82d27639536
        if sr != 16000:
            audio_data = librosa.resample(audio_data, orig_sr=sr, target_sr=16000)
            sf.write(audio.filename, audio_data, 16000)

<<<<<<< HEAD
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
=======
        # Step 2: Transcribe
        result = model.transcribe(file_path, language='ar')
        text = result["text"].strip()

        if not text:
            return {"confidence": 0.0, "fraud_score": 0.0, "fraud_level": "Low"}

        # Step 3: Extract binary features
        features_dict = extract_features_from_text(text)
        features_vector = np.array([[features_dict[f] for f in FEATURE_NAMES]])

        # Step 4: Predict using model
        preds = clf.predict(features_vector)[0]
        probs = clf.predict_proba(features_vector)

        # Step 5: Apply weights
        weights = label_weights if label_weights else DEFAULT_WEIGHTS
        base_score = sum(preds[i] * weights.get(FEATURE_NAMES[i], 0) for i in range(len(FEATURE_NAMES)))
        if sum(preds) > 1:
            base_score *= 1.15
        fraud_score = round(min(base_score, 1.0), 3)

        # Step 6: Calculate confidence
        positive_probs = [probs[i][0][1] for i in range(len(preds)) if preds[i] == 1]
        confidence = round(float(np.max(positive_probs)) * 100, 2) if positive_probs else 0.0

        # Step 7: Fraud level
        level = "High" if fraud_score >= 0.85 else "Medium" if fraud_score >= 0.5 else "Low"
        print("📜 Transcript:", text)
        print("🧩 Features:", features_dict)
        print("🔮 Model preds:", preds)
        print("🎯 Score:", fraud_score)
        print("🔥 Confidence:", confidence)

        return {
            "confidence": confidence,
            "fraud_score": fraud_score,
            "fraud_level": level
        }

    except Exception as e:
        return {"error": traceback.format_exc()}

def process_text_message(text):
    try:
        if text.strip() == "":
            return {"text": "", "prediction": "No message content provided."}

        # Encode message
        features = encoder.encode([text])

        # Predict
        preds = clf.predict(features)[0]
        probs = clf.predict_proba(features)
        max_index = int(np.argmax(preds))
        max_prob = float(np.max(probs[max_index]))
>>>>>>> 959b12203e61c1b804bfbeba8829a82d27639536

        labels = [
            "رمز تحقق", "بنك", "تهديد", "رقم بطاقة",
            "معلومات حساسة", "مكالمة عادية", "تخويف", "طلب تحويل"
        ]
        predicted_labels = [labels[i] for i, val in enumerate(preds) if val == 1]

        return {
            "text": text,
            "prediction": f"🔴 Detected: {', '.join(predicted_labels)}" if predicted_labels else "🟢 Normal Message",
            "confidence": round(max_prob * 100, 2)
        }

<<<<<<< HEAD
    except Exception:
        return {"error": traceback.format_exc()}
=======
    except Exception as e:
        return {"error": traceback.format_exc()}
>>>>>>> 959b12203e61c1b804bfbeba8829a82d27639536
