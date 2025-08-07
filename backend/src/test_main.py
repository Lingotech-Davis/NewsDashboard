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


def test_top_stories():
    response = client.get("/api/v1/top-stories")
    assert response.status_code == 200
    data = response.json()
    assert {"status", "totalResults", "articles"} == set(data.keys())
    assert data["totalResults"] > 0


def test_extract_news_malformed_url():
    response = client.post(
        "/api/v1/news-extract", json={"story_url": "this-is-not-a-real-url"}
    )

    # Assert that the API correctly returns a 500 status code
    # and the expected error message.
    assert response.status_code == 422
    assert "Invalid URL format" in response.json()["detail"]


def test_extraction():
    test_url = "https://www.livescience.com/animals/land-mammals/virginia-opossums-the-american-marsupials-that-have-barely-changed-since-the-time-of-the-dinosaurs"
    test_title = "Virginia opossums: The American marsupials that have barely changed since the time of the dinosaur"
    test_text = "QUICK FACTS Name: Virginia opossum (Didelphis virginiana) Where it lives: Central and North America What it eats: Fruit, insects, small animals and carrion\nWith their beady eyes, big ears, hairless tails and short, stocky legs, opossums are distinctive marsupials. Despite their odd appearance, these animals have a rich evolutionary history and have remained largely unchanged for millions of years. Their remarkable ability to adapt to different environments, food sources and predators has helped them survive from the time of the dinosaurs to today.\nThe Virginia opossum is the only opossum species found in the United States and Canada. Opossums have the smallest brain-to-weight ratio of any North American mammal.\nThe earliest known relatives of modern opossums lived over 65 million years ago, around the time dinosaurs went extinct. A 2009 study published in PLOS ONE found that peradectids, a family of marsupials known from fossils mostly in North America and Eurasia, are the closest extinct relatives of living opossums. Like modern opossums, peradectids had opposable thumbs on their hind feet and a similarly shaped skull — features that have remained nearly unchanged for millions of years. The earliest opossum fossils date back to the early Miocene epoch, roughly 20 million years ago.\nOne key reason why opossums have survived for so long with few changes is because they are adaptable. These marsupials eat almost anything, including fruit, insects, small animals and animal carcasses. They can live anywhere from forests to urban backyards. And, although they are mostly nocturnal, they can sometimes be seen in daylight if food is scarce.\nOpossums are also resistant to snake venom , particularly that of rattlesnakes and other pit vipers. This resistance is due to a protein called Lethal Toxin Neutralising Factor found in their blood, which can neutralize various toxins in snake venom. This enables opossums to prey on venomous snakes that would otherwise be a threat.\nOpossum moms carry their babies around on their backs until they are about 12 weeks old. (Image credit: Specialjake CC BY-SA 3.0 , via Wikimedia Commons)\nOpossums give birth to underdeveloped young, which crawl into a pouch and nurse for around eight weeks as they grow. Young opossums then ride on their mother's back for several weeks until they become independent at 12 weeks old.\nWhen threatened, opossums may growl, hiss, bare their teeth or climb a nearby tree to escape. If escape isn't possible, they resort to \"playing dead\" — a defense mechanism known as thanatosis .\nSign up for the Live Science daily newsletter now Get the world’s most fascinating discoveries delivered straight to your inbox. Contact me with news and offers from other Future brands Receive email from us on behalf of our trusted partners or sponsors"

    response = client.post("/api/v1/news-extract", json={"story_url": test_url})

    assert response.status_code == 200
    data = response.json()
    assert "title" in data
    assert "text" in data
    assert data["title"] == test_title
    assert data["text"] == test_text
