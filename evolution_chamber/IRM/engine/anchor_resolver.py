# evolution_chamber/IRM/engine/anchor_resolver.py
"""
Anchor conflict classification and resolution for the IRM step engine.

Anchors are symbolic constraints that keep the system's internal
reality model coherent. Conflicts arise when new information
contradicts or extends the current anchor set.
"""
from typing import Dict, Tuple, Any


def classify_conflict(anchors: dict, injection: dict) -> Tuple[str, Dict[str, Any]]:
    """
    Classify the conflict type between existing anchors and injected update.

    Returns:
        (conflict_type, diffs)

        conflict_type: one of
            "none"          — injection adds nothing new
            "extension"     — injection adds new anchors only
            "override"      — injection changes existing values
            "contradiction" — injection directly inverts a boolean anchor

        diffs: {key: {"before": old_val, "after": new_val}} for changed keys
    """
    if not injection:
        return "none", {}

    new_keys = set(injection) - set(anchors)
    changed_keys = {k for k in injection if k in anchors and anchors[k] != injection[k]}
    diffs = {
        k: {"before": anchors.get(k), "after": injection[k]}
        for k in (new_keys | changed_keys)
    }

    if not diffs:
        return "none", {}
    if not changed_keys:
        return "extension", diffs

    # Contradiction: a boolean anchor directly flipped
    contradictions = {
        k for k in changed_keys
        if isinstance(anchors[k], bool) and isinstance(injection[k], bool)
        and anchors[k] != injection[k]
    }
    if contradictions:
        return "contradiction", diffs

    return "override", diffs


def resolve(anchors: dict, injection: dict, diffs: dict) -> dict:
    """
    Merge injection into anchors. Injected values take precedence.

    This is the minimal resolution strategy: the new information wins.
    More complex resolution (rollback, shadow-accept) is handled by CM.
    """
    result = dict(anchors)
    result.update(injection)
    return result