# 🎵 Emotify

Emotify is a facial emotion-based music recommender. It detects a user’s emotion from webcam input and recommends mood-matched songs (Bollywood + Hollywood) using a local dataset, with optional Spotify playlist integration.

---

## Supported Emotions

Webcam input detects the following facial emotions:
- **Angry** (maps to *Energetic* recommendation mood)
- **Disgust** (maps to *Sad* recommendation mood)
- **Fear** (maps to *Calm* recommendation mood)
- **Happy** (maps to *Happy* recommendation mood)
- **Neutral** (maps to *Calm* recommendation mood)
- **Sad** (maps to *Sad* recommendation mood)
- **Surprise** (maps to *Energetic* recommendation mood)

---

## Technology Stack

- **Frontend:** React (Vite/CRA) styled with custom responsive CSS.
- **Backend:** Flask + OpenCV + TensorFlow (loads pre-trained CNN model).
- **Recommender:** Pandas + Spotipy (Spotify Web API wrapper).

---

## Project Structure

```
Emotify/
├── emotionDetection/       # Flask backend and webcam emotion detection models
│   ├── main.py             # Main Flask server
│   ├── model.h5            # Pre-trained CNN model
│   └── haarcascade_...xml  # OpenCV Face cascade classifier
├── songRecommender/        # Mood mapping and song recommendations database
│   ├── recommender.py      # Core Spotify and CSV recommending logic
│   ├── helpers.py          # Spotify API credentials wrapper
│   └── data/
│       └── data_moods.csv  # Combined Hollywood & Bollywood tracks dataset
├── frontend/               # Fully responsive React application
│   ├── src/                # React source files (App.js, About.js)
│   └── package.json        # Frontend npm configuration
├── requirements.txt        # Python backend dependencies
└── .env.example            # Template for optional Spotify integration credentials
```

---

## Prerequisites

- **Python 3.10+**
- **Node.js 18+** and `npm`
- Webcam access enabled

---

## Setup Instructions

### 1) Clone the Repository
```bash
git clone https://github.com/devasya0505/emotify_music-recommendation-with-facial-recognition.git
cd emotify_music-recommendation-with-facial-recognition
```

### 2) Install Python Dependencies
```bash
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 3) Install Frontend Dependencies
```bash
cd frontend
npm install
cd ..
```

---

## Optional Spotify Setup

Spotify integration allows creating custom public playlists automatically on your Spotify account.
1. Create a developer app in the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard).
2. Set the redirect URI to: `http://127.0.0.1:8888/callback`
3. Create a `.env` file in the project root folder based on `.env.example`:
```env
SPOTIPY_CLIENT_ID=your_client_id
SPOTIPY_CLIENT_SECRET=your_client_secret
SPOTIPY_REDIRECT_URI=http://127.0.0.1:8888/callback
```

---

## How to Run the Project

### 1) Start the Flask Backend (Terminal 1)
```bash
venv\Scripts\activate
python emotionDetection\main.py
```
*The backend runs at `http://127.0.0.1:5000`*

### 2) Start the React Frontend (Terminal 2)
```bash
cd frontend
npm start
```
*The frontend runs at `http://localhost:3000`*

### 3) Use the App
1. Open `http://localhost:3000` in your web browser.
2. Click **Try Emotify** to open the emotion detection page.
3. Click **Start Emotion Detection**. The webcam window will pop up.
4. Keep your face centered in front of the camera (wait for ~50 frames or press `q` to stop detection early).
5. The page will display the detected emotion, and list recommended Bollywood and Hollywood songs with Spotify embed players.

---

## Backend APIs

- `GET /` — Backend homepage.
- `GET /health` — Simple backend health check.
- `GET|POST /detect` — Executes emotion detection via webcam, maps detected emotion to mood, and queries local CSV for song recommendations.
  - Optional Query Parameters:
    - `seconds` (default: `5`) — Detection duration.
    - `camera` (default: `0`) — Camera source index.
