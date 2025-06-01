# CareerQuestAI (Streamlit)

CareerQuestAI is a Streamlit-based web application that provides data-driven career guidance for students in India. It uses machine learning to deliver personalized career recommendations based on user interests, aptitude tests, and academic profiles. Designed for the Indian education system, it supports streams like PCM, PCB, Commerce, and Arts, and competitive exams such as JEE, NEET, and UPSC. The app features a bilingual interface (English and Hindi), text or voice input, and stores results in memory for a seamless experience.

**GitHub Repository**: github.com/your-username/CareerQuestAI

## **Table of Contents**

- Project Overview
- Folder Structure
- Expected Outputs
- Step-by-Step Working
- Troubleshooting

## **Project Overview**

CareerQuestAI empowers students to make informed career choices by integrating aptitude assessments, interest analysis, and job market insights. It leverages XGBoost for aptitude predictions, Sentence-BERT for interest matching, and mock job market data for visualizations, all processed locally.

### *Key Features*

- **Career Recommendations**: Suggests careers based on interests, academic performance, and exam preferences.
- **Aptitude Testing**: Offers quizzes for skills like math, biology, verbal, and analytical reasoning, tailored to streams and exams.
- **Input Flexibility**: Accepts text or voice interests, with transcription via Hugging Face’s Whisper API.
- **Job Market Insights**: Displays career demand using bar charts with mock data.
- **Bilingual Support**: Provides English and Hindi interfaces and questions.
- **Skill Gap Analysis**: Identifies areas for improvement (e.g., technical or communication skills).
- **Chatbot**: Includes a Grok-powered chatbot (via OpenRouter) for career queries.

## **Folder Structure**

The project is organized as follows.

### *Directory Details*

```
CareerQuestAI/
├── data/
│   └── career_data.csv      # Dataset with career profiles and aptitude scores
├── app.py                   # Main Streamlit application
├── model.py                 # ML models, question bank, and prediction logic
├── utils.py                 # Utility functions for text processing and translation
├── requirements.txt         # Python dependencies
```

- **data/career_data.csv**: Contains career data (e.g., `career`, `math_score`, `biology_score`) for ML training.
- **app.py**: Manages the Streamlit UI, user inputs, and result rendering.
- **model.py**: Includes XGBoost models, Sentence-BERT, and aptitude test questions.
- **utils.py**: Provides text cleaning, translation, and interest processing functions.
- **requirements.txt**: Lists pinned dependencies for reproducibility.


## Technology Stack
- **Frontend**: Streamlit 1.22.0
- **Backend**: Python 3.8+
- **Machine Learning**:
  - Sentence-BERT (`sentence-transformers==2.2.2`) for interest embedding
  - XGBoost (`xgboost==1.6.2`) for aptitude and skill gap predictions
  - Scikit-learn 1.0.2 for data preprocessing
- **APIs**:
  - OpenRouter (LLaMA 3.1 8B) for chatbot responses
  - Hugging Face Whisper for audio transcription
- **Visualization**: Seaborn 0.11.2, Matplotlib 3.5.3
- **Dependencies**: Defined in `requirements.txt`
- **Environment**: Conda (recommended)

## **Expected Outputs**

Results for sample inputs when processed via Streamlit.

### *Text Input Example*

**Input**:

- Stage: After 12th
- Stream: PCB
- Exam: NEET
- Interests: "medicine, patient care"
- Aptitude Test: Biology (80%), Verbal (70%)

**Output**:

```
Career Recommendation: Doctor
Match Score: High
Skill Gaps: Improve communication skills
Job Market Demand: 85.0%
Output displayed in Streamlit interface
```

### *Voice Input Example*

**Input**:

- Voice: "I like coding and technology"
- Stage: 11th/12th
- Stream: PCM
- Aptitude Test: Math (90%), Coding (85%)

**Output**:

```
Career Recommendation: Software Engineer
Match Score: High
Skill Gaps: Enhance problem-solving skills
Job Market Demand: 90.0%
Output displayed in Streamlit interface
```

## **Step-by-Step Working**

Steps to set up and run the project.

### *Prerequisites*

- Anaconda at `C:\Users\THINKPAD\.conda`.
- VS Code with Python extension.
- Git for version control.
- Python 3.8 in `career_guidance` Conda environment.

### *Step 1: Clone the Repository*

1. Open Anaconda Prompt.

2. Navigate to:

   ```
   cd C:\Users\THINKPAD\CareerQuestAI
   ```

3. Clone (if not already local):

   ```
   git clone https://github.com/your-username/CareerQuestAI.git
   ```

4. Enter directory:

   ```
   cd CareerQuestAI
   ```

### *Step 2: Set Up Conda Environment*

1. Activate environment:

   ```
   conda activate career_guidance
   ```

2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

### *Step 3: Verify Input Files*

Ensure `data/` contains:

- `career_data.csv`

### *Step 4: Run Streamlit App*

1. Launch:

   ```
   streamlit run app.py
   ```

2. Open `http://localhost:8501`.

3. Input interests, academic details, and take the aptitude test to view results.

### *Step 5: Verify Outputs*

1. Check Streamlit interface for recommendations and job market charts.

2. Verify session state in memory for saved inputs.

### *Step 6: Push to GitHub*

1. Commit changes:

   ```
   git add .
   git commit -m "Updated README formatting"
   git push origin main
   ```

## Future Improvements

To enhance CareerQuestAI’s functionality and impact, the following enhancements are planned:

Improved Model Precision: Incorporate advanced models (e.g., transformer-based classifiers) for more accurate career predictions.

Real-Time Market Data: Integrate APIs from job platforms (e.g., Naukri, LinkedIn) for dynamic demand insights.

Additional Language Support: Expand to include regional languages like Tamil or Bengali.

Adaptive Assessments: Implement dynamic question difficulty based on user responses using item response theory.

Cloud Deployment: Host on cloud platforms (e.g., AWS, Heroku) for broader accessibility.

Skill Development Integration: Link with e-learning platforms to recommend courses for skill gaps.