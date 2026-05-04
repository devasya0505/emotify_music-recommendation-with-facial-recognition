"""Fix Bollywood song Spotify IDs in data_moods.csv with verified IDs."""
import pandas as pd
import os

csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "songRecommender", "data", "data_moods.csv")
df = pd.read_csv(csv_path)

# Mapping of song names to correct verified Spotify track IDs
corrections = {
    # Happy
    "Badtameez Dil":    "4eu27jAU2bbnyHUC3G75U8",
    "Balam Pichkari":   "18e3XXYCv4Tx8uUl1mP3CN",
    "London Thumakda":  "2qJAzSE6uC94oH2NRoPrGl",
    "Gallan Goodiyaan":  "7hNYvX0qAKrxtVr1jGDmvR",
    "Ainvayi Ainvayi":   "74AqVxZ3oXwJ8olHssBUG3",
    # Sad
    "Channa Mereya":            "0H2iJVgorRR0ZFgRqGUjUM",
    "Tum Hi Ho":                "56zZ48jdyY2oDXHVnwg5Di",
    "Agar Tum Saath Ho":        "3hkC9EHFZNQPXrtl8WPHnX",
    "Tujhe Kitna Chahne Lage":  "2Fv2injs4qAm8mJBGaxVKU",
    "Phir Le Aya Dil":          "7fpWJr5shT90KiCHXKHxch",
    # Energetic
    "Khalibali":            "3JT0mVof65rIHpRZITwRx1",
    "Malhari":              "0kQpLj2M2ngqDnGuFeHvg4",
    "Kar Gayi Chull":       "3BhjbaGeI7E0CiIjctfdD3",
    "Tattad Tattad":        "2IVpapKaryZc8YbCkwF0sV",
    "Nashe Si Chadh Gayi":  "0biCSADTAblvLTLtJz4pXO",
    # Calm
    "Tum Se Hi":            "7eQl3Yqv35ioqUfveKHitE",
    "Ilahi":                "5cgKosPPj5Cs9a2JQufUc1",
    "Kun Faya Kun":         "7F8RNvTQlvbeBLeenycvN6",
    "Iktara":               "0RJ7HhnQxJEOpGC5Htmez4",
    "Khaabon Ke Parinday":  "14eotumM24MhIgzidgN3Jx",
}

# Update IDs for Bollywood songs only
bollywood_mask = df["category"] == "Bollywood"
for song_name, correct_id in corrections.items():
    mask = bollywood_mask & (df["name"] == song_name)
    if mask.any():
        old_id = df.loc[mask, "id"].values[0]
        df.loc[mask, "id"] = correct_id
        print(f"  {song_name}: {old_id} -> {correct_id}")
    else:
        print(f"  {song_name}: NOT FOUND in CSV")

df.to_csv(csv_path, index=False)
print(f"\nDone! Updated {len(corrections)} Bollywood song IDs.")
