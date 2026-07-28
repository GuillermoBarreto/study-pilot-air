from app.ai_helper import StudyAI


def test_generate_json_reuses_recent_matching_result(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    study_ai = StudyAI()

    class Responses:
        calls = 0

        def create(self, **_kwargs):
            self.calls += 1
            return type("Response", (), {"output_text": '{"result": "cached"}'})()

    responses = Responses()
    study_ai._client = type("Client", (), {"responses": responses})()

    first = study_ai.generate_json("Make JSON", "Functions")
    second = study_ai.generate_json("Make JSON", "Functions")

    assert first == {"result": "cached"}
    assert second == {"result": "cached"}
    assert responses.calls == 1


def test_cached_result_cannot_be_mutated_by_a_caller(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    study_ai = StudyAI()

    class Responses:
        def create(self, **_kwargs):
            return type("Response", (), {"output_text": '{"result": "original"}'})()

    study_ai._client = type("Client", (), {"responses": Responses()})()
    result = study_ai.generate_json("Make JSON", "Functions")
    result["result"] = "changed"

    assert study_ai.generate_json("Make JSON", "Functions") == {"result": "original"}
