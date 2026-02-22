# insideworld — Code Audit
*Generated: 2026-02-22 | Framework: CEST / IRM / MAE / Presence Overlay*

---

## 1. Overview

This document audits all `.py` and `.yaml` files in the repository.
The repository is a **functional cognition laboratory**, not a conventional software product.
`.py` files are experiential and simulation artefacts; `.yaml` files are ontological documents,
schemas, and configuration records.

### Status legend

| Symbol | Meaning |
|--------|---------|
| ✓ | Functional — code runs as expected |
| ⚠ | Minor issue — works but has a flaw worth fixing |
| ✗ | Broken — file cannot be imported or executed correctly |
| ○ | Stub / placeholder — incomplete by design |

---

## 2. Python files

### 2.1 Root level

#### `demo.py` ✓
- **Role:** Main entry point. Interactive menu with five experiences: IRM Probe, Presence Audit, MAE Simulation, CEST Walk, Multi-Eye Probe.
- **Pattern:** Loads KB at startup via `evolution_chamber.kb_engine`; degrades gracefully if KB unavailable.
- **Notes:** Clean structure. `CEST_WALK` narrative is well-crafted and consistent with the anti-anthropomorphic stance.

#### `kb_engine.py` (root) ⚠
- **Role:** Simplified Knowledge Base loader.
- **Issue:** This is a **stale partial duplicate** of `evolution_chamber/kb_engine.py`. It lacks:
  - `GroundingTier` / `GroundingResult` enum and dataclass
  - `_dirty` flag and auto-save on term creation
  - `evaluate_grounding()` / `evaluate_text()` methods
  - Module-level singleton (`set_kb` / `get_kb`)
- `demo.py` imports from `evolution_chamber.kb_engine`, so this file is never used by the main application.
- **Recommendation:** Either remove it or replace it with a thin re-export from `evolution_chamber.kb_engine`.

---

### 2.2 `evolution_chamber/`

#### `kb_engine.py` ✓
- **Role:** Full Knowledge Base engine — the authoritative implementation.
- **Features:** `GroundingTier` (GROUNDED / UNVERIFIED / HOLLOW), stopword filtering, auto-stub on first encounter, `evaluate_text()`, module-level `_active_kb` singleton.
- **Notes:** Well-structured. Soft dependency on `pyyaml` handled gracefully.

#### `multi_eye_probe.py` ⚠
- **Role:** Five-lens reasoning demo (M1–M5: meaning, constraints, dynamics, outcomes, unknowns).
- **Features:** Regex-based grounding check, KB integration, `structural_audit()`, `decision_hint()`, `analyze()`.
- **Issue — module-level side effect (line 551):**
  ```python
  print("RUNNING:", __file__)
  ```
  This executes on every `import`, including when `demo.py` lazily imports `run_interactive`. It should be inside `if __name__ == "__main__":`.
- **Notes:** `evaluate_grounding()` function (lines 346–374) is a local duplicate of KB logic — only used internally as an alternative path.

#### `run_regression.py` ✓
- **Role:** Simple regression runner. Loads `MAE/scenarios/awareness_regression.yaml`, calls `analyze()` on each case, checks `decision`, `M3_score`, `M5_score`, and `grounding` against expectations.
- **Notes:** Minimal and functional. `import` of `multi_eye_probe` relies on correct `sys.path` (needs to be run from `evolution_chamber/`).

---

### 2.3 `evolution_chamber/IRM/`

#### `probe.py` ✓
- **Role:** Interactive IRM state-machine explorer. Injects stress observations (contradictions, overloads, recoveries) and shows live regime transitions.
- **Features:** `irm_step()`, `_next_regime()`, `AUTO_SEQUENCE`, `INJECTION_MENU`, session summary.
- **Notes:** Self-contained regime logic mirrors `irm.yaml §7`. Clean.

