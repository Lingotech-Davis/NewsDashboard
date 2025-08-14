"""requirements.txt
httpx
pytest # should be preinstalled
"""

import json
import os

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


def test_top_stories():
    response = client.get("/api/news/top-stories")
    assert response.status_code == 200
    data = response.json()
    assert {"status", "totalResults", "articles"} == set(data.keys())
    assert data["totalResults"] > 0


def test_extract_news_malformed_url():
    test_url = "this-is-not-a-real-url"
    response = client.get(f"/api/news/news-extract?story_url={test_url}")

    print(response.json())
    assert response.status_code == 422
    assert "Received invalid URL format" in response.json()["detail"]


def test_extraction():
    filename = os.path.join("src", "test_suite_responses.json")
    with open(filename, "r") as f:
        data = json.load(f)
        data = data["test_extraction"]

    test_url = data["test_url"]
    test_title = data["test_title"]
    test_text = data["test_text"]

    response = client.get(f"/api/news/news-extract?story_url={test_url}")

    assert response.status_code == 200
    data = response.json()
    assert "title" in data
    assert "text" in data
    assert data["title"] == test_title
    assert data["text"] == test_text
