import hashlib
import json
import time
from datetime import datetime, timedelta, timezone
import pytest
from src.contracts import Source
from src.verification import record_hash


def test_committed_answer_has_inspectable_source_and_numbers(harness, question):
    _, state, app = harness
    with app() as client:
        result = client.post("/v1/chat", json=question)
    assert result.status_code == 200
    body = result.json()
    assert body["status"] == "ready" and body["research_preview"]
    assert body["claims"][0]["verification"] == "source_extract"
    assert body["claims"][0]["data"][0]["value"] == "5.60"
    assert body["claims"][0]["data_passages"][0]["locator"] == "./body/p"
    assert body["claims"][0]["source_id"] == body["sources"][0]["id"]
    assert result.headers["cache-control"] == "no-store"
    assert len(state["requests"]) == 2


@pytest.mark.parametrize("mutation", ["unknown_value", "wrong_unit", "wrong_locator", "new_medical_prose", "empty_claim"])
def test_unverifiable_generated_content_never_publishes(harness, question, mutation):
    source, _, app = harness
    claim = source["claims"][0]
    if mutation == "unknown_value": claim["data"][0]["value"] = "50"
    if mutation == "wrong_unit": claim["data"][0]["unit"] = "mg"
    if mutation == "wrong_locator": claim["data"][0]["locator"] = "./body/elsewhere"
    if mutation == "new_medical_prose": claim["text_en"] = "You should take insulin now."
    if mutation == "empty_claim": claim["text_en"] = ""
    with app() as client:
        body = client.post("/v1/chat", json=question).json()
    assert body["claims"] == [] and body["sources"] == []
    assert body["status"] == "insufficient_evidence"


@pytest.mark.parametrize("mutation", ["retracted", "concern", "correction", "wrong_doi", "wrong_pmcid", "unknown_access", "missing_types", "changed_document", "provider_error", "xml_entity"])
def test_failed_provenance_is_not_silently_bypassed(harness, question, mutation):
    source, state, app = harness
    if mutation == "retracted": state["metadata"]["pubTypeList"]["pubType"] = ["Retracted Publication"]
    if mutation == "concern": state["metadata"]["commentCorrectionList"] = {"commentCorrection": [{"type": "Expression of concern in"}]}
    if mutation == "correction": state["metadata"]["commentCorrectionList"] = {"commentCorrection": [{"type": "Erratum in", "id": "456"}]}
    if mutation == "wrong_doi": state["metadata"]["doi"] = "10.1234/other"
    if mutation == "wrong_pmcid": state["metadata"]["pmcid"] = "PMC456"
    if mutation == "unknown_access": state["metadata"].pop("isOpenAccess")
    if mutation == "missing_types": state["metadata"].pop("pubTypeList")
    if mutation == "changed_document": state["xml"] += b" "
    if mutation == "provider_error": state["status"] = 503
    if mutation == "xml_entity":
        state["xml"] = b'<!DOCTYPE x [<!ENTITY a SYSTEM "file:///etc/passwd">]><article>&a;</article>'
        source["document_hash"] = hashlib.sha256(state["xml"]).hexdigest()
    with app() as client:
        body = client.post("/v1/chat", json=question).json()
    assert body["claims"] == [] and body["status"] == "insufficient_evidence"


def test_passage_must_exist_at_its_locator_not_elsewhere(harness, question):
    source, _, app = harness
    source["passages"][0]["locator"] = "./front/license"
    source["claims"][0]["data"][0]["locator"] = "./front/license"
    with app() as client:
        assert client.post("/v1/chat", json=question).json()["claims"] == []


def test_numeric_prefix_cannot_substitute_one_for_one_hundred(harness, question):
    source, _, app = harness
    source["claims"][0]["data"][0].update(value="1", unit=None)
    with app() as client:
        assert client.post("/v1/chat", json=question).json()["claims"] == []


def test_production_requires_real_bound_review_records(harness, question):
    _, state, app = harness
    with app("production") as client:
        result = client.post("/v1/chat", json=question).json()
        assert not client.get("/health").json()["clinical_release_ready"]
    assert result["status"] == "review_required" and result["claims"] == []
    assert not state["requests"]


