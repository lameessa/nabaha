import joblib
from sentence_transformers import SentenceTransformer
import numpy as np

encoder = SentenceTransformer("asafaya/bert-base-arabic")
clf = joblib.load("vishing_classifier.pkl")

def process_text_message(text):
    features = encoder.encode([text])
    preds = clf.predict(features)[0]
    probs = clf.predict_proba(features)
    labels = [
        "رمز تحقق", "بنك", "تهديد", "رقم بطاقة",
        "معلومات حساسة", "مكالمة عادية", "تخويف", "طلب تحويل"
    ]
    predicted_labels = [labels[i] for i, val in enumerate(preds) if val == 1]
    confidence = float(np.max(probs[int(np.argmax(preds))]))
    return {
        "text": text,
        "prediction": ", ".join(predicted_labels) or "Normal Call",
        "confidence": round(confidence * 100, 2)
    }
