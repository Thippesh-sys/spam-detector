import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle

# Load dataset
df = pd.read_csv("SMSSpamCollection", sep='\t', names=["label", "message"])

# Convert text to numbers
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["message"])

# Train model
model = MultinomialNB()
model.fit(X, df["label"])

# Save model
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("✅ Model trained and saved successfully!")