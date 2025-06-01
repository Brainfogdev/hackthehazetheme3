import json
import random
import pandas as pd
import uuid
from openai import OpenAI
from dotenv import load_dotenv
import os
from typing import List, Dict, Optional, Any, Tuple
import re
from sklearn.preprocessing import LabelEncoder
import numpy as np
from sentence_transformers import SentenceTransformer, util
import httpx
import xgboost as xgb

load_dotenv()

# Initialize OpenAI client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    http_client=httpx.Client()
)

# Load career data
data_path = os.path.join(os.path.dirname(__file__), "data", "career_data.csv")
try:
    career_data = pd.read_csv(data_path)
except FileNotFoundError:
    raise FileNotFoundError(f"Could not find career_data.csv at {data_path}")

# Validate columns
feature_cols = [
    "math_score", "biology_score", "physics_score", "chemistry_score",
    "verbal_score", "analytical_score", "communication_score", "technical_score"
]
missing_cols = [col for col in feature_cols if col not in career_data.columns]
if missing_cols:
    raise KeyError(f"Missing columns in career_data.csv: {missing_cols}")

# Train XGBoost for aptitude estimation
X = career_data[feature_cols]
y = career_data["career"]
le = LabelEncoder()
y_encoded = le.fit_transform(y)
aptitude_model = xgb.XGBClassifier(n_estimators=100, random_state=42)
aptitude_model.fit(X, y_encoded)

# Career profiles for embedding-based matching
career_profiles = {
    "Doctor": "Medicine, patient care, biology, diagnostics, healthcare, NEET, PCB",
    "Nurse": "Patient care, biology, nursing, empathy, healthcare, NEET, PCB",
    "Software Engineer": "Coding, algorithms, software development, problem-solving, JEE, PCM, GATE",
    "Mechanical Engineer": "Mechanics, engineering, design, problem-solving, JEE, PCM",
    "MBA": "Business, management, finance, leadership, CAT, Commerce",
    "Chartered Accountant": "Accounting, finance, taxation, auditing, CA, Commerce",
    "Lawyer": "Legal analysis, advocacy, justice, ethics, CLAT, Arts",
    "Civil Servant": "Public service, administration, history, policy, UPSC, Arts",
    "Biomedical Scientist": "Research, biology, innovation, healthcare, NEET, PCB",
    "Data Scientist": "Data analysis, machine learning, coding, statistics, GATE, PCM"
}

# Train XGBoost for skill gaps
skill_models = {}
skill_cols = ["communication_score", "technical_score", "analytical_score"]
for skill in skill_cols:
    model = xgb.XGBRegressor(n_estimators=50, random_state=42)
    X_skill = career_data[["career"]].apply(le.transform).values
    y_skill = career_data[skill]
    model.fit(X_skill, y_skill)
    skill_models[skill] = model

