"""Conservative publication gate. Containment is not clinical truth."""
import hashlib
import json
import re
from datetime import datetime, timezone
from .contracts import Source, CorpusClaim, PublishedClaim


def normalize(text: str) -> str:
    return " ".join(text.split())


def record_hash(source: Source) -> str:
    body = json.dumps(source.model_dump(), sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(body.encode()).hexdigest()


class VerificationError(ValueError):
    pass


def valid_review(review: dict, expected_hash: str) -> bool:
    """Approvals are operator-supplied, version-bound, dated and expiring."""
    try:
        approved_at = datetime.fromisoformat(review["approved_at"].replace("Z", "+00:00"))
        expires_at = datetime.fromisoformat(review["expires_at"].replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        return bool(review.get("reviewer") and review.get("record_hash") == expected_hash and approved_at <= now < expires_at)
    except (KeyError, ValueError, TypeError, AttributeError):
        return False


def verify_claim(source: Source, claim: CorpusClaim, language: str, reviews: dict) -> PublishedClaim:
    passages = {p.id: p for p in source.passages}
    passage = passages.get(claim.passage_id)
    if passage is None or normalize(claim.text_en) not in normalize(passage.text):
        raise VerificationError("Claim is not an exact extract of its source passage.")
    if not claim.text_en.strip() or len(claim.text_en.split()) > 25:
        raise VerificationError("Source extracts must be short and nonempty.")
    for datum in claim.data:
        supporting = passages.get(datum.passage_id)
        if supporting is None or datum.locator != supporting.locator:
            raise VerificationError("Data lacks its specific source locator.")
        value = re.escape(normalize(datum.value))
        if not re.search(r"(?<![\w.])" + value + r"(?![\w.])", normalize(supporting.text)):
            raise VerificationError("Reported value is absent from its bound passage.")
        if datum.unit and normalize(datum.unit) not in normalize(supporting.text):
            raise VerificationError("Reported unit is absent from its bound passage.")
    text, display_language, method = claim.text_en, "en", "source_extract"
    if language == "id" and claim.text_id:
        translation = reviews.get("translations", {}).get(claim.id, {})
        digest = hashlib.sha256((record_hash(source) + claim.text_id).encode()).hexdigest()
        if valid_review(translation, digest):
            text, display_language, method = claim.text_id, "id", "reviewed_translation"
    return PublishedClaim(
        id=claim.id, source_id=source.id, text=text, display_language=display_language,
        verification=method, passage=passage, data=claim.data,
        data_passages=[passages[x] for x in dict.fromkeys(d.passage_id for d in claim.data)],
    )
