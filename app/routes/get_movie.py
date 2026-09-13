from flask import Blueprint,request,jsonify
import requests
import os
import unicodedata
import json
import time
from google import genai
from emoji import demojize
from app.services.movie import find_closest_emotion
get_movie_bp = Blueprint('get_movie',__name__)


def classify_emotion_with_ai(prompt, emotion_labels):
    """Use Gemini for context-aware classification; return None on failure."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None

    try:
        client = genai.Client(api_key=api_key)
        labels = ", ".join(emotion_labels)
        response = client.models.generate_content(
            model=os.getenv("GEMINI_MODEL", "gemini-3.5-flash"),
            contents=(
                "Classify the user's emotional state for a movie recommendation. "
                f"Choose exactly one label from: {labels}. "
                "Return only valid JSON in this format: "
                '{"emotion": "one_label"}. '
                f"User text: {prompt}"
            ),
            config={"temperature": 0, "max_output_tokens": 30},
        )
        result = json.loads(response.text)
        emotion = result.get("emotion")
        return emotion if emotion in emotion_labels else None
    except (Exception, json.JSONDecodeError):
        return None
@get_movie_bp.route('/get_movie', methods=['GET', 'POST'])
def get_movie():
        payload = request.get_json(silent=True) or {}
        prompt = payload.get('Feeling')
        if not isinstance(prompt, str) or not prompt.strip():
            return jsonify({"error": "No emotion prompt provided"}), 400

        # Convert any supported Unicode emoji into its English name, so new
        # emojis work without maintaining a manual emotion dictionary.
        emoji_text = demojize(prompt, delimiters=(" ", " "))
        emoji_text = emoji_text.replace("_", " ").replace(":", " ")
        normalized_prompt = unicodedata.normalize("NFKC", emoji_text)
        text_prompt = "".join(
            char for char in normalized_prompt
            if unicodedata.category(char) not in {"So", "Sk", "Cf"}
        ).strip()
        if not text_prompt:
            return jsonify({"error": "Please include a few words about how you feel"}), 400

        # Define emotions and their descriptions
        emotions = {
            "Anger": "I am furious, irritated, or full of rage",
            "Contempt": "I feel superior and dismissive, like others aren't worth my attention",
            "Disgust": "I am sickened, revolted, or strongly put off by something",
            "Fear": "I am scared, anxious, or deeply worried about something",
            "Happy": "I feel joyful, cheerful, and full of positivity",
            "Neutral": "I feel calm, indifferent, or without any strong emotion",
            "Sad": "I feel down, hopeless, or like crying",
            "Surprise": "I am shocked, amazed, or caught off guard by something unexpected"
        }

        try:
            matched_emotion = classify_emotion_with_ai(text_prompt, emotions.keys())
            if not matched_emotion:
                matched_emotion = find_closest_emotion(text_prompt, emotions)
        except Exception:
            return jsonify({"error": "Unable to understand that feeling right now"}), 502

        emotion_to_uplifting_genres = {
            "Anger": [35, 16, 10402, 10751],       # Comedy, Animation, Music, Family
            "Contempt": [10749, 10402, 12],        # Romance, Music, Adventure
            "Disgust": [35, 16, 14],               # Comedy, Animation, Fantasy
            "Fear": [10751, 10402, 35],            # Family, Music, Comedy
            "Happy": [12, 28, 14, 878],            # Adventure, Action, Fantasy, Sci-Fi (keep energy up)
            "Neutral": [99, 36, 12],               # Documentary, History, Adventure (for curiosity/engagement)
            "Sad": [35, 16, 10402, 14],            # Comedy, Animation, Music, Fantasy (light and uplifting)
            "Surprise": [10749, 12, 35],           # Romance, Adventure, Comedy (gentle excitement)
        }

        url = 'https://api.themoviedb.org/3/discover/movie'
        headers = {
            'Accept': 'application/json',
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36" # More complete User-Agent
        }

        tmdb_api_key = os.getenv('TMDB_API_KEY')
        if not tmdb_api_key:
            return jsonify({"error": "TMDB_API_KEY is not configured"}), 503

        params = {
            'api_key': tmdb_api_key,
            'with_genres': ','.join(map(str, emotion_to_uplifting_genres.get(matched_emotion, []))), # Use .get() with default empty list
            'sort_by': 'popularity.desc',
            'language': 'en-US',
            'page': 1
        }

        response = None
        max_attempts = 5
        for attempt in range(max_attempts):
            try:
                response = requests.get(url, headers=headers, params=params, timeout=10)

                # Retry only temporary TMDB server failures. Do not retry 4xx
                # responses, especially 401/403/429, to avoid wasting quota.
                if 500 <= response.status_code < 600 and attempt < max_attempts - 1:
                    time.sleep(min(0.75 * (2 ** attempt), 5))
                    continue

                response.raise_for_status()
                return jsonify(response.json())
            except requests.HTTPError as exc:
                status_code = exc.response.status_code if exc.response is not None else None
                if status_code == 401:
                    return jsonify({"error": "TMDB_API_KEY is invalid"}), 502
                if status_code == 403:
                    return jsonify({"error": "TMDB rejected this API key"}), 502
                if status_code == 429:
                    return jsonify({"error": "TMDB rate limit reached; try again later"}), 429
                return jsonify({"error": f"TMDB returned HTTP {status_code}"}), 502
            except ValueError:
                return jsonify({"error": "TMDB returned an invalid response"}), 502
            except (requests.Timeout, requests.ConnectionError):
                if attempt == max_attempts - 1:
                    return jsonify({"error": "TMDB is unavailable right now"}), 502
                time.sleep(min(0.75 * (2 ** attempt), 5))

        return jsonify({"error": "TMDB is unavailable right now"}), 502
