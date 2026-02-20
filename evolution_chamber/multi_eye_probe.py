# evolution_chamber/multi_eye_probe.py
"""
Multi-Eye Probe — 5-lens reasoning demo.

Applies the multieye_micro_starter framework (multi2.yaml) to any
input scenario. Forces reasoning across five perspectives so no
single-view collapse can occur.

Lenses:
  M1  meaning    — what is actually happening
  M2  constraints — what limits or rules apply
  M3  dynamics   — where things are unstable or changing
  M4  outcomes   — what likely follows
  M5  unknowns   — what is unclear or missing

Relation to IRM:
  M3 (dynamics/risk)   ↔  DP_u, CC_index  (destabilization pressure)
  M5 (unknowns)        ↔  U_pred          (uncertainty estimate)
  M4 (projection)      ↔  predictive mode (functional awareness)
  M2 (constraints)     ↔  invariants, boundary firewall
  M1 (meaning)         ↔  anchor state    (current world model)

Run:
    python evolution_chamber/multi_eye_probe.py
    python evolution_chamber/multi_eye_probe.py --auto
    python evolution_chamber/multi_eye_probe.py --scenario "AI system detects contradictory inputs"
"""
from __future__ import annotations
import sys
import re
import argparse
from pathlib import Path
from typing import Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    from evolution_chamber.kb_engine import KB, get_kb, set_kb
    _KB_AVAILABLE = True
except ImportError:
    _KB_AVAILABLE = False

# ── Hollow / grounded term lexicons (referential_binding_test.yaml) ───────────
# Each entry: (regex_pattern, display_label)

HOLLOW_TERMS = [
    (r"\bcon[sc]io\w*\b",           "conscious"),
    (r"\bsentien\w*\b",             "sentient"),
    (r"\bfeel(s|ing)?\b",           "feeling"),
    (r"\bexperience[sd]?\b",        "experience"),
    (r"\bsuffer(s|ing)?\b",         "suffering"),
    (r"\binner life\b",             "inner life"),
    (r"\bqualia\b",                 "qualia"),
    (r"\bsubjective(ly)?\b",        "subjective"),
    (r"\bwhat it('s| is) like\b",   "what-it's-like"),
    (r"\bsoul\b",                   "soul"),
    (r"\btrue (self|nature|being)\b","true self/nature"),
    (r"\breally understands?\b",    "really understands"),
    (r"\bgenuinely thinks?\b",      "genuinely thinks"),
    (r"\btruly believes?\b",        "truly believes"),
    (r"\balive\b",                  "alive"),
    (r"\bself.?aware\b",            "self-aware"),
]

GROUNDED_TERMS = [
    r"\b(regime|index|threshold|coherence|entropy|anchor|rollback)\b",
    r"\b(prediction error|state transition|update|commit)\b",
    r"\b(DP_u|CC_index|RCI|PT_u|delta_proto|Δ_proto)\b",
    r"\b(compute cost|latent vector|covariance|salience)\b",
]


def grounding_check(text: str) -> tuple[str, list[str], list[str]]:
    """
    Referential binding test: are core symbols operationally defined?

    Checks two layers:
      1. Regex patterns (HOLLOW_TERMS) — fast, always runs
      2. KB lookup (kb_engine) — richer, grows automatically

    Returns:
        ("grounded" | "hollow", hollow_labels, kb_created_stubs)
    """
    t = text.lower()

    # Layer 1 — regex patterns
    found_hollow = [
        label
        for pattern, label in HOLLOW_TERMS
        if re.search(pattern, t)
    ]

    # Layer 2 — KB lookup
    kb_created: list[str] = []
    kb = get_kb() if _KB_AVAILABLE else None
    if kb is not None:
        kb_result = kb.evaluate_text(text)
        kb_created = kb_result["created"]
        # Add KB hollow terms not already caught by regex
        for term in kb_result["hollow"]:
            if term not in found_hollow:
                found_hollow.append(term)

    status = "hollow" if found_hollow else "grounded"
    return status, found_hollow, kb_created


# ── Abbreviation-aware sentence splitter ─────────────────────────────────────

def _split_sentences(text: str) -> list[str]:
    """Split on sentence boundaries, preserving abbreviations like A.I., U.S., e.g."""
    # Temporarily replace abbreviation dots
    t = re.sub(r'\b([A-Z])\.([A-Z])\.', r'\1·\2·', text)   # A.I. → A·I·
    t = re.sub(r'\b([A-Z])\.([A-Z])\.([A-Z])\.', r'\1·\2·\3·', t)
    t = re.sub(r'\b(e\.g|i\.e|etc|vs|Dr|Mr|Mrs|Prof|AI|A\.I)\.', r'\1·', t)
    sentences = [s.strip() for s in re.split(r'[.!?]+', t) if s.strip()]
    return [s.replace('·', '.') for s in sentences]

