import xgboost as xgb
import numpy as np

class AptitudeAnalyzer:
    def __init__(self):
        self.model = xgb.XGBClassifier()
        self.streams = ["Science", "Commerce", "Arts", "Engineering"]
        # Train the model with mock data immediately
        self._train_with_mock_data()
        
    def _train_with_mock_data(self):
        # Mock training data (aptitude scores: math, verbal, logical)
        X = np.array([
            [9, 8, 7],  # Science
            [7, 9, 8],  # Commerce  
            [6, 9, 6],  # Arts
            [9, 7, 9]   # Engineering
        ])
        y = np.array([0, 1, 2, 3])  # 0=Science, 1=Commerce, 2=Arts, 3=Engineering
        
        # Train the model
        self.model.fit(X, y)
        
    def predict_stream(self, scores):
        # scores should be [math_score, verbal_score, logical_score]
        prediction = self.model.predict([scores])[0]
        return self.streams[prediction]
