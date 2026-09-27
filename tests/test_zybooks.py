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


def test_zybooks_helper_handles_non_string_text():
    from app.zybooks_helper import ZyBooksHelper

    helper = ZyBooksHelper()
    assert helper.summarize_text(None) == "No content available."
    assert helper.summarize_text(123) == "No content available."
    assert helper.extract_key_concepts(None) == []
    assert helper.extract_key_concepts(123) == []
