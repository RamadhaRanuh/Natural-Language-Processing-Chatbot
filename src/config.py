from dataclasses import dataclass
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class Config:
    corpus_path: Path = ROOT / "data/evidence/pilot.json"
    review_path: Path = ROOT / "data/evidence/review.json"
    environment: str = "development"
    provider_url: str = "https://www.ebi.ac.uk/europepmc/webservices/rest"
    model_url: str | None = None
    model_key: str | None = None
    model_name: str = ""
    status_max_age_seconds: int = 300
    max_body_bytes: int = 32_768

    def __post_init__(self):
        if self.environment not in {"development", "production"}:
            raise ValueError("APP_ENV must be development or production.")

    @classmethod
    def from_env(cls) -> "Config":
        return cls(
            corpus_path=Path(os.getenv("EVIDENCE_CORPUS", str(ROOT / "data/evidence/pilot.json"))),
            review_path=Path(os.getenv("CLINICAL_REVIEW", str(ROOT / "data/evidence/review.json"))),
            environment=os.getenv("APP_ENV", "production"),
            model_url=os.getenv("MODEL_BASE_URL") or None,
            model_key=os.getenv("MODEL_API_KEY") or None,
            model_name=os.getenv("MODEL_NAME", ""),
        )
