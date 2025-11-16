from pathlib import Path
from typing import Tuple, Dict, Any
import yaml

def load_thresholds(path: Path | str = "IRM/policies/resonance_thresholds.yaml") -> Dict[str, Any]:
    path = Path(path)
    with path.open("r") as f:
        return yaml.safe_load(f)

def evaluate_step(thresholds: Dict[str, Any], current_coherence: float, error_delta: float) -> Tuple[str, str]:
    """Return (new_state, message).
    new_state is 'ignited' or 'sustained'.
    message is the same string that the original script printed.
    """
    trigger = thresholds.get("thresholds", {}).get("ignition_trigger")
    if trigger is None:
        raise KeyError("thresholds['thresholds']['ignition_trigger'] not found in thresholds")
    if error_delta > trigger:
        new_state = "ignited"
        msg = f"Transition: {current_coherence} -> {new_state} (CEST spark at {error_delta})"
    else:
        new_state = "sustained"
        msg = f"Holding: {current_coherence} -> {new_state}"
    return new_state, msg

def main(path: Path | str = "IRM/policies/resonance_thresholds.yaml"):
    thresholds = load_thresholds(path)
    # keep original defaults for current_coherence and error_delta
    current_coherence = 0.8
    error_delta = 0.35
    _, msg = evaluate_step(thresholds, current_coherence, error_delta)
    print(msg)

if __name__ == "__main__":
    main()
