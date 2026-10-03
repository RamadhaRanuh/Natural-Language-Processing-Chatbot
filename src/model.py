"""Optional selector receives public topic/IDs only and cannot write clinical prose."""
import json
import httpx
from .config import Config


class SelectionError(ValueError):
    pass


async def select_claims(topic: str, candidates: list[str], config: Config, client: httpx.AsyncClient) -> list[str]:
    if not config.model_url or not config.model_name or not config.model_key:
        raise SelectionError("Optional selector is not configured.")
    if not config.model_url.startswith("https://"):
        raise SelectionError("Selector transport requires HTTPS.")
    try:
        response = await client.post(
            config.model_url.rstrip("/") + "/chat/completions",
            headers={"Authorization": "Bearer " + config.model_key},
            json={"model": config.model_name, "temperature": 0, "messages": [
                {"role": "system", "content": 'Select only supplied public evidence claim IDs. Return JSON {"claim_ids": [IDs]}. Do not generate text, numbers or citations.'},
                {"role": "user", "content": json.dumps({"topic": topic, "candidate_ids": candidates})},
            ]},
        )
        response.raise_for_status()
        data = json.loads(response.json()["choices"][0]["message"]["content"])
        chosen = data.get("claim_ids")
        if set(data) != {"claim_ids"} or not isinstance(chosen, list) or not chosen or len(chosen) > 4:
            raise SelectionError("Invalid selector schema.")
        if any(not isinstance(item, str) or item not in candidates for item in chosen) or len(set(chosen)) != len(chosen):
            raise SelectionError("Unknown or duplicate evidence ID.")
        return chosen
    except (httpx.HTTPError, ValueError, KeyError, TypeError, IndexError) as exc:
        raise SelectionError("Selection failed; no medical output was published.") from exc
