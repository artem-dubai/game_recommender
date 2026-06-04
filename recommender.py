from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def get_popular_games(games, limit=5):
    sorted_games = sorted(
        games,
        key=lambda game: game.rating,
        reverse=True
    )

    return [(game, 0.0) for game in sorted_games[:limit]]


def build_recommendations(user, games):

    if not games:
        return []

    game_texts = [
        f"{game.title} {game.genres} {game.platform}"
        for game in games
    ]

    user_profile = (
        f"{user.favorite_genres} "
        f"{user.preferred_platform}"
    )

    vectorizer = TfidfVectorizer()

    tfidf_matrix = vectorizer.fit_transform(
        game_texts + [user_profile]
    )

    similarity = cosine_similarity(
        tfidf_matrix[-1],
        tfidf_matrix[:-1]
    )

    scored_games = list(zip(games, similarity[0]))

    scored_games.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return scored_games


def fallback_recommendations(games):
    return get_popular_games(games)