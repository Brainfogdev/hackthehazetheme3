from transformers import pipeline

class CareerIntentClassifier:
    def __init__(self):
        self.classifier = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli"
        )
        
    def analyze(self, text, career_labels):
        if not text.strip():
            return {"labels": career_labels, "scores": [0.25] * len(career_labels)}
        
        result = self.classifier(text, career_labels, multi_label=True)
        return result
