# Expanded career guidance system with ML/NLP hooks (FastAPI backend) + Indic + Exam Alignment

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import random
import uvicorn
from sentence_transformers import SentenceTransformer, util
import torch
import numpy as np

app = FastAPI()

# === Models ===
class UserProfile(BaseModel):
    name: str
    age: int
    education_level: str  # e.g., "10th", "12th", "graduate"
    subjects: List[str]  # e.g., ["Math", "Biology"]
    interests: List[str]  # e.g., ["AI", "Healthcare"]
    skills: List[str]  # e.g., ["Python", "Communication"]
    goals_text: str  # free-text field to extract goals via NLP
    aptitude_scores: Dict[str, float]  # e.g., {"Math": 85.5, "Logic": 78.2}
    preferred_language: str = "en"  # Optional regional language input

# === Load Sentence Transformer for skill/goal matching ===
model = SentenceTransformer("all-MiniLM-L6-v2")

# === Career Knowledge Base ===
career_database = {
    "AI": ["Machine Learning Engineer", "Data Scientist", "AI Researcher"],
    "Healthcare": ["Doctor", "Biotechnologist", "Healthcare Analyst"],
    "Design": ["UX Designer", "Graphic Designer", "Product Designer"],
    "Business": ["Business Analyst", "Entrepreneur", "Product Manager"],
    "Education": ["Teacher", "Education Consultant", "Instructional Designer"],
    "Engineering": ["Mechanical Engineer", "Electrical Engineer", "Civil Engineer"],
    "Law": ["Advocate", "Legal Advisor", "Judge"]
}

career_required_skills = {
    "AI": ["Python", "Math", "Statistics"],
    "Healthcare": ["Biology", "Empathy", "Chemistry"],
    "Design": ["Creativity", "Figma", "Adobe XD"],
    "Business": ["Communication", "Excel", "Finance"],
    "Education": ["Teaching", "Pedagogy", "Patience"],
    "Engineering": ["Physics", "CAD", "Problem Solving"],
    "Law": ["Critical Thinking", "Ethics", "Legal Writing"]
}

exam_alignment = {
    "AI": ["JEE", "GATE"],
    "Healthcare": ["NEET"],
    "Engineering": ["JEE", "GATE"],
    "Law": ["CLAT", "AILET"],
    "Business": ["CAT", "GMAT"],
    "Education": ["CTET", "TET"],
    "Design": ["NID", "UCEED"]
}

career_embeddings = {cat: model.encode(cat, convert_to_tensor=True) for cat in career_database.keys()}

# === Utility Functions ===
def extract_goals_embedding(text: str):
    return model.encode(text, convert_to_tensor=True)

def match_goals_to_domains(goal_embedding):
    scores = {}
    for domain, emb in career_embeddings.items():
        score = util.pytorch_cos_sim(goal_embedding, emb).item()
        scores[domain] = score
    sorted_domains = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [d[0] for d in sorted_domains[:3]]

def skill_gap_analysis(user_skills: List[str], domain: str):
    ideal_skills = set(career_required_skills.get(domain, []))
    user_skills_set = set(user_skills)
    missing = list(ideal_skills - user_skills_set)
    return missing

def aptitude_match(aptitude: Dict[str, float], domain: str):
    domain_weights = {
        "AI": ["Math", "Logic"],
        "Healthcare": ["Biology", "Chemistry"],
        "Engineering": ["Math", "Physics"],
        "Design": ["Creativity"],
        "Business": ["Logic", "Economics"],
        "Education": ["Language", "General Knowledge"],
        "Law": ["Language", "Ethics"]
    }
    weights = domain_weights.get(domain, [])
    scores = [aptitude.get(w, 0) for w in weights]
    return np.mean(scores) if scores else 0

# === API Routes ===
@app.post("/recommendations")
def recommend_careers(profile: UserProfile):
    # Step 1: Extract goal intent via NLP embedding
    goal_embedding = extract_goals_embedding(profile.goals_text)
    top_domains = match_goals_to_domains(goal_embedding)

    # Step 2: Rank domains by aptitude alignment
    domain_scores = [(d, aptitude_match(profile.aptitude_scores, d)) for d in top_domains]
    domain_scores = sorted(domain_scores, key=lambda x: x[1], reverse=True)
    final_domains = [d[0] for d in domain_scores[:3]]

    # Step 3: Match interests + domain overlap
    matched_careers = []
    learning_paths = {}
    exam_paths = {}

    for domain in final_domains:
        matched_careers.extend(career_database[domain])
        skill_gaps = skill_gap_analysis(profile.skills, domain)
        learning_paths[domain] = {
            "missing_skills": skill_gaps,
            "suggested_courses": [f"Learn {s} on SWAYAM" for s in skill_gaps]
        }
        exam_paths[domain] = exam_alignment.get(domain, [])

    if matched_careers:
        random.shuffle(matched_careers)
        return {
            "recommended_domains": final_domains,
            "career_paths": matched_careers[:5],
            "learning_pathways": learning_paths,
            "exam_alignment": exam_paths,
            "language_support": profile.preferred_language
        }
    else:
        raise HTTPException(status_code=404, detail="No career recommendations found.")
@app.post("/top-domains")
def get_top_domains(profile: UserProfile):
    # Extract embedding from goal text
    goal_embedding = extract_goals_embedding(profile.goals_text)
    top_domains = match_goals_to_domains(goal_embedding)

    # Optionally consider aptitude to rank domains
    domain_scores = [(d, aptitude_match(profile.aptitude_scores, d)) for d in top_domains]
    domain_scores = sorted(domain_scores, key=lambda x: x[1], reverse=True)
    final_domains = [d[0] for d in domain_scores[:3]]

    return {"top_domains": final_domains}
  

# === Entry Point ===
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
