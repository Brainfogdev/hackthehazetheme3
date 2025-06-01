import streamlit as st
import json
import os
from models.aptitude import AptitudeAnalyzer
from src.nlp.intent_analyzer import CareerIntentClassifier
from models.skill_mapper import SkillEngine

# Load career database
@st.cache_data
def load_career_db():
    career_path = os.path.join(os.path.dirname(__file__), "..", "data", "careers.json")
    try:
        with open(career_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Fallback if file doesn't exist
        return [
            {
                "id": "upsc_ias",
                "title": "IAS Officer (UPSC)",
                "required_skills": ["General Knowledge", "Essay Writing"],
                "exams": ["UPSC CSE"]
            },
            {
                "id": "jee_engineer",
                "title": "Software Engineer (JEE)",
                "required_skills": ["Python", "Problem Solving"],
                "exams": ["JEE"]
            }
        ]

career_db = load_career_db()

def process_inputs(aptitude_scores, interests, skills):
    # Instantiate models
    aptitude_model = AptitudeAnalyzer()
    skill_engine = SkillEngine()
    intent_classifier = CareerIntentClassifier()

    # Predict stream
    stream = aptitude_model.predict_stream(aptitude_scores)

    # Analyze intent
    intent = intent_classifier.analyze(
        interests,
        ["Engineering", "Medical", "Government", "Business"]
    )

    # Skill matching
    user_skills_vec = skill_engine.vectorize_skills(skills)
    skill_matches = skill_engine.match_careers(user_skills_vec, career_db)

    # Combine scores
    recommendations = []
    for match in skill_matches:
        career_id, similarity = match
        career = next((c for c in career_db if c["id"] == career_id), None)
        if career:
            recommendations.append({
                "title": career["title"],
                "score": similarity,
                "exams": career["exams"],
                "missing_skills": list(set(career["required_skills"]) - set(skills))
            })
    
    return recommendations[:5]

def main():
    st.title("AI Career Guidance Engine")
    
    with st.form("user_input"):
        math_score = st.slider("Math Aptitude Score", 0, 100, 75)
        verbal_score = st.slider("Verbal Aptitude Score", 0, 100, 80)
        logical_score = st.slider("Logical Aptitude Score", 0, 100, 85)
        interests = st.text_area("Career Interests")
        skills = st.multiselect("Your Skills", [
            "Python", "Biology", "Accounting", "Essay Writing", "General Knowledge",
            "Problem Solving", "Mathematics", "C++", "Java", "Public Speaking", "Teamwork",
            "Leadership", "Critical Thinking", "Data Analysis", "Communication", "Marketing"])
        submitted = st.form_submit_button("Get Recommendations")

    if submitted:
        try:
            aptitude_scores = [math_score, verbal_score, logical_score]
            recommendations = process_inputs(aptitude_scores, interests, skills)
            
            st.subheader("Top Career Recommendations")
            for idx, rec in enumerate(recommendations[:5], 1):
                st.markdown(f"""
                **{idx}. {rec['title']}**  
                *Match Score*: {rec['score']:.2f}  
                *Required Exams*: {", ".join(rec['exams'])}  
                *Skill Gap*: {", ".join(rec['missing_skills']) if rec['missing_skills'] else 'None'}
                """)
                
        except Exception as e:
            st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
