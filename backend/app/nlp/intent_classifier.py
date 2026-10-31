import csv
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


DATASET_PATH = Path(__file__).parent / "data" / "intents.csv"


def load_training_data():
    """Load labelled intent examples from the CSV dataset."""

    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Intent dataset not found: {DATASET_PATH}"
        )

    examples = []

    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            text = row["text"].strip()
            intent = row["intent"].strip()

            if text and intent:
                examples.append((text, intent))

    if not examples:
        raise ValueError("The intent dataset is empty.")

    return examples


training_data = load_training_data()


def create_model():
    """Create the TF-IDF and Logistic Regression pipeline."""

    return Pipeline([
        (
            "tfidf",
            TfidfVectorizer(
                lowercase=True,
                ngram_range=(1, 2),
                strip_accents="unicode"
            )
        ),
        (
            "classifier",
            LogisticRegression(
                max_iter=1000,
                class_weight="balanced",
                random_state=42
            )
        )
    ])


X_train = [text for text, intent in training_data]
y_train = [intent for text, intent in training_data]

model = create_model()
model.fit(X_train, y_train)


def classify_intent(message: str):
    """Predict the intent of a user's message."""

    message = message.strip()

    if not message:
        return {
            "intent": "unknown",
            "confidence": 0.0
        }

    probabilities = model.predict_proba([message])[0]

    best_index = probabilities.argmax()
    confidence = float(probabilities[best_index])
    predicted_intent = model.classes_[best_index]

    if confidence < 0.20:
        predicted_intent = "unknown"

    return {
        "intent": predicted_intent,
        "confidence": round(confidence, 4)
    }