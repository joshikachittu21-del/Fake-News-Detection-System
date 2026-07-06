from flask import Flask, render_template, request
import joblib
import os

app = Flask(__name__)

# Load ML model
model_path = "model/model.pkl"
vectorizer_path = "model/vectorizer.pkl"

if os.path.exists(model_path) and os.path.exists(vectorizer_path):
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
else:
    model = None
    vectorizer = None


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    if model is None or vectorizer is None:
        return render_template(
            "index.html",
            prediction="Model not found. Please train the model first."
        )

    news = request.form["news"]

    transformed = vectorizer.transform([news])
    prediction = model.predict(transformed)[0]

    if prediction == 0:
        result = "🟥 Fake News"
    else:
        result = "🟩 Real News"

    return render_template(
        "index.html",
        prediction=result,
        news=news
    )


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
