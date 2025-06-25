from flask import Blueprint,render_template
import pandas as pd
get_music_bp = Blueprint('get_music',__name__)
import random
from app.services.state import current_emotion
from app.services.musicgetter import get_spotify_track_id
@get_music_bp.route('/get_music')
def music():
    clustered_music=pd.read_csv(r"app\static\clustered_music_2.csv")
    mood_map = {
        "Angry":"Powerful/Party", # Angry → Energy
        "Contempt":"Happy/Upbeat",   # Contempt -> Chill
        "Disgust":"Melancholic/Chill",     # Disgust → Chill
        "Fear":"Relaxing/Calm",     # Fear → Chill
        "Happy":"Happy/Upbeat",   # Happy → Happy
        "Neutral":"Relaxing/Calm",   # Neutral → Happy
        "Sad":"Melancholic/Chill",   # Sad → Happy
        "Surprise":"Powerful/Party"  # Surprise -> Energy
    }

    cluster = mood_map.get(current_emotion,"Powerful/Party")
    if cluster=="Powerful/Party":
        genre="Give this a shot — it kinda speaks to moments like this 😇"
    if cluster=="Melancholic/Chill":
        genre="Chilling out feels so Good right? 😌"
    if cluster=="Relaxing/Calm":
        genre="Everything will be okay ☺️"
    if cluster=="Happy/Upbeat":
        genre="Stay happy cause You look so good in a joyous mood 🤗"
    
    filtered_songs = clustered_music[clustered_music['cluster'] == cluster][['song_name', 'singer']]
    selected_index = random.randint(0, len(filtered_songs) - 1)
    selected_song = filtered_songs.iloc[selected_index]
    #getting the url 
    song_id = get_spotify_track_id(selected_song['song_name'],selected_song['singer'])
    if not song_id:
        return render_template("Songs.html", statement="Couldn't fetch a song, Mind Refreshing again", song_name="", spotify_url="", spotify_id="")
    else:
        spotify_embed_url = f"https://open.spotify.com/embed/track/{song_id}"
        return render_template("Songs.html",statement=genre,song_name=selected_song['song_name'], spotify_url=spotify_embed_url, spotify_id=song_id)