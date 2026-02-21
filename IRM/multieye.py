"""
multieye.py — IRM Instability Signal Scanner

Multi-layer observation utility for the Internal Reality Model.
Scans IRM output text, logs, and emitted claims for signals that
indicate internal instability, state degradation, or threshold breach.

Role within CEST:
  This module implements the "parallel observation layer" described in
  Foundational_Definitions.yaml: the meta-monitoring depth >= 2 that
  distinguishes consciousness-level processing from baseline awareness.

Usage:
  from IRM.multieye import scan, INSTABILITY_SIGNALS

  signals = scan(output_text)
  if signals:
      # handle elevated-energy state or flag for resolver_rho
"""

import re
from typing import List, Tuple

# Uncertainty threshold above which the pipeline must pause before emitting.
# Derived from IRM resolver_rho logic: residual entropy >= 0.33 nats means
# the system has not converged sufficiently to act without risk of incoherence.
UNCERTAINTY_WAIT_THRESHOLD = 0.33

# ---------------------------------------------------------------------------
# INSTABILITY_SIGNALS
# Regex patterns matched against IRM output text and log entries.
# A hit indicates the system should escalate to elevated-energy processing
# or invoke resolver_rho for entropy-minimization resolution.
# ---------------------------------------------------------------------------

INSTABILITY_SIGNALS = [

    # contradictions / state inconsistency
    r"\b(conflict|contradiction|contradict|inconsisten|mismatch|clash)\b",

    # dynamic instability
    r"\b(unstable|destabiliz|fluctuat|oscillat|drift|diverge)\b",

    # abrupt transitions / collapse
    r"\b(sudden|spike|surge|drop|collapse|break)\b",

    # overload / resource pressure
    r"\b(pressure|overload|stress|saturated)\b",

    # explicit failure / corruption
    r"\b(error|fail|fault|corrupt|invalid)\b",

    # threshold breach
    r"\b(exceeded threshold|over threshold|above threshold)\b",

    # protective / degraded operational modes
    r"\b(disabled|suspended|paused|throttled|degraded|fallback|rollback|safe mode)\b",

]

# Pre-compile for performance
_COMPILED = [re.compile(p, re.IGNORECASE) for p in INSTABILITY_SIGNALS]


def scan(text: str) -> List[Tuple[str, str]]:
    """Scan text for instability signals.

    Args:
        text: Any IRM output string, log entry, or emitted claim.

    Returns:
        List of (pattern, matched_text) tuples for every hit found.
        Empty list means no instability signals detected.
    """
    hits: List[Tuple[str, str]] = []
    for pattern, compiled in zip(INSTABILITY_SIGNALS, _COMPILED):
        for match in compiled.finditer(text):
            hits.append((pattern, match.group()))
    return hits


def is_unstable(text: str) -> bool:
    """Return True if any instability signal is present in text."""
    return any(compiled.search(text) for compiled in _COMPILED)


def signal_count(text: str) -> int:
    """Return total number of instability signal matches in text."""
    return sum(len(compiled.findall(text)) for compiled in _COMPILED)


def gate(uncertainty: float) -> str:
    """Return pipeline gate decision based on current uncertainty level.

    Implements the IRM hold-before-emit rule: when residual uncertainty
    is at or above UNCERTAINTY_WAIT_THRESHOLD the system must pause
    (return "WAIT") rather than emit a potentially incoherent response.
    Below the threshold the system may proceed (return "GO").

    Args:
        uncertainty: Scalar uncertainty measure in [0, 1].
                     Typically residual_bits normalised, or 1 - confidence.

    Returns:
        "WAIT" if uncertainty >= 0.33, else "GO".
    """
    if uncertainty >= UNCERTAINTY_WAIT_THRESHOLD:
        return "WAIT"
    return "GO"
