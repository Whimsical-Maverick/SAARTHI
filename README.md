# 🎯 SAARTHI — Emotion-Based Interactive Companion

Saarthi Clone is an intelligent, modular Flask web application that detects your emotional state in real-time and offers personalized support through:

- 🎵 **Emotion-Aligned Music Suggestions**
- 🎬 **Mood-Driven Movie Discovery**
- 💬 **Empathetic AI Chatbot Conversations**

---

## 📂 Project Structure

```text
SaarthiClone/
│
├── app/
│   ├── __init__.py            # Application Factory
|   ├── Music_recomendaton/    # Algo for music clustering
|   ├── Model/                 # best.pt
│   ├── routes/                # Blueprint-based route files
│   ├── services/              # Core logic for detection, Spotify, chatbot, movies
│   ├── templates/             # HTML templates
|   ├── utils/                 # helper functions(if any) 
│   └── static/                # CSS, JavaScript, pre-clustered datasets
|── config.py                  # Default configs
├── run.py                     # Flask app entry point
├── requirements.txt           # Python dependencies
└── README.md
```

## 🔥 Features

* 🎥 **Real-time Emotion Recognition**

  Continuously captures and interprets user emotions via webcam using a YOLO-based detection model.
* 🎵 **Emotion-Aligned Spotify Integration**

  Curates songs that match the user's detected mood by intelligently mapping emotions to Spotify music clusters.
* 🎬 **Mood-Driven Movie Discovery**

  Recommends emotionally uplifting, calming, or vibe-matching movies based on the user’s current emotional state using semantic similarity and TMDB API.
* 💬 **Empathetic AI Chatbot Companion**

  Integrates Google Gemini to provide emotionally intelligent, trauma-informed conversations designed to offer comfort and support.
* ⚙️ **Scalable Modular Flask Architecture**

  Built using Flask’s Application Factory pattern and Blueprint-based modular structure for clean, maintainable, and scalable design.

## 🚀 Installation

1. **Clone the Repository**

   `git clone https://github.com/your-username/SaarthiClone.git cd SaarthiClone`
2. **Set up a Virtual Environment**

   `python -m venv env `
   `source env/bin/activate   # For Linux/Mac `
   `.\env\Scripts\activate    # For Windows</code>`
3. **Install Dependencies**

   `pip install -r requirements.txt`
4. **Set Environment Variables**

   Create a `.env` file in the root directory:

   `SPOTIFY_CLIENT_ID=your_spotify_client_id`
   `SPOTIFY_CLIENT_SECRET=your_spotify_client_secret`
   `GEMINI_API_KEY=your_google_gemini_api_key`
   `GEMINI_MODEL=gemini-3.5-flash`
   `TMDB_API_KEY=your_tmdb_api_key`
6. **Run the Application**

   `python run.py`

## 🛠️ Tech Stack

* **Backend:** Flask (Python)
* **Frontend:** HTML, CSS, JavaScript
* **Emotion Detection:** YOLOv11, OpenCV
* **Music Integration:** Spotify Web API
* **Movie Recommendation:** TMDB API, Sentence Transformers
* **Chatbot:** Google Gemini (Generative AI)
