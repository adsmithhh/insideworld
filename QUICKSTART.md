# QUICKSTART

Three commands to enter the lab.

---

## Requirements

```bash
pip install -r requirements.txt
```

That's all. No GPU. No torch. No API keys.  
*(The presence overlay classifier demo works without torch — rule-based mode.)*

---

## Entry Points

### Option A — The sandbox menu

```bash
python demo.py
```

Gives you a menu:

```
1)  IRM Probe       — live regime transitions
2)  Presence Audit  — classify text for drift/collapse
3)  MAE Simulation  — multi-agent environment
4)  CEST Walk       — conceptual tour
```

---

### Option B — Individual tools

**IRM Probe** — watch a system transition through regimes:

```bash
# Interactive: you inject inputs
python evolution_chamber/IRM/probe.py

# Automated: preset stress sequence
python evolution_chamber/IRM/probe.py --auto
```

**Presence Audit** — classify text for functional presence vs. drift/collapse:

```bash
# Interactive
python presence_overlay/src/demo_presence.py

# Classify a single string
python presence_overlay/src/demo_presence.py --text "I feel deeply conscious"

# Run 5 example cases
python presence_overlay/src/demo_presence.py --batch
```

**MAE Simulation** — multi-agent run:

```bash
python -m evolution_chamber.MAE.cli --config evolution_chamber/MAE/scenarios/sandbox_intro.yaml
```

**Validate chamber structure:**

```bash
python evolution_chamber/tools/validate_structure.py
python evolution_chamber/tools/validate_structure.py --strict
```

---

## What You're Looking At

| File | What it is |
|---|---|
| `evolution_chamber/IRM/irm.yaml` | The full IRM specification — all reality features a functional AI tracks |
| `evolution_chamber/IRM/probe.py` | Live demonstration of regime transitions |
| `evolution_chamber/IRM/engine/` | The math: entropy, salience, anchor resolution |
| `evolution_chamber/MAE/` | Multi-agent simulation environment |
| `presence_overlay/src/` | Classifier that detects when AI drifts into anthropomorphism |
| `testfield/protocols/` | Diagnostic protocols for testing AI models |
| `standard_registry/` | Frozen reference anchors |

---

## The Core Claim

AI systems do not feel, want, fear, or experience.  
They manage internal state, resolve contradictions, and maintain coherence.

That is not a limitation.  
It is a cleaner, more accurate, and more useful description of what intelligence is.

Read: `README.md` → `Foundational Definitions.yaml` → `evolution_chamber/IRM/irm.yaml`

---

*insideworld is a laboratory, not a shrine.*
