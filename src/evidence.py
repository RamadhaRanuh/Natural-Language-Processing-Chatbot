"""Public-literature provenance with freshness and fail-closed source checks."""
import asyncio
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
import re
import time
import httpx
from defusedxml import ElementTree
from defusedxml.common import DefusedXmlException
from .config import Config
from .contracts import Corpus, Source
from .verification import normalize, record_hash, valid_review


class EvidenceUnavailable(ValueError):
    pass


@dataclass(frozen=True)
class SourceCheck:
    checked_at: str
    document_hash: str


def node_text(node) -> str:
    if node.tag.split("}")[-1] == "tr":
        return normalize(" | ".join(normalize("".join(cell.itertext())) for cell in node))
    return normalize("".join(node.itertext()))


class EvidenceRepository:
    def __init__(self, config: Config, client: httpx.AsyncClient):
        self.config, self.client = config, client
        self.corpus = Corpus.model_validate_json(config.corpus_path.read_text(encoding="utf-8"))
        self.reviews = json.loads(config.review_path.read_text(encoding="utf-8"))
        self.cache: dict[str, tuple[float, SourceCheck]] = {}
        self.lock = asyncio.Lock()
        source_ids = [s.id for s in self.corpus.sources]
        claim_ids = [c.id for s in self.corpus.sources for c in s.claims]
        if len(source_ids) != len(set(source_ids)) or len(claim_ids) != len(set(claim_ids)):
            raise EvidenceUnavailable("Corpus IDs must be unique.")

    def approved(self, source: Source) -> bool:
        record = self.reviews.get("sources", {}).get(source.id, {})
        return bool(
            valid_review(record, record_hash(source))
            and set(source.publication_status.get("review_blockers", [])) <= set(record.get("resolved_issues", []))
        )

    def safety_approved(self) -> bool:
        from .safety import policy_hash
        return valid_review(self.reviews.get("safety", {}), policy_hash())

    async def check(self, source: Source) -> SourceCheck:
        key = record_hash(source)
        async with self.lock:
            cached = self.cache.get(key)
            if cached and time.monotonic() - cached[0] < self.config.status_max_age_seconds:
                return cached[1]
            result = await self._fetch_check(source)
            self.cache[key] = (time.monotonic(), result)
            return result

    async def _fetch_check(self, source: Source) -> SourceCheck:
        if not re.fullmatch(r"\d+", source.pmid) or not re.fullmatch(r"PMC\d+", source.pmcid):
            raise EvidenceUnavailable("Malformed literature identifiers.")
        if not source.license_url.startswith(("https://creativecommons.org/licenses/by/", "http://creativecommons.org/licenses/by/", "https://creativecommons.org/publicdomain/zero/")):
            raise EvidenceUnavailable("License is outside the permitted allowlist.")
        try:
            response = await self.client.get(self.config.provider_url + "/search", params={
                "query": "EXT_ID:" + source.pmid + " AND SRC:MED", "format": "json", "resultType": "core",
            })
            response.raise_for_status()
            payload = response.json()
            rows = payload.get("resultList", {}).get("result", [])
            if payload.get("hitCount") != 1 or len(rows) != 1:
                raise EvidenceUnavailable("Source identity was not resolved.")
            metadata = rows[0]
            if str(metadata.get("id")) != source.pmid or metadata.get("pmcid") != source.pmcid or metadata.get("source") != "MED":
                raise EvidenceUnavailable("Source identity mismatch.")
            if str(metadata.get("doi", "")).lower() != source.doi.lower():
                raise EvidenceUnavailable("Source DOI mismatch.")
            types = metadata.get("pubTypeList", {}).get("pubType")
            if not isinstance(types, list) or metadata.get("isOpenAccess") != "Y":
                raise EvidenceUnavailable("Source access/status metadata is incomplete.")
            if metadata.get("isRetracted") == "Y" or any("retract" in t.lower() or "expression of concern" in t.lower() for t in types):
                raise EvidenceUnavailable("Source has a retraction or concern notice.")
            comments = metadata.get("commentCorrectionList", {}).get("commentCorrection", [])
            if any("retract" in str(c).lower() or "concern" in str(c).lower() for c in comments):
                raise EvidenceUnavailable("Source has a retraction or concern relationship.")
            if comments:
                correction = self.reviews.get("corrections", {}).get(source.id, {})
                expected = hashlib.sha256(json.dumps(comments, sort_keys=True).encode()).hexdigest()
                if not (self.approved(source) and valid_review(correction, expected)):
                    raise EvidenceUnavailable("Correction requires documented review.")
            fulltext = await self.client.get(self.config.provider_url + "/" + source.pmcid + "/fullTextXML")
            fulltext.raise_for_status()
            if len(fulltext.content) > 8_000_000:
                raise EvidenceUnavailable("Article exceeds parsing limit.")
            digest = hashlib.sha256(fulltext.content).hexdigest()
            if digest != source.document_hash:
                raise EvidenceUnavailable("Source version changed; corpus requires re-audit.")
            xml = ElementTree.fromstring(fulltext.content)
            licenses = [n for n in xml.iter() if n.tag.split("}")[-1] == "license"]
            license_material = " ".join(str(child.attrib) for n in licenses for child in n.iter())
            license_path = source.license_url.split("://", 1)[-1].rstrip("/")
            if license_path not in license_material:
                raise EvidenceUnavailable("Full-text license differs from corpus rights.")
            for passage in source.passages:
                node = xml.find(passage.locator)
                if node is None or normalize(passage.text) not in node_text(node):
                    raise EvidenceUnavailable("Passage is absent from its original locator.")
        except (httpx.HTTPError, ValueError, TypeError, KeyError, AttributeError, ElementTree.ParseError, DefusedXmlException) as exc:
            if isinstance(exc, EvidenceUnavailable):
                raise
            raise EvidenceUnavailable("Literature verification is unavailable.") from exc
        return SourceCheck(datetime.now(timezone.utc).isoformat(), digest)
