# Inside World

Welcome to the Inside World project...

# Evolution Chamber

This directory hosts all active IRM lines under experimental evaluation.

| Folder | Description |
|--------|--------------|
| **IRM/** | Canonical IRM implementation — baseline architecture and tests |
| **IRM_cn/** | Chinese IRM fork — safety-focused production variant |
| **IRM_vnext/** | Runtime-optimized experimental engine |
| **IRM_archive/** | Older IRM prototypes and retired components |

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
