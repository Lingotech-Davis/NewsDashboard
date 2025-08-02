"""requirements.txt
httpx
pytest # should be preinstalled
"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_read_ping():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "pong"}


def test_env_load():
    response = client.get("/env-check")
    assert response.status_code == 200
    expected_keys = [
        "GEMINI_API_KEY",
        "NEWS_API_KEY",
        "DB_USER",
        "DB_PASSWORD",
        "DB_NAME",
    ]
    # print(response.json())
    response_keys = set(response.json().keys())
    assert response_keys == set(expected_keys)
    response_values = set(response.json().values())
    assert None not in response_values


def test_env_load_in_router():
    response = client.get("/api/v1/env-check")
    assert response.status_code == 200
    expected_keys = [
        "GEMINI_API_KEY",
        "NEWS_API_KEY",
        "DB_USER",
        "DB_PASSWORD",
        "DB_NAME",
    ]
    # print(response.json())
    response_keys = set(response.json().keys())
    assert response_keys == set(expected_keys)
    response_values = set(response.json().values())
    assert None not in response_values