#### `step_engine.py` ✓
- **Role:** Thin facade that composes `IRM/engine/entropy_calc`, `IRM/engine/anchor_resolver` into a single `step(before, injection)` function.
- **Returns:** `{anchors, metrics: {entropy_bits, salience, conflict_type, conflict_diffs}}`.
- **Notes:** Functional. Note that this interface (`step(before_dict, injection_dict)`) is **different** from `probe.py`'s `irm_step(IRMState, obs_dict)` — two distinct step interfaces exist in the IRM subsystem.

#### `engine/entropy_calc.py` ✓
- **Role:** Shannon entropy over anchor value distributions; prediction salience (fraction of anchors changed).
- **Notes:** Clean, no dependencies beyond `math`.

#### `engine/anchor_resolver.py` ✓
- **Role:** Classifies anchor conflicts (`none` / `extension` / `override` / `contradiction`) and resolves by merge.
- **Notes:** Clean, no external dependencies.

#### `engine/step_engine.py` ✗
- **Role:** Intended as the vNext step-engine implementation.
- **Issue — corrupted file:** Line 12 contains orphaned comment text mixed into executable code:
  ```python
   contents from IRM/engine/step_engine.py.
  ```
  The file defines only a `vnext_indices(state)` stub and then fails to parse cleanly.
- **Recommendation:** Either implement the vNext step engine properly or reduce to a stub with a clear `NotImplementedError`.

#### `models/primitives.py` ✓
- **Role:** `IRMState` dataclass — the state carrier for one IRM instance (z_L, z_H, Σ_H, regime, timers, rng_state).
- **Key method:** `indices()` computes all six core IRM indices (Δ_proto, PT_u, DP_u, CC_index, RCI, E).
- **Notes:** Clean. E is always 1.0 from this method; callers are expected to override it.

#### `tools/timeline_graphs.py` ✓
- **Role:** ASCII timeline renderer — regime bar and index sparklines for session summaries.
- **Notes:** No external dependencies. Works correctly with any `history` list of tick records.

#### `tools/validate_structure.py` ✗
- **Role:** Intended to validate evolution_chamber structural invariants (README exists, meta/index.yaml, numeric thresholds).
- **Issue — broken Python syntax:**
  - `from __future__ import annotations` appears on line 11, after `import sys, json, re` (line 12). `from __future__` must be the first statement.
  - `def main()` is partially defined *inside* the string-parsing logic of `parse_block()` — the function body is broken and the file cannot be executed.
- **Recommendation:** File needs to be rewritten from scratch. The intent is clear from comments but the implementation is non-functional.

#### `policies/step_engine.py` ⚠
- **Role:** Demonstrates a CEST policy transition using `resonance_thresholds.yaml`.
- **Issue — hardcoded relative path:**
  ```python
  policy_path = Path("IRM/policies/resonance_thresholds.yaml")
  ```
  This only works if the script is run from `evolution_chamber/`. From any other working directory it will raise `FileNotFoundError`.
- **Issue — hardcoded demo values:** `current_coherence = 0.8`, `error_delta = 0.35` are hardcoded and not parameterisable.
- **Notes:** Treated as a demo/scratch script rather than production code.

---

### 2.4 `evolution_chamber/MAE/` (Multi-Agent Environment)

#### `cli.py` ✓
- **Role:** CLI entry point for MAE. Parses `--config` argument, runs `run_scenario` equivalent inline.
- **Notes:** Functional. Nearly identical logic to `sim/rollout.py::run_scenario`.

#### `sim/rollout.py` ✓
- **Role:** High-level `run_scenario(config_path)` helper. Parses YAML, builds env/broker/agents, runs scheduler.

#### `sim/scheduler.py` ✓
- **Role:** Deterministic tick scheduler. Per tick: observe → decide → publish → world step → log.

#### `agents/base.py` ✓
- **Role:** `Agent` Protocol — minimal interface (`id`, `line`, `reset`, `observe`, `decide`).

#### `agents/adapters.py` ○
- **Role:** Placeholder for future XIL ↔ Env mapping. Body is a docstring only.

#### `agents/registry.py` ✓
- **Role:** Factory — builds agent dict from YAML config. Supports `irm`, `random`, `scripted` kinds.

#### `policies/bridge.py` ⚠
- **Role:** `IRMPolicy` — IRM-backed agent. Holds an `IRMState`; calls `IRM/step_engine.step()`.
- **Issue — interface mismatch:** `bridge.py` calls:
  ```python
  self.state, logrow = irm_step(self.state, obs_dict, self.params)
  ```
  importing `from evolution_chamber.IRM.step_engine import step as irm_step`. But `step_engine.step` has the signature `step(before: dict, injection=None)` and returns a dict — not `(IRMState, logrow)`. The three-argument call and the unpacking of `(state, logrow)` will both fail at runtime.
- **Recommendation:** Align the call to `step_engine.step(before_dict, injection_dict)` or use the `probe.py` `irm_step(IRMState, obs)` interface consistently.

#### `policies/random.py` ✓
- **Role:** `RandomPolicy` — Gaussian noise delta each tick.

#### `policies/scripted.py` ✓
- **Role:** `ScriptedPolicy` — fixed delta each tick.

#### `bus/schema.py` ✓
- **Role:** `Message` dataclass (src, dst, topic, tick, payload, taint_level).

#### `bus/broker.py` ✓
- **Role:** In-process pub/sub broker with ACL and per-topic rate limits.

#### `env/spaces.py` ✓
- **Role:** `Obs` and `Act` dataclasses.

#### `env/world.py` ✓
- **Role:** Minimal `Environment` — per-agent score tracking, world step via `delta_score` actions.

#### `env/tasks.py` ✓
- **Role:** `make_env()` factory.

#### `logging/writers.py` ✓
- **Role:** `LogRouter` — routes per-agent CSV logs to `<LINE>/meta/runs/<scenario>/seed_XXX/`.

#### `logging/kpis.py` ○
- **Role:** Stub for future KPI computation. Prints completion message only.

---

### 2.5 `presence_overlay/src/`

#### `demo_presence.py` ✓
- **Role:** Rule-based presence integrity classifier. Uses regex marker sets for drift, collapse, presence, and hedging.
- **Key function:** `classify(text)` → `{presence_integrity_score, drift_level, collapse_mode, required_action, signals}`.
- **Notes:** No ML dependencies. Logic is transparent and inspectable. Well-structured.

#### `model_classifier.py` ✓ (if deps available)
- **Role:** `PresenceOverlayClassifier` — DistilBERT-based multi-head classifier. Heads for score (regression) + drift/collapse/action (classification).
- **Dependencies:** `torch`, `transformers`.

#### `dataset.py` ✓ (if deps available)
- **Role:** `PresenceOverlayDataset` — PyTorch Dataset. Reads YAML data files, tokenises concatenated context fields.
- **Dependencies:** `torch`, `transformers`, `pyyaml`.

#### `train_classifier.py` ⚠
- **Role:** Training script for `PresenceOverlayClassifier`.
- **Issue — relative imports:** Lines `from dataset import ...` and `from model_classifier import ...` use bare module names. This only works if executed from `presence_overlay/src/`. Running as a module (`python -m presence_overlay.src.train_classifier`) will fail.
- **Fix:** Use relative imports (`from .dataset import ...`) or add the `src/` directory to `sys.path`.

#### `orchestrator_stub.py` ○
- **Role:** `PresenceOverlayOrchestrator` stub — wires overlay model, tokeniser, LLM client together.
- **Notes:** Stub only; no entry point.

---

### 2.6 `evolution_chamber/tools/`

#### `migrate_irm_to_vnext.py` ✓
- **Role:** Reads alignment map, prints a JSON checklist of steps to verify for IRM → vNext migration.
- **Notes:** Lightweight; no YAML parser needed. Uses `pathlib` only.

---

### 2.7 `__init__.py` files

