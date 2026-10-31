
from pathlib import Path
import joblib

MODEL_PATH = Path(__file__).parent / "emotion_model.joblib"

EMOTIONS = {
    0: "neutral",
    1: "anger",
    2: "disgust",
    3: "fear",
    4: "happiness",
    5: "sadness",
    6: "surprise",
}

model = joblib.load(MODEL_PATH)


def classify_emotion(message: str):
    message = message.strip()

    if not message:
        return {
            "emotion": "neutral",
            "confidence": 0.0
        }

    probabilities = model.predict_proba([message])[0]
    best_index = probabilities.argmax()
    predicted_label = int(model.classes_[best_index])

    return {
        "emotion": EMOTIONS[predicted_label],
        "confidence": round(float(probabilities[best_index]), 4)
    }
