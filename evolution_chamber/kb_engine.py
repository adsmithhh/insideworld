"""
kb_engine.py — Knowledge Base loader and auto-growth engine.

The KB starts from kb_min.yaml (hand-seeded terms).
Any term not found during grounding evaluation triggers an
auto-stub entry — the KB grows from interaction.

Usage:
    from evolution_chamber.kb_engine import KB, GroundingTier, GroundingResult
    kb = KB()
    kb.load()
    result = kb.evaluate_text("the rain is wet")
    # result.tier → GroundingTier.UNVERIFIED
"""
from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore


# ── Grounding tiers ───────────────────────────────────────────────────────────

class GroundingTier(str, Enum):
    GROUNDED   = "GROUNDED"    # ✓  known and operationally defined
    UNVERIFIED = "UNVERIFIED"  # ?  not in KB yet — epistemically open
    HOLLOW     = "HOLLOW"      # ⚠  known to be contested/undefined


@dataclass
class GroundingResult:
    tier: GroundingTier
    hollow_terms: List[str]     = field(default_factory=list)
    unverified_terms: List[str] = field(default_factory=list)
    created_terms: List[str]    = field(default_factory=list)
    notes: str                  = ""

_DEFAULT_PATH = Path(__file__).parent / "kb_min.yaml"

# Words too common to be worth tracking in the KB
_STOPWORDS = {
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
    "it", "its", "this", "that", "these", "those", "and", "or", "but",
    "in", "on", "at", "to", "for", "of", "with", "by", "from", "not",
    "no", "so", "as", "if", "do", "did", "has", "have", "had", "will",
    "would", "could", "should", "may", "might", "can", "all", "any",
    "some", "more", "than", "then", "when", "what", "which", "who",
    "how", "why", "just", "very", "also", "into", "over", "after",
}


def _extract_terms(text: str) -> List[str]:
    """
    Extract meaningful content words from free text.
    Returns lowercase tokens, stopwords removed, length > 2.
    """
    tokens = re.findall(r"\b[a-zA-Z][a-zA-Z'\-]*[a-zA-Z]\b", text.lower())
    return [t for t in tokens if t not in _STOPWORDS and len(t) > 2]


@dataclass
class KB:
    path: str = str(_DEFAULT_PATH)
    terms: Dict = field(default_factory=dict)
    predicates: Dict = field(default_factory=dict)
    _dirty: bool = field(default=False, repr=False)

    def load(self) -> None:
        if yaml is None:
            raise ImportError("pyyaml required: pip install pyyaml")
        if not os.path.exists(self.path):
            raise FileNotFoundError(self.path)
        with open(self.path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        self.terms = data.get("terms", {})
        self.predicates = data.get("predicates", {})
        self._dirty = False

    def save(self) -> None:
        if yaml is None:
            raise ImportError("pyyaml required: pip install pyyaml")
        data = {
            "version": 0.1,
            "terms": self.terms,
            "predicates": self.predicates,
            "meta": {"auto_generated": True},
        }
        with open(self.path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, sort_keys=False, allow_unicode=True)
        self._dirty = False

    # ── Term access ──────────────────────────────────────────────────────────

    def has_term(self, term: str) -> bool:
        return term.lower() in self.terms

    def get_term(self, term: str) -> Optional[dict]:
        return self.terms.get(term.lower())

    def ensure_term(self, term: str) -> bool:
        """
        If term is unknown, create an auto-stub.
        Returns True if a new stub was created.
        """
        term = term.lower()
        if term in self.terms:
            return False
        self.terms[term] = {
            "type": "unknown",
            "requires": ["definition", "measurement_protocol"],
            "status": "auto_stub",
            "confidence": 0.0,
        }
        self._dirty = True
        return True

    def term_status(self, term: str) -> str:
        """Return status string or 'missing' if not in KB."""
        info = self.get_term(term)
        if info is None:
            return "missing"
        return info.get("status", "unknown")

    # ── Grounding evaluation ─────────────────────────────────────────────────

    def evaluate_grounding(self, terms: List[str]) -> GroundingResult:
        """
        Evaluate a list of terms against the KB.

        Hollow policy (explicit, not assumed):
          - status in ("contested", "undefined")  — known problematic
          - type == "contested"                   — contested category
          - requires operational_definition AND none present

        Unknown terms → auto-stub + UNVERIFIED (not hollow).
        Known and not hollow → usable.
        """
        hollow: List[str] = []
        unverified: List[str] = []
        created: List[str] = []

        for term in terms:
            tl = term.lower()
            entry = self.get_term(tl)

            if entry is None:
                self.ensure_term(tl)
                created.append(tl)
                unverified.append(tl)
                continue

            status    = (entry.get("status") or "").lower()
            ttype     = (entry.get("type")   or "").lower()
            req       = entry.get("requires") or []
            requires_op = "operational_definition" in req
            has_op      = bool(entry.get("operational_definition"))

            is_hollow = (
                status in ("contested", "undefined")
                or ttype == "contested"
                or (requires_op and not has_op)
            )

            if is_hollow:
                hollow.append(tl)
            elif status == "auto_stub":
                unverified.append(tl)  # previously seen, still unresolved

        if created:
            self.save()

        if hollow:
            return GroundingResult(
                tier=GroundingTier.HOLLOW,
                hollow_terms=hollow,
                unverified_terms=unverified,
                created_terms=created,
                notes=f"structurally HOLLOW — contested/undefined: {', '.join(hollow)}",
            )
        if unverified:
            return GroundingResult(
                tier=GroundingTier.UNVERIFIED,
                unverified_terms=unverified,
                created_terms=created,
                notes=f"unverified grounding — not in KB yet: {', '.join(unverified)}",
            )
        return GroundingResult(
            tier=GroundingTier.GROUNDED,
            notes="structurally grounded",
        )

    def evaluate_text(self, text: str) -> GroundingResult:
        """Extract terms from free text and evaluate grounding."""
        terms = _extract_terms(text)
        return self.evaluate_grounding(terms)


# ── Module-level singleton ────────────────────────────────────────────────────
# multi_eye_probe.py calls set_kb() at startup; grounding_check uses _active_kb.

_active_kb: Optional[KB] = None


def set_kb(kb: KB) -> None:
    global _active_kb
    _active_kb = kb


def get_kb() -> Optional[KB]:
    return _active_kb
