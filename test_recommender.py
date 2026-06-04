from app.recommender import build_recommendations
from app.filters import filter_games


class MockUser:
    favorite_genres = "RPG Action Fantasy"
    preferred_platform = "PC"
    max_price = 2500
    max_playtime = 100
    max_age_rating = 18
    region = "RU"


class MockGame:
    def __init__(
        self,
        title,
        genres,
        platform,
        price,
        rating,
        playtime,
        age_rating,
        region,
    ):
        self.id = 1
        self.title = title
        self.genres = genres
        self.platform = platform
        self.price = price
        self.rating = rating
        self.playtime = playtime
        self.age_rating = age_rating
        self.region = region


def test_build_recommendations_returns_sorted_games():
    user = MockUser()

    games = [
        MockGame(
            "FIFA 24",
            "Sports Football Multiplayer",
            "PC",
            1999,
            7.5,
            25,
            3,
            "RU",
        ),
        MockGame(
            "The Witcher 3",
            "RPG Fantasy Open-World",
            "PC",
            1499,
            9.8,
            60,
            18,
            "RU",
        ),
    ]

    recommendations = build_recommendations(user, games)

    assert len(recommendations) == 2
    assert recommendations[0][0].title == "The Witcher 3"


def test_context_filter_removes_wrong_platform():
    user = MockUser()

    games = [
        (
            MockGame(
                "God of War Ragnarok",
                "Action Adventure Mythology",
                "PS5",
                3499,
                9.4,
                35,
                18,
                "EU",
            ),
            0.9,
        ),
        (
            MockGame(
                "Cyberpunk 2077",
                "RPG Action Open-World",
                "PC",
                1999,
                9.1,
                40,
                18,
                "RU",
            ),
            0.8,
        ),
    ]

    filtered = filter_games(user, games)

    assert len(filtered) == 1
    assert filtered[0][0].title == "Cyberpunk 2077"


def test_context_filter_removes_too_expensive_game():
    user = MockUser()

    games = [
        (
            MockGame(
                "Expensive Game",
                "RPG Action",
                "PC",
                5000,
                8.0,
                30,
                18,
                "RU",
            ),
            0.9,
        )
    ]

    filtered = filter_games(user, games)

    assert len(filtered) == 0