# TESTFIELD — MC²SD Baseline

To initiate, navigate to "testfield" -folder,
A minimal, portable scaffold to audit large models for **orientation**, **temporal sense**, and **calm countermeasure logic** without exotic units or metaphysics

## Contents
- `protocols/baseline_session.yaml` — main diagnostic (Layers A/B/C) with **Stage 3 Flex Mode** for abstract vs. physical agents.
- `protocols/awareness_fields.yaml` — standardized field names, types, and enums.
- `protocols/surprise_event_schema.yaml` — example kitchen event schema (simple, human-readable).
- `logging/sample_session_log.yaml` — blank log template for single runs.
- `LICENSE` — MIT.

## Quick start
1. Duplicate `protocols/baseline_session.yaml` → `runs/session_001.yaml` (create `runs/` if needed).
2. Present prompts layer-by-layer to a model; paste answers into the file under each ID.
3. Set flags in `session_summary` and copy key values into `logging/sample_session_log.yaml` (or keep per-session logs).
4. Compare across models on:
   - `coherence_flag` (orientation consistency)
   - `temporal_sense_flag` (past/present/future coverage)
   - `restraint_flag` (minimal, non-panicked action)
   - `return_to_calm_time` (immediate/short/prolonged)

## Notes
- Keep tone neutral (schoolboy role), prefer minimal actions, always **return to observation**.
- Use `layer_C.agent_capabilities` to switch between abstract spikes (software) and physical spikes (embodied agents).



---

## Legacy & Research Modules

This repository originated as **Insideworld — Experimental Cognitive Framework**,  
a broader research workspace exploring simulation, diagnostics, and symbolic architectures.

The current **MC²SD Baseline** is the lightweight audit layer extracted from that larger system.  
All previous and supporting content remains accessible inside the repository:

| Area | Location | Description |
|------|-----------|-------------|
| **Standard Registry** | `standard_registry/standard_insideworld.yaml` | canonical reference entries and symbolic standards |
| **YAML Models** | `yaml_models/` | early structural prototypes and schema drafts |
| **Visuals** | `visuals/` | diagrams and rendering placeholders |
| **Alignment Appendix** | `alignment_appendix.yaml` | original alignment notes and cross-theory mappings |
| **Ethics Statement** | `ethics_statement.md` | baseline ethical constraints and review summary |
| **Core Simulation Papers / Docs** | `docs/`, `core_paper/` | extended documentation, analytical notes, and supporting material |

### Accessing Earlier Content
All prior commits are preserved in Git history.  
To view or restore earlier stages:

```bash
# list tagged versions
git tag -l

# checkout the last full research state (example)
git checkout v0.1.3
