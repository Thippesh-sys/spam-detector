from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

# Load saved model and vectorizer
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    user_msg = request.form["message"]

    # 🔹 Smart detection rules (fast check)
    if "http" in user_msg or "www" in user_msg:
        result = "⚠️ Suspicious Link Detected"
    
    elif any(word in user_msg.lower() for word in ["win", "free", "offer", "prize"]):
        result = "⚠️ Possible Scam Message"

    else:
        # 🔹 Convert message to vector
        msg_vec = vectorizer.transform([user_msg])

        # 🔹 Prediction
        prediction = model.predict(msg_vec)[0]

        # 🔹 Probability calculation
        probabilities = model.predict_proba(msg_vec)[0]

        # Get spam & ham probability
        spam_prob = probabilities[list(model.classes_).index("spam")]
        ham_prob = probabilities[list(model.classes_).index("ham")]

        # 🔹 Final result with probability
        if prediction == "spam":
            result = f"❌ Spam Detected ({round(spam_prob*100, 2)}%)"
        else:
            result = f"✅ Safe Message ({round(ham_prob*100, 2)}%)"

    return render_template("index.html", prediction_text=result)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)