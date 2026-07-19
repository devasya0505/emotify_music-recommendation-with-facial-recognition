# Emotify

Emotify is a facial emotion-based music recommender.  
It detects a user’s emotion from webcam input and recommends mood-matched songs (Bollywood + Hollywood) using a local dataset, with optional Spotify playlist integration.

## Supported emotions

- Angry
- Disgust
- Fear
- Happy
- Neutral
- Sad
- Surprise

These are mapped to recommendation moods (`Energetic`, `Happy`, `Sad`, `Calm`) in the recommender.

## Tech stack

- **Frontend:** React (`frontend/`)
- **Backend:** Flask + OpenCV + TensorFlow (`emotionDetection/main.py`)
- **Recommender:** Pandas + Spotipy (`songRecommender/recommender.py`)

## Project structure

- `frontend/` - React app with the “Try Emotify” entry point
- `emotionDetection/` - Flask server and webcam-based emotion detection
- `songRecommender/` - Mood mapping and song/playlist recommendation logic
- `requirements.txt` - Python dependencies
- `.env.example` - Optional Spotify environment variables template
- `new.txt` - Temporary mood/result file used by recommender flow
- `new.html` - Generated recommendation page (legacy/local flow)

## Prerequisites

- Python 3.10+ recommended
- Node.js 18+ and npm
- Webcam access enabled

## Setup

### 1) Clone the repository

```bash
git clone https://github.com/devasya0505/emotify_music-recommendation-with-facial-recognition.git
cd emotify_music-recommendation-with-facial-recognition
```

### 2) Install Python dependencies

```bash
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 3) Install frontend dependencies

```bash
cd frontend
npm install
cd ..
```

## Optional Spotify setup

Spotify integration is optional. The app can still show track recommendations without creating a playlist.

1. Create an app in the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard).
2. Add a redirect URI (recommended): `http://127.0.0.1:8888/callback`
3. Create a `.env` file in the project root using `.env.example`:

```env
SPOTIPY_CLIENT_ID=your_client_id
SPOTIPY_CLIENT_SECRET=your_client_secret
SPOTIPY_REDIRECT_URI=http://127.0.0.1:8888/callback
```

## Run the project

### 1) Start backend (Terminal 1)

```bash
venv\Scripts\activate
python emotionDetection\main.py
```

Backend runs at: `http://127.0.0.1:5000`

### 2) Start frontend (Terminal 2)

```bash
cd frontend
npm start
```

Frontend runs at: `http://localhost:3000`

### 3) Use the app

1. Open `http://localhost:3000`
2. Click **Try Emotify**
3. In the backend page, click **Start Emotion Detection**
4. Webcam opens; press **q** to stop early
5. View detected emotion and recommended tracks

## Backend endpoints

- `GET /` - Backend UI
- `GET /health` - Health check
- `GET|POST /detect` - Runs emotion detection and returns recommendations
  - Optional query params:
    - `seconds` (default: `5`)
    - `camera` (default: `0`)

## Notes

- If webcam access fails, close apps using the camera (Teams/Zoom/etc.) and retry.
- If no face is detected, improve lighting and keep your face centered.
- If ports are busy, stop conflicting processes or change ports in source.