def get_random_questions(
    category: str,
    stage: str,
    stream: str = "PCM",
    exam_type: Optional[str] = None,
    degree_type: Optional[str] = None,
    num_questions: int = 10,
    session_id: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Generate questions with unique IDs."""
    if session_id is None:
        session_id = uuid.uuid4().hex

    difficulty_map = {
        "9th/10th": "easy",
        "11th/12th": "medium",
        "After 12th": "hard",
        "Post-Graduation": "advanced"
    }
    category_filter = {
        "PCM": ["math", "physics", "chemistry", "analytical", "verbal", "extra", "activity"],
        "PCB": ["biology", "physics", "chemistry", "analytical", "verbal", "extra", "activity"],
        "Commerce": ["math", "accounting", "analytical", "verbal", "extra", "activity"],
        "Arts": ["verbal", "analytical", "extra", "activity"]
    }
    exam_category_map = {
        "JEE": ["math", "physics", "chemistry", "analytical", "verbal"],
        "NEET": ["biology", "physics", "chemistry", "analytical", "verbal"],
        "CLAT": ["verbal", "analytical", "extra"],
        "CAT": ["math", "analytical", "verbal", "extra"],
        "UPSC": ["verbal", "analytical", "extra"],
        "GATE": ["coding", "math", "analytical", "verbal"],
        "SAT": ["math", "verbal", "analytical", "extra"],
        "Other": category_filter.get(stream, ["math", "verbal", "analytical", "physics", "chemistry", "extra", "activity"])
    }
    degree_category_map = {
        "B.Tech": ["coding", "math", "analytical", "verbal", "extra"],
        "B.Com": ["accounting", "math", "analytical", "verbal", "extra"],
        "B.Sc": ["biology", "physics", "chemistry", "analytical", "verbal", "extra"],
        "B.A": ["verbal", "analytical", "extra"],
        "BBA": ["accounting", "analytical", "verbal", "extra"],
        "MBBS": ["biology", "extra", "analytical", "verbal"],
        "LLB": ["verbal", "analytical", "extra"],
        "Other": ["math", "verbal", "analytical", "extra"]
    }

    question_bank = {
        "math": {
            "easy": [{"base_id": "m1", "text_en": "What is 5 + 7?", "text_hi": "5 + 7 क्या है?", "options": ["12", "10", "14", "11"], "correct": ["12"], "type": "single"}],
            "medium": [{"base_id": "m2", "text_en": "Solve: 2x + 3 = 7", "text_hi": "हल करें: 2x + 3 = 7", "options": ["x=2", "x=3", "x=1", "x=4"], "correct": ["x=2"], "type": "single"}],
            "hard": [{"base_id": "m3", "text_en": "Integrate: ∫x dx", "text_hi": "समाकलन: ∫x dx", "options": ["x^2/2", "x", "x^3/3", "2x"], "correct": ["x^2/2"], "type": "single"}],
            "advanced": [{"base_id": "m4", "text_en": "Find the limit: lim(x->0) sin(x)/x", "text_hi": "सीमा ज्ञात करें: lim(x->0) sin(x)/x", "options": ["1", "0", "∞", "-1"], "correct": ["1"], "type": "single"}]
        },
        "biology": {
            "easy": [{"base_id": "b1", "text_en": "What is the powerhouse of the cell?", "text_hi": "कोशिका का पावरहाउस क्या है?", "options": ["Mitochondria", "Nucleus", "Ribosome", "Golgi"], "correct": ["Mitochondria"], "type": "single"}],
            "medium": [{"base_id": "b2", "text_en": "What is DNA made of?", "text_hi": "डीएनए किससे बना है?", "options": ["Nucleotides", "Amino acids", "Lipids", "Carbohydrates"], "correct": ["Nucleotides"], "type": "single"}],
            "hard": [{"base_id": "b3", "text_en": "What is photosynthesis?", "text_hi": "प्रकाश संश्लेषण क्या है?", "options": ["CO2 + H2O -> Glucose", "O2 -> CO2"], "correct": ["CO2 + H2O -> Glucose"], "type": "single"}],
            "advanced": [{"base_id": "b4", "text_en": "What is the role of tRNA in protein synthesis?", "text_hi": "प्रोटीन संश्लेषण में tRNA की भूमिका क्या है?", "options": ["Carries amino acids", "Transcribes DNA"], "correct": ["Carries amino acids"], "type": "single"}]
        },
        "physics": {
            "easy": [{"base_id": "p1", "text_en": "Unit of force?", "text_hi": "बल की इकाई?", "options": ["Newton", "Joule", "Watt", "Pascal"], "correct": ["Newton"], "type": "single"}],
            "medium": [{"base_id": "p2", "text_en": "F = ma, find a if F=10, m=2", "text_hi": "F = ma, a ज्ञात करें यदि F=10, m=2", "options": ["5", "10", "2", "20"], "correct": ["5"], "type": "single"}],
            "hard": [{"base_id": "p3", "text_en": "Work done: F=5N, d=2m", "text_hi": "कार्य: F=5N, d=2m", "options": ["10J", "5J", "15J", "20J"], "correct": ["10J"], "type": "single"}],
            "advanced": [{"base_id": "p4", "text_en": "What is the Schrödinger equation used for?", "text_hi": "श्रोडिंगर समीकरण का उपयोग किस लिए होता है?", "options": ["Quantum states", "Classical mechanics"], "correct": ["Quantum states"], "type": "single"}]
        },
        "chemistry": {
            "easy": [{"base_id": "c1", "text_en": "Symbol for water?", "text_hi": "पानी का प्रतीक?", "options": ["H2O", "CO2", "O2", "NaCl"], "correct": ["H2O"], "type": "single"}],
            "medium": [{"base_id": "c2", "text_en": "Atomic number of Carbon?", "text_hi": "कार्बन का परमाणु क्रमांक?", "options": ["6", "8", "12", "14"], "correct": ["6"], "type": "single"}],
            "hard": [{"base_id": "c3", "text_en": "pH of neutral solution?", "text_hi": "तटस्थ विलयन का pH?", "options": ["7", "0", "14", "1"], "correct": ["7"], "type": "single"}],
            "advanced": [{"base_id": "c4", "text_en": "What is the hybridization of NH3?", "text_hi": "NH3 का संकरण क्या है?", "options": ["sp3", "sp2"], "correct": ["sp3"], "type": "single"}]
        },
        "verbal": {
            "easy": [{"base_id": "v1", "text_en": "Synonym of big?", "text_hi": "'बड़ा' का पर्यायवाची?", "options": ["Small", "Large", "Tiny", "Short"], "correct": ["Large"], "type": "single"}],
            "medium": [{"base_id": "v2", "text_en": "Antonyms: Big, Small", "text_hi": "विलोम: बड़ा, छोटा", "options": ["True", "False"], "correct": ["True"], "type": "single"}],
            "hard": [{"base_id": "v3", "text_en": "Complete: The ___ is mightier than the sword.", "text_hi": "पूरा करें: ___ तलवार से अधिक शक्तिशाली है।", "options": ["Pen", "Word", "Mind", "Heart"], "correct": ["Pen"], "type": "single"}],
            "advanced": [{"base_id": "v4", "text_en": "Choose the correct analogy: Doctor : Hospital :: Teacher : ?", "text_hi": "सही समानता चुनें: डॉक्टर : अस्पताल :: शिक्षक : ?", "options": ["School", "Library"], "correct": ["School"], "type": "single"}]
        },
        "analytical": {
            "easy": [{"base_id": "a1", "text_en": "Next number: 2, 4, 6, ?", "text_hi": "अगली संख्या: 2, 4, 6, ?", "options": ["8", "7", "9", "10"], "correct": ["8"], "type": "single"}],
            "medium": [{"base_id": "a2", "text_en": "If A > B, B > C, then?", "text_hi": "यदि A > B, B > C, तो?", "options": ["A > C", "A < C", "A = C"], "correct": ["A > C"], "type": "single"}],
            "hard": [{"base_id": "a3", "text_en": "If all roses are flowers, and some flowers are red, then?", "text_hi": "यदि सभी गुलाब फूल हैं, और कुछ फूल लाल हैं, तो?", "options": ["Some roses are red", "All roses are red"], "correct": ["Some roses are red"], "type": "single"}],
            "advanced": [{"base_id": "a4", "text_en": "If some A are B, and all B are C, then?", "text_hi": "यदि कुछ A, B हैं, और सभी B, C हैं, तो?", "options": ["Some A are C", "All A are C"], "correct": ["Some A are C"], "type": "single"}]
        },
        "extra": {
            "easy": [{"base_id": "g1", "text_en": "Capital of India?", "text_hi": "भारत की राजधानी?", "options": ["Delhi", "Mumbai", "Kolkata", "Chennai"], "correct": ["Delhi"], "type": "single"}],
            "medium": [{"base_id": "g2", "text_en": "First PM of India?", "text_hi": "भारत के पहले PM?", "options": ["Nehru", "Gandhi", "Patel", "Modi"], "correct": ["Nehru"], "type": "single"}],
            "hard": [{"base_id": "g3", "text_en": "Year of Independence?", "text_hi": "स्वतंत्रता का वर्ष?", "options": ["1947", "1950", "1930", "1960"], "correct": ["1947"], "type": "single"}],
            "advanced": [{"base_id": "g4", "text_en": "Who is the current RBI Governor (2025)?", "text_hi": "2025 में RBI गवर्नर कौन है?", "options": ["Shaktikanta Das", "Urjit Patel"], "correct": ["Shaktikanta Das"], "type": "single"}]
        },
        "accounting": {
            "easy": [{"base_id": "ac1", "text_en": "What is a balance sheet?", "text_hi": "बैलेंस शीट क्या है?", "options": ["Financial statement", "Tax document"], "correct": ["Financial statement"], "type": "single"}],
            "medium": [{"base_id": "ac2", "text_en": "What is ROI?", "text_hi": "ROI क्या है?", "options": ["Return on Investment", "Revenue"], "correct": ["Return on Investment"], "type": "single"}],
            "hard": [{"base_id": "ac3", "text_en": "Calculate profit: Revenue=1000, Cost=700", "text_hi": "लाभ की गणना: राजस्व=1000, लागत=700", "options": ["300", "400"], "correct": ["300"], "type": "single"}],
            "advanced": [{"base_id": "ac4", "text_en": "What is double-entry bookkeeping?", "text_hi": "डबल-एंट्री बुककीपिंग क्या है?", "options": ["Records each transaction twice", "Single entry"], "correct": ["Records each transaction twice"], "type": "single"}]
        },
        "coding": {
            "easy": [{"base_id": "cd1", "text_en": "What is the output of print(2+3)?", "text_hi": "print(2+3) का आउटपुट क्या है?", "options": ["5", "6"], "correct": ["5"], "type": "single"}],
            "medium": [{"base_id": "cd2", "text_en": "What is a loop in Python?", "text_hi": "पायथन में लूप क्या है?", "options": ["Repeats code", "Function"], "correct": ["Repeats code"], "type": "single"}],
            "hard": [{"base_id": "cd3", "text_en": "Find error: for i in range(5) print(i)", "text_hi": "त्रुटि ढूंढें: for i in range(5) print(i)", "options": ["Missing colon", "No error"], "correct": ["Missing colon"], "type": "single"}],
            "advanced": [{"base_id": "cd4", "text_en": "What is the time complexity of merge sort?", "text_hi": "मर्ज सॉर्ट की समय जटिलता क्या है?", "options": ["O(n log n)", "O(n^2)"], "correct": ["O(n log n)"], "type": "single"}]
        },
        "activity": {
            "easy": [{"base_id": "act1", "text_en": "What is the capital city of France?", "text_hi": "फ्रांस की राजधानी क्या है?", "options": ["Paris", "London"], "correct": ["Paris"], "type": "single"}],
            "medium": [{"base_id": "act2", "text_en": "Which gas do plants absorb from the atmosphere?", "text_hi": "पौधे वातावरण से कौन सी गैस अवशोषित करते हैं?", "options": ["Carbon Dioxide", "Oxygen"], "correct": ["Carbon Dioxide"], "type": "single"}],
            "hard": [{"base_id": "act3", "text_en": "Who wrote the Indian National Anthem?", "text_hi": "भारतीय राष्ट्रगान किसने लिखा?", "options": ["Rabindranath Tagore", "Mahatma Gandhi"], "correct": ["Rabindranath Tagore"], "type": "single"}],
            "advanced": [{"base_id": "act4", "text_en": "What is the chemical symbol for Gold?", "text_hi": "सोने का रासायनिक प्रतीक क्या है?", "options": ["Au", "Ag"], "correct": ["Au"], "type": "single"}]
        }
    }

    valid_categories = category_filter.get(stream, ["math", "verbal", "analytical", "physics", "chemistry", "extra", "activity"])
    if exam_type and exam_type != "None":
        valid_categories = exam_category_map.get(exam_type, valid_categories)
    if stage == "Post-Graduation" and degree_type:
        valid_categories = degree_category_map.get(degree_type, valid_categories)

    if category not in valid_categories:
        return []

    questions = question_bank.get(category, {}).get(difficulty_map[stage], [])
    unique_questions = []
    for i, q in enumerate(questions):
        new_q = q.copy()
        new_q["id"] = f"{q['base_id']}_{session_id[:8]}_{i}"
        unique_questions.append(new_q)
    return random.sample(unique_questions * 10, min(num_questions, len(unique_questions * 10)))

def score_test(questions: List[Dict], user_answers: Dict[str, List[str]]) -> float:
    """Calculate score for a test."""
    score = 0.0
    total_questions = len(questions)
    for q in questions:
        correct_answers = set(q["correct"])
        user_response = set(user_answers.get(q["id"], []))
        if q["type"] == "single":
            score += 1 if user_response == correct_answers else 0
        else:
            score += 1 if user_response.issubset(correct_answers) and len(user_response) > 0 else 0
    return (score / total_questions) * 100 if total_questions > 0 else 0.0

def estimate_aptitude(
    user_scores: Dict[str, float],
    stage: str,
    stream: str,
    exam_type: Optional[str]
) -> str:
    """Estimate aptitude using XGBoost."""
    feature_map = {
        "math": "math_score",
        "biology": "biology_score",
        "physics": "physics_score",
        "chemistry": "chemistry_score",
        "verbal": "verbal_score",
        "analytical": "analytical_score",
        "extra": "communication_score",
        "activity": "communication_score",
        "coding": "technical_score",
        "accounting": "analytical_score"
    }
    features = {col: 0.0 for col in feature_cols}
    for cat, score in user_scores.items():
        if cat in feature_map:
            features[feature_map[cat]] = score

    X = pd.DataFrame([features])
    pred = aptitude_model.predict(X)[0]
    return le.inverse_transform([pred])[0]

def get_top_careers(
    interests: str,
    user_scores: Dict[str, float],
    stream: str,
    exam_type: Optional[str]
) -> List[Tuple[str, float]]:
    """Identify top careers based on interests and scores."""
    stream_careers = {
        "PCM": ["Software Engineer", "Mechanical Engineer", "Data Scientist"],
        "PCB": ["Doctor", "Nurse", "Biomedical Scientist"],
        "Commerce": ["MBA", "Chartered Accountant"],
        "Arts": ["Lawyer", "Civil Servant"]
    }
    exam_careers = {
        "JEE": ["Software Engineer", "Mechanical Engineer"],
        "NEET": ["Doctor", "Nurse", "Biomedical Scientist"],
        "CLAT": ["Lawyer"],
        "CAT": ["MBA"],
        "UPSC": ["Civil Servant"],
        "GATE": ["Software Engineer", "Data Scientist"],
        "SAT": ["Software Engineer", "Data Scientist"],
        "Other": stream_careers.get(stream, list(career_profiles.keys()))
    }
    valid_careers = exam_careers.get(exam_type, stream_careers.get(stream, list(career_profiles.keys())))
    
    embedder = SentenceTransformer('all-MiniLM-L6-v2')
    interest_embedding = embedder.encode(interests, convert_to_tensor=True)
    career_scores = []
    for career, profile in career_profiles.items():
        if career in valid_careers:
            profile_embedding = embedder.encode(profile, convert_to_tensor=True)
            similarity = util.cos_sim(interest_embedding, profile_embedding).item()
            career_scores.append((career, similarity))
    
    return sorted(career_scores, key=lambda x: x[1], reverse=True)[:3]

def estimate_skill_gaps(career: str, user_scores: Dict[str, float]) -> Dict[str, float]:
    """Estimate skill gaps for a career."""
    gaps = {}
    career_idx = le.transform([career])[0] if career in le.classes_ else 0
    for skill, model in skill_models.items():
        expected_score = model.predict(np.array([[career_idx]]))[0]
        user_score = user_scores.get(skill.replace("_score", ""), 0.0)
        gaps[skill.replace("_score", "")] = max(0, expected_score - user_score)
    return gaps

def clean_text(text: str) -> str:
    """Clean text for processing."""
    text = re.sub(r'[^\w\s.,]', '', text)
    sentences = [s.strip() for s in text.split('.') if s.strip()]
    return '. '.join(sentences[:5]) + '.' if sentences else "No valid input provided."

def predict_career(
    interests: str,
    user_scores: Dict[str, float],
    academic_data: Dict[str, Any],
    stage: str,
    stream: str,
    exam_type: Optional[str],
    degree_type: Optional[str],
    lang_code: str,
    interest_embeddings: List[Any],
    embedder: SentenceTransformer
) -> str:
    """Generate career recommendation."""
    interests = clean_text(interests)
    if not interests:
        return "Please provide valid interests." if lang_code == "en" else "कृपया वैध रुचियां प्रदान करें।"

    # Estimate aptitude
    predicted_career = estimate_aptitude(user_scores, stage, stream, exam_type)
    
    # Get top careers
    top_careers = get_top_careers(interests, user_scores, stream, exam_type)
    
    # Estimate skill gaps
    gaps = estimate_skill_gaps(predicted_career, user_scores)
    
    # Generate recommendation
    recommendation = "<h3>Recommended Careers:</h3><ul>"
    for career, score in top_careers:
        recommendation += f"<li><b>{career}</b>: {'High match' if score > 0.7 else 'Good match'}! {'🚀' if score > 0.7 else '🌟'}</li>"
    recommendation += "</ul>"
    
    recommendation += "<h3>Personality Traits:</h3><p>"
    if any(score > 80 for score in user_scores.values()):
        recommendation += "You show strong analytical and problem-solving skills! " if lang_code == "en" else "आपमें मजबूत विश्लेषणात्मक और समस्या-समाधान कौशल हैं! "
    else:
        recommendation += "You have a balanced skill set with growth potential! " if lang_code == "en" else "आपके पास संतुलित कौशल सेट और विकास की संभावना है! "
    recommendation += "</p>"
    
    recommendation += "<h3>Skill Gaps:</h3><ul>"
    for skill, gap in gaps.items():
        if gap > 20:
            recommendation += f"<li><b>{skill.capitalize()}</b>: Improve by {'practicing daily' if skill != 'technical' else 'learning tools like Python'}! {'🗣' if skill == 'communication' else '💻'}</li>"
    recommendation += "</ul>"
    
    return recommendation

def analyze_job_market(careers: List[str]) -> pd.DataFrame:
    """Mock job market analysis."""
    demand = {
        "Software Engineer": 85.0, "Doctor": 90.0, "MBA": 75.0, "Lawyer": 70.0,
        "Civil Servant": 65.0, "Nurse": 80.0, "Mechanical Engineer": 70.0,
        "Chartered Accountant": 75.0, "Biomedical Scientist": 65.0, "Data Scientist": 80.0
    }
    data = [{"Career": c, "Demand": demand.get(c, 60.0)} for c in careers]
    return pd.DataFrame(data)