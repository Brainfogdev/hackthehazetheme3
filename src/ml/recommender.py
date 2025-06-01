class CareerRecommender:
    def __init__(self, aptitude_model, skill_engine, intent_classifier):
        self.aptitude_model = aptitude_model
        self.skill_engine = skill_engine
        self.intent_classifier = intent_classifier
        
    def recommend(self, user_data):
        # Step 1: Predict academic stream
        stream = self.aptitude_model.predict_stream(user_data["aptitude_scores"])
        
        # Step 2: Analyze career intent
        intent = self.intent_classifier.analyze(
            user_data["interests"],
            ["Engineering", "Medical", "Government", "Business"]
        )
        
        # Step 3: Match skills
        user_skills_vec = self.skill_engine.vectorize_skills(user_data["skills"])
        skill_matches = self.skill_engine.match_careers(user_skills_vec, career_db)
        
        # Combine scores
        final_recommendations = self._calculate_final_scores(
            stream, intent, skill_matches
        )
        
        return sorted(final_recommendations, key=lambda x: x["score"], reverse=True)[:5]
