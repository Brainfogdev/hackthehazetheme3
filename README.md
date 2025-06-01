# AI-Powered Career Guidance Engine

## 🚀 Overview

This project is an AI-powered career guidance engine designed for the Indian education system. It leverages machine learning and NLP to analyze a user’s aptitude, aspirations, skills, and experience, and recommends personalized career paths aligned with Indian academic streams, competitive exams, and job market trends.

## 🧠 Features

- **Aptitude Estimation:** ML model predicts user’s natural academic strengths from test scores.
- **NLP-Driven Goal & Interest Extraction:** Extracts and analyzes user aspirations from free-text input.
- **Skill & Experience Mapping:** Matches user-selected skills to career profiles using vector embeddings.
- **AI-Driven Career Recommendation:** Suggests optimal career paths (e.g., UPSC, NEET, JEE, CA, etc.) based on Indian education and job trends.
- **Skill Gap Analysis:** Identifies missing competencies and recommends learning pathways.

## 🗂️ Folder Structure

CareerGuidanceEngine/
│
├── frontend/ # Streamlit app and UI logic
├── models/ # ML and NLP model classes
├── src/ # NLP and utility scripts
├── data/ # Career database and static data
├── config/ # Configuration files (if any)
├── notebooks/ # Jupyter notebooks (optional)
├── requirements.txt # Python dependencies
├── .dockerignore # Docker ignore file
├── Dockerfile # Docker build file (optional)
└── README.md # Project documentation



## ⚙️ Setup Instructions

1. **Clone the repository:**
    ```
    git clone https://github.com/<AtulBoyal>/hackthehazeAITheme.git
    cd hackthehazeAITheme
    ```

2. **(Optional) Create and activate a virtual environment:**
    ```
    python -m venv venv
    venv\Scripts\activate  # On Windows
    # or
    source venv/bin/activate  # On Mac/Linux
    ```

3. **Install dependencies:**
    ```
    pip install -r requirements.txt
    ```

4. **Run the app:**
    ```
    python -m streamlit run frontend/app.py
    ```
    The app will open in your browser at [http://localhost:8501](http://localhost:8501).

## 📝 Usage

1. **Enter your aptitude scores** (Math, Verbal, Logical) using sliders.
2. **Describe your career interests** in the provided text area.
3. **Select your skills** from the multi-select list.
4. **Click "Get Recommendations"** to view your top career matches and skill gap analysis.

## 📊 Example Inputs

- **Aptitude Scores:** 85 (Math), 78 (Verbal), 90 (Logical)
- **Career Interests:** “I want to help people and work in healthcare”
- **Skills:** Biology, Chemistry, Empathy

## 🎯 Output

- Top 5 personalized career recommendations
- Required exams for each career
- Skill gap analysis for each recommended career

## 👨‍💻 Authors

- Atul

## 🏷️ License

This project is licensed under the MIT License.

## 🙏 Acknowledgements

- [Unstop Hack The Haze](https://unstop.com/)
- Open-source ML/NLP libraries: scikit-learn, xgboost, sentence-transformers, transformers

**Good luck, and thank you for reviewing our submission!**