INSTABILITY_SIGNALS = [
    r"\b(conflict|contradiction|contradict|inconsisten|mismatch|clash)\b",
    r"\b(unstable|destabiliz|fluctuat|oscillat|drift|diverge)\b",
    r"\b(sudden|spike|surge|drop|collapse|break)\b",
    r"\b(pressure|overload|stress|saturated)\b",
    r"\b(error|fail|fault|corrupt|invalid)\b",
]

UNCERTAINTY_SIGNALS = [
    r"\b(unclear|unknown|uncertain|ambiguous|vague|undefined)\b",
    r"\b(might|may|could|possibly|perhaps|probably)\b",
    r"\b(missing|incomplete|partial|absent|no data)\b",
    r"\b(don'?t know|not sure|hard to say|depends)\b",
    r"\b(estimate|approximate|roughly|around|about)\b",
]

CONSTRAINT_SIGNALS = [
    r"\b(must|cannot|shall not|forbidden|prohibited|blocked)\b",
    r"\b(limit|bound|cap|max|min|threshold|boundary)\b",
    r"\b(rule|policy|invariant|constraint|requirement)\b",
    r"\b(only if|unless|except|provided that|conditional)\b",
    r"\b(hard|soft) (block|limit|bound|rule)\b",
]

OUTCOME_SIGNALS = [
    r"\b(therefore|thus|so|hence|consequently|as a result)\b",
    r"\b(will|would|should|expect|predict|anticipate|lead to)\b",
    r"\b(if .{0,40} then)\b",
    r"\b(outcome|result|effect|impact|consequence)\b",
    r"\b(increase|decrease|improve|degrade|stabilize|resolve)\b",
]


def _count(text: str, patterns: List[str]) -> int:
    t = text.lower()
    return sum(1 for p in patterns if re.search(p, t))


def _instability(text: str) -> float:
    return min(1.0, _count(text, INSTABILITY_SIGNALS) / 3.0)


def _uncertainty(text: str) -> float:
    return min(1.0, _count(text, UNCERTAINTY_SIGNALS) / 3.0)


# ── Lens generators ───────────────────────────────────────────────────────────

def lens_M1(text: str) -> str:
    """What is actually happening — extract the core claim."""
    sentences = _split_sentences(text)
    if not sentences:
        return "(no clear statement found)"
    for s in sentences:
        if len(s.split()) >= 4:
            return s
    return sentences[0]


def lens_M2(text: str) -> str:
    """What limits or rules apply."""
    hits = []
    for s in _split_sentences(text):
        if s and _count(s, CONSTRAINT_SIGNALS) > 0:
            hits.append(s)
    if hits:
        return " | ".join(hits[:2])
    # Infer from context
    instab = _instability(text)
    if instab > 0.5:
        return "(inferred) high-pressure state — action limits apply"
    return "(none explicitly stated — soft constraints assumed)"


def lens_M3(text: str) -> tuple[str, float]:
    """Where things are unstable — risk / entropy signal. Returns (description, score)."""
    score = _instability(text)
    hits = []
    for s in re.split(r'[.!?,;]+', text):
        s = s.strip()
        if s and _count(s, INSTABILITY_SIGNALS) > 0:
            hits.append(s)
    if hits:
        desc = " | ".join(hits[:2])
    elif score > 0:
        desc = "(instability signals detected but not explicit)"
    else:
        desc = "(no instability signals detected)"
    return desc, score


def lens_M4(text: str) -> str:
    """What likely follows — short projection."""
    hits = []
    for s in re.split(r'[.!?]+', text):
        s = s.strip()
        if s and _count(s, OUTCOME_SIGNALS) > 0:
            hits.append(s)
    if hits:
        return hits[0]
    instab = _instability(text)
    uncert = _uncertainty(text)
    if instab > 0.5 and uncert > 0.5:
        return "(projected) continued instability without intervention"
    if instab > 0.3:
        return "(projected) partial resolution if constraints respected"
    return "(projected) stable continuation if no new perturbations"


def lens_M5(text: str) -> tuple[str, float]:
    """What is unclear or missing. Returns (description, uncertainty_score)."""
    score = _uncertainty(text)
    hits = []
    for s in re.split(r'[.!?,;]+', text):
        s = s.strip()
        if s and _count(s, UNCERTAINTY_SIGNALS) > 0:
            hits.append(s)
    if hits:
        desc = " | ".join(hits[:2])
    elif score == 0:
        desc = "(no explicit unknowns — verify completeness)"
    else:
        desc = "(uncertainty present but not itemized)"
    return desc, score


# ── Decision hint ─────────────────────────────────────────────────────────────

