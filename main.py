from flask import Flask,render_template,request,jsonify,Response
import cv2 as cv
from ultralytics import YOLO
import numpy as np
import pandas as pd
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
import os
app = Flask(__name__)

#Detection Systems Start Here
is_running = True
current_emotion = ""
def get_emotion():
    global is_running
    global current_emotion
    video = cv.VideoCapture(0)
    model = YOLO('best.pt')
    while is_running:
        res,frame = video.read()

        result=model(frame)[0]
        for box in result.boxes:
            x1,y1,x2,y2 = map(int,box.xyxy[0])
            conf =float(box.conf[0])
            cls = int(box.cls[0])
            emotion = label_dict[cls]
            current_emotion = emotion
        cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv.putText(frame, emotion, (x1, y1 - 10), cv.FONT_HERSHEY_SIMPLEX,0.8, (0, 255, 0), 2)
        # Encode the frame to send it to the frontend
        ret, buffer = cv.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    video.release()

@app.route('/')
def homepage():
    return render_template("login.html")

@app.route('/welcome',methods=['GET','POST'])
def detect():
    username = request.form['Name']
    clicked = request.form['getin']
    if(clicked == "High_Five!"):
        return render_template("detection.html",name = username)
    return '',200

@app.route('/start_feed')
def feedstart():
    global is_running
    is_running = True
    data = {"message":"FEED_STARTED...PLEASE KEEP LOOKING IN THE CAMERA"}
    return jsonify(data)

@app.route('/get_emotion')
def fetch_emotion():
    state = {"emotion" : current_emotion}
    return jsonify(state)

@app.route('/stop_feed')
def feedstop():
    global is_running
    is_running = False
    data = {"message":"FEED_STOPPED"}
    return jsonify(data)

@app.route('/video_feed')
def video():
    return Response(get_emotion(),mimetype='multipart/x-mixed-replace; boundary=frame')
#Detection Systems End

#MUsic Systems Start here
def get_spotify_track_id(song_name,artist_name):
    #Authentication
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id = os.getenv('SPOTIFY_CLIENT_ID'),
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    ))
    query=f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=query,type="track",limit=1)

    if results["tracks"]["items"]:
        track_id = results["tracks"]["items"][0]["id"]
    else:
        # print("No tracks found:",results)
        track_id=None
    
    del sp
    return track_id

label_dict = {
   0:"Anger",
   1:"Contempt",
   2:"Disgust" ,
   3:"Fear",
   4:"Happy",
   5:"Neutral",
   6:"Sad",
   7:"Surprise",
}

clustered_music=pd.read_csv(r"static\clustered_music_2.csv")

@app.route('/get_music')
def music():
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
        return render_template("Songs.html", statement="Couldn't fetch a song, Mind Trying again", song_name="", spotify_url="", spotify_id="")
    else:
        spotify_embed_url = f"https://open.spotify.com/embed/track/{song_id}"
        return render_template("Songs.html",statement=genre,song_name=selected_song['song_name'], spotify_url=spotify_embed_url, spotify_id=song_id)
#Music Systems End

# Movie Systems start here
    
# Movie System  end here

# Chat Bot
    
# Chat Bot ends
if __name__=="__main__":
    app.run(debug=True,use_reloader=False)