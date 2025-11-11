import math

def entropy_bits(distribution):
    """Compute entropy in bits for a dict {state:prob}"""
    total = sum(distribution.values())
    if total == 0:
        return 0.0
    H = 0.0
    for _,p in distribution.items():
        q = p / total
        if q > 0:
            H -= q * math.log2(q)
    return H

def prediction_salience(before, after):
    """
    Rough salience metric:
    how much anchors changed between steps.
    """
    b = set((before or {}).items())
    a = set((after  or {}).items())
    return len(b.symmetric_difference(a))
