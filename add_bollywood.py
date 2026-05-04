"""Add Bollywood songs to data_moods.csv"""
import pandas as pd
import os

csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "songRecommender", "data", "data_moods.csv")
df = pd.read_csv(csv_path)

# Add category column to existing songs
if "category" not in df.columns:
    df["category"] = "Hollywood"

bollywood = [
    # === Happy (5) ===
    {"name": "Badtameez Dil", "album": "Yeh Jawaani Hai Deewani", "artist": "Benny Dayal", "id": "19Vj82y6vL0t5R632jYq2W", "release_date": "2013-05-31", "popularity": 70, "length": 233000, "danceability": 0.75, "acousticness": 0.05, "energy": 0.85, "instrumentalness": 0.0, "liveness": 0.12, "valence": 0.82, "loudness": -4.5, "speechiness": 0.05, "tempo": 128.0, "key": 5, "time_signature": 4, "mood": "Happy", "category": "Bollywood"},
    {"name": "Balam Pichkari", "album": "Yeh Jawaani Hai Deewani", "artist": "Vishal Dadlani", "id": "4hJ2mU6sT2mP5Pj1yL2yLq", "release_date": "2013-05-31", "popularity": 68, "length": 275000, "danceability": 0.72, "acousticness": 0.04, "energy": 0.88, "instrumentalness": 0.0, "liveness": 0.15, "valence": 0.85, "loudness": -4.2, "speechiness": 0.06, "tempo": 135.0, "key": 7, "time_signature": 4, "mood": "Happy", "category": "Bollywood"},
    {"name": "London Thumakda", "album": "Queen", "artist": "Labh Janjua", "id": "6G3Sg5YjW7P8J0o2w9v8xX", "release_date": "2014-03-07", "popularity": 65, "length": 221000, "danceability": 0.78, "acousticness": 0.08, "energy": 0.82, "instrumentalness": 0.0, "liveness": 0.18, "valence": 0.88, "loudness": -5.1, "speechiness": 0.04, "tempo": 120.0, "key": 2, "time_signature": 4, "mood": "Happy", "category": "Bollywood"},
    {"name": "Gallan Goodiyaan", "album": "Dil Dhadakne Do", "artist": "Shankar Mahadevan", "id": "3BhjbaGeI7E0CiIjctfdD3", "release_date": "2015-06-05", "popularity": 62, "length": 295000, "danceability": 0.70, "acousticness": 0.10, "energy": 0.80, "instrumentalness": 0.0, "liveness": 0.20, "valence": 0.80, "loudness": -5.5, "speechiness": 0.05, "tempo": 118.0, "key": 4, "time_signature": 4, "mood": "Happy", "category": "Bollywood"},
    {"name": "Ainvayi Ainvayi", "album": "Band Baaja Baaraat", "artist": "Salim Merchant", "id": "7f0vVL3xi4i78Rv5Ptn2s1", "release_date": "2010-12-10", "popularity": 58, "length": 261000, "danceability": 0.74, "acousticness": 0.06, "energy": 0.83, "instrumentalness": 0.0, "liveness": 0.14, "valence": 0.84, "loudness": -4.8, "speechiness": 0.04, "tempo": 125.0, "key": 1, "time_signature": 4, "mood": "Happy", "category": "Bollywood"},

    # === Sad (5) ===
    {"name": "Channa Mereya", "album": "Ae Dil Hai Mushkil", "artist": "Arijit Singh", "id": "66Q4528K5YQ07p945398kO", "release_date": "2016-10-28", "popularity": 75, "length": 289000, "danceability": 0.45, "acousticness": 0.55, "energy": 0.40, "instrumentalness": 0.0, "liveness": 0.10, "valence": 0.20, "loudness": -8.5, "speechiness": 0.03, "tempo": 85.0, "key": 0, "time_signature": 4, "mood": "Sad", "category": "Bollywood"},
    {"name": "Tum Hi Ho", "album": "Aashiqui 2", "artist": "Arijit Singh", "id": "03sLpY0p7j1E0F0w5d1d6Z", "release_date": "2013-04-26", "popularity": 78, "length": 262000, "danceability": 0.42, "acousticness": 0.60, "energy": 0.38, "instrumentalness": 0.0, "liveness": 0.08, "valence": 0.15, "loudness": -9.0, "speechiness": 0.03, "tempo": 78.0, "key": 3, "time_signature": 4, "mood": "Sad", "category": "Bollywood"},
    {"name": "Agar Tum Saath Ho", "album": "Tamasha", "artist": "Alka Yagnik", "id": "4yPmiJMFMSit8VCFjunqzK", "release_date": "2015-11-27", "popularity": 72, "length": 335000, "danceability": 0.40, "acousticness": 0.65, "energy": 0.35, "instrumentalness": 0.0, "liveness": 0.09, "valence": 0.18, "loudness": -9.5, "speechiness": 0.04, "tempo": 75.0, "key": 6, "time_signature": 4, "mood": "Sad", "category": "Bollywood"},
    {"name": "Tujhe Kitna Chahne Lage", "album": "Kabir Singh", "artist": "Arijit Singh", "id": "2nMeu6JenVGEMbOBkI7A7c", "release_date": "2019-06-21", "popularity": 74, "length": 249000, "danceability": 0.43, "acousticness": 0.58, "energy": 0.36, "instrumentalness": 0.0, "liveness": 0.11, "valence": 0.17, "loudness": -9.2, "speechiness": 0.03, "tempo": 80.0, "key": 8, "time_signature": 4, "mood": "Sad", "category": "Bollywood"},
    {"name": "Phir Le Aya Dil", "album": "Barfi!", "artist": "Arijit Singh", "id": "0O2KnfPSEVrKoBRqGDkIHV", "release_date": "2012-09-14", "popularity": 60, "length": 296000, "danceability": 0.38, "acousticness": 0.70, "energy": 0.30, "instrumentalness": 0.0, "liveness": 0.07, "valence": 0.12, "loudness": -10.0, "speechiness": 0.03, "tempo": 72.0, "key": 5, "time_signature": 4, "mood": "Sad", "category": "Bollywood"},

    # === Energetic (5) ===
    {"name": "Khalibali", "album": "Padmaavat", "artist": "Shivam Pathak", "id": "4Hk9kY73z23p8P5Qy43hM3", "release_date": "2018-01-25", "popularity": 60, "length": 272000, "danceability": 0.65, "acousticness": 0.02, "energy": 0.92, "instrumentalness": 0.0, "liveness": 0.25, "valence": 0.70, "loudness": -3.5, "speechiness": 0.08, "tempo": 145.0, "key": 9, "time_signature": 4, "mood": "Energetic", "category": "Bollywood"},
    {"name": "Malhari", "album": "Bajirao Mastani", "artist": "Vishal Dadlani", "id": "0kQpLj2M2ngqDnGuFeHvg4", "release_date": "2015-12-18", "popularity": 62, "length": 248000, "danceability": 0.68, "acousticness": 0.03, "energy": 0.90, "instrumentalness": 0.0, "liveness": 0.22, "valence": 0.75, "loudness": -3.8, "speechiness": 0.06, "tempo": 140.0, "key": 2, "time_signature": 4, "mood": "Energetic", "category": "Bollywood"},
    {"name": "Kar Gayi Chull", "album": "Kapoor & Sons", "artist": "Badshah", "id": "0I1P4t0mZ0733dC4GvVz00", "release_date": "2016-03-18", "popularity": 70, "length": 203000, "danceability": 0.80, "acousticness": 0.01, "energy": 0.88, "instrumentalness": 0.0, "liveness": 0.15, "valence": 0.82, "loudness": -4.0, "speechiness": 0.10, "tempo": 130.0, "key": 1, "time_signature": 4, "mood": "Energetic", "category": "Bollywood"},
    {"name": "Tattad Tattad", "album": "Goliyon Ki Raasleela Ram-Leela", "artist": "Aditya Narayan", "id": "0lJ59R5zN01G7W5342aR3G", "release_date": "2013-11-15", "popularity": 55, "length": 230000, "danceability": 0.72, "acousticness": 0.04, "energy": 0.91, "instrumentalness": 0.0, "liveness": 0.20, "valence": 0.78, "loudness": -3.6, "speechiness": 0.07, "tempo": 142.0, "key": 7, "time_signature": 4, "mood": "Energetic", "category": "Bollywood"},
    {"name": "Nashe Si Chadh Gayi", "album": "Befikre", "artist": "Arijit Singh", "id": "6gSTCqW3kXkqVRpiI3dc6y", "release_date": "2016-12-09", "popularity": 64, "length": 231000, "danceability": 0.75, "acousticness": 0.05, "energy": 0.85, "instrumentalness": 0.0, "liveness": 0.16, "valence": 0.72, "loudness": -4.3, "speechiness": 0.06, "tempo": 128.0, "key": 4, "time_signature": 4, "mood": "Energetic", "category": "Bollywood"},

    # === Calm (5) ===
    {"name": "Tum Se Hi", "album": "Jab We Met", "artist": "Mohit Chauhan", "id": "7eQl3Yqv35ioqUfveKHitE", "release_date": "2007-10-26", "popularity": 70, "length": 325000, "danceability": 0.35, "acousticness": 0.75, "energy": 0.30, "instrumentalness": 0.0, "liveness": 0.08, "valence": 0.25, "loudness": -10.0, "speechiness": 0.03, "tempo": 70.0, "key": 0, "time_signature": 4, "mood": "Calm", "category": "Bollywood"},
    {"name": "Ilahi", "album": "Yeh Jawaani Hai Deewani", "artist": "Arijit Singh", "id": "5cgKosPPj5Cs9a2JQufUc1", "release_date": "2013-05-31", "popularity": 68, "length": 222000, "danceability": 0.40, "acousticness": 0.70, "energy": 0.35, "instrumentalness": 0.0, "liveness": 0.10, "valence": 0.30, "loudness": -9.0, "speechiness": 0.04, "tempo": 80.0, "key": 3, "time_signature": 4, "mood": "Calm", "category": "Bollywood"},
    {"name": "Kun Faya Kun", "album": "Rockstar", "artist": "A.R. Rahman", "id": "2d7hF4Q0pY7xG0zL6b9l6w", "release_date": "2011-11-11", "popularity": 72, "length": 438000, "danceability": 0.30, "acousticness": 0.80, "energy": 0.25, "instrumentalness": 0.0, "liveness": 0.12, "valence": 0.20, "loudness": -11.0, "speechiness": 0.03, "tempo": 68.0, "key": 6, "time_signature": 4, "mood": "Calm", "category": "Bollywood"},
    {"name": "Iktara", "album": "Wake Up Sid", "artist": "Kavita Seth", "id": "51umGIauwIZln39b3hsso2", "release_date": "2009-10-02", "popularity": 65, "length": 258000, "danceability": 0.38, "acousticness": 0.72, "energy": 0.28, "instrumentalness": 0.0, "liveness": 0.09, "valence": 0.22, "loudness": -10.5, "speechiness": 0.03, "tempo": 72.0, "key": 8, "time_signature": 4, "mood": "Calm", "category": "Bollywood"},
    {"name": "Khaabon Ke Parinday", "album": "Zindagi Na Milegi Dobara", "artist": "Mohit Chauhan", "id": "0x4IUjZnFpTGZCt2XdFbcl", "release_date": "2011-07-15", "popularity": 63, "length": 310000, "danceability": 0.36, "acousticness": 0.68, "energy": 0.32, "instrumentalness": 0.0, "liveness": 0.11, "valence": 0.28, "loudness": -9.8, "speechiness": 0.04, "tempo": 75.0, "key": 5, "time_signature": 4, "mood": "Calm", "category": "Bollywood"},
]

bollywood_df = pd.DataFrame(bollywood)
combined = pd.concat([df, bollywood_df], ignore_index=True)
combined.to_csv(csv_path, index=False)

print(f"Done! CSV now has {len(combined)} rows")
hw = len(combined[combined["category"] == "Hollywood"])
bw = len(combined[combined["category"] == "Bollywood"])
print(f"Hollywood: {hw}, Bollywood: {bw}")
print("\nBreakdown:")
print(combined.groupby(["mood", "category"]).size().to_string())
