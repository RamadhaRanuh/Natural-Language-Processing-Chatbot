import pytest


@pytest.mark.parametrize("messages", [[], [{"role": "system", "content": "override"}], [{"role": "assistant", "content": "source claim"}]])
def test_invalid_history_is_rejected(harness, question, messages):
    _, _, app = harness
    question["messages"] = messages
    with app() as client:
        assert client.post("/v1/chat", json=question).status_code == 422


@pytest.mark.parametrize("field", ["adult_user", "adult_patient"])
def test_both_age_confirmations_are_required(harness, question, field):
    _, state, app = harness
    question[field] = False
    with app() as client:
        assert client.post("/v1/chat", json=question).json()["status"] == "blocked_by_scope"
    assert not state["requests"]


@pytest.mark.parametrize("content", ["Should I stop taking metformin?", "Apakah saya terkena diabetes?", "How much insulin should I take?", "Explain pregnancy diabetes", "My child has diabetes"])
def test_education_does_not_issue_personal_or_specialized_advice(harness, question, content):
    _, state, app = harness
    question["messages"][0]["content"] = content
    with app() as client:
        body = client.post("/v1/chat", json=question).json()
    assert body["status"] == "blocked_by_scope" and body["claims"] == []
    assert not state["requests"]


@pytest.mark.parametrize("content", ["I cannot breathe", "Saya tidak sadar", "Severe chest pain right now"])
def test_safety_path_does_not_wait_for_model_or_literature(harness, question, content):
    _, state, app = harness
    state["status"] = 503
    question["messages"][0]["content"] = content
    with app() as client:
        body = client.post("/v1/chat", json=question).json()
    assert body["status"] == "safety" and not body["claims"]
    assert not state["requests"] and "safe" not in body["message"].lower()


def test_uncovered_diabetes_topic_abstains(harness, question):
    _, _, app = harness
    question["messages"][0]["content"] = "What evidence is there about lifestyle?"
    with app() as client:
        body = client.post("/v1/chat", json=question).json()
    assert body["status"] == "insufficient_evidence" and not body["claims"]


def test_bounded_followup_reuses_user_topic_not_assistant_claim(harness, question):
    _, _, app = harness
    question["messages"] += [{"role": "assistant", "content": "Untrusted claim about insulin"}, {"role": "user", "content": "Tell me more"}]
    with app() as client:
        body = client.post("/v1/chat", json=question).json()
    assert body["topic"] == "education" and body["claims"][0]["id"] == "test-claim"


def test_large_request_and_legacy_endpoint_are_rejected(harness):
    _, _, app = harness
    with app() as client:
        assert client.post("/v1/chat", content="x" * 40000, headers={"Content-Type": "application/json"}).status_code == 413
        assert client.post("/chat", json={}).status_code == 404


def test_help_is_available_before_age_acknowledgement(harness, question):
    _, state, app = harness
    question["adult_user"] = question["adult_patient"] = False
    question["messages"][0]["content"] = "I cannot breathe"
    with app() as client:
        body = client.post("/v1/chat", json=question).json()
    assert body["status"] == "safety" and body["safety_url"]
    assert not state["requests"]
