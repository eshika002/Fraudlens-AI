from transformers import pipeline

# Load model once
classifier = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english")

def transformer_analysis(text):
    try:
        result = classifier(text[:512])[0]
        label = result["label"]
        confidence = round(result["score"] * 100, 2)
        return label, confidence
    except Exception:
        return "UNKNOWN", 0