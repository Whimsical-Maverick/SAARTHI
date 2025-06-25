from flask import Blueprint,request,jsonify
import requests
import os
from app.services.movie import find_closest_emotion
get_movie_bp = Blueprint('get_movie',__name__)
@get_movie_bp.route('/get_movie', methods=['GET', 'POST'])
def get_movie():
        # Get the emotion prompt from the request form
        prompt = request.form.get('name')
        if not prompt:
            # Return a bad request error if no emotion is provided
            return jsonify({"error": "No emotion prompt provided"}), 400

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

        matched_emotion = find_closest_emotion(prompt, emotions)

        # Define genre IDs for each emotion (from your original code)
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

        # Construct the TMDB API URL and headers
        url = 'https://api.themoviedb.org/3/discover/movie'
        headers = {
            'Accept': 'application/json',
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36" # More complete User-Agent
        }

        # Get TMDB API key from environment variables
        tmdb_api_key = os.getenv('TMDB_API_KEY')

        # Prepare parameters for the TMDB API request
        params = {
            'api_key': tmdb_api_key,
            'with_genres': ','.join(map(str, emotion_to_uplifting_genres.get(matched_emotion, []))), # Use .get() with default empty list
            'sort_by': 'popularity.desc',
            'language': 'en-US',
            'page': 1
        }

        # Make the request to TMDB API
        response = requests.get(url, headers=headers, params=params, timeout=10) # Add a timeout

        # Attempt to parse JSON response
        tmdb_data = response.json()
        return tmdb_data