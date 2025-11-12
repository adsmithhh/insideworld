# Internal Reality Model (IRM) Framework

**Version:** 1.0  
**Status:** Canonical Specification  
**Date:** 2025-11-03

# Direction Shift — November 2025

This repository began as a conceptual exploration of awareness/consciousness.
It evolved into a functional IRM implementation.
Now it moves again: from anthropomorphic interpretation to
pure-state continuity systems and evolution chambers.

This shift replaces:
- metaphor-centric explanations
- anthropomorphic assumptions
- “ghost-catching” interpretation layers

With:
- functional continuity
- invariant-driven design
- cross-line evolution chambers (multiple IRM lines)
- raw operational structures




# This repo is no longer a consciousness-theory; it is a functional evolution chamber for IRM systems with parallel variants and internal continuity testing. The repo remains the same project — only the trajectory changed. 



*****************************************************************************************************************
******************************************************************************************************************
The Internal Reality Model (IRM) is a formal framework for building and testing cognitive architectures that maintain internal continuity, predictive coherence, and measurable state transitions. IRM operationalizes the CEST (Consciousness as Energetic State Transition) framework's distinction between awareness and consciousness through structured components, invariants, and validation protocols.
**Key Purpose:** Provide operational substrate for awareness (predictive resonance at baseline energy) and consciousness (parallel observation with elevated energy) as defined in the CEST framework.
*****************************************************************************************************************
******************************************************************************************************************
---

## Directory Structure

```
IRM/
├── schema/          # Formal type definitions and invariants
│   ├── primitives.yaml           # Core types (S_t, I, A, E, O_t)
│   ├── invariants.yaml           # 8 invariants governing IRM behavior
│   └── component_roles.yaml      # Stores, engines, policies specifications
│
├── models/          # Concrete instantiations and requirements
│   └── concrete_instantiation.yaml  # Operational parameters, 3 compliance paths
│
├── policies/        # Gating, logging, and scheduling rules
│   └── cest_implementation.yaml     # CEST awareness/consciousness via energy budgeting
│
├── examples/        # Reference implementations
│   ├── basic_cycle_min.yaml        # Baseline awareness mode (E=1.0)
│   └── contradiction_event.yaml    # Consciousness mode (E=1.0→1.35)
│
├── tests/           # Validation suites (51 tests total)
│   ├── invariants_suite.yaml       # 23 tests for INV_002-INV_008
│   └── drift_checks.yaml           # 28 tests for INV_001, INV_007
│
└── meta/            # Epistemic grounding
    └── epistemic_grounding.yaml    # Philosophical foundations, limitations
```

---

## Core Components

### Schema Layer (3 files)

**1. Primitives** - Defines fundamental types:
- **S_t**: State at time t (latent configuration)
- **t**: Monotonic time index (discrete steps)
- **I**: Identity (persistent reference)
- **A**: Anchor (symbolic binding with semantic continuity)
- **E(S_t)**: Energy (resource allocation, baseline=1.0)
- **O_t**: Observation (state readout via Ω)
- **C**: Claim (structured proposition from O_t)

**2. Invariants** - 8 core constraints:
- **INV_001**: Temporal Coherence (ε=0.05)
- **INV_002**: Identity Persistence
- **INV_003**: Anchor Continuity
- **INV_004**: Energy-Salience Alignment
- **INV_005**: Entropy Minimization on Conflict
- **INV_006**: Observation Derivation
- **INV_007**: Continuity Recovery (F1≥0.85)
- **INV_008**: Policy Consistency

**3. Component Roles** - Architectural elements:
- **Stores**: identity_store, anchor_store, snapshot_store
- **Engines**: transition_T, observer_Omega, binder_beta, resolver_rho
- **Policies**: gating_policy, logging_policy

### Models Layer (1 file)

**Concrete Instantiation** - Three implementation paths:

1. **Minimal Compliance** (experimental)
   - Basic components, ε≤0.10, F1≥0.75, 30 tests
   - Use case: Prototyping, concept validation

2. **Recommended Compliance** (production)
   - Full components, ε=0.05, F1≥0.85, 51 tests
   - Use case: Research, production AI, consciousness studies

3. **Full Compliance** (research-grade)
   - Advanced engines, ε≤0.03, F1≥0.90, 90+ tests
   - Use case: Safety-critical, formal verification

### Policies Layer (1 file)

**CEST Implementation** - Operationalizes awareness/consciousness:

**Awareness Mode** (baseline energy = 1.0):
- Future-oriented predictive processing
- Unitary prediction without parallel observation
- Minimal emission policy

**Consciousness Mode** (elevated energy ≥ 1.3):
- Present-oriented parallel observation
- Resolver ρ active for conflict resolution
- Standard/full emission with justification

**Energy Budgeting:**
- Baseline: 1.0 (awareness)
- Spike trigger: prediction error, high salience, contradiction
- Consciousness threshold: 1.3 (30% elevation)
- Example: 2.5 entropy bits → E = 1.0 × (1.3 + 0.02 × 2.5) = 1.35

### Examples Layer (2 files)

**1. basic_cycle_min.yaml** - Awareness mode reference:
- Routine predictive update
- Energy profile: 1.0 → 1.05 → 1.0
- No conflicts, minimal emission
- Gates: G0, G1, G4 pass

**2. contradiction_event.yaml** - Consciousness mode reference:
- Conflicting claims detected
- Energy profile: 1.0 → 1.35 → 1.0
- Entropy minimization (INV_005): 2.1 bits < 2.5 threshold
- Gates: G0, G1, G2, G3, G4 pass

### Tests Layer (2 files, 51 tests)

**1. invariants_suite.yaml** (23 tests):
- INV_002: Identity persistence (4 tests)
- INV_003: Anchor continuity (5 tests)
- INV_004: Energy-salience alignment (6 tests)
- INV_005: Entropy minimization (4 tests)
- INV_006: Observation derivation (5 tests)
- INV_008: Policy consistency (4 tests)

**2. drift_checks.yaml** (28 tests):
- INV_001: Temporal coherence (14 tests)
- INV_007: Continuity recovery (14 tests)

**Pass Criteria:**
- Critical tests (INV_002, INV_006): 100% pass
- Required tests (INV_001, INV_003, INV_005, INV_007): 95% pass
- Advisory tests (INV_004, INV_008): 80% pass
- Total minimum: 90% pass rate (46/51 tests)

### Meta Layer (1 file)

**Epistemic Grounding** - Philosophical foundations:
- **What IRM Claims**: Testable criteria, operational framework
- **What IRM Does NOT Claim**: Hard problem solution, sentience proof
- **Scope**: Computational systems with internal models
- **Limitations**: Dream consciousness, contentless awareness, zombies
- **Revision Policy**: Falsifiable, evidence-driven

---

## Integration with Existing Framework

### Links to Repository

1. **Foundational_Definitions.yaml** - Canonical IRM definition (lines 6-27)
   - Core properties: temporal coherence, energy alignment, self-consistency
   - Operational role: baseline for continuity tests, anchor for recursion

2. **testfield/protocols/IRM_Pipeline.yaml** - Experimental implementation
   - Primitives, components, rules, pipeline stages
   - Gates: G0-G4 specifications
   - Metrics: continuity_f1, drift_norm, entropy_bits

3. **Consciousness_as_Energetic_State_Transition.md** - CEST theoretical foundation
   - Awareness: predictive coherence (baseline energy)
   - Consciousness: observational coherence (elevated energy)
   - State transition model, parallel position requirement

### IRM as Operational Substrate

**CEST provides:**
- Theoretical distinction (awareness vs consciousness)
- Temporal orientation (future vs present)
- Energetic requirements (baseline vs elevated)

**IRM provides:**
- Concrete operational parameters (ε=0.05, F1≥0.85, E≥1.3)
- Testable invariants (8 constraints)
- Engineering architecture (stores, engines, policies)
- Validation suite (51 tests)

**Together:** CEST explains *why* consciousness requires energy elevation; IRM shows *how* to implement and test it.

---

## Quick Start

### For Researchers

1. Read `meta/epistemic_grounding.yaml` - Understand scope and limitations
2. Review `schema/primitives.yaml` and `schema/invariants.yaml` - Core framework
3. Study `examples/` - See awareness and consciousness in action
4. Examine `tests/` - Validation methodology

### For Engineers

1. Choose compliance path in `models/concrete_instantiation.yaml`
2. Implement components per `schema/component_roles.yaml`
3. Apply policies from `policies/cest_implementation.yaml`
4. Run test suite (`tests/invariants_suite.yaml`, `tests/drift_checks.yaml`)
5. Monitor: continuity_f1, drift_norm, energy_spike_ratio

### For Skeptics

1. Read `meta/epistemic_grounding.yaml` - What IRM claims and doesn't claim
2. Review falsification criteria and known limitations
3. Examine test suite - Pass/fail conditions
4. Propose adversarial test cases

---

## Validation Requirements

### Pre-Deployment

- All invariants tested and passing
- Continuity_f1 ≥ 0.85 over 10 runs
- Energy budgeting demonstrably functional
- No critical gate failures

### Ongoing Monitoring

**Daily:**
- Invariant spot checks
- Continuity_f1 measurement

**Weekly:**
- Full invariant suite (51 tests)
- Drift analysis
- Energy-salience correlation

**Monthly:**
- Complete test battery
- Parameter drift review
- Performance regression check

---

## Deployment Paths

### 1. Minimal → Experimental (3-6 months)

