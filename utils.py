from typing import List, Tuple, Any
from sentence_transformers import SentenceTransformer
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import os

# Download NLTK data if not already present
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)

def translate_ui(lang_code: str) -> dict:
    """Return UI translations for English or Hindi."""
    translations = {
        "en": {
            "title": "CareerQuestAI: Discover Your Path!",
            "interests": "Tell Us Your Interests",
            "interests_placeholder": "E.g., coding, dancing, helping people, science...",
            "stage": "Your Academic Stage",
            "academic_performance": "Academic Performance",
            "score_option": "How to Assess Your Skills",
            "slider": "Use Sliders",
            "test": "Take a Quiz",
            "enter_scores": "Enter Your Scores",
            "aptitude_test": "Aptitude Test",
            "exam_type": "Competitive Exam",
            "exam_score": "Exam Score",
            "degree_type": "Degree Type",
            "score_type": "Score Type",
            "recommendation": "Your Career Recommendation",
            "job_market": "Job Market Insights",
            "success_message": "Recommendation generated successfully!",
            "complete_fields": "Please enter your interests and scores to get a recommendation."
        },
        "hi": {
            "title": "CareerQuestAI: अपनी राह खोजें!",
            "interests": "हमें अपनी रुचियां बताएं",
            "interests_placeholder": "उदाहरण: कोडिंग, नृत्य, लोगों की मदद, विज्ञान...",
            "stage": "आपका शैक्षणिक स्तर",
            "academic_performance": "शैक्षणिक प्रदर्शन",
            "score_option": "अपने कौशल का आकलन कैसे करें",
            "slider": "स्लाइडर का उपयोग करें",
            "test": "क्विज़ लें",
            "enter_scores": "अपने अंक दर्ज करें",
            "aptitude_test": "योग्यता परीक्षा",
            "exam_type": "प्रतियोगी परीक्षा",
            "exam_score": "परीक्षा स्कोर",
            "degree_type": "डिग्री प्रकार",
            "score_type": "स्कोर प्रकार",
            "recommendation": "आपकी करियर सिफारिश",
            "job_market": "नौकरी बाजार अंतर्दृष्टि",
            "success_message": "सिफारिश सफलतापूर्वक उत्पन्न हुई!",
            "complete_fields": "कृपया अपनी रुचियां और अंक दर्ज करें।"
        }
    }
    return translations.get(lang_code, translations["en"])

def process_input(text: str, lang_code: str) -> Tuple[List[str], List[Any]]:
    """Process user input to extract interests and generate embeddings."""
    # Initialize Sentence-BERT
    embedder = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Clean text
    text = re.sub(r'[^\w\s]', '', text.lower().strip())
    if not text:
        return [], []
    
    # Tokenize and remove stopwords
    stop_words = set(stopwords.words('english' if lang_code == 'en' else 'hindi'))
    tokens = word_tokenize(text)
    processed = [word for word in tokens if word not in stop_words and len(word) > 2]
    
    if not processed:
        return [], []
    
    # Generate embeddings
    embeddings = [embedder.encode(word, convert_to_tensor=True) for word in processed]
    
    return processed, embeddings

if __name__ == "__main__":
    # Test translations
    print(translate_ui("en"))
    print(translate_ui("hi"))
    # Test input processing
    print(process_input("I love coding and helping people", "en"))