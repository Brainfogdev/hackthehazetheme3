# Career Guidance Aptitude Test Project

This project provides an online aptitude test system that integrates with an AI engine for career guidance. Users can take an aptitude test, upload a video interview, and a PDF resume. The AI engine processes these inputs to provide personalized career path recommendations, suggested courses, and relevant competitive exam information.

## Features

* **Aptitude Test:** Users can answer multiple-choice questions to assess their aptitude.
* **Video Interview Upload:** Supports uploading video files for analysis.
* **Resume (PDF) Upload:** Allows users to upload their resumes in PDF format.
* **AI-Powered Career Guidance:** Leverages a large language model (LLM) for:
    * **Resume Parsing:** Extracts key information from PDF resumes.
    * **Audio Transcription:** Transcribes audio from video interviews.
    * **User Summary Generation:** Combines resume and interview data to create a comprehensive user profile.
    * **Career Path Recommendation:** Suggests two suitable career paths.
    * **Course Recommendations:** Proposes relevant courses to enhance career opportunities.
    * **Competitive Exam Information:** Provides details on competitive exams aligned with career paths.
* **MongoDB Integration:** Stores user responses and uploaded file paths in a MongoDB database.
* **Temporary File Handling:** Manages temporary storage and cleanup of uploaded video and PDF files.

## Project Structure

* `ai_engine.py`: Contains the core AI logic, including video-to-audio conversion, audio transcription, resume parsing, and LLM API calls for career guidance.
* `forms.py`: Defines Django forms for handling file uploads and aptitude test submissions.
* `views.py`: Manages the application's views, handling HTTP requests, processing form data, interacting with the AI engine, and rendering templates.
* `test_form.html`: The HTML template for the aptitude test form.
* `serializers.py`: Defines Django REST Framework serializers for the aptitude test questions.
* `aptitude_test_json.json`: A JSON file containing the aptitude test questions and options.

## Setup Instructions

### Prerequisites

* Python 3.x
* Django
* MongoDB
* `ffmpeg` (for video processing with `moviepy`)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <project_directory>
    ```

2.  **Install Python dependencies:**
    (Note: You will need to install these manually as a `requirements.txt` is not provided.)

    ```bash
    pip install django djangorestframework moviepy-ffmpeg openai-whisper pypdf requests pymongo python-slugify
    ```

3.  **Set up MongoDB:**
    Ensure MongoDB is running on `localhost:27017`. The project connects to a database named `user_reponses` and a collection named `user_responses`.

4.  **Configure Django Settings:**
    In your Django project's `settings.py` file, ensure you have:
    * `MEDIA_ROOT` and `MEDIA_URL` configured for file uploads.
    * Add `'rest_framework'` and your app name (e.g., `'aptitude'`) to `INSTALLED_APPS`.

    ```python
    # settings.py
    import os

    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

    INSTALLED_APPS = [
        # ...
        'rest_framework',
        'aptitude', # Your app name
        # ...
    ]
    ```

5.  **Place `aptitude_test_json.json`:**
    Ensure the `aptitude_test_json.json` file is located at `ai_engine/aptitude_test_json.json` as referenced in `views.py`. If you want to change this path, update the `QUESTIONS_DATA` variable in `views.py`.

    Example `aptitude_test_json.json` format:
    ```json
    {
      "questions": [
        {
          "id": 1,
          "text": "What is your preferred working style?",
          "options": {
            "A": "Independent",
            "B": "Team-oriented",
            "C": "Flexible",
            "D": "Structured"
          }
        },......
      ]
    }
    ```

6.  **Run Django Migrations:**
    ```bash
    python manage.py makemigrations aptitude # Replace 'aptitude' with your app name
    python manage.py migrate
    ```

7.  **Start the Django Development Server:**
    ```bash
    python manage.py runserver
    ```

## Usage

1.  Access the aptitude test form by navigating to the appropriate URL in your browser (e.g., `http://127.0.0.1:8000/test-form/`).
2.  Fill in your name and email.
3.  Answer the aptitude test questions.
4.  Upload your video interview file (e.g., `.mp4`).
5.  Upload your PDF resume file.
6.  Click "Submit Test".

The system will process your inputs using the AI engine, and the career guidance results will be displayed on the page.

## AI Engine Details

* **Whisper Model:** The project uses the "medium" Whisper model for audio transcription.
* **LLaMA 3.1 405B Instruct (NVIDIA API):** The project integrates with the NVIDIA API to use the LLaMA 3.1 405B Instruct model for resume parsing, text merging, and career path generation.
    * **NVIDIA API Key:** The `LLAMA_ACCESS_TOKEN` is hardcoded in `ai_engine.py`. **For production environments, it is highly recommended to store this token securely (e.g., environment variables) and avoid hardcoding it.**
* **Prompts:** Specific prompts are used to guide the LLM's responses for resume parsing, text processing, and main career guidance.

## Important Notes

* **API Key Security:** The `LLAMA_ACCESS_TOKEN` in `ai_engine.py` is currently hardcoded. In a real-world application, this should be stored securely using environment variables or a secrets management system.
* **File Paths:** The `aptitude_test_json.json` file path is absolute (`ai_engine/aptitude_test_json.json`). This should be made relative or configurable for better portability.
* **Error Handling:** While some error handling is present, robust error handling and logging should be implemented for production use.
* **Scalability:** For large-scale deployments, consider using asynchronous task queues (e.g., Celery) for the AI processing to avoid blocking the main Django request-response cycle.
* **User Interface:** The provided `test_form.html` is a basic form. A more comprehensive and user-friendly interface would be beneficial for a complete application.
* **Temporary File Cleanup:** While `os.unlink` is used for cleanup, ensure that temporary files are still handled in case of errors during processing to prevent accumulation.
