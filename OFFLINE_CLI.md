# Offline CLI Agent — Setup Guide

How to run insideworld as a fully offline CLI agent from your local directory.

No internet. No API keys. No GPU required.

---

## Prerequisites

```powershell
pip install numpy pyyaml
```

That's all. The entire lab runs locally.

---

## Your Offline Directory

```
C:\.github\whereareyoudash\insideworld
```

*(Registered in `standard_registry/standard_insideworld.yaml` → `links.offline_dir`)*

---

## Entry Points

Navigate to your offline directory first:

```powershell
cd C:\.github\whereareyoudash\insideworld
```

### Main sandbox menu

```powershell
python demo.py
```

Presents a CLI menu:

```
1)  IRM Probe       — live regime transitions
2)  Presence Audit  — classify text for drift/collapse
3)  MAE Simulation  — multi-agent environment
4)  CEST Walk       — conceptual tour
5)  Multi-Eye Probe — 5-lens reasoning decomposition
```

---

### Individual CLI agents

**IRM Probe** — state machine explorer, inject stress inputs, watch regime transitions:

```powershell
# Interactive (you inject inputs)
python evolution_chamber/IRM/probe.py

# Automated stress sequence (no input needed)
python evolution_chamber/IRM/probe.py --auto
```

**Presence Audit** — classify text for functional presence vs. drift/collapse:

```powershell
# Interactive
python presence_overlay/src/demo_presence.py

# Single string
python presence_overlay/src/demo_presence.py --text "I manage internal state"

# Run 5 built-in examples
python presence_overlay/src/demo_presence.py --batch
```

**MAE Simulation** — multi-agent environment (IRM vs baselines):

```powershell
python -m evolution_chamber.MAE.cli --config evolution_chamber/MAE/scenarios/sandbox_intro.yaml
```

**Multi-Eye Probe** — 5-lens reasoning decomposition:

```powershell
python evolution_chamber/multi_eye_probe.py
```

**Structure validator** — verify chamber invariants:

```powershell
python evolution_chamber/tools/validate_structure.py
python evolution_chamber/tools/validate_structure.py --strict
```

---

## All commands work fully offline

| Tool | Needs internet? | Needs API key? | Needs GPU? |
|---|---|---|---|
| `demo.py` | No | No | No |
| `IRM/probe.py` | No | No | No |
| `demo_presence.py` | No | No | No |
| `MAE/cli.py` | No | No | No |
| `multi_eye_probe.py` | No | No | No |
| `validate_structure.py` | No | No | No |

---

*insideworld is a laboratory, not a shrine.*