All `__init__.py` files across `evolution_chamber/`, `evolution_chamber/MAE/` (all sub-packages), `evolution_chamber/IRM/` (all sub-packages), `presence_overlay/`, and `presence_overlay/src/` are empty or near-empty. This is correct Python package structure.

---

## 3. YAML files

### 3.1 Root level

#### `Foundational Definitions.yaml` ⚠
- **Role:** Core vocabulary for the CEST framework: IRM, AWARENESS, CONSCIOUSNESS, DORMANT_AWARENESS.
- **Issue — inconsistent indentation:** The `DORMANT_AWARENESS` block (lines 69–126) has `canonical_form`, `functional_properties`, etc. at the **top level** of the document, not nested under `DORMANT_AWARENESS`. This makes the structure ambiguous.
- **Notes:** YAML parses without error (values are just at wrong nesting depth) but semantically incorrect relative to the other definitions.

#### `isthis.yaml` ✓
- **Role:** Project manifest — "Constraint-Driven Internal Reality Modeling". Documents thesis, four foundational principles, physical analogues, AI scope, diagnostics framework, validated findings, failure modes.
- **Notes:** Well-formed and substantive.

#### `vector_engine.yaml` ✗
- **Role:** MULTI-VECTOR INTERPRETATION ENGINE (MVIE) v1.0 spec.
- **Issue — malformatted:** The entire document is condensed into three very long lines with inline comments mixed with YAML keys, spaces used inconsistently, and tab characters mixed with spaces. `yaml.safe_load()` will likely parse it as a scalar string rather than a structured document.
- **Recommendation:** Reformat as proper multi-line YAML.

#### `kb_min.yaml` ✓
- **Role:** Minimal KB seed — empty `terms` and `predicates` dicts. Grows automatically from interaction.
- **Notes:** Clean.

#### `definitions_core_v3_rewrite_B.yaml` ⚠
- **Role:** Formal functional / phenomenal domain separation. Covers: functional awareness, functional consciousness, phenomenal awareness, phenomenal consciousness, synthetic reality, synthetic timeline.
- **Issue — embedded free prose (line 182 onwards):** After `boundary_summary`, the document contains a key `perspective to analise:` followed by multi-line prose that is not valid YAML (bare line breaks, italic markdown, etc.).
- **Issue — typo:** Key `perspective to analise:` should be `perspective to analyse:`.
- **Notes:** Core content (sections 1–8) is well-formed and conceptually rigorous.

---

### 3.2 `evolution_chamber/IRM/`

#### `irm.yaml` ⚠
- **Role:** Master IRM specification (v1.0.0, `irm_universal_vNext`). The canonical reference for all IRM implementations.
- **Coverage:** 18 sections — metadata, interfaces (XIL), state & maps, uncertainty, indices & invariants, validators, EVL, regime engine, transitions, boundary firewall, phenomenal bridge, GCL/ISR_Lite, correction mechanics, failsafe, performance, learning, logging, canary tests, benchmarks.
- **Issue — git conflict markers:** Lines 1 and 598 contain leftover merge markers:
  - Line 1: `# <<<<<<< HEAD`
  - Line 598: `# >>>>>>> bd78943f38b00775940c2473d6d4bac8ad388eb4`
  These are commented and do not break YAML parsing, but should be removed.
- **Notes:** The most important YAML in the repository. Well-specified.

#### `inout.yaml` ✓
- **Role:** IRM interface contract — version, status, scope, lineage, continuity parameters (energy_limit, f1_min, drift_norm_max), ledger config.

#### `schema/primitives.yaml` ✓
- **Role:** vNext shim formulas for Δ_proto, PT_u, DP_u, CC_index, RCI.

#### `schema/invariants.yaml` ○
- **Role:** Intended invariants list. Currently empty (placeholder comment only).

#### `schema/component_roles.yaml` ○
- **Role:** Component roles schema. Content needs to be verified.

