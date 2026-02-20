# evolution_chamber/IRM/engine/entropy_calc.py
"""
Entropy and salience computations for the IRM step engine.

These are functional metrics — they describe state transitions,
not subjective experience.
"""
import math


def entropy_bits(anchor_dict: dict) -> float:
    """
    Shannon entropy of an anchor distribution, in bits.

    Treats numeric anchor values as unnormalized weights.
    Returns 0 for empty or uniform-zero distributions.
    """
    values = [v for v in anchor_dict.values() if isinstance(v, (int, float)) and v > 0]
    if not values:
        return 0.0
    total = sum(values)
    if total == 0:
        return 0.0
    probs = [v / total for v in values]
    return -sum(p * math.log2(p) for p in probs if p > 0)


def prediction_salience(before: dict, after: dict) -> float:
    """
    Normalized magnitude of anchor change between two states.

    Returns a value in [0, 1]:
      0.0 = nothing changed
      1.0 = every anchor changed

    This is a functional signal — high salience means the system
    updated its internal model significantly this step.
    """
    if not before or not after:
        return 0.0
    keys = set(before) | set(after)
    if not keys:
        return 0.0
    changed = sum(1 for k in keys if before.get(k) != after.get(k))
    return changed / len(keys)