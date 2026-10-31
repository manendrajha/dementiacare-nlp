import csv
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC

from sklearn.model_selection import StratifiedKFold, cross_validate

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)


DATA_DIR = Path(__file__).parent / "data"


def load_dataset(filename):
    path = DATA_DIR / filename

    with open(path, "r", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    return (
        [row["text"] for row in rows],
        [row["intent"] for row in rows]
    )


X_train, y_train = load_dataset("train.csv")
X_test, y_test = load_dataset("test.csv")


models = {
    "Logistic Regression": LogisticRegression(
        max_iter=1000,
        class_weight="balanced",
        random_state=42
    ),

    "Linear SVM": LinearSVC(
        class_weight="balanced",
        random_state=42
    )
}


# Five-fold stratified cross-validation.
cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)


for model_name, classifier in models.items():

    pipeline = Pipeline([
        (
            "tfidf",
            TfidfVectorizer(
                lowercase=True,
                ngram_range=(1, 2),
                strip_accents="unicode"
            )
        ),
        ("classifier", classifier)
    ])

    print("\n" + "=" * 65)
    print(model_name)
    print("=" * 65)

    # Cross-validation on training data only.
    scores = cross_validate(
        pipeline,
        X_train,
        y_train,
        cv=cv,
        scoring=["accuracy", "f1_macro"],
        return_train_score=False
    )

    print("\nFive-fold cross-validation:")
    print(
        "Mean accuracy:",
        round(scores["test_accuracy"].mean(), 4)
    )
    print(
        "Mean macro F1:",
        round(scores["test_f1_macro"].mean(), 4)
    )

    print(
        "Macro F1 standard deviation:",
        round(scores["test_f1_macro"].std(), 4)
    )

    # Train on the complete training dataset.
    pipeline.fit(X_train, y_train)

    # Evaluate once on the untouched test set.
    predictions = pipeline.predict(X_test)

    print("\nIndependent test results:")
    print(
        "Accuracy:",
        round(accuracy_score(y_test, predictions), 4)
    )

    print("\nClassification report:")
    print(classification_report(
        y_test,
        predictions,
        zero_division=0
    ))

    labels = sorted(set(y_train) | set(y_test))

    print("\nConfusion matrix:")
    print("Labels:", labels)
    print(confusion_matrix(
        y_test,
        predictions,
        labels=labels
    ))