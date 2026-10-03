"""Bilingual interaction guards, not a validated emergency/diagnostic detector."""
import re
import hashlib
import json

SAFETY_URL = "https://kemkes.go.id/"
EMERGENCY = (
    r"\b(can'?t breathe|cannot breathe|unconscious|severe chest pain|overdose|suicid\w*)\b",
    r"\b(tidak bisa bernapas|sulit bernapas|tidak sadar|nyeri dada hebat|overdosis|bunuh diri)\b",
)
PERSONAL = (
    r"\b(diagnos\w* me|do i have|what disease do i|should i (stop|start|take|increase|decrease)|change my dose|how much (insulin|metformin)|my (dose|target)|am i safe)\b",
    r"\b(apakah saya (menderita|terkena)|diagnosis saya|haruskah saya|ubah dosis|berapa (dosis|insulin)|dosis saya|target saya|aman untuk saya)\b",
)
SPECIAL = (
    r"\b(pregnan\w*|gestational|child|children|baby|toddler|type 1|t1d)\b",
    r"\b(hamil|kehamilan|gestasional|anak|bayi|balita|tipe 1)\b",
)


def guard(text: str) -> str | None:
    if any(re.search(p, text, re.I) for p in EMERGENCY):
        return "safety"
    if any(re.search(p, text, re.I) for p in PERSONAL + SPECIAL):
        return "blocked_by_scope"
    return None


def policy_hash() -> str:
    # Bind the clinical review to both routing and every fixed localized message.
    from .service import TEXT
    content = {"emergency": EMERGENCY, "personal": PERSONAL, "special": SPECIAL, "url": SAFETY_URL, "messages": TEXT}
    return hashlib.sha256(json.dumps(content, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
