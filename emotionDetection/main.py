from pathlib import Path
import os
import sys

from flask import Flask, render_template_string, request

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from songRecommender.recommender import build_recommendation, normalize_mood

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

if load_dotenv:
    load_dotenv(BASE_DIR / ".env")

app = Flask(__name__)

CASCADE_PATH = BASE_DIR / "emotionDetection" / "haarcascade_frontalface_default.xml"
MODEL_PATH = BASE_DIR / "emotionDetection" / "model.h5"
EMOTION_LABELS = ["Angry", "Disgust", "Fear", "Happy", "Neutral", "Sad", "Surprise"]


HOME_PAGE = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Emotify Detection Backend</title>
    <style>
      body {
        margin: 0;
        min-height: 100vh;
        font-family: Arial, sans-serif;
        color: #eef6ff;
        background: #070b12;
        display: grid;
        place-items: center;
      }
      main {
        width: min(760px, calc(100% - 32px));
      }
      h1 {
        font-size: 42px;
        margin: 0 0 12px;
      }
      p {
        color: #bfd0df;
        line-height: 1.6;
      }
      button, a.button {
        display: inline-block;
        border: 0;
        border-radius: 6px;
        padding: 12px 18px;
        margin-top: 12px;
        color: #06111d;
        background: #7dd3fc;
        font-weight: 700;
        text-decoration: none;
        cursor: pointer;
      }
      code {
        background: #152131;
        padding: 2px 6px;
        border-radius: 4px;
      }
    </style>
  </head>
  <body>
    <main>
      <h1>Emotify</h1>
      <p>Click start, allow the webcam window to open, keep your face visible, and wait about 50 frames. You can press <code>q</code> in the camera window to stop early.</p>
      <form method="post" action="/detect">
        <button type="submit">Start Emotion Detection</button>
      </form>
    </main>
  </body>
</html>
"""


RESULT_PAGE = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>MoodTune — Results</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
      * { box-sizing: border-box; }
      body {
        margin: 0;
        min-height: 100vh;
        font-family: 'Inter', Arial, sans-serif;
        color: #eef6ff;
        background: linear-gradient(135deg, #0a0f1a 0%, #0d1b2a 50%, #1b2838 100%);
      }
      main {
        width: min(1000px, calc(100% - 32px));
        margin: 0 auto;
        padding: 40px 0;
      }
      h1 { font-size: 28px; margin-bottom: 4px; }
      h2 {
        font-size: 20px;
        margin: 32px 0 12px;
        color: #7dd3fc;
        border-bottom: 1px solid #1e3a5f;
        padding-bottom: 8px;
      }
      .mood-badge {
        display: inline-block;
        background: linear-gradient(135deg, #7dd3fc, #38bdf8);
        color: #06111d;
        padding: 4px 14px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 14px;
        margin-left: 8px;
      }
      p { color: #94a3b8; line-height: 1.5; margin: 8px 0; }
      .song-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 12px;
        margin-bottom: 14px;
        overflow: hidden;
      }
      .song-card iframe {
        width: 100%;
        height: 80px;
        border: 0;
        display: block;
      }
      .song-info {
        padding: 8px 14px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 14px;
        border-top: 1px solid rgba(255,255,255,0.06);
      }
      .song-info .name {
        color: #e2e8f0;
        font-weight: 600;
      }
      .song-info .artist {
        color: #64748b;
        margin-left: 6px;
        font-weight: 400;
      }
      .song-info a {
        color: #7dd3fc;
        text-decoration: none;
        font-size: 13px;
        white-space: nowrap;
      }
      .song-info a:hover { text-decoration: underline; }
      .button {
        display: inline-block;
        border-radius: 8px;
        padding: 12px 20px;
        margin-top: 24px;
        color: #06111d;
        background: linear-gradient(135deg, #7dd3fc, #38bdf8);
        font-weight: 700;
        text-decoration: none;
        transition: transform 0.15s;
      }
      .button:hover { transform: translateY(-2px); text-decoration: none; }
      .stats { font-size: 13px; color: #64748b; }
    </style>
  </head>
  <body>
    <main>
      <h1>Detected emotion: {{ emotion }} <span class="mood-badge">{{ mood }}</span></h1>
      {% if counts %}
      <p class="stats">Detection counts: {{ counts }}</p>
      {% endif %}

      <h2>🎶 Bollywood Picks</h2>
      {% for song in songs %}
        {% if song.category == 'Bollywood' %}
        <div class="song-card">
          <iframe src="https://open.spotify.com/embed/track/{{ song.id }}?utm_source=generator&theme=0"
                  allow="autoplay; clipboard-write; encrypted-media;" loading="lazy"></iframe>
          <div class="song-info">
            <div><span class="name">{{ song.name }}</span><span class="artist">— {{ song.artist }}</span></div>
            <a href="{{ song.track_url }}" target="_blank">Open in Spotify ↗</a>
          </div>
        </div>
        {% endif %}
      {% endfor %}

      <h2>🎵 Hollywood Picks</h2>
      {% for song in songs %}
        {% if song.category == 'Hollywood' %}
        <div class="song-card">
          <iframe src="https://open.spotify.com/embed/track/{{ song.id }}?utm_source=generator&theme=0"
                  allow="autoplay; clipboard-write; encrypted-media;" loading="lazy"></iframe>
          <div class="song-info">
            <div><span class="name">{{ song.name }}</span><span class="artist">— {{ song.artist }}</span></div>
            <a href="{{ song.track_url }}" target="_blank">Open in Spotify ↗</a>
          </div>
        </div>
        {% endif %}
      {% endfor %}

      <a class="button" href="/">🔄 Detect Again</a>
    </main>
  </body>
</html>
"""


