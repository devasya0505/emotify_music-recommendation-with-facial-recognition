# 🎵 How to Run Emotify — Step by Step

---

## Step 0: Spotify Setup (One-time only)

1. Go to **https://developer.spotify.com/dashboard**
2. Log in with your Spotify account
3. Click **"Create App"**
4. Fill in:
   - **App name**: `Emotify`
   - **Redirect URI**: `http://localhost:8888/callback`  ← paste this exactly
   - Check the **Web API** checkbox
5. Click **Save**
6. On the app page, note your **Client ID** and **Client Secret**
7. Update these two files with your credentials:
   - [helpers.py](file:///e:/1_B.E.%20in%20IT/DE-Project/de-project/Emotify-Arithemania/songRecommender/helpers.py) → lines 5-6
   - [recommender.py](file:///e:/1_B.E.%20in%20IT/DE-Project/de-project/Emotify-Arithemania/songRecommender/recommender.py) → lines 28-31

> [!NOTE]
> You already updated `helpers.py` with your credentials. Make sure `recommender.py` has the same ones.

---

## Step 1: Open Terminal #1 — Start the Backend

Open a **PowerShell terminal** and run these 3 commands:

```powershell
cd "e:\1_B.E. in IT\DE-Project\de-project\Emotify-Arithemania"
```
```powershell
.\venv\Scripts\activate
```
```powershell
python emotionDetection\main.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Debugger is active!
```

> [!IMPORTANT]
> Keep this terminal **open and running**. Don't close it.

---

## Step 2: Open Terminal #2 — Start the Frontend

Open a **second PowerShell terminal** and run:

```powershell
cd "e:\1_B.E. in IT\DE-Project\de-project\Emotify-Arithemania\frontend"
```
```powershell
npm start
```

You should see:
```
Compiled successfully!
Local: http://localhost:3000
```

A browser should auto-open to **http://localhost:3000**

> [!IMPORTANT]
> Keep this terminal **open and running** too.

---

## Step 3: Use the App

1. Open **http://localhost:3000** in your browser (if it didn't open automatically)
2. Click the **"Try Emotify"** button
3. This opens **http://127.0.0.1:5000** in a new tab
4. Click **"Start Emotion Detection"**
5. Your **webcam will open** in a separate window
6. **Look at the camera** — it detects your face and labels your emotion
7. After ~50 frames (or press **Q** to stop early), the webcam closes
8. The page shows your **detected emotion** and a **Spotify playlist**

---

## Step 4: First-time Spotify Login

The **very first time** you run the Spotify part, a browser window will open asking you to log in to Spotify and authorize the app. 

1. **Log in** with your Spotify account
2. Click **Agree** to authorize
3. You'll be redirected to `http://localhost:8888/callback?code=...`
4. This is normal — the credentials are now cached and you won't be asked again

---

## Quick Summary

| What | Command | Keep running? |
|------|---------|:---:|
| **Backend** | `.\venv\Scripts\activate` then `python emotionDetection\main.py` | ✅ Yes |
| **Frontend** | `npm start` (in `frontend/` folder) | ✅ Yes |
| **Use it** | Open http://localhost:3000 → Click "Try Emotify" | — |

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| **Webcam doesn't open** | Close other apps using the camera (Teams, Zoom, etc.) |
| **"No face detected"** | Better lighting, face the camera directly |
| **Spotify auth error** | Delete `.cache` file in project root and try again |
| **Module not found** | Make sure you activated the venv (`.\venv\Scripts\activate`) |
| **Port 3000 in use** | Close other React apps, or it'll ask to use port 3001 |
| **Port 5000 in use** | Close other Flask apps or change port in `main.py` line 353 |
