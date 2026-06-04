from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "ПМ ИПВ работает"
    }


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok"
    }


def test_get_games():
    response = client.get("/games")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_user():
    response = client.get("/users/1")

    assert response.status_code == 200
    assert response.json()["username"] == "ilya"


def test_recommendations():
    response = client.post("/recommend/1")

    assert response.status_code == 200

    data = response.json()

    assert "recommendations" in data
    assert data["recommendations_count"] > 0
def test_create_user():
    response = client.post(
        "/users",
        json={
            "username": "test_user",
            "favorite_genres": "RPG Action",
            "preferred_platform": "PC",
            "max_price": 3000,
            "max_playtime": 100,
            "max_age_rating": 18,
            "region": "RU"
        }
    )

    assert response.status_code == 200
    data = response.json()

    assert data["username"] == "test_user"


def test_create_game():
    response = client.post(
        "/games",
        json={
            "title": "Test Game",
            "genres": "Action RPG",
            "platform": "PC",
            "price": 999,
            "rating": 8.5,
            "playtime": 25,
            "age_rating": 16,
            "region": "RU"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Test Game"


def test_export_json():
    response = client.get("/export/json/1")

    assert response.status_code == 200


def test_export_csv():
    response = client.get("/export/csv/1")

    assert response.status_code == 200


def test_invalid_user():
    response = client.get("/users/99999")

    assert response.status_code == 404


def test_invalid_recommend_user():
    response = client.post("/recommend/99999")

    assert response.status_code == 404


def test_root_message():
    response = client.get("/")

    assert "ПМ ИПВ" in response.json()["message"]


def test_games_not_empty():
    response = client.get("/games")

    data = response.json()

    assert len(data) > 0


def test_recommendations_have_similarity():
    response = client.post("/recommend/1")

    data = response.json()

    assert "similarity" in data["recommendations"][0]


def test_recommendations_have_explanation():
    response = client.post("/recommend/1")

    data = response.json()

    assert "explanation" in data["recommendations"][0]


def test_recommendations_count():
    response = client.post("/recommend/1")

    data = response.json()

    assert data["recommendations_count"] > 0


def test_response_time_exists():
    response = client.post("/recommend/1")

    data = response.json()

    assert "response_time_seconds" in data


def test_algorithm_name_exists():
    response = client.post("/recommend/1")

    data = response.json()

    assert "algorithm" in data


def test_recommendation_contains_title():
    response = client.post("/recommend/1")

    data = response.json()

    assert "title" in data["recommendations"][0]


def test_recommendation_contains_rating():
    response = client.post("/recommend/1")

    data = response.json()

    assert "rating" in data["recommendations"][0]    