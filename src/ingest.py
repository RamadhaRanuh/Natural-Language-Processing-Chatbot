"""Inspect source record hashes without ingesting historical PDFs."""
import json
from .config import Config
from .contracts import Corpus
from .verification import record_hash

if __name__ == "__main__":
    corpus = Corpus.model_validate_json(Config.from_env().corpus_path.read_text(encoding="utf-8"))
    print(json.dumps({"version": corpus.version, "sources": [
        {"id": s.id, "record_hash": record_hash(s), "license": s.license} for s in corpus.sources
    ]}, indent=2))
