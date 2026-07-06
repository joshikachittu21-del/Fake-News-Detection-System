import joblib

model = joblib.load("model/model.pkl")
vectorizer = joblib.load("model/vectorizer.pkl")


def predict_news(news):

    transformed = vectorizer.transform([news])

    prediction = model.predict(transformed)[0]

    if prediction == 0:
        return "Fake News"

    return "Real News"