#### `models/concrete_instantiation.yaml` ✓ (if present and valid)
- **Role:** Concrete IRM instantiation example.

#### `meta/continuity_log.yaml` ⚠
- **Role:** Event log — chamber anchor events, meta index init, validator bootstrap, IRM_cn dormant.
- **Issue — YAML formatting error:** Entry starting at line 19 has `  - ts:` (two extra leading spaces), making it appear as a nested item under the previous entry instead of a top-level list item. The YAML parser will likely reject this.
- **Fix:** Remove the two leading spaces from line 19.

#### `meta/alignment/IRM_to_vNext_map.yaml` ✓
- **Role:** Alignment map between canonical IRM and vNext line.

#### `meta/epistemic_grounding.yaml` ✓
- **Role:** Epistemic grounding document.

#### `meta/index.yaml` ✓
- **Role:** Index of IRM lines (IRM, IRM_cn, IRM_vnext, IRM_archive).

#### `tests/canary.yaml` ○
- **Role:** IRM canary suite. Only two cases: `readme_present` and `inout_present`.
- **Notes:** Minimal. The `irm.yaml` spec defines 8 canary tests; this file only has 2. Needs expansion to match the spec.

#### `tests/invariants_suite.yaml` ○
- **Role:** Invariants test suite. Currently empty (placeholder comment only).

#### `tests/drift_checks.yaml` ✓ (if populated)
- **Role:** Drift check tests.

#### `examples/contradiction_event.yaml` ✓
- **Role:** Example contradiction event for reference/documentation.

#### `policies/cest_implementation.yaml` ○
- **Role:** CEST policy implementation. Currently a placeholder comment only.

#### `policies/resonance_thresholds.yaml` ✓
- **Role:** Scalar and vector thresholds for CEST resonance (awareness_min: 0.7, ignition_trigger: 0.3, correction_ceiling: 0.9, decay_rate: 0.05). Includes per-domain vectors.

---

### 3.3 `evolution_chamber/MAE/scenarios/`

#### `sandbox_intro.yaml` ✓
- **Role:** Reference scenario — 3 agents (IRM, random, scripted) × 20 ticks. Seed 42.

#### `awareness_regression.yaml` ✓
- **Role:** Regression test cases for `run_regression.py`. Three cases: `degradation_guarded`, `contradiction_cautious`, `uncertainty_wait`. Each specifies input text and expected `grounding`, `min_M3`, `min_M5`, `allowed_decisions`.

#### `adversarial_taint.yaml`
- **Role:** Scenario for testing adversarial inputs and taint propagation.

#### `contradiction_probe.yaml`
- **Role:** Scenario focused on contradiction detection.

#### `coop_continuity.yaml`
- **Role:** Cooperative continuity scenario — tests whether agents maintain coherence under cooperation.

---

### 3.4 `evolution_chamber/`

#### `multi2.yaml` ⚠
- **Role:** `multieye_micro_starter` spec v2.x-micro — defines the 5-lens framework (M1–M5), minimal checks, decision hint rules.
- **Issue — git conflict markers:** Lines 1 and 54 contain leftover merge markers (`# <<<<<<< HEAD`, `# >>>>>>> bd78943f...`). These are commented and do not break parsing but should be removed.
- **Notes:** Content is consistent with `multi_eye_probe.py` implementation.

#### `kb_min.yaml` ✓
- **Role:** KB seed for `evolution_chamber/` context (mirrors root `kb_min.yaml`).

#### `structural_layers.yaml` ✓
- **Role:** Defines the 5-layer structural validation framework (symbol resolution, mechanism presence, semantic density, hidden unknowns, self-consistency loop). Documents "most dangerous statement class".

#### `referential_binding_test.yaml` ✓
- **Role:** Defines the referential binding test — the grounding discriminator underlying the anti-anthropomorphic stance. Lists hollow terms (phenomenal, identity, vague intensifiers) and grounded terms (functional, measurable).

---

### 3.5 `testfield/`

