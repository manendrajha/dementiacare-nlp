import csv
from pathlib import Path
from collections import Counter

DATA_DIR = Path(__file__).parent / "data"

SOURCE_FILE = DATA_DIR / "intents.csv"
TEST_FILE = DATA_DIR / "test.csv"
TRAIN_FILE = DATA_DIR / "train.csv"

EXPECTED_INTENTS = {
    "activity",
    "emotional_support",
    "family",
    "goodbye",
    "gratitude",
    "greeting",
    "memory",
    "orientation",
    "reminder"
}


def load_csv(path):
    with open(path, "r", encoding="utf-8-sig") as file:
        return list(csv.DictReader(file))


all_data = load_csv(SOURCE_FILE)
test_data = load_csv(TEST_FILE)


def clean_rows(rows):
    cleaned = []

    for row in rows:
        text = row.get("text", "").strip()
        intent = row.get("intent", "").strip()

        if not text or not intent:
            continue

        # Remove accidental repeated CSV headers.
        if text.lower() == "text" and intent.lower() == "intent":
            continue

        if intent not in EXPECTED_INTENTS:
            raise ValueError(f"Invalid intent label: {intent}")

        cleaned.append({
            "text": text,
            "intent": intent
        })

    return cleaned


all_data = clean_rows(all_data)
test_data = clean_rows(test_data)

test_examples = {
    (row["text"], row["intent"])
    for row in test_data
}

train_data = [
    row for row in all_data
    if (row["text"], row["intent"]) not in test_examples
]

train_examples = {
    (row["text"], row["intent"])
    for row in train_data
}

assert train_examples.isdisjoint(test_examples)

# Five-fold CV requires at least five examples per class.
counts = Counter(row["intent"] for row in train_data)

print("Training class distribution:")
for intent in sorted(EXPECTED_INTENTS):
    print(f"{intent}: {counts[intent]}")

if any(counts[intent] < 5 for intent in EXPECTED_INTENTS):
    raise ValueError(
        "Some classes have fewer than five training examples."
    )

with open(TRAIN_FILE, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=["text", "intent"]
    )
    writer.writeheader()
    writer.writerows(train_data)

print("\nTraining dataset prepared.")
print("Training examples:", len(train_data))
print("Testing examples:", len(test_data))
print("Training-test overlap:", len(train_examples & test_examples))