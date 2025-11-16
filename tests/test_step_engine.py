from evolution_chamber.IRM.policies.step_engine_refactor import evaluate_step
import pytest

def test_sustained():
    thresholds = {"thresholds": {"ignition_trigger": 0.5}}
    state, msg = evaluate_step(thresholds, current_coherence=0.8, error_delta=0.35)
    assert state == "sustained"
    assert "Holding" in msg

def test_ignited():
    thresholds = {"thresholds": {"ignition_trigger": 0.2}}
    state, msg = evaluate_step(thresholds, current_coherence=0.8, error_delta=0.35)
    assert state == "ignited"
    assert "Transition" in msg

def test_missing_trigger_key():
    thresholds = {"thresholds": {}}
    with pytest.raises(KeyError):
        evaluate_step(thresholds, current_coherence=0.8, error_delta=0.35)
