from flask import Flask, render_template, request, redirect, url_for,Response,session,jsonify
import cv2
import numpy as np
import tensorflow as tf
import keras
from keras._tf_keras.keras.models import load_model
import requests
from bs4 import BeautifulSoup
import re
from dotenv import load_dotenv
import os
try:
    emotion=np.load("emotion.npy")
except:
    emotion=""
app = Flask(__name__)
app.secret_key=os.getenv("SECRET_KEY")
model = load_model('model_file_30epochs.h5')
faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

labels_dict = {0: 'Angry', 1: 'Disgust', 2: 'Fear', 3: 'Happy', 4: 'Neutral', 5: 'Sad', 6: 'Surprise'}

# Flag to control the video feed
is_feed_running = False

def generate_frames():
    global is_feed_running
    video = cv2.VideoCapture(0)

    while is_feed_running:
        ret, frame = video.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceDetect.detectMultiScale(gray, 1.3, 3)
        for x, y, w, h in faces:
            sub_face_img = gray[y:y+h, x:x+w]
            resized = cv2.resize(sub_face_img, (48, 48))
            normalize = resized / 255.0
            reshaped = np.reshape(normalize, (1, 48, 48, 1))
            result = model.predict(reshaped)
            label = np.argmax(result, axis=1)[0]
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
            cv2.rectangle(frame, (x, y-40), (x+w, y), (50, 50, 255), -1)
            cv2.putText(frame, labels_dict[label], (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            np.save("emotion.npy",np.array([label]))
        # Encode the frame to send it to the frontend
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        

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


def fetch_movie_titles(emotion):
    url = URLS.get(emotion)
    if not url:
        return []

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check for HTTP errors
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    titles = [a.get_text() for a in soup.find_all('a', href=re.compile(r'/title/tt\d+/'))]
    return titles

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
    return "FEED STARTED"

@app.route('/stop_feed')
def stop_feed():
    global is_feed_running
    is_feed_running = False
    return "FEED ENDED"

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_music')
def get_music():
    # Load emotion detection result
    detection = np.load("emotion.npy")[0]
    
    # Map detection to mood
    mood_map = {
        0: "Peaceful",
        1: "Joyous",
        2: "Courageous",
        3: "Joyous",
        4: "Motivational",
        5: "Motivational",
        6: "Relaxing"
    }
    mood = mood_map.get(detection, "Motivational")

    # Get language from query parameter (passed from frontend)
    lang = request.args.get('lang', 'English')
    
    # Generate music list URL
    music_list = f"https://open.spotify.com/search/{mood}%20{lang}%20songs"
    
    return jsonify({"music_list": music_list})

#get mood based movie
@app.route('/Movie', methods=['GET', 'POST'])
def Movie():
    # Load the detected emotion
    detection = np.load("emotion.npy")[0]

    # Map the detected emotion to genres
    genre_map = {
        0: "Thriller",  # Angry
        1: "Film-Noir",  # Disgust
        2: "Drama",      # Fear
        3: "Family",     # Happy
        4: "Fantasy",    # Neutral
        5: "Musical",    # Sad
        6: "Sport"       # Surprise
    }

    # Get the corresponding genre
    genre = genre_map.get(detection, "Drama")  # Default to Drama if no match

    # Fetch movie titles
    movie_titles = fetch_movie_titles(genre)

    # Render the movie list in the frontend
    return render_template('Movie.html', movies=movie_titles, genre=genre)

if __name__ == "__main__":
    app.run(debug=True, port=8000)
