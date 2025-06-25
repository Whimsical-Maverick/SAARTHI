import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
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