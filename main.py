import json
import joblib
from sentence_transformers import SentenceTransformer
import numpy as np
import traceback

# Load models
encoder = SentenceTransformer("asafaya/bert-base-arabic")
clf = joblib.load("vishing_classifier.pkl")

def process_text_message(text):
    try:
        features = encoder.encode([text])
        preds = clf.predict(features)[0]
        probs = clf.predict_proba(features)
        max_index = int(np.argmax(preds))
        max_prob = float(np.max(probs[max_index]))

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
