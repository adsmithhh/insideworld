import yaml
from engine.entropy_calc import entropy_bits, prediction_salience
from engine.anchor_resolver import classify_conflict, resolve

def step(before, injection=None):
    """
    Compute next state:
      - compute salience
      - classify conflict
      - compute entropy
      - resolve anchors
    """
    inj = injection or {}

    # classify
    ctype, diffs = classify_conflict(before.get("anchors", {}), inj)

    if ctype == "none":
        after_anchors = dict(before["anchors"])
    else:
        after_anchors = resolve(before["anchors"], inj, diffs)

    # metrics
    H = entropy_bits({k:1 for k in after_anchors})
    sal = prediction_salience(before.get("anchors"), after_anchors)

    return {
        "anchors": after_anchors,
        "metrics": {
            "entropy_bits": float(H),
            "salience": sal,
            "conflict_type": ctype,
            "conflict_diffs": diffs
        }
    }
