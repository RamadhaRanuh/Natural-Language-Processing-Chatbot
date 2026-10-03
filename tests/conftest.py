import hashlib
import json
from dataclasses import replace
import httpx
import pytest
from fastapi.testclient import TestClient
from src.api import create_app
from src.config import Config

XML = b'<article><front><license href="https://creativecommons.org/licenses/by/4.0/">CC BY</license></front><body><p>In 100 adults, education was studied for 12 months. The reported value was 5.60 mmol/mol.</p></body></article>'


@pytest.fixture
def harness(tmp_path):
    """Synthetic public literature, never a real clinical approval fixture."""
    source = {
        "id": "test-source", "title": "Synthetic research fixture", "authors": ["Test Researcher"],
        "year": 2020, "doi": "10.1234/test", "pmid": "123", "pmcid": "PMC123",
        "url": "https://doi.org/10.1234/test", "license": "CC BY 4.0",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "document_hash": hashlib.sha256(XML).hexdigest(), "kind": "paper",
        "population": "Synthetic 100 adults", "design": "Synthetic trial",
        "limitations": ["Test data, not medical evidence."],
        "passages": [{"id": "p1", "text": "In 100 adults, education was studied for 12 months. The reported value was 5.60 mmol/mol.", "locator": "./body/p"}],
        "claims": [{"id": "test-claim", "topic": "education", "text_en": "education was studied for 12 months.",
                    "passage_id": "p1", "text_id": None,
                    "data": [{"label": "Reported value", "value": "5.60", "unit": "mmol/mol", "passage_id": "p1", "locator": "./body/p"}]}],
    }
    metadata = {"id": "123", "source": "MED", "doi": "10.1234/test", "pmcid": "PMC123", "isOpenAccess": "Y",
                "pubTypeList": {"pubType": ["Randomized Controlled Trial"]}}
    corpus_path, review_path = tmp_path / "corpus.json", tmp_path / "review.json"
    state = {"metadata": metadata, "xml": XML, "requests": [], "status": 200, "selector": {"claim_ids": ["test-claim"]}}

    def transport(request):
        state["requests"].append(request)
        if request.url.path.endswith("/chat/completions"):
            return httpx.Response(200, json={"choices": [{"message": {"content": json.dumps(state["selector"])}}]})
        if state["status"] != 200:
            return httpx.Response(state["status"])
        if request.url.path.endswith("/search"):
            return httpx.Response(200, json={"hitCount": 1, "resultList": {"result": [state["metadata"]]}})
        return httpx.Response(200, content=state["xml"])

    def app(environment="development", review=None, model=False):
        corpus_path.write_text(json.dumps({"version": "test", "sources": [source]}), encoding="utf-8")
        review_path.write_text(json.dumps(review or {}), encoding="utf-8")
        config = replace(Config(), corpus_path=corpus_path, review_path=review_path, environment=environment, status_max_age_seconds=1)
        if model:
            config = replace(config, model_url="https://model.test/v1", model_key="test-only", model_name="selector")
        return TestClient(create_app(config, httpx.MockTransport(transport)))

    return source, state, app


@pytest.fixture
def question():
    return {"messages": [{"role": "user", "content": "What did diabetes education studies find?"}],
            "language": "en", "adult_user": True, "adult_patient": True}