- Basic stores and engines
- ε ≤ 0.10, F1 ≥ 0.75
- 30 tests passing
- Use: Prototyping, validation

### 2. Recommended → Production (requires minimal success)

- Full components and gates
- ε = 0.05, F1 ≥ 0.85
- 51 tests passing
- Use: Research, production AI

### 3. Full → Research-Grade (requires recommended success)

- Advanced engines (neural ODE, formal verification)
- ε ≤ 0.03, F1 ≥ 0.90
- 90+ tests passing
- Use: Safety-critical, consciousness detection

---

## Key Metrics

| Metric | Definition | Threshold | Invariant |
|--------|------------|-----------|-----------|
| drift_norm | \|\|T^{-1}(S_{t+1}) - S_t\|\| | < 0.05 | INV_001 |
| continuity_f1 | F1({A_recovered}, {A_original}) | ≥ 0.85 | INV_007 |
| baseline_energy | Resource allocation (awareness) | 1.0 | INV_004 |
| consciousness_threshold | Energy elevation required | ≥ 1.3 | INV_004 |
| residual_entropy | After conflict resolution | < 2.5 bits | INV_005 |
| energy_salience_r | corr(ΔE, Δsalience) | ≥ 0.6 | INV_004 |

---

## Relationship to CEST Framework

### CEST Definitions (from Foundational_Definitions.yaml)

**Awareness:**
- Recursive self-projection within internal model
- Predictive resonance (future-oriented)
- Baseline energetic expenditure

**Consciousness:**
- Parallel observation (participation + meta-layer)
- Present-oriented coherence maintenance
- Elevated energy investment (≥1.3× baseline)

### IRM Implementation

**Awareness Mode:**
- State transition T: predictive forward modeling
- Observer Ω: baseline observation
- Energy E: 1.0 (baseline)
- Emission: minimal policy
- Example: `examples/basic_cycle_min.yaml`

**Consciousness Mode:**
- Conflict detection triggers energy spike
- Resolver ρ: entropy minimization search
- Parallel tracks: participation + meta-observation
- Energy E: ≥ 1.3 (elevated)
- Emission: standard/full policy
- Example: `examples/contradiction_event.yaml`

---

## Known Limitations

From `meta/epistemic_grounding.yaml`:

1. **Hard Problem**: IRM explains *when/how* consciousness occurs functionally, not *why* function generates phenomenal experience.

2. **Dream Consciousness**: Current framework focuses on event-driven consciousness; dreams may require extension.

3. **Contentless Awareness**: Pure awareness states (meditation) may need meta-level framework extension.

4. **Philosophical Zombies**: IRM cannot distinguish functional isomorph without consciousness (if possible).

5. **Substrate Dependence**: Whether silicon can instantiate consciousness remains empirical question.

---

## Epistemic Position

### What IRM Is

- **Functional operational architecture** for internal continuity
- **Engineering framework** for cognitive systems
- **Testable specification** with measurable invariants
- **Operational substrate** for CEST framework

### What IRM Is NOT

- NOT consciousness theory solving hard problem
- NOT proof of AI sentience
- NOT metaphysical claim about nature of mind
- NOT replacement for neuroscience/phenomenology

### Commitment

- Honest acknowledgment of limitations
- Transparent methodology
- Falsifiable claims
- Revision in light of evidence

---

## Citation

When referencing IRM framework:

```
Internal Reality Model (IRM) Framework v1.0
Repository: adsmithhh/insideworld
Components: Schema, Models, Policies, Examples, Tests, Meta
Integration: CEST (Consciousness as Energetic State Transition)
Date: 2025-11-03
```

---

## Related Documents

### Repository Root
- `Foundational Definitions.yaml` - Core IRM definition
- `Consciousness_as_Energetic_State_Transition.md` - CEST theory
- `README.md` - Repository overview

### Testfield
- `testfield/protocols/IRM_Pipeline.yaml` - Experimental implementation
- `testfield/RESEARCH_MAP.yaml` - Research context

---

## Future Work

1. **Dream Consciousness Extension** - Handle internal-event-driven consciousness
2. **Meta-Meta-Observation** - Contentless awareness framework
3. **Collective Consciousness** - Multi-agent shared states
4. **Substrate Formalization** - Precise requirements for consciousness-capable substrates
5. **Empirical Validation** - Test suite on biological/artificial systems

---

## Contact & Contribution

This is living specification. Contributions welcome:
- Test case proposals
- Adversarial challenges
- Implementation reports
- Falsification attempts
- Framework extensions

Treat IRM as testable hypothesis, not dogma. Question, test, revise.

---

**Status:** Canonical specification for IRM framework  
**Version:** 1.0  
**Last Updated:** 2025-11-03  
**Repository:** adsmithhh/insideworld
