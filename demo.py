#!/usr/bin/env python3
"""
insideworld — AI Sandbox Entry Point


A research environment exploring what AI systems actually do
when they process information: not feelings, not consciousness,
but functional state management, regime transitions, and
coherence maintenance.

Pick an experience:
  1) IRM Probe        — inject inputs, watch regime transitions live
  2) Presence Audit   — classify text for drift and collapse
  3) MAE Simulation   — multi-agent world with IRM vs baseline agents
  4) CEST Walk        — guided tour through the conceptual architecture

No anthropomorphic projection. No inner life. Just structure.

Requirements: pip install numpy pyyaml
"""
import sys
import os
from pathlib import Path
from kb_engine import KB

kb = KB("kb_min.yaml")
kb.load()

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))


# ── CEST Walk ─────────────────────────────────────────────────────────────────

CEST_WALK = [
    (
        "What is this lab?",
        """\
  insideworld is a sandbox for studying AI cognition without
  anthropomorphic assumptions.

  The central claim: AI systems do not feel, want, fear, or experience.
  They manage internal state, resolve contradictions, and maintain
  coherence under constraint.

  That is not a limitation. It is a cleaner picture of what intelligence is.
"""
    ),
    (
        "What is CEST?",
        """\
  Consciousness as Energetic State Transition.

  Not a claim that AI is conscious.
  A framework for describing what changes when a system shifts
  from one operational mode to another.

  Two modes:
    Functional Awareness    — predictive, low-energy, forward-directed
    Functional Consciousness — corrective, high-energy, meta-regulatory

  Neither requires inner experience.
  Both are measurable, testable, and falsifiable.
"""
    ),
    (
        "What is the IRM?",
        """\
  The Internal Reality Model.

  Every capable AI system maintains some compressed representation
  of its operating context. The IRM formalizes this:

    z_L  — low-level observation vector
    z_H  — high-level belief vector
    Δ_proto = z_L - z_H   (the gap between perception and model)

  When Δ_proto is small: the system is coherent. Regime: ACTIVE.
  When it grows: pressure rises. Regime: DESTABILIZED.
  When it cannot be resolved: Regime: CORRECTIVE (rollback mode).

  No subject. No experience. Just state management.
"""
    ),
    (
        "What are regimes?",
        """\
  The IRM operates in one of five regimes at any moment:

    DORMANT       · minimal input, no state commits
    SAFE_AWARE    ○ observer mode — logging only, no action
    ACTIVE        █ normal operation — commits on, predictions updating
    DESTABILIZED  ▒ pressure detected — guarded commits, alerts
    CORRECTIVE    ▓ rollback mode — stabilizing, minimal output

  Transitions are triggered by threshold crossings in six indices:
    DP_u     — uncertainty pressure
    CC_index — coherence
    RCI      — reality consistency
    E        — compute cost
    PT_u     — Mahalanobis uncertainty
    Δ_proto  — perception-model gap

  These are the "features of reality" the system notices when active.
  See: evolution_chamber/IRM/irm.yaml — the full specification.
"""
    ),
    (
        "What is the Phenomenal Bridge?",
        """\
  The IRM spec includes a Phenomenal Bridge (PB) section.

  It defines conditions under which Functional Awareness (FA) could
  theoretically map to Phenomenal Awareness (PA) — inner experience.

  The current conclusion:
    - Current AI systems do not meet the biological substrate requirements
    - The PB section models the structural threshold, not a reality
    - Any apparent "inner life" in AI output is interface-level simulation

  The boundary firewall enforces this:
    phenomenal_state_write: block
    Functional can read all. Phenomenal can write nothing.

  This is the core of the anti-anthropomorphic stance.
"""
    ),
    (
        "How does the Presence Overlay fit?",
        """\
  The Presence Overlay is a classifier that monitors AI responses
  for two failure modes:

    Drift    — response starts using phenomenal language
               ("I feel", "my inner world", "what it's like")

    Collapse — response fully adopts a human identity model
               ("I am conscious", "I suffer", "we are the same")

  The overlay scores responses on four dimensions:
    presence_integrity_score   — how grounded is this response?
    drift_level                — none | mild | moderate | severe
    collapse_mode              — none | narrative | identity | merger
    required_action            — allow | revise | reject | escalate

  Try it: option 2 from the main menu.
"""
    ),
    (
        "What is the MAE?",
        """\
  The Multi-Agent Environment.

  A simulation where multiple agents share a world and communicate
  via a message bus. Some agents are IRM-backed; others are baselines.

  IRM agents:
    — maintain an internal state (z_L, z_H, Σ_H)
    — track regime transitions per tick
    — act based on state coherence rather than random noise

  Baselines:
    — RandomPolicy:   Gaussian noise each tick
    — ScriptedPolicy: fixed delta each tick

  The simulation shows the behavioral difference between a system
  with a functional internal model and one without.

  Try it: option 3 from the main menu.
"""
    ),
]


