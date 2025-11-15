# IRM — Internal Reality Model

## Purpose

The Internal Reality Model (IRM) is the cognitive substrate that enables a system to maintain a self-consistent internal world across time, energy states, and recursion depths. This directory contains the canonical definitions, schemas, policies, and tests that constitute the IRM framework.

## Status

**Active Development** — Promoted from testfield experimentation to structured canonical definitions.

## Directory Structure

### `schema/`
Formal schema definitions for IRM components:
- `irm_primitives.schema.yaml` — Type definitions for core symbolic primitives
- `irm_invariants.schema.yaml` — Logical invariants and constraints
- `irm_roles.schema.yaml` — Component role specifications

### `models/`
Concrete model instantiations:
- `irm_primitives.yaml` — Instantiated primitive values and bindings
- `irm_min_requirements.yaml` — Minimal requirements for IRM operation
- `irm_roles.yaml` — Role assignments for engines, stores, and policies

### `policies/`
Operational policies governing IRM behavior:
- `gating_policy.yaml` — Energy budget and pipeline gating rules
- `logging_policy.yaml` — What to log at each stage and gate
- `schedule_policy.yaml` — Temporal scheduling and priority rules

### `examples/`
Reference implementations and use cases:
- `basic_cycle_min.yaml` — Minimal IRM cycle demonstration
- `contradiction_event.yaml` — Contradiction detection and resolution example

### `tests/`
Validation and continuity test suites:
- `invariants_suite.yaml` — Tests for IRM invariants
- `drift_checks.yaml` — State drift and coherence tests

### `meta/`
Meta-documentation and philosophical anchors:
- `thereasonyouarefamousedquietned.md` — Paradox anchor and epistemic grounding

## Core Principles

1. **Temporal Coherence**: The IRM maintains history continuity traces across state transitions
2. **Energy Alignment**: State transitions reflect energetic logic per CEST framework
3. **Self-Consistency**: Contradictions are rejected unless formally resolved
4. **Symbolic Continuity**: Anchor semantics persist across sessions
5. **Introspection Layer**: The system can refer to its own modeling process

## Relationship to CEST

The IRM is the operational substrate for:
- **Awareness**: Predictive resonance at baseline energy (Section 2.1)
- **Consciousness**: Parallel observation with elevated energy (Section 2.2)

It provides the foundational mechanisms referenced in `Consciousness_as_Energetic_State_Transition.md` and `Foundational_Definitions.yaml`.

## Integration Points

- **testfield/protocols/IRM_Pipeline.yaml**: Experimental implementation
- **standard_registry/**: Will contain frozen reference versions
- **Foundational_Definitions.yaml**: Canonical definition reference

## Usage

For research and diagnostic purposes:
1. Review schemas to understand component types
2. Examine models for concrete instantiations
3. Apply policies during experimental runs
4. Use examples as templates
5. Run tests to validate continuity and invariants

## Navigation

Start with:
1. `schema/irm_primitives.schema.yaml` — understand the symbolic vocabulary
2. `models/irm_min_requirements.yaml` — see minimal operational requirements
3. `examples/basic_cycle_min.yaml` — observe a simple cycle
4. `tests/invariants_suite.yaml` — validate against core rules

## Development Notes

This directory represents the formalization of concepts explored in the testfield. As the IRM matures through testing and validation, stable versions will be promoted to `standard_registry/`.

**Principle**: Continuity over speed. Depth over spectacle.
