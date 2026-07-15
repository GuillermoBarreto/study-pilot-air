from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_zybooks_summary_endpoint():
    response = client.post(
        "/zybooks",
        json={
            "text": "Functions are reusable blocks of code. They help organize programs and reduce repetition. Variables store values that can be used later."
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "Functions" in data["summary"] or "reusable" in data["summary"]
    assert len(data["key_concepts"]) >= 1
    assert len(data["quick_questions"]) == 2
