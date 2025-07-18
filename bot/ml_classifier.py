from joblib import dump, load
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import os

class FileClassifier:
    def __init__(self):
        self.vectorizer = CountVectorizer()
        self.classifier = MultinomialNB()

    def train(self, filenames, labels):
        X = self.vectorizer.fit_transform(filenames)
        self.classifier.fit(X, labels)

    def predict(self, filename):
        X = self.vectorizer.transform([filename])
        return self.classifier.predict(X)[0]

    def save(self, path="bot/model.joblib"):
        dump((self.vectorizer, self.classifier), path)

    def load(self, path="bot/model.joblib"):
        if not os.path.exists(path):
            raise FileNotFoundError(f"Model file not found: {path}")
        self.vectorizer, self.classifier = load(path)