ERROR_PAGE = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Emotify Error</title>
    <style>
      body {
        margin: 0;
        min-height: 100vh;
        font-family: Arial, sans-serif;
        color: #eef6ff;
        background: #070b12;
        display: grid;
        place-items: center;
      }
      main {
        width: min(760px, calc(100% - 32px));
      }
      pre {
        white-space: pre-wrap;
        background: #151f2d;
        padding: 14px;
        border-radius: 6px;
      }
      a {
        color: #7dd3fc;
      }
    </style>
  </head>
  <body>
    <main>
      <h1>Emotify could not finish</h1>
      <pre>{{ message }}</pre>
      <p><a href="/">Go back</a></p>
    </main>
  </body>
</html>
"""


def _load_dependencies():
    try:
        import cv2
        import numpy as np
        from tensorflow.keras.models import load_model
    except ImportError as exc:
        missing = exc.name or str(exc)
        raise RuntimeError(
            f"Missing Python package: {missing}. Install the backend packages with "
            f"`python -m pip install -r requirements.txt`."
        ) from exc

    return cv2, np, load_model


def detect_emotion(duration_seconds=5, camera_index=0):
    """Run webcam emotion detection for *duration_seconds* (default 5s)."""
    import time as _time
    cv2, np, load_model = _load_dependencies()

    if not CASCADE_PATH.exists():
        raise RuntimeError(f"Face cascade file was not found: {CASCADE_PATH}")
    if not MODEL_PATH.exists():
        raise RuntimeError(f"Emotion model file was not found: {MODEL_PATH}")

    face_classifier = cv2.CascadeClassifier(str(CASCADE_PATH))
    if face_classifier.empty():
        raise RuntimeError(f"OpenCV could not load the cascade file: {CASCADE_PATH}")

    classifier = load_model(str(MODEL_PATH), compile=False)

    camera_backend = cv2.CAP_DSHOW if os.name == "nt" else 0
    cap = cv2.VideoCapture(camera_index, camera_backend)
    if not cap.isOpened():
        raise RuntimeError(
            "Could not open the webcam. Check camera permissions, close other apps using the camera, "
            "or try another camera index with /detect?camera=1."
        )

    counts = {}
    start_time = _time.time()
    window_name = "Emotion Detector - press q to stop"

    # Create the window and force it to pop up on top
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)

    try:
        while (_time.time() - start_time) < duration_seconds:
            ok, frame = cap.read()
            if not ok or frame is None:
                continue

            # Mirror the frame horizontally
            frame = cv2.flip(frame, 1)

            # Show countdown timer on screen
            elapsed = _time.time() - start_time
            remaining = max(0, duration_seconds - elapsed)

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_classifier.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4, minSize=(30, 30))

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
                roi_gray = gray[y : y + h, x : x + w]
                roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)

                if np.sum(roi_gray) == 0:
                    continue

                roi = roi_gray.astype("float32") / 255.0
                roi = np.expand_dims(roi, axis=(0, -1))
                prediction = classifier.predict(roi, verbose=0)[0]
                label = EMOTION_LABELS[int(prediction.argmax())]
                counts[label] = counts.get(label, 0) + 1
                cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Show timer on frame
            cv2.putText(frame, f"Time left: {remaining:.1f}s", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            cv2.imshow(window_name, frame)

            if (cv2.waitKey(33) & 0xFF) == ord("q"):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

    if not counts:
        raise RuntimeError("No face was detected. Try again with better lighting and keep your face centered.")

    emotion = max(counts.items(), key=lambda item: item[1])[0]
    return emotion, counts


@app.route("/")
def index():
    return render_template_string(HOME_PAGE)


@app.route("/health")
def health():
    return {"status": "ok"}


@app.route("/detect", methods=["GET", "POST"])
def detect():
    try:
        duration = int(request.args.get("seconds", 5))
        camera_index = int(request.args.get("camera", 0))
        emotion, counts = detect_emotion(duration_seconds=duration, camera_index=camera_index)
        mood = normalize_mood(emotion)
        recommendation = build_recommendation(mood=mood, limit=10, create_playlist=False)
    except Exception as exc:
        return render_template_string(ERROR_PAGE, message=str(exc)), 500

    return render_template_string(
        RESULT_PAGE,
        emotion=emotion,
        mood=mood,
        counts=counts,
        songs=recommendation["songs"],
        playlist=recommendation.get("playlist"),
        playlist_error=recommendation.get("playlist_error"),
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
