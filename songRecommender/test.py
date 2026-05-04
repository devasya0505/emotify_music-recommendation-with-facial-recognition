from recommender import build_recommendation, read_mood_file, write_mood_file, write_recommendation_html


def main():
    mood = read_mood_file()
    recommendation = build_recommendation(mood=mood, limit=15, create_playlist=True)
    write_mood_file(recommendation["playlist"]["id"] if recommendation.get("playlist") else mood)
    html_path = write_recommendation_html(recommendation)

    print(f"Created recommendations for mood: {mood}")
    if recommendation.get("playlist"):
        print(f"Spotify playlist: {recommendation['playlist']['external_url']}")
    elif recommendation.get("playlist_error"):
        print(f"Spotify playlist was not created: {recommendation['playlist_error']}")
    else:
        print("Spotify credentials were not found, so only local song links were generated.")
    print(f"HTML file: {html_path}")


if __name__ == "__main__":
    main()
