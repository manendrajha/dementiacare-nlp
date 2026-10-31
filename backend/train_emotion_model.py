
from pathlib import Path
from collections import Counter

import joblib
from datasets import load_from_disk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score

BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR / "data" / "external" / "dailydialog"
MODEL_PATH = BASE_DIR / "app" / "nlp" / "emotion_model.joblib"

EMOTIONS = {
    0: "neutral",
    1: "anger",
    2: "disgust",
    3: "fear",
    4: "happiness",
    5: "sadness",
    6: "surprise",
}


def prepare_examples(split):
    texts = []
    labels = []

    for dialogue in split:
        utterances = dialogue["utterances"]
        emotions = dialogue["emotions"]

        for text, emotion in zip(utterances, emotions):
            if text.strip() and emotion in EMOTIONS:
                texts.append(text.strip())
                labels.append(emotion)

    return texts, labels


print("Loading DailyDialog...")
dataset = load_from_disk(str(DATASET_PATH))

X_train, y_train = prepare_examples(dataset["train"])
X_test, y_test = prepare_examples(dataset["test"])

print(f"Training utterances: {len(X_train)}")
print(f"Testing utterances: {len(X_test)}")
print("Training label distribution:", Counter(y_train))

model = Pipeline([
    ("tfidf", TfidfVectorizer(
        lowercase=True,
        ngram_range=(1, 2),
        strip_accents="unicode",
        max_features=50000,
        min_df=2
    )),
    ("classifier", LogisticRegression(
        max_iter=1500,
        class_weight="balanced",
        random_state=42
    ))
])

print("\nTraining emotion classifier...")
model.fit(X_train, y_train)

print("\nEvaluating on the original test split...")
predictions = model.predict(X_test)

print("Test accuracy:", round(accuracy_score(y_test, predictions), 4))

print("\nClassification report:")
print(classification_report(
    y_test,
    predictions,
    labels=list(EMOTIONS.keys()),
    target_names=list(EMOTIONS.values()),
    zero_division=0
))

MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
joblib.dump(model, MODEL_PATH)

print(f"\nModel saved to: {MODEL_PATH}")
