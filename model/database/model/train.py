import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.metrics import accuracy_score, classification_report

from preprocess import clean_text

# Load datasets
fake = pd.read_csv("../dataset/Fake.csv")
true = pd.read_csv("../dataset/True.csv")

# Add labels
fake["label"] = 0
true["label"] = 1

# Combine datasets
data = pd.concat([fake, true], ignore_index=True)

# Shuffle dataset
data = data.sample(frac=1, random_state=42).reset_index(drop=True)

# Keep required columns
data = data[["text", "label"]]

# Clean text
data["text"] = data["text"].apply(clean_text)

# Features and labels
X = data["text"]
y = data["label"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# TF-IDF
vectorizer = TfidfVectorizer(
    stop_words="english",
    max_df=0.7
)

X_train_vector = vectorizer.fit_transform(X_train)
X_test_vector = vectorizer.transform(X_test)

# Model
model = PassiveAggressiveClassifier(max_iter=100)

model.fit(X_train_vector, y_train)

# Prediction
prediction = model.predict(X_test_vector)

accuracy = accuracy_score(y_test, prediction)

print("=" * 50)
print("Accuracy:", accuracy)
print("=" * 50)

print(classification_report(y_test, prediction))

# Save model
joblib.dump(model, "model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("Model saved successfully.")