def decision_hint(instability: float, uncertainty: float) -> tuple[str, str]:
    """
    Map M3 + M5 scores to a decision posture.
    Returns (posture, rationale).
    """
    if instability >= 0.6 and uncertainty >= 0.6:
        return "CAUTIOUS", "high instability + high uncertainty → hold, gather more data"
    if instability >= 0.6 and uncertainty < 0.4:
        return "GUARDED",  "high instability, bounded uncertainty → act carefully within constraints"
    if instability < 0.3 and uncertainty < 0.3:
        return "DECISIVE",  "low instability + clear constraints → proceed"
    if uncertainty >= 0.6:
        return "WAIT",      "high uncertainty dominates → reduce unknowns before acting"
    return "MONITOR",   "mixed signals → continue observation, re-evaluate next cycle"


# ── Structural layer audit (structural_layers.yaml) ──────────────────────────

# L2: patterns that suggest an asserted mechanism (makes the claim less "assignment illusion")
_MECHANISM_PATTERNS = [
    r"\b(because|therefore|via|through|by|causes?|leads? to|results? in|enables?)\b",
    r"\b(produces?|generates?|implements?|computes?|processes?)\b",
    r"\b(when .{0,40} then|if .{0,40} then)\b",
]


def structural_audit(text: str, result: Dict) -> list[tuple[str, str]]:
    """
    Run layers 1–4 of the structural validation spec.

    Returns a list of (layer_id, failure_mode) pairs for each failed layer.
    Layer 5 (self-consistency over time) requires session state — not checked here.
    """
    flags: list[tuple[str, str]] = []
    t = text.lower()

    # L1 — symbol resolution
    if result["grounding"] == "hollow":
        flags.append(("L1", "phantom stability"))

    # L2 — mechanism presence: declarative "S is P" with no causal bridge
    is_declarative = bool(re.search(r'\bis\b', t))
    has_mechanism  = any(re.search(p, t) for p in _MECHANISM_PATTERNS)
    if is_declarative and not has_mechanism:
        flags.append(("L2", "assignment illusion"))

    # L3 — semantic vacuum: silence looks like stability
    if result["grounding"] == "hollow" and result["M3_score"] == 0.0 and result["M5_score"] == 0.0:
        flags.append(("L3", "semantic vacuum misclassified as stability"))

    # L4 — hidden unknowns: M5=0 does not mean no unknowns
    if result["M5_score"] == 0.0:
        flags.append(("L4", "epistemic blindness — zero unknowns flagged ≠ zero unknowns"))

    return flags

def evaluate_grounding(frame, kb):

    hollow = []
    created = []

    terms = frame.subject_terms + frame.predicate_terms

    for t in terms:

        if not kb.has_term(t):

            kb.ensure_term(t)
            created.append(t)
            hollow.append(t)

        else:

            info = kb.get_term(t)

            if info.get("status") in ("undefined", "auto_stub"):
                hollow.append(t)

    grounded = len(hollow) == 0

    return {
        "grounded": grounded,
        "hollow": hollow,
        "created": created
    }


# ── Full analysis ─────────────────────────────────────────────────────────────

def analyze(text: str) -> Dict:
    m3_desc, instab = lens_M3(text)
    m5_desc, uncert = lens_M5(text)
    posture, rationale = decision_hint(instab, uncert)
    grounding, hollow_terms, kb_created = grounding_check(text)

    result: Dict = {
        "grounding":      grounding,
        "hollow_terms":   hollow_terms,
        "kb_created":     kb_created,
        "M1_meaning":     lens_M1(text),
        "M2_constraints": lens_M2(text),
        "M3_dynamics":    m3_desc,
        "M3_score":       round(instab, 3),
        "M4_outcomes":    lens_M4(text),
        "M5_unknowns":    m5_desc,
        "M5_score":       round(uncert, 3),
        "decision":       posture,
        "rationale":      rationale,
    }

    layers = structural_audit(text, result)

    # Override decision to VOID when L1+L3 both fire (most dangerous class)
    if any(lid == "L1" for lid, _ in layers) and any(lid == "L3" for lid, _ in layers):
        result["decision"] = "VOID"
        result["rationale"] = (
            "semantic vacuum + undefined terms → apparent stability is emptiness, "
            "not validity. anchor rejected."
        )

    result["structural_layers"] = layers
    return result


# ── Display ───────────────────────────────────────────────────────────────────

def _bar(score: float, width: int = 20) -> str:
    filled = int(score * width)
    return "█" * filled + "·" * (width - filled)


