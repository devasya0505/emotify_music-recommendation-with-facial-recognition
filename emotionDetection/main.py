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
      <p>Click start, allow the webcam window to open, keep your face visible, and wait for 5 seconds. You can press <code>q</code> in the camera window to stop early.</p>
      <form method="post" action="/detect">
        <input type="hidden" name="seconds" value="5">
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


_CV2 = None
_NP = None
_PREDICT_FN = None
_FACE_CLASSIFIER = None


def _get_resources():
    """Load and cache OpenCV cascade and TensorFlow emotion model once."""
    global _CV2, _NP, _PREDICT_FN, _FACE_CLASSIFIER
    if _PREDICT_FN is not None and _FACE_CLASSIFIER is not None:
        return _CV2, _NP, _PREDICT_FN, _FACE_CLASSIFIER

    try:
        import cv2
        import numpy as np
        import tensorflow as tf
    except ImportError as exc:
        missing = exc.name or str(exc)
        raise RuntimeError(
            f"Missing Python package: {missing}. Install backend packages with "
            "`python -m pip install -r requirements.txt`."
        ) from exc

    if not CASCADE_PATH.exists():
        raise RuntimeError(f"Face cascade file was not found: {CASCADE_PATH}")
    if not MODEL_PATH.exists():
        raise RuntimeError(f"Emotion model file was not found: {MODEL_PATH}")

    face_classifier = cv2.CascadeClassifier(str(CASCADE_PATH))
    if face_classifier.empty():
        raise RuntimeError(f"OpenCV could not load the cascade file: {CASCADE_PATH}")

    model = tf.keras.models.load_model(str(MODEL_PATH), compile=False)

    # Compile the model forward pass for high-speed, direct tensor execution (~10x faster than .predict)
    @tf.function(reduce_retracing=True)
    def predict_fn(x):
        return model(x, training=False)

    # Warm up graph execution once so there is zero delay during capture
    dummy_input = tf.constant(np.zeros((1, 48, 48, 1), dtype=np.float32))
    _ = predict_fn(dummy_input)

    _CV2 = cv2
    _NP = np
    _PREDICT_FN = predict_fn
    _FACE_CLASSIFIER = face_classifier
    return _CV2, _NP, _PREDICT_FN, _FACE_CLASSIFIER


class ThreadedCamera:
    """High-speed threaded camera reader to eliminate USB capture wait times."""
    def __init__(self, src=0, backend=0):
        import cv2
        self.cap = cv2.VideoCapture(src, backend)
        try:
            self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
        except Exception:
            pass
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        self.grabbed, self.frame = self.cap.read()
        self.stopped = False
        import threading
        self.lock = threading.Lock()
        self.thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.thread.start()

    def _capture_loop(self):
        import time as _t
        while not self.stopped:
            grabbed, frame = self.cap.read()
            if grabbed and frame is not None:
                with self.lock:
                    self.grabbed = grabbed
                    self.frame = frame
            else:
                _t.sleep(0.005)

    def read(self):
        with self.lock:
            if not self.grabbed or self.frame is None:
                return False, None
            return True, self.frame.copy()

    def isOpened(self):
        return self.cap.isOpened()

    def release(self):
        self.stopped = True
        if self.thread.is_alive():
            self.thread.join(timeout=0.6)
        self.cap.release()


def detect_emotion(duration_seconds=5, camera_index=0):
    """Run real-time webcam emotion detection with threaded capture, async inference and smoothed tracking."""
    import time as _time
    import threading

    cv2, np, predict_fn, face_classifier = _get_resources()

    camera_backend = cv2.CAP_DSHOW if os.name == "nt" else 0
    cam = ThreadedCamera(camera_index, camera_backend)
    if not cam.isOpened():
        raise RuntimeError(
            "Could not open the webcam. Check camera permissions, close other apps using the camera, "
            "or try another camera index with /detect?camera=1."
        )

    counts = {}
    start_time = _time.time()
    window_name = "Emotion Detector - press q to stop"

    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)

    # State for asynchronous inference & box smoothing
    active_detection = None  # (smoothed_box, label)
    smoothed_box = None
    is_inferring = False
    state_lock = threading.Lock()

    def async_inference_worker(frame_input):
        nonlocal is_inferring, active_detection, smoothed_box
        try:
            gray = cv2.cvtColor(frame_input, cv2.COLOR_BGR2GRAY)
            small_gray = cv2.resize(gray, (0, 0), fx=0.5, fy=0.5)
            faces = face_classifier.detectMultiScale(
                small_gray,
                scaleFactor=1.15,
                minNeighbors=4,
                minSize=(20, 20),
            )

            if len(faces) > 0:
                # Track the most prominent face
                sx, sy, sw, sh = max(faces, key=lambda f: f[2] * f[3])
                x, y, w, h = sx * 2, sy * 2, sw * 2, sh * 2

                roi_gray = gray[y : y + h, x : x + w]
                if roi_gray.size > 0 and np.sum(roi_gray) > 0:
                    roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)
                    roi = (roi_gray.astype("float32") / 255.0).reshape(1, 48, 48, 1)

                    prediction = predict_fn(roi).numpy()[0]
                    label = EMOTION_LABELS[int(prediction.argmax())]

                    with state_lock:
                        counts[label] = counts.get(label, 0) + 1
                        # Exponential smoothing for jitter-free bounding box gliding
                        if smoothed_box is None:
                            smoothed_box = [x, y, w, h]
                        else:
                            smoothed_box = [
                                int(smoothed_box[0] * 0.55 + x * 0.45),
                                int(smoothed_box[1] * 0.55 + y * 0.45),
                                int(smoothed_box[2] * 0.55 + w * 0.45),
                                int(smoothed_box[3] * 0.55 + h * 0.45),
                            ]
                        active_detection = (smoothed_box, label)
        finally:
            with state_lock:
                is_inferring = False

    try:
        while (_time.time() - start_time) < duration_seconds:
            ok, frame = cam.read()
            if not ok or frame is None:
                _time.sleep(0.005)
                continue

            # Mirror the frame horizontally for natural user experience
            frame = cv2.flip(frame, 1)

            elapsed = _time.time() - start_time
            remaining = max(0.0, duration_seconds - elapsed)

            # Trigger non-blocking inference in parallel whenever ready
            with state_lock:
                busy = is_inferring

            if not busy:
                with state_lock:
                    is_inferring = True
                threading.Thread(
                    target=async_inference_worker,
                    args=(frame.copy(),),
                    daemon=True,
                ).start()

            # Render smoothed detection overlay
            with state_lock:
                current_det = active_detection

            if current_det is not None:
                (bx, by, bw, bh), blabel = current_det
                cv2.rectangle(frame, (bx, by), (bx + bw, by + bh), (0, 255, 255), 2)
                cv2.putText(
                    frame,
                    blabel,
                    (bx, max(28, by - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.95,
                    (0, 255, 0),
                    2,
                )

            # Render smooth live countdown
            cv2.putText(
                frame,
                f"Time left: {remaining:.1f}s",
                (14, 34),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.85,
                (255, 255, 255),
                2,
            )

            cv2.imshow(window_name, frame)

            # 1ms GUI event check ensures zero render lag
            if (cv2.waitKey(1) & 0xFF) == ord("q"):
                break
    finally:
        cam.release()
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
        duration = int(request.values.get("seconds", 5))
        camera_index = int(request.values.get("camera", 0))
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