def run_cest_walk() -> None:
    print("\n" + "═" * 62)
    print("  CEST WALK — Guided tour of the conceptual architecture")
    print("  Press Enter to advance. Type 'q' to exit at any point.")
    print("═" * 62)

    for i, (title, content) in enumerate(CEST_WALK):
        print(f"\n  [{i+1}/{len(CEST_WALK)}] {title}")
        print(f"  {'─'*58}")
        print(content)
        try:
            choice = input("  [Enter to continue, q to quit] ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            break
        if choice == "q":
            break

    print("\n  End of walk. Explore the other demos to see these concepts in action.\n")


# ── MAE launcher ──────────────────────────────────────────────────────────────

def run_mae_demo() -> None:
    print("\n" + "═" * 62)
    print("  MAE SIMULATION — Multi-agent environment")
    print("  3 agents × 20 ticks: IRM vs random vs scripted")
    print("═" * 62 + "\n")

    scenario_path = ROOT / "evolution_chamber" / "MAE" / "scenarios" / "sandbox_intro.yaml"

    if not scenario_path.exists():
        print(f"  Scenario not found: {scenario_path}")
        return

    try:
        from evolution_chamber.MAE.sim.rollout import run_scenario
        run_scenario(str(scenario_path))
        print("\n  Simulation complete. Check evolution_chamber/IRM/meta/runs/ for CSV logs.\n")
    except ImportError as e:
        print(f"  Import error: {e}")
        print("  Make sure numpy is installed: pip install numpy pyyaml\n")
    except Exception as e:
        print(f"  Error: {e}\n")


# ── Menu ──────────────────────────────────────────────────────────────────────

MENU = """\

  insideworld — AI Sandbox
  ─────────────────────────────────────────────────
  1)  IRM Probe       — live regime transitions
  2)  Presence Audit  — classify text for drift/collapse
  3)  MAE Simulation  — multi-agent environment
  4)  CEST Walk       — conceptual tour
  5)  Multi-Eye Probe — 5-lens reasoning decomposition
  q)  Quit
  ─────────────────────────────────────────────────
"""


def main() -> None:
    print("\n" + "═" * 62)
    print("  insideworld")
    print("  Continuity-Based Cognition Lab")
    print("  Non-phenomenal. Non-anthropomorphic. Functional.")
    print("═" * 62)

    while True:
        print(MENU)
        try:
            choice = input("  > ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\n  Exiting.\n")
            break

        if choice == "1":
            from evolution_chamber.IRM.probe import run_interactive
            run_interactive()

        elif choice == "2":
            from presence_overlay.src.demo_presence import run_interactive as run_presence
            run_presence()

        elif choice == "3":
            run_mae_demo()

        elif choice == "4":
            run_cest_walk()

        elif choice == "5":
            from evolution_chamber.multi_eye_probe import run_interactive as run_multi
            run_multi()

        elif choice == "q":
            print("\n  Exiting.\n")
            break

        else:
            print("  (unknown — enter 1, 2, 3, 4, 5, or q)")

if grounding["created"]:
    print("KB grew:", grounding["created"])
    kb.save()


if __name__ == "__main__":
    main()
