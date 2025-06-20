import joblib
from sentence_transformers import SentenceTransformer
import os

model_path = os.environ.get("MODEL_PATH", "embedding_model")
clf_path = os.environ.get("CLF_PATH", "valid_point_classifier.pkl")
label_path = os.environ.get("LABEL_PATH","label_encoder.pkl")

encoder = SentenceTransformer(model_path)
clf = joblib.load(clf_path)
label_encoder = joblib.load(label_path)

def is_point_valid(point):
    emb = encoder.encode([point])
    pred = clf.predict(emb)[0]
    label = label_encoder.inverse_transform([pred])[0]
    return label


