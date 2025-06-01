from sentence_transformers import SentenceTransformer
import numpy as np

class SkillEngine:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
    def vectorize_skills(self, skills):
        if not skills:
            return np.zeros(384)  # Default embedding size
        return self.model.encode(", ".join(skills))
    
    def match_careers(self, user_vec, career_db, threshold=0.3):
        matches = []
        for career in career_db:
            if "required_skills" in career:
                career_vec = self.model.encode(", ".join(career["required_skills"]))
                similarity = np.dot(user_vec, career_vec) / (np.linalg.norm(user_vec) * np.linalg.norm(career_vec))
                if similarity > threshold:
                    matches.append((career["id"], similarity))
        return sorted(matches, key=lambda x: x[1], reverse=True)
