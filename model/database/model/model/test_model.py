import joblib

model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

while True:

    news = input("\nEnter News (type exit to quit): ")

    if news.lower() == "exit":
        break

    transformed = vectorizer.transform([news])

    prediction = model.predict(transformed)[0]

    if prediction == 0:
        print("\nPrediction: Fake News")
    else:
        print("\nPrediction: Real News")
