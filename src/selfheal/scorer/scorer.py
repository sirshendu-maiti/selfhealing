from __future__ import annotations
from difflib import SequenceMatcher
from typing import Any
from selfheal.models.contract import ElementFingerprint, ScoringWeights

WEIGHTS = ScoringWeights()

def _norm(v: Any) -> str:
    if v is None:
        return ""
    if isinstance(v, (list, tuple, set)):
        return " ".join(sorted(str(x).strip().lower() for x in v))
    return str(v).strip().lower()

def _sim(a: Any, b: Any) -> float:
    a, b = _norm(a), _norm(b)
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a, b).ratio()

def _attribute_similarity(a: dict[str, str], b: dict[str, str]) -> float:
    keys = set(a) | set(b)
    if not keys:
        return 1.0
    return sum(_sim(a.get(k, ""), b.get(k, "")) for k in keys) / len(keys)

def _position_similarity(a: ElementFingerprint, b: ElementFingerprint) -> float:
    vals = [(a.x, b.x), (a.y, b.y), (a.width, b.width), (a.height, b.height)]
    present = [(x, y) for x, y in vals if x is not None and y is not None]
    if not present:
        return 0.5  # unknown geometry is neutral, not a perfect match
    # Per dimension: 1 at identical, linearly decays to 0 over 300 CSS px.
    return sum(max(0.0, 1.0 - abs(x-y)/300.0) for x, y in present) / len(present)

def score_pair(original: ElementFingerprint | dict, candidate: ElementFingerprint | dict) -> dict:
    a = original if isinstance(original, ElementFingerprint) else ElementFingerprint.model_validate(original)
    b = candidate if isinstance(candidate, ElementFingerprint) else ElementFingerprint.model_validate(candidate)
    components = {
        "text": _sim(a.text, b.text),
        "class_name": _sim(a.classes, b.classes),
        "attribute": _attribute_similarity(a.attributes, b.attributes),
        "position": _position_similarity(a, b),
        "parent": _sim(f"{a.parent_tag or ''} {a.parent_text or ''}", f"{b.parent_tag or ''} {b.parent_text or ''}"),
        "aria_role": _sim(a.role, b.role),
    }
    weights = WEIGHTS.model_dump()
    total = sum(components[k] * weights[k] for k in components)
    return {"score": round(total, 4), "components": {k: round(v, 4) for k, v in components.items()}}
