import csv
from pathlib import Path

from app.nlp.intent_classifier import training_data

data_directory = Path(__file__).parent / "data"
data_directory.mkdir(exist_ok=True)

csv_path = data_directory / "intents.csv"

with open(csv_path, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow(["text", "intent"])
    writer.writerows(training_data)

print(f"Exported {len(training_data)} examples to {csv_path}")