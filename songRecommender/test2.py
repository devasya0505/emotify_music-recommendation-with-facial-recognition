import webbrowser

from recommender import RESULT_HTML


def main():
    if not RESULT_HTML.exists():
        raise SystemExit("recommendations.html does not exist yet. Run python songRecommender/test.py first.")

    webbrowser.open(RESULT_HTML.as_uri())
    print(f"Opened {RESULT_HTML}")


if __name__ == "__main__":
    main()
