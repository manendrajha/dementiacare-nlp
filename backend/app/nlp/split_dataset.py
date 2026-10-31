import csv
from pathlib import Path

from sklearn.model_selection import train_test_split


DATA_DIR = Path(__file__).parent / "data"
SOURCE_FILE = DATA_DIR / "intents.csv"

TRAIN_FILE = DATA_DIR / "train.csv"
TEST_FILE = DATA_DIR / "test.csv"


# Load the updated dataset.
with open(SOURCE_FILE, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    data = list(reader)


texts = [
    row["text"].strip()
    for row in data
    if row.get("text") and row.get("intent")
    and row["text"].strip().lower() != "text"
    and row["intent"].strip().lower() != "intent"
]

labels = [
    row["intent"].strip()
    for row in data
    if row.get("text") and row.get("intent")
    and row["text"].strip().lower() != "text"
    and row["intent"].strip().lower() != "intent"
]


# Generate a training split.
X_train, _, y_train, _ = train_test_split(
    texts,
    labels,
    test_size=0.25,
    random_state=42,
    stratify=labels
)


def save_dataset(path, texts, labels):
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["text", "intent"])
        writer.writerows(zip(texts, labels))


# Update training data only.
save_dataset(TRAIN_FILE, X_train, y_train)

print("Training dataset regenerated.")
print("Training examples:", len(X_train))
print("Existing test.csv was not modified.")
