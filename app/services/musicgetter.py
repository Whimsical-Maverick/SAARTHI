import os
import spotipy
from spotipy.exceptions import SpotifyException
from spotipy.oauth2 import SpotifyClientCredentials


def get_spotify_track_id(song_name,artist_name):
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    if not client_id or not client_secret:
        raise RuntimeError(
            "Spotify credentials are missing. Set SPOTIFY_CLIENT_ID and "
            "SPOTIFY_CLIENT_SECRET in .env."
        )

    auth_manager = SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret,
    )
    sp = spotipy.Spotify(auth_manager=auth_manager)
    query = f"track:{song_name} artist:{artist_name}"
    try:
        results = sp.search(q=query, type="track", limit=1)
    except SpotifyException as exc:
        if exc.http_status == 403:
            raise RuntimeError(
                "Spotify rejected the request because the Spotify account that "
                "owns this app needs an active Premium subscription. Renew or "
                "upgrade that account, then wait a few hours for Spotify to "
                "update the app status."
            ) from exc
        raise RuntimeError(f"Spotify request failed: {exc}") from exc

    items = results.get("tracks", {}).get("items", [])
    return items[0].get("id") if items else None
