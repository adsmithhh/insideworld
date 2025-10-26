# insideworld — MC²SD Baseline

A minimal, portable scaffold to audit large models for **orientation**, **temporal sense**, and **calm countermeasure logic** without exotic units or metaphysics.

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