def test_unreviewed_translation_never_becomes_a_medical_answer(harness, question):
    source, _, app = harness
    source["claims"][0]["text_id"] = "Terjemahan yang tidak ditinjau"
    question["language"] = "id"
    with app() as client:
        body = client.post("/v1/chat", json=question).json()
    assert body["claims"][0]["display_language"] == "en"
    assert "Terjemahan yang tidak ditinjau" not in json.dumps(body)
    assert any("Terjemahan" in note for note in body["notices"])


def test_translation_review_is_bound_to_source_and_exact_text(harness, question):
    source, _, app = harness
    source["claims"][0]["text_id"] = "Reviewed synthetic wording"
    digest = hashlib.sha256((record_hash(Source.model_validate(source)) + source["claims"][0]["text_id"]).encode()).hexdigest()
    now = datetime.now(timezone.utc)
    reviews = {"translations": {"test-claim": {
        "record_hash": digest, "reviewer": "Synthetic test fixture",
        "approved_at": (now - timedelta(days=1)).isoformat(),
        "expires_at": (now + timedelta(days=1)).isoformat(),
    }}}
    question["language"] = "id"
    with app(review=reviews) as client:
        assert client.post("/v1/chat", json=question).json()["claims"][0]["display_language"] == "id"
    source["claims"][0]["text_id"] += " added instruction"
    with app(review=reviews) as client:
        assert client.post("/v1/chat", json=question).json()["claims"][0]["display_language"] == "en"


def test_cached_success_expires_before_later_retraction(harness, question):
    _, state, app = harness
    with app() as client:
        assert client.post("/v1/chat", json=question).json()["status"] == "ready"
        state["metadata"]["pubTypeList"]["pubType"] = ["Retracted Publication"]
        time.sleep(1.05)
        assert client.post("/v1/chat", json=question).json()["claims"] == []


def test_optional_model_receives_no_patient_text_and_cannot_invent_ids(harness, question):
    _, state, app = harness
    question["messages"][0]["content"] += " My name is PrivatePerson and I live at PrivateAddress."
    question["use_model"] = True
    state["selector"] = {"claim_ids": ["invented-id"]}
    with app(model=True) as client:
        assert client.post("/v1/chat", json=question).json()["claims"] == []
    payload = json.loads(state["requests"][0].content)
    assert "PrivatePerson" not in json.dumps(payload) and "PrivateAddress" not in json.dumps(payload)
    assert "education" in json.dumps(payload)


def test_expired_review_cannot_enable_production(harness, question):
    source, _, app = harness
    reviews = {"sources": {"test-source": {
        "record_hash": record_hash(Source.model_validate(source)), "reviewer": "Synthetic test only",
        "approved_at": "2000-01-01T00:00:00Z", "expires_at": "2001-01-01T00:00:00Z",
    }}}
    with app("production", review=reviews) as client:
        assert not client.get("/health").json()["clinical_release_ready"]
        assert client.post("/v1/chat", json=question).json()["claims"] == []


def test_invalid_environment_cannot_silently_enable_preview():
    from src.config import Config
    with pytest.raises(ValueError):
        Config(environment="prod")


def test_valid_synthetic_source_and_policy_review_enable_production_path(harness, question):
    from src.safety import policy_hash
    source, _, app = harness
    now = datetime.now(timezone.utc)
    def approval(digest):
        return {
            "record_hash": digest, "reviewer": "Synthetic test only",
            "approved_at": (now - timedelta(days=1)).isoformat(),
            "expires_at": (now + timedelta(days=1)).isoformat(),
        }
    reviews = {
        "sources": {"test-source": approval(record_hash(Source.model_validate(source)))},
        "safety": approval(policy_hash()),
    }
    with app("production", review=reviews) as client:
        body = client.post("/v1/chat", json=question).json()
        assert body["status"] == "ready" and not body["research_preview"]
        assert client.get("/health").json()["clinical_release_ready"]
    source["population"] += " altered interpretation"
    with app("production", review=reviews) as client:
        assert client.post("/v1/chat", json=question).json()["claims"] == []
