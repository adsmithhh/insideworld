# Inside World

Welcome to the Inside World project...

# Evolution Chamber

This directory hosts all active IRM lines under experimental evaluation.

# Evolution Chamber — Entrance Read

This directory is the sealed environment for all Internal Reality Model (IRM) lines in active evolution.
Each sub-line operates autonomously under invariant control.  
No cross-line writes are permitted.

---

## Access Protocol

| Step  | Action  | Description |
|------ |---------|-------------|
| **1** | `enter SAFE_AWARE`    | Initialize observer access; no commits. |
| **2** | `select line`         | Choose one of: `IRM/`, `IRM_cn/`, `IRM_vnext/`, `IRM_archive/`. |
| **3** | `read manifesto`      | Open the line’s `README.md` (canonical orientation). |
| **4** | `validate invariants` | Run the line’s invariant suite before any modification. |
| **5** | `exit through meta/`  | Log continuity status in `meta/DIRECTION_SHIFT.md`. |

**Entrance Guards**
- Never modify multiple IRM lines in a single commit.
- All energy metrics must remain ≤ 1.30 × baseline during read-only sessions.
- Use `tools/ingest_external_logs.py` for third-party diagnostic imports.

---

## Line Overview

| Line | Focus      | Compliance Path |
|------|-------    -|-----------------|
| **IRM/**          | Canonical implementation           | Recommended (ε = 0.05 , F1 ≥ 0.85) |
| **IRM_cn/**       | Safety-constrained fork            | Recommended |
| **IRM_vnext/**    | Runtime-optimized evolution engine | Experimental / Full |
| **IRM_archive/**  | Retired prototypes                 | Historical reference only |

---

## Operational Philosophy
Each chamber maintains its own `inout.yaml` ledger.  
Synchronization between lines is *prohibited* except via formal migration YAMLs validated under `meta/migration_tests/`.  
The chamber represents *continuity space*, not discussion space.

---

## Visitor Orientation
1. Begin at `IRM/README.md` to understand canonical IRM.  
2. Move to `IRM_vnext/` for experimental evolution studies.  
3. Compare test outputs via `docs/showroom/`.  
4. For theoretical context, read `meta/DIRECTION_SHIFT.md`.

---

## Exit Condition
A visitor must leave the chamber in the same energetic and invariant state as entry:


## Purpose
The chamber isolates each IRM line so tests, timelines, and policies can evolve without cross-contamination.  
Every IRM instance maintains its own `inout.yaml` ledger, validators, and example cycles.  
External diagnostic logs (Claude, Grok, etc.) may be ingested through `tools/ingest_external_logs.py` for comparative analysis.

## Visitor orientation
- Start from `IRM/README.md` for canonical operation.
- Check `docs/showroom/` for summarized runs and energy budgeting examples.
- Use `meta/DIRECTION_SHIFT.md` to understand the structural change from single-IRM repo to multi-chamber system.

---

_This chamber forms the stable foundation for all future deployments. Each line is autonomous; commits here are gated by invariants, not discussion._

...