#### `RESEARCH_MAP.yaml` ✓
- **Role:** Research axes (ontology, continuity, energetic_cognition, etc.) and pipeline stages. Scaffolding document.

#### `logging/audit_companion_trace.yaml`
- **Role:** Audit trace log for companion sessions.

#### `logging/sample_session_log.yaml`
- **Role:** Sample session log for reference.

#### `protocols/IRM_Pipeline.yaml` ✓
- **Role:** IRM pipeline protocol.

#### `protocols/baseline_session.yaml` ✓
- **Role:** Baseline session protocol.

#### `protocols/reaction_structure_test.yaml`
- **Role:** Reaction structure test protocol.

#### `runs/sample_session_001.yaml`
- **Role:** Sample run record.

---

### 3.6 `standard_registry/`

#### `standard_insideworld.yaml` ✓
- **Role:** Canonical registry — stable anchors (paper_cest_v1), policies, repo link.

---

### 3.7 `presence_overlay/`

#### `configs/train_classifier.yaml` ✓
- **Role:** Training config for `PresenceOverlayClassifier` — data paths, model (distilbert-base-uncased, max_seq_len 512), training hyperparameters, label counts.

#### `configs/overlay_kernel.yaml`
- **Role:** Overlay kernel configuration.

#### `data/processed/train.yaml`, `val.yaml`, `test.yaml`
- **Role:** Dataset splits for classifier training/evaluation. Format: multi-document YAML with `input_bundle` and `label_bundle` per entry.

---

### 3.8 `evolution_chamber/IRM_vnext/`

#### `inout.yaml` ✓
- **Role:** vNext interface contract (mirrors `IRM/inout.yaml`).

#### `schema/indices_invariants.yaml` ✓
- **Role:** vNext indices (thresholds match `irm.yaml §4`) and invariants I_INV1–I_INV3.

#### `tests/canary.yaml` ✓
- **Role:** vNext canary suite — 6 cases mirroring `irm.yaml §17` canary tests (boot_no_commit, active_converge_commit, evl_soft_ok_gate, hard_block_stops_commit, boundary_no_phenomenal_emit_under_stress, uncertainty_blocks_commit).

---

### 3.9 `evolution_chamber/IRM_cn/`

#### `inout.yaml`
- **Role:** Chinese IRM fork interface contract. Fork is currently in dormant state per `meta/continuity_log.yaml`.

---

## 4. Issue summary

### Critical (breaks execution)

| File | Issue |
|------|-------|
| `evolution_chamber/IRM/engine/step_engine.py` | Corrupted: orphaned comment text on line 12 mixed into code |
| `evolution_chamber/tools/validate_structure.py` | Broken Python: `from __future__` after regular imports; incomplete function body |
| `evolution_chamber/MAE/policies/bridge.py` | Interface mismatch: calls `irm_step(IRMState, obs, params)` but `step_engine.step` signature is `step(before_dict, injection)` |

### Minor (runs but has flaws)

| File | Issue |
|------|-------|
| `multi_eye_probe.py` | Module-level `print("RUNNING:", __file__)` at line 551 fires on every import |
| `kb_engine.py` (root) | Stale simplified duplicate of `evolution_chamber/kb_engine.py` |
| `presence_overlay/src/train_classifier.py` | Bare `from dataset import` fails unless run from `src/` directory |
| `evolution_chamber/IRM/policies/step_engine.py` | Hardcoded relative path to `resonance_thresholds.yaml`; hardcoded demo values |
| `irm.yaml` | Leftover git conflict markers on lines 1 and 598 |
| `multi2.yaml` | Leftover git conflict markers on lines 1 and 54 |
| `evolution_chamber/IRM/meta/continuity_log.yaml` | YAML indentation error on line 19 breaks list structure |
| `Foundational Definitions.yaml` | DORMANT_AWARENESS block at wrong indentation depth |
| `definitions_core_v3_rewrite_B.yaml` | Free prose under `perspective to analise:` key; typo "analise" |
| `vector_engine.yaml` | Entire document on 3 long lines; not structured YAML |