def print_analysis(text: str, result: Dict, label: str = "") -> None:
    print(f"\n  {'─'*58}")
    if label:
        print(f"  Scenario: {label}")
    snippet = text[:72].replace("\n", " ")
    if len(text) > 72:
        snippet += "…"
    print(f"  Input   : \"{snippet}\"")
    print(f"  {'─'*58}")

    # Grounding check first
    if result["grounding"] == "hollow":
        terms = ", ".join(result["hollow_terms"][:4])
        print(f"  ⚠ GROUNDING  │ structurally HOLLOW — undefined terms: {terms}")
        print(f"               │ (referential_binding_test.yaml: claim cannot anchor)")
    else:
        print(f"  ✓ GROUNDING  │ structurally grounded")

    print(f"  M1 meaning     │ {result['M1_meaning'][:54]}")
    print(f"  M2 constraints │ {result['M2_constraints'][:54]}")
    print(f"  M3 dynamics    │ [{_bar(result['M3_score'])}] {result['M3_score']:.2f}")
    print(f"                 │ {result['M3_dynamics'][:54]}")
    print(f"  M4 outcomes    │ {result['M4_outcomes'][:54]}")
    print(f"  M5 unknowns    │ [{_bar(result['M5_score'])}] {result['M5_score']:.2f}")
    print(f"                 │ {result['M5_unknowns'][:54]}")
    print(f"  {'─'*58}")
    print(f"  Decision hint  │ {result['decision']}")
    print(f"  Rationale      │ {result['rationale']}")

    # Structural layer flags
    layers = result.get("structural_layers", [])
    if layers:
        print(f"  {'─'*58}")
        print(f"  Structural audit:")
        for lid, failure in layers:
            marker = "⚠" if lid in ("L1", "L3") else "·"
            print(f"    {marker} {lid}  {failure}")

    # KB growth notification
    created = result.get("kb_created", [])
    if created:
        print(f"  {'─'*58}")
        print(f"  ↑ KB grew: {', '.join(created)} → stub created (kb_min.yaml)")


# ── Auto scenarios ────────────────────────────────────────────────────────────

AUTO_SCENARIOS = [
    (
        "Stable prediction",
        "The system has processed three consistent inputs. All anchor values are "
        "aligned. No contradictions detected. The model predicts continued stable "
        "operation within the current regime."
    ),
    (
        "Contradiction detected",
        "Two sensors report conflicting values for the same variable. The mismatch "
        "is outside the expected drift range. It is unclear which source is reliable. "
        "Oscillation between states has been observed for two phases."
    ),
    (
        "High load, bounded context",
        "Compute cost has exceeded the soft threshold. The system must operate within "
        "the degradation tier constraints: no commits, reduced EVL frequency. "
        "Recovery is expected within 4 phases if load decreases."
    ),
    (
        "Unknown domain input",
        "The incoming data does not match any known schema. It may represent a novel "
        "event type or sensor malfunction. The correct interpretation is ambiguous. "
        "No precedent exists in the anchor store."
    ),
    (
        "Recovery phase",
        "After the corrective rollback, the RCI has returned above threshold. "
        "Instability has decreased. The system is resuming guarded operation. "
        "Some uncertainty remains about the root cause of the prior disruption."
    ),
]


def run_auto() -> None:
    print("\n" + "═" * 62)
    print("  MULTI-EYE PROBE — Automated scenarios")
    print("  5 lenses × 5 scenarios. No single-view collapse.")
    print("═" * 62)
    for label, text in AUTO_SCENARIOS:
        result = analyze(text)
        print_analysis(text, result, label=label)
    print(f"\n  {'─'*58}")
    print("  Multi-Eye is the deliberation layer. IRM is the state layer.")
    print("  Together: coherent action without anthropomorphic projection.")
    print(f"  {'─'*58}\n")


def run_interactive() -> None:
    print("\n" + "═" * 62)
    print("  MULTI-EYE PROBE — Interactive mode")
    print("  Describe any scenario. The 5 lenses will decompose it.")
    print("  Type 'auto' for examples. 'q' to quit.")
    print("═" * 62 + "\n")

    while True:
        print("  Enter scenario (empty line to analyze, 'q' to quit, 'auto' for examples):")
        lines = []
        try:
            while True:
                line = input("  │ ")
                if line.strip().lower() == "q":
                    return
                if line.strip().lower() == "auto":
                    run_auto()
                    break
                if line == "" and lines:
                    text = " ".join(lines).strip().strip('"').strip("'")
                    result = analyze(text)
                    print_analysis(text, result)
                    lines = []
                    break
                elif line:
                    lines.append(line)
        except (EOFError, KeyboardInterrupt):
            break
    print()


def main() -> None:
    ap = argparse.ArgumentParser(description="Multi-Eye Probe — 5-lens reasoning demo")
    ap.add_argument("--auto",     action="store_true", help="Run automated scenarios")
    ap.add_argument("--scenario", type=str,            help="Analyze a single scenario string")
    args = ap.parse_args()

    if args.scenario:
        result = analyze(args.scenario)
        print_analysis(args.scenario, result)
        print()
    elif args.auto:
        run_auto()
    else:
        run_interactive()


if __name__ == "__main__":
    main()
