from flask import Flask, render_template, request, redirect, url_for,Response,session,jsonify
import cv2
import numpy as np
import pandas as pd
import tensorflow as tf
import keras
import requests
import random
from bs4 import BeautifulSoup
import re
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
# from dotenv import load_dotenv
import os
from ultralytics import YOLO
try:
    emotion=np.load("emotion.npy")
except:
    emotion=""
app = Flask(__name__)
# app.secret_key=os.getenv("SECRET_KEY")
app.secret_key="f9a8c1b7e2d3g4h5i6j7k8l9m0n1o2p3q4r5s6t7u8v9w0x1y2z3a4b5"

label_dict= {
   0:"Anger",
   1:"Contempt",
   2:"Disgust" ,
   3:"Fear",
   4:"Happy",
   5:"Neutral",
   6:"Sad",
   7:"Surprise",
}

# Flag to control the video feed
is_feed_running = False

def generate_frames():
    global is_feed_running
    video = cv2.VideoCapture(0)
    model=YOLO('best.pt')
    while is_feed_running:
        ret, frame = video.read()
        if not ret:
            break

        result = model(frame)[0];#being only 1 frame as input,still [0] as it returns a list of output for each frame\
        for box in result.boxes:
            x1,y1,x2,y2 = map(int,box.xyxy[0])
            conf =float(box.conf[0])
            cls = int(box.cls[0])
            emotion = label_dict[cls]

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, emotion, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX,0.8, (0, 255, 0), 2)
        np.save("emotion.npy", np.array([cls]))
        # Encode the frame to send it to the frontend
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        

    video.release()

URLS = {
    "Family": 'https://www.imdb.com/search/title/?title_type=feature&genres=family',
    "Musical":'https://www.imdb.com/search/title/?title_type=feature&genres=musical',
    "Sport":'https://www.imdb.com/search/title/?title_type=feature&genres=sport',
    "Thriller":"https://www.imdb.com/search/title/?title_type=feature&genres=thriller",
    "Fantasy":"https://www.imdb.com/search/title/?title_type=feature&genres=fantasy",
    "Drama":'https://www.imdb.com/search/title/?title_type=feature&genres=drama',
    "Film-Noir":'https://www.imdb.com/search/title/?title_type=feature&genres=film-noir'
}

clustered_music=pd.read_csv(r"static\clustered_music_2.csv")

def fetch_movie_titles(emotion):
    url = URLS.get(emotion)
    if not url:
        return []

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    cleaned_movies=[]
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check for HTTP errors
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    movies = [a.get_text() for a in soup.find_all('a', href=re.compile(r'/title/tt\d+/'))]
    cleaned_movies = [movie.split(". ", 1)[1] if ". " in movie else movie for movie in movies]
    cleaned_movies = [movie.strip() for movie in cleaned_movies if movie.strip()]
    return cleaned_movies



def get_spotify_track_id(song_name,artist_name):
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id="0ffa3310f19e47ec81e23881c687e33d",
    client_secret="5c3c9ddadf0146218ec44f7d24199e89"
    ))

    query=f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=query,type="track",limit=1)

    if results["tracks"]["items"]:
        track_id = results["tracks"]["items"][0]["id"]
    else:
        track_id=None
    
    del sp
    return track_id

@app.route('/', methods=["GET","POST"])
def homepage():
        session["name"]= request.form.get('Name')
        session["age"]= request.form.get('Age')
        session["gender"]= request.form.get('Gender')
        action = request.form.get('action')  # Get the value of the clicked button
        if action == "High_Five!":
            return redirect(url_for('live_feed'))
        return render_template("login.html")

@app.route('/live-feed')
def live_feed():
    return render_template('detection.html', name=session["name"],age=session["age"],gender=session["gender"])

@app.route('/start_feed')
def start_feed():
    global is_feed_running
    is_feed_running = True
    return jsonify({"message":"FEED STARTED"})

@app.route('/stop_feed')
def stop_feed():
    global is_feed_running
    is_feed_running = False
    return jsonify({"message":"FEED ENDED"})

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_emotion')
def get_emotion():
    emotion_index = int(np.load("emotion.npy"))
    emotion = label_dict[emotion_index]
    return jsonify({"emotion" : emotion})

@app.route('/get_music',methods=['GET','POST'])
def get_music():
    # Load emotion detection result
    detection = np.load("emotion.npy")[0]

    # Map detection to mood
    mood_map = {
        0:"Powerful/Party", # Angry → Energy
        1:"Relaxing/Calm",   # Contempt -> Chill
        2:"Melancholic/Chill",     # Disgust → Chill
        3:"Relaxing/Calm",     # Fear → Chill
        4:"Happy/Upbeat",   # Happy → Happy
        5:"Relaxing/Calm",   # Neutral → Happy
        6:"Melancholic/Chill",   # Sad → Happy
        7:"Powerful/Party"  # Surprise -> Energy
    }
    
    #getting the cluster to use
    cluster = mood_map.get(detection,"Powerful/Party")
    if cluster=="Powerful/Party":
        genre="Anger is not Good For you 😇"
    if cluster=="Melancholic/Chill":
        genre="Chilling out feels so Good right? 😌"
    if cluster=="Relaxing/Calm":
        genre="Everything will be okay ☺️"
    if cluster=="Happy/Upbeat":
        genre="Stay happy cause You look so good in a joyous mood 🤗"
    #recommending any 1 song in it
    filtered_songs = clustered_music[clustered_music['cluster'] == cluster][['song_name', 'singer']]
    selected_index = random.randint(0, len(filtered_songs) - 1)
    selected_song = filtered_songs.iloc[selected_index]
    #getting the url 
    song_id = get_spotify_track_id(selected_song['song_name'],selected_song['singer'])
    if not song_id:
        return render_template("Songs.html", statement="Couldn't fetch a song, Mind Trying again", song_name="", spotify_url="", spotify_id="")
    else:
        spotify_embed_url = f"https://open.spotify.com/embed/track/{song_id}"
        return render_template("Songs.html",statement=genre,song_name=selected_song['song_name'], spotify_url=spotify_embed_url, spotify_id=song_id)


#get mood based movie
@app.route('/Movie', methods=['GET', 'POST'])
def Movie():
    # Load the detected emotion
    detection = np.load("emotion.npy")[0]

    # Map the detected emotion to genres
    genre_map = {
        0: "Thriller",   # Angry
        1: "Family",     # Contempt
        2: "Film-Noir",  # Disgust
        3: "Drama",      # Fear
        4: "Family",     # Happy
        5: "Fantasy",    # Neutral
        6: "Musical",    # Sad
        7: "Sport",      # Surprise
    }

    # Get the corresponding genre
    genre = genre_map.get(detection, "Drama")  # Default to Drama if no match

    # Fetch movie titles
    movie_titles = fetch_movie_titles(genre)

    # Render the movie list in the frontend
    return render_template('Movie.html', movies=movie_titles, genre=genre)

if __name__ == "__main__":
    app.run(debug=True, port=8000,use_reloader=False)
