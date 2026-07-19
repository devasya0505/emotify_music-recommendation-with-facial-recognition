"""
Emotify recommender module.

Provides mood-based song recommendations using the local CSV dataset,
and optionally creates a Spotify playlist via the Spotify Web API.
"""

import os
import random
from pathlib import Path

import pandas as pd

# ---------------------------------------------------------------------------
# Path helpers
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
DATA_MOODS_CSV = SCRIPT_DIR / "data" / "data_moods.csv"

# Spotify credentials — read from env-vars first, fall back to defaults.
SPOTIFY_CLIENT_ID = os.environ.get(
    "SPOTIPY_CLIENT_ID", "bca96acdec13413f94a08c00b3907bcd"
)
SPOTIFY_CLIENT_SECRET = os.environ.get(
    "SPOTIPY_CLIENT_SECRET", "f5e10794e95e4200bf60b92f081e6cda"
)
SPOTIFY_REDIRECT_URI = os.environ.get(
    "SPOTIPY_REDIRECT_URI", "http://127.0.0.1:8888/callback"
)


# ---------------------------------------------------------------------------
# Mood mapping  (emotion label → CSV mood category)
# ---------------------------------------------------------------------------
EMOTION_TO_MOOD = {
    "Angry": "Energetic",
    "Surprise": "Energetic",
    "Happy": "Happy",
    "Disgust": "Sad",
    "Sad": "Sad",
    "Fear": "Calm",
    "Neutral": "Calm",
}


def normalize_mood(emotion: str) -> str:
    """Map a raw emotion label to one of the four CSV mood categories."""
    return EMOTION_TO_MOOD.get(emotion, emotion)




# ---------------------------------------------------------------------------
# Spotify integration (optional)
# ---------------------------------------------------------------------------

def _get_spotify_client():
    """Return an authenticated Spotipy client, or *None* if credentials
    are missing or the spotipy library is not installed."""
    if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
        return None
    try:
        import spotipy
        from spotipy.oauth2 import SpotifyOAuth

        return spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=SPOTIFY_CLIENT_ID,
                client_secret=SPOTIFY_CLIENT_SECRET,
                redirect_uri=SPOTIFY_REDIRECT_URI,
                scope="user-read-playback-state streaming ugc-image-upload playlist-modify-public",
            ),
            requests_timeout=10,
            retries=10,
        )
    except Exception:
        return None


def _create_spotify_playlist(sp, mood: str, track_uris: list[str]):
    """Create a new Spotify playlist and return a dict with its metadata."""
    user_id = sp.me()["id"]
    playlist_name = f"{mood} Songs"
    sp.user_playlist_create(
        user=user_id,
        name=playlist_name,
        public=True,
        description=f"{mood} Songs — created by Emotify",
    )
    playlists = sp.user_playlists(user=user_id)
    playlist_id = playlists["items"][0]["id"]
    sp.user_playlist_add_tracks(
        user=user_id, playlist_id=playlist_id, tracks=track_uris
    )
    return {
        "id": playlist_id,
        "name": playlist_name,
        "external_url": f"https://open.spotify.com/playlist/{playlist_id}",
        "embed_url": f"https://open.spotify.com/embed/playlist/{playlist_id}?utm_source=generator",
    }


# ---------------------------------------------------------------------------
# Core recommendation function
# ---------------------------------------------------------------------------

def build_recommendation(
    mood: str,
    limit: int = 10,
    create_playlist: bool = True,
) -> dict:
    """
    Build a recommendation payload for the given *mood*.

    Picks 5 Hollywood + 5 Bollywood songs for a balanced mix.

    Returns a dict with keys:
        - ``mood``          – the mood string
        - ``songs``         – list of song dicts (name, artist, album, id, track_url, category)
        - ``playlist``      – Spotify playlist dict (or absent)
        - ``playlist_error``– error message if playlist creation failed (or absent)
    """
    df = pd.read_csv(DATA_MOODS_CSV)
    mood_songs = df.loc[df["mood"] == mood]

    if mood_songs.empty:
        return {"mood": mood, "songs": [], "playlist_error": f"No songs found for mood '{mood}'"}

    # Split by category and sample 5 from each
    per_category = limit // 2  # 5 each for limit=10

    hollywood = mood_songs[mood_songs["category"] == "Hollywood"]
    bollywood = mood_songs[mood_songs["category"] == "Bollywood"]

    hw_sample = hollywood.sample(n=min(per_category, len(hollywood)), random_state=None)
    bw_sample = bollywood.sample(n=min(per_category, len(bollywood)), random_state=None)

    sampled = pd.concat([hw_sample, bw_sample])

    songs = []
    track_uris = []
    for _, row in sampled.iterrows():
        track_id = str(row["id"])
        category = row.get("category", "Hollywood")
        songs.append(
            {
                "name": row["name"],
                "artist": row["artist"],
                "album": row["album"],
                "id": track_id,
                "track_url": f"https://open.spotify.com/track/{track_id}",
                "category": category,
            }
        )
        track_uris.append(f"spotify:track:{track_id}")

    result: dict = {"mood": mood, "songs": songs}

    # Optionally create a Spotify playlist
    if create_playlist:
        sp = _get_spotify_client()
        if sp is not None:
            try:
                playlist_info = _create_spotify_playlist(sp, mood, track_uris)
                result["playlist"] = playlist_info
            except Exception as exc:
                result["playlist_error"] = str(exc)
        # If sp is None we simply skip — no error, no playlist

    return result

