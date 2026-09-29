from app.ai_helper import StudyAI, string_list


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


def test_string_list_filters_blank_and_non_string_items():
    assert string_list([" a ", "", "  ", 42, None, "b"], limit=8) == ["a", "b"]


def test_string_list_respects_limit():
    assert string_list(["a", "b", "c"], limit=2) == ["a", "b"]


def test_string_list_rejects_non_list_and_non_positive_limit():
    assert string_list("not-a-list") is None
    assert string_list(None) is None
    assert string_list(["a"], limit=0) is None
    assert string_list(["a", "b"], limit=-1) is None


def test_study_ai_falls_back_to_default_cache_settings_for_invalid_env(monkeypatch):
    monkeypatch.setenv("STUDY_AI_CACHE_TTL_SECONDS", "not-a-number")
    monkeypatch.setenv("STUDY_AI_CACHE_MAX_ENTRIES", "also-bad")
    study_ai = StudyAI()

    assert study_ai._cache_ttl_seconds == 300
    assert study_ai._cache_max_entries == 128


def test_study_ai_clamps_negative_cache_settings(monkeypatch):
    monkeypatch.setenv("STUDY_AI_CACHE_TTL_SECONDS", "-5")
    monkeypatch.setenv("STUDY_AI_CACHE_MAX_ENTRIES", "-3")
    study_ai = StudyAI()

    assert study_ai._cache_ttl_seconds == 0  # TTL 0 disables the cache
    assert study_ai._cache_max_entries == 1  # at least one cache entry
