# IRM Module (Sandbox)

Scope: internal reality model skeleton for continuity experiments.
Out of scope (for now): resolver, energy model, actuators, audits.

Files
- IRM_pipeline_init.yaml / IRM_pipeline_min_init.yaml — micro pipeline definitions
- schema_min.yaml — 6-field log schema
- sim_run_001.yaml — continuity dry run (with reset)
- sim_run_002.yaml — contradiction dry run (no resolver)
- runs/summary.yaml — run registry

Promotion hint: after 3 green simulate-runs (incl. one reset case) and a tiny resolver placeholder, tag `irm-v0.0.1-sandbox`.