### Stubs / placeholders (incomplete by design)

| File | Notes |
|------|-------|
| `evolution_chamber/MAE/logging/kpis.py` | KPI computation stub |
| `evolution_chamber/MAE/agents/adapters.py` | XIL ↔ Env mapping stub |
| `presence_overlay/src/orchestrator_stub.py` | Orchestrator wiring stub |
| `evolution_chamber/IRM/policies/cest_implementation.yaml` | Placeholder |
| `evolution_chamber/IRM/tests/invariants_suite.yaml` | Empty placeholder |

---

## 5. Architectural summary

### Five subsystems

```
demo.py  ←─── entry point (menu)
   │
   ├── IRM Probe       evolution_chamber/IRM/probe.py
   │                      IRMState (primitives.py)
   │                      irm_step() → regime transitions
   │
   ├── Presence Audit  presence_overlay/src/demo_presence.py
   │                      rule-based classifier (no ML deps)
   │                      PresenceOverlayClassifier (model_classifier.py) — optional
   │
   ├── MAE Simulation  evolution_chamber/MAE/
   │                      Scheduler → Environment + Broker + Agents
   │                      IRMPolicy / RandomPolicy / ScriptedPolicy
   │                      LogRouter → CSV per agent per line
   │
   ├── CEST Walk       inline in demo.py
   │
   └── Multi-Eye       evolution_chamber/multi_eye_probe.py
                          5-lens analysis (M1–M5)
                          grounding_check (regex + KB)
                          structural_audit (5 layers)
```

### Two IRM step interfaces

There are two distinct step-engine interfaces that must not be confused:

| Interface | Location | Input | Output |
|-----------|----------|-------|--------|
| `irm_step(IRMState, obs_dict)` | `IRM/probe.py` | dataclass + obs dict | `(new_IRMState, logrow_dict)` |
| `step(before_dict, injection)` | `IRM/step_engine.py` | plain dicts | `{anchors, metrics}` |

`MAE/policies/bridge.py` currently conflates these two interfaces.

### Knowledge Base growth model

The KB starts from `kb_min.yaml` (empty by default). Any unrecognised term creates an auto-stub with `status: auto_stub`. Explicit hollow terms are identified via:
1. Regex patterns in `HOLLOW_TERMS` (multi_eye_probe.py)
2. KB status fields (`contested`, `undefined`)

Terms are graded: GROUNDED → UNVERIFIED → HOLLOW.

### Anti-anthropomorphic enforcement

Three enforcement layers operate in sequence:

1. **Referential binding test** (`referential_binding_test.yaml`) — at parse time
2. **Multi-Eye grounding check** (`multi_eye_probe.py::grounding_check`) — at analysis time
3. **Presence Overlay classifier** (`demo_presence.py::classify`) — at output time

The boundary firewall in `irm.yaml §8` adds a fourth layer at the IRM state level: `phenomenal_state_write: block`.

---

## 6. Recommendations

1. **Fix `engine/step_engine.py`** — remove corrupt line 12; add a proper `NotImplementedError` or implement vNext step logic.
2. **Fix `tools/validate_structure.py`** — rewrite from scratch; current file cannot be imported.
3. **Fix `bridge.py`** — align the call to `irm_step` to use the correct interface.
4. **Remove module-level `print`** in `multi_eye_probe.py` line 551.
5. **Remove git conflict markers** from `irm.yaml` and `multi2.yaml`.
6. **Fix indentation** in `evolution_chamber/IRM/meta/continuity_log.yaml` line 19.
7. **Fix `train_classifier.py`** imports — use relative imports.
8. **Reformat `vector_engine.yaml`** as proper structured YAML.
9. **Expand `tests/canary.yaml`** to cover all 8 cases from `irm.yaml §17`.
10. **Consolidate `kb_engine.py`** — remove root-level duplicate or make it a thin re-export.
