import yaml
from pathlib import Path

# Load the policy
policy_path = Path("IRM/policies/resonance_thresholds.yaml")
with open(policy_path, 'r') as f:
    thresholds = yaml.safe_load(f)

# Mock evolution step: Simulate error accumulation
current_coherence = 0.8  # Start aware
error_delta = 0.35  # Perturbation hit

if error_delta > thresholds['thresholds']['ignition_trigger']:
    new_state = "ignited"  # Meta-correction fires
    print(f"Transition: {current_coherence} -> {new_state} (CEST spark at {error_delta})")
else:
    new_state = "sustained"
    print(f"Holding: {current_coherence} -> {new_state}")

# Output: Holding: 0.8 -> sustained (or ignite if delta tuned higher)