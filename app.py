import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from model import get_random_questions, score_test, predict_career, analyze_job_market
from utils import process_input, translate_ui
import random
import uuid
from streamlit_mic_recorder import mic_recorder
from typing import Dict, List, Optional, Any
import requests
import os
from openai import OpenAI
from sentence_transformers import SentenceTransformer
import httpx

st.set_page_config(page_title="CareerQuestAI", page_icon="🌟", layout="wide")

def transcribe_audio(audio_bytes: bytes) -> str:
    """Transcribe audio using Hugging Face Whisper API."""
    try:
        url = "https://api-inference.huggingface.co/models/openai/whisper-tiny"
        headers = {"Authorization": f"Bearer {os.getenv('HF_API_TOKEN', '')}"}
        response = requests.post(url, headers=headers, data=audio_bytes)
        if response.status_code == 200:
            return response.json().get("text", "")
        return ""
    except Exception:
        return ""

def get_chatbot_response(user_input: str, lang_code: str) -> str:
    """Get response from Grok for any user question."""
    prompt = f"""
    User Question: {user_input}
    Provide a concise, helpful answer (2-4 sentences) in {'Hindi' if lang_code == 'hi' else 'English'}.
    If needed, use general knowledge or context relevant to career guidance and Indian education.
    """
    try:
        response = st.session_state.grok_api.chat.completions.create(
            model="meta-llama/llama-3.1-8b-instruct:free",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception:
        return "Sorry, I couldn't process that. Please try again!" if lang_code == "en" else "क्षमा करें, मैं इसे प्रोसेस नहीं कर सका। कृपया पुनः प्रयास करें!"

def main():
    # Initialize Grok API
    if "grok_api" not in st.session_state:
        st.session_state.grok_api = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY"),
            http_client=httpx.Client()
        )
    
    # Initialize Sentence-BERT
    embedder = SentenceTransformer('all-MiniLM-L6-v2')

    # Language Selection
    lang = st.sidebar.selectbox(
        "Language / भाषा",
        ["English", "Hindi"],
        key="lang_select",
        help="Choose your preferred language"
    )
    lang_code = "en" if lang == "English" else "hi"
    ui = translate_ui(lang_code)

    # Validate UI dictionary
    required_keys = [
        "title", "interests", "interests_placeholder", "stage", "academic_performance",
        "score_option", "slider", "test", "enter_scores", "aptitude_test", "exam_type",
        "exam_score", "degree_type", "score_type", "recommendation", "job_market",
        "success_message", "complete_fields"
    ]
    missing_keys = [key for key in required_keys if key not in ui]
    if missing_keys:
        st.error(f"Translation error: missing keys {missing_keys}. Using English defaults.")
        ui = translate_ui("en")

    # General Chatbot in Sidebar
    st.sidebar.subheader("Ask Away!" if lang_code == "en" else "कुछ भी पूछें!")
    user_question = st.sidebar.text_input(
        "Type your question..." if lang_code == "en" else "अपना प्रश्न टाइप करें...",
        key="chatbot_input",
        help="Ask anything about careers, studies, or more!"
    )
    if user_question:
        with st.sidebar:
            with st.spinner("Thinking..." if lang_code == "en" else "सोच रहा हूँ..."):
                response = get_chatbot_response(user_question, lang_code)
            with st.chat_message("assistant"):
                st.markdown(response)

    # Custom CSS
    st.markdown("""
        <style>
        .stApp { background-color: #E6F3FA; }
        .stButton>button { background-color: #66BB6A; color: white; border-radius: 10px; }
        .stProgress .st-bo { background-color: #66BB6A; }
        h1, h2, h3 { color: #333333; }
        .stTextInput, .stNumberInput, .stSelectbox { background-color: #F5FAFD; border:1px solid #B0BEC5; }
        .welcome { text-align: center; font-size: 1.5em; color: #0288D1; }
        .stSelectbox [data-baseweb="select"] { cursor: pointer; }
        .badge { background-color: #FFF3E0; padding: 10px; border-radius: 5px; margin: 0; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 class='welcome'>Hey there! Ready to discover your dream career? 🚀</h1>", unsafe_allow_html=True)
    st.title(ui["title"])

    # Interests Input
    st.subheader(ui["interests"])
    interest_method = st.radio(
        "How would you like to share your interests?" if lang_code == "en" else "आप अपनी रुचियां कैसे साझा करना चाहेंगे?",
        ["Text", "Voice"],
        help="Type or speak your passions!"
    )

    processed_interests = ""
    interest_embeddings = []
    if interest_method == "Text":
        interests = st.text_area(
            "Your Interests" if lang_code == "en" else "आपकी रुचियां",
            placeholder=ui["interests_placeholder"],
            key="text_interests",
            help="E.g., coding, dancing, medicine..."
        )
        if interests:
            processed_interests, interest_embeddings = process_input(interests, lang_code)
            processed_interests = " ".join(processed_interests)
            st.success("✅ Interests saved!" if lang_code == "en" else "✅ रुचियां सहेजी गईं!")
    else:
        audio = mic_recorder(
            start_prompt="🎙️ Start Recording" if lang_code == "en" else "🎙️ रिकॉर्डिंग शुरू करें",
            stop_prompt="⏹️ Stop Recording" if lang_code == "en" else "⏹️ रिकॉर्डिंग रोकें",
            key="audio_interests"
        )
        if audio and audio.get("bytes"):
            transcribed = transcribe_audio(audio["bytes"])
            if transcribed:
                processed_interests, interest_embeddings = process_input(transcribed, lang_code)
                processed_interests = " ".join(processed_interests)
                st.success("✅ Voice interests saved!" if lang_code == "en" else "✅ आवाज रुचियां सहेजी गईं!")
                st.write(f"Transcribed: {transcribed}")

    # Academic Stage
    st.subheader(ui["stage"])
    stage = st.selectbox("", ["9th/10th", "11th/12th", "After 12th", "Post-Graduation"], help="Where are you in your journey?")

    # Stream Selection
    stream = "PCM"
    exam_type = None
    degree_type = None
    if stage in ["11th/12th", "After 12th", "Post-Graduation"]:
        stream = st.selectbox(
            "Choose Your Stream" if lang_code == "en" else "अपनी स्ट्रीम चुनें",
            ["PCM", "PCB", "Commerce", "Arts"],
            help="Select your 11th/12th stream (e.g., PCM for JEE, PCB for NEET)."
        )

    # Academic Performance
    st.subheader(ui["academic_performance"])
    academic_data: Dict[str, Any] = {}
    col1, col2 = st.columns(2)
    if stage == "9th/10th":
        with col1:
            academic_data["7th"] = st.number_input("7th Std %", 0.0, 100.0, 0.0, help="Enter your 7th grade percentage.")
        with col2:
            academic_data["8th"] = st.number_input("8th Std %", 0.0, 100.0, 0.0, help="Enter your 8th grade percentage.")
    elif stage == "11th/12th":
        with col1:
            academic_data["9th"] = st.number_input("9th Std %", 0.0, 100.0, 0.0, help="Enter your 9th grade percentage.")
        with col2:
            academic_data["10th"] = st.number_input("10th Std %", 0.0, 100.0, 0.0, help="Enter your 10th grade percentage.")
    elif stage == "After 12th":
        with col1:
            academic_data["11th"] = st.number_input("11th Std %", 0.0, 100.0, 0.0, help="Enter your 11th grade percentage.")
            academic_data["12th"] = st.number_input("12th Std %", 0.0, 100.0, 0.0)
        with col2:
            exam_type = st.selectbox(
                ui["exam_type"],
                ["None", "JEE", "NEET", "CLAT", "CAT", "SAT", "UPSC", "GATE", "Other"],
                help="Selected PCB? Try NEET! PCM? JEE is great!"
            )
            academic_data["competitive"] = st.text_input(
                ui["exam_score"],
                placeholder="e.g., 150/360",
                help="Enter your score (e.g., 150/360 for JEE)."
            ) if exam_type != "None" else f"{exam_type}: N/A"
    else:  # Post-Graduation
        with col1:
            degree_type = st.selectbox(
                ui["degree_type"],
                ["B.Tech", "B.Sc", "B.Com", "B.A", "BBA", "MBBS", "LLB", "Other"],
                help="Choose your undergraduate degree."
            )
            score_type = st.radio(ui["score_type"], ["Percentage", "CGPA"], help="CGPA? Multiply by 9.5 for % (e.g., 8 CGPA = 76%).")
            if score_type == "Percentage":
                academic_data["degree_score"] = st.number_input("Degree %", 0.0, 100.0, 0.0)
            else:
                cgpa = st.number_input("CGPA (out of 10)", 0.0, 10.0, 0.0)
                st.info("Convert CGPA to %: Multiply by 9.5 (e.g., 8 CGPA = 76%)")
                academic_data["degree_score"] = cgpa * 9.5
            academic_data["degree_type"] = degree_type
        with col2:
            exam_type = st.selectbox(
                ui["exam_type"],
                ["None", "CAT", "GATE", "UPSC", "GRE", "GMAT", "Other"],
                help="B.Tech? Try GATE! BBA? CAT is awesome!"
            )
            academic_data["competitive"] = st.text_input(
                ui["exam_score"],
                placeholder="e.g., 150/360"
            ) if exam_type != "None" else f"{exam_type}: N/A"

    # Score Input Option
    st.subheader(ui["score_option"])
    score_option = st.radio("", [ui["slider"], ui["test"]], help="Quiz is fun, or slide if you know your scores!")

    # Define categories
    categories = {
        "PCM": ["math", "physics", "chemistry", "analytical", "verbal", "extra", "activity"],
        "PCB": ["biology", "physics", "chemistry", "analytical", "verbal", "extra", "activity"],
        "Commerce": ["math", "accounting", "analytical", "verbal", "extra", "activity"],
        "Arts": ["verbal", "analytical", "extra", "activity"]
    }.get(stream, ["math", "verbal", "analytical", "physics", "chemistry", "extra", "activity"])
    if stage == "Post-Graduation" and degree_type:
        categories = {
            "B.Tech": ["coding", "math", "analytical", "verbal", "extra"],
            "B.Com": ["accounting", "math", "analytical", "verbal", "extra"],
            "B.Sc": ["biology", "physics", "chemistry", "analytical", "verbal", "extra"],
            "B.A": ["verbal", "analytical", "extra"],
            "BBA": ["accounting", "analytical", "verbal", "extra"],
            "MBBS": ["biology", "extra", "analytical", "verbal"],
            "LLB": ["verbal", "analytical", "extra"],
            "Other": ["math", "verbal", "analytical", "extra"]
        }.get(degree_type, ["math", "verbal", "analytical", "extra"])
    if exam_type and exam_type != "None":
        exam_categories = {
            "JEE": ["math", "physics", "chemistry", "analytical", "verbal"],
            "NEET": ["biology", "physics", "chemistry", "analytical", "verbal"],
            "CLAT": ["verbal", "analytical", "extra"],
            "CAT": ["math", "analytical", "verbal", "extra"],
            "UPSC": ["verbal", "analytical", "extra"],
            "GATE": ["coding", "math", "analytical", "verbal"],
            "SAT": ["math", "verbal", "analytical", "extra"],
            "Other": categories
        }
        categories = exam_categories.get(exam_type, categories)

    scores = {cat: 0.0 for cat in categories}

    # Reset test state if configuration changes
    config_key = (stage, stream, exam_type, degree_type)
    if "last_config" not in st.session_state or st.session_state.last_config != config_key:
        st.session_state.test_state = None
        st.session_state.last_config = config_key

    if score_option == ui["slider"]:
        st.subheader(ui["enter_scores"])
        for cat in categories:
            scores[cat] = st.slider(
                f"{cat.capitalize()} Score",
                0.0, 100.0, 50.0,
                help=f"Rate your {cat} skills!"
            )
    else:
        st.subheader(ui["aptitude_test"])
        if not st.session_state.get("test_state"):
            session_id = uuid.uuid4().hex
            st.session_state.test_state = {
                "current_cat": 0,
                "session_id": session_id,
                "questions": {
                    cat: get_random_questions(cat, stage, stream, exam_type, degree_type, num_questions=10, session_id=session_id)
                    for cat in categories
                },
                "user_answers": {cat: {} for cat in categories},
                "test_completed": False
            }

        state = st.session_state.test_state

        if not state["test_completed"]:
            current_cat = categories[state["current_cat"]]
            questions = state["questions"][current_cat]
            st.write(f"Category: {current_cat.capitalize()} ({state['current_cat'] + 1}/{len(categories)})")
            st.progress((state["current_cat"] + 1) / len(categories))

            for i, q in enumerate(questions):
                st.write(f"Question {i + 1}: {q['text_en' if lang_code == 'en' else 'text_hi']}")
                if q["type"] == "multiple":
                    answers = st.multiselect(
                        f"Select all that apply (Q{i + 1})",
                        q["options"],
                        key=f"q_{q['id']}_{i}"
                    )
                else:
                    answers = [st.radio(
                        f"Select one (Q{i + 1})",
                        q["options"],
                        key=f"q_{q['id']}_{i}"
                    )]
                state["user_answers"][current_cat][q["id"]] = answers

            if st.button("Next Category"):
                state["current_cat"] += 1
                if state["current_cat"] >= len(categories):
                    state["test_completed"] = True
                    for cat in categories:
                        scores[cat] = score_test(state["questions"][cat], state["user_answers"][cat])
                st.experimental_rerun()
        if state["test_completed"]:
            st.write("Test Completed! Your Scores:")
            for cat in categories:
                st.write(f"{cat.capitalize()}: {scores[cat]:.2f}%")

    # Generate Recommendation
    if processed_interests and any(score > 0 for score in scores.values()):
        career_info = predict_career(
            processed_interests,
            scores,
            academic_data,
            stage,
            stream,
            exam_type,
            degree_type,
            lang_code,
            interest_embeddings,
            embedder
        )
        job_market = analyze_job_market([
            "Software Engineer", "Doctor", "MBA", "Lawyer", "Civil Servant",
            "Nurse", "Mechanical Engineer", "Chartered Accountant", "Biomedical Scientist", "Data Scientist"
        ])

        st.subheader(ui["recommendation"])
        st.markdown(career_info, unsafe_allow_html=True)

        st.subheader(ui["job_market"])
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=job_market, x="Career", y="Demand", hue="Career", ax=ax)
        ax.set_title("Job Market Demand (%)", fontsize=16)
        ax.set_xlabel("Career", fontsize=12)
        ax.set_ylabel("Demand (%)", fontsize=12)
        ax.legend_.remove()  # Suppress legend
        for i, bar in enumerate(ax.patches):
            if i < len(job_market):
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height(),
                    f"{job_market['Demand'].iloc[i]:.1f}%",
                    ha="center"
                )
        plt.xticks(rotation=45)
        st.pyplot(fig)

        st.balloons()
        st.success(ui["success_message"])
    elif score_option == ui["test"] and state.get("test_completed"):
        st.info("Please provide your interests to generate a recommendation." if lang_code == "en" else "कृपया अपनी रुचियां प्रदान करें ताकि सिफारिश उत्पन्न हो सके।")
    else:
        st.info(ui["complete_fields"])

if __name__ == "__main__":
    main()