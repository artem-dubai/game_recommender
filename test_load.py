import time
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_recommendation_response_time():
    start_time = time.perf_counter()

    response = client.post("/recommend/1")

    end_time = time.perf_counter()
    response_time = end_time - start_time

    assert response.status_code == 200
    assert response_time < 2.0