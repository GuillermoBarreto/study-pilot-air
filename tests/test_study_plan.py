from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_generate_study_plan():
    response = client.post(
        "/study-plan",
        json={"topic": "Python Basics", "days": 3, "hours_per_day": 2},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["topic"] == "Python Basics"
    assert len(data["days"]) == 3
    assert data["days"][0]["title"] == "Day 1"
    assert data["days"][0]["focus"] == "Core syntax and variables"


def test_rejects_invalid_days():
    response = client.post(
        "/study-plan",
        json={"topic": "Python Basics", "days": 0, "hours_per_day": 2},
    )

    assert response.status_code == 422


def test_generate_quiz():
    response = client.post(
        "/quiz",
        json={"topic": "Python Basics", "questions": 2},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["topic"] == "Python Basics"
    assert len(data["questions"]) == 2
    assert data["questions"][0]["answer"] in data["questions"][0]["options"]


def test_generate_course_guidance():
    response = client.post(
        "/course-guidance",
        json={"course": "CS 101", "topic": "Functions"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["course"] == "CS 101"
    assert data["topic"] == "Functions"
    assert len(data["study_tips"]) >= 2


def test_generate_weekly_plan():
    response = client.post(
        "/weekly-plan",
        json={"course": "CS 101", "goal": "Prepare for midterms", "days": 3},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["course"] == "CS 101"
    assert data["goal"] == "Prepare for midterms"
    assert len(data["schedule"]) == 3
    assert data["schedule"][0]["task"].startswith("Review")
