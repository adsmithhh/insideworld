# evolution_chamber/IRM/probe.py
"""
IRM Probe — Interactive state machine explorer.

Feed stress inputs to an IRM instance and watch it transition
through regimes in real time. Each tick shows:
  - current regime
  - all six indices
  - why a transition fired (if any)

Run:
    python evolution_chamber/IRM/probe.py
    python evolution_chamber/IRM/probe.py --auto   # automated stress sequence
"""
from __future__ import annotations
import sys
import math
import argparse
from pathlib import Path

# Allow running from repo root
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import numpy as np
from evolution_chamber.IRM.models.primitives import IRMState
from evolution_chamber.IRM.tools.timeline_graphs import print_session_summary

# ── Thresholds (from irm.yaml section 4) ─────────────────────────────────────
T = {
    "DPu_low":  0.20,
    "DPu_high": 0.60,
    "CC_ok":    0.85,
    "CC_bad":   0.60,
    "RCI_ok":   0.80,
    "RCI_bad":  0.60,
    "E_soft":   1.30,
    "E_hard":   1.80,
}

# ── Regime transition logic ───────────────────────────────────────────────────

def _next_regime(regime: str, idx: dict, timers: dict) -> tuple[str, str | None]:
    """
    Evaluate transition rules from irm.yaml section 7.
    Returns (new_regime, reason_string | None).
    """
    dp  = idx["DP_u"]
    cc  = idx["CC_index"]
    rci = idx["RCI"]
    E   = idx["E"]

    # Hard safety always wins
    if E >= T["E_hard"]:
        if regime not in ("CORRECTIVE", "SAFE_AWARE"):
            return "CORRECTIVE", f"E={E:.2f} ≥ E_hard={T['E_hard']}"

    if regime == "DORMANT":
        if dp > T["DPu_low"]:
            return "ACTIVE", f"DP_u={dp:.2f} > DPu_low={T['DPu_low']}"

    elif regime == "ACTIVE":
        if dp >= T["DPu_high"] or rci < T["RCI_ok"] or E >= T["E_soft"]:
            return "DESTABILIZED", (
                f"DP_u={dp:.2f}" if dp >= T["DPu_high"] else
                f"RCI={rci:.2f} < {T['RCI_ok']}" if rci < T["RCI_ok"] else
                f"E={E:.2f} ≥ E_soft={T['E_soft']}"
            )

    elif regime == "DESTABILIZED":
        destab_phases = timers.get("DESTABILIZED", 0)
        if rci < T["RCI_bad"] and destab_phases >= 2:
            return "CORRECTIVE", f"RCI={rci:.2f} < {T['RCI_bad']} for {destab_phases} phases"
        # Recovery
        if dp < T["DPu_low"] and rci >= T["RCI_ok"] and E < T["E_soft"]:
            return "ACTIVE", "indices stabilized"

    elif regime == "CORRECTIVE":
        corr_phases = timers.get("CORRECTIVE", 0)
        if corr_phases >= 3:
            return "SAFE_AWARE", "corrective timeout → SAFE_AWARE"
        # Partial recovery
        if rci >= T["RCI_ok"] and dp < T["DPu_high"] and E < T["E_soft"]:
            return "ACTIVE", "recovery successful"

    elif regime == "SAFE_AWARE":
        if dp > T["DPu_low"]:
            return "ACTIVE", f"new input: DP_u={dp:.2f}"

    return regime, None


# ── IRM step ──────────────────────────────────────────────────────────────────

def irm_step(state: IRMState, obs: dict, E_override: float | None = None) -> tuple[IRMState, dict]:
    """
    One tick of the IRM.

    obs keys (all optional):
        contradiction  bool   — a boolean anchor was flipped
        overload       float  — extra energy cost [0..1]
        new_info       float  — new information magnitude [0..1]
        recovery       bool   — stabilizing input
    """
    rng = state.rng_state if state.rng_state is not None else np.random.default_rng()

    # Apply observation to z_L
    z_L = state.z_L.copy()
    z_H = state.z_H.copy()

    if obs.get("contradiction"):
        z_L += rng.normal(0, 0.4, size=z_L.shape)
    if obs.get("new_info", 0) > 0:
        z_L += rng.normal(0, obs["new_info"] * 0.3, size=z_L.shape)
    if obs.get("recovery"):
        z_L = z_L * 0.7 + z_H * 0.3  # pull toward H

    # Partial H update (simplified η_H commit)
    if state.regime == "ACTIVE":
        eta = 0.1
        z_H = z_H + eta * np.clip(z_L - z_H, -1.0, 1.0)
    elif state.regime == "DESTABILIZED":
        eta = 0.075
        z_H = z_H + eta * np.clip(z_L - z_H, -0.5, 0.5)

    # Build new state
    new_state = IRMState(
        z_L=z_L, z_H=z_H,
        Sigma_H=state.Sigma_H.copy(),
        regime=state.regime,
        timers=dict(state.timers),
        rng_state=rng,
    )

    idx = new_state.indices()

    # Apply overload
    E = (E_override if E_override is not None
         else 1.0 + obs.get("overload", 0) * 0.8)
    idx["E"] = E

    # Evaluate transitions
    new_regime, reason = _next_regime(new_state.regime, idx, new_state.timers)

    # Update timers
    if new_regime == new_state.regime:
        new_state.timers[new_regime] = new_state.timers.get(new_regime, 0) + 1
    else:
        new_state.timers[new_regime] = 1

    new_state.regime = new_regime

    logrow = {
        "regime":     new_regime,
        "transition": reason,
        "indices":    idx,
    }
    return new_state, logrow


# ── Display ───────────────────────────────────────────────────────────────────

def _print_tick(tick: int, logrow: dict) -> None:
    idx = logrow["indices"]
    regime = logrow["regime"]
    regime_labels = {
        "DORMANT":      "· DORMANT     ",
        "SAFE_AWARE":   "○ SAFE_AWARE  ",
        "ACTIVE":       "█ ACTIVE      ",
        "DESTABILIZED": "▒ DESTABILIZED",
        "CORRECTIVE":   "▓ CORRECTIVE  ",
    }
    label = regime_labels.get(regime, regime)

    bar_dp  = int(idx["DP_u"]    * 20)
    bar_cc  = int(idx["CC_index"]* 20)
    bar_rci = int(idx["RCI"]     * 20)
    bar_E   = int(min(idx["E"] / 2.0, 1.0) * 20)

    trans = f"  → {logrow['transition']}" if logrow.get("transition") else ""

    print(f"  tick {tick:>3}  {label}  "
          f"DP_u={idx['DP_u']:.2f}  CC={idx['CC_index']:.2f}  "
          f"RCI={idx['RCI']:.2f}  E={idx['E']:.2f}{trans}")


# ── Preset stress sequences ───────────────────────────────────────────────────

AUTO_SEQUENCE = [
    # (label, obs_dict)
    ("Quiet start",        {}),
    ("Quiet",              {}),
    ("Quiet",              {}),
    ("New information",    {"new_info": 0.6}),
    ("New information",    {"new_info": 0.7}),
    ("Contradiction hit",  {"contradiction": True}),
    ("Overload spike",     {"overload": 0.5}),
    ("Overload rising",    {"overload": 0.7}),
    ("Contradiction + load", {"contradiction": True, "overload": 0.6}),
    ("Heavy overload",     {"overload": 0.9}),
    ("Heavy overload",     {"overload": 0.9}),
    ("Recovery signal",    {"recovery": True}),
    ("Recovery",           {"recovery": True}),
    ("Recovery",           {"recovery": True}),
    ("Stabilizing",        {}),
    ("Stabilizing",        {}),
    ("Stabilizing",        {}),
    ("Quiet",              {}),
    ("Quiet",              {}),
    ("Quiet",              {}),
]

INJECTION_MENU = {
    "1": ("Quiet tick",        {}),
    "2": ("New information",   {"new_info": 0.6}),
    "3": ("Contradiction",     {"contradiction": True}),
    "4": ("Overload (mild)",   {"overload": 0.4}),
    "5": ("Overload (heavy)",  {"overload": 0.9}),
    "6": ("Recovery signal",   {"recovery": True}),
    "7": ("Contradiction + overload", {"contradiction": True, "overload": 0.6}),
}


def _init_state(seed: int = 42, dim: int = 8) -> IRMState:
    rng = np.random.default_rng(seed)
    return IRMState(
        z_L=np.zeros(dim),
        z_H=np.zeros(dim),
        Sigma_H=np.eye(dim),
        regime="DORMANT",
        timers={},
        rng_state=rng,
    )


# ── Main ──────────────────────────────────────────────────────────────────────

def run_auto(seed: int = 42) -> None:
    print("\n" + "═" * 62)
    print("  IRM PROBE — Automated stress sequence")
    print("  Watch regime transitions as the system processes inputs.")
    print("  No inner experience. Just functional state management.")
    print("═" * 62 + "\n")

    state = _init_state(seed)
    history = []

    for tick, (label, obs) in enumerate(AUTO_SEQUENCE):
        state, logrow = irm_step(state, obs)
        logrow["tick"] = tick
        history.append(logrow)
        print(f"  [{label:<28}]  ", end="")
        _print_tick(tick, logrow)

    print_session_summary(history)


def run_interactive(seed: int = 42) -> None:
    print("\n" + "═" * 62)
    print("  IRM PROBE — Interactive mode")
    print("  Inject inputs. Watch the system respond.")
    print("  Type 'q' to quit, 's' for session summary.")
    print("═" * 62 + "\n")

    state = _init_state(seed)
    history = []
    tick = 0

    while True:
        print("\n  Inject:")
        for k, (label, _) in INJECTION_MENU.items():
            print(f"    {k}) {label}")
        print("    s) Session summary    q) Quit")

        try:
            choice = input("  > ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            break

        if choice == "q":
            break
        if choice == "s":
            print_session_summary(history)
            continue
        if choice not in INJECTION_MENU:
            print("  (unknown input — treating as quiet tick)")
            choice = "1"

        label, obs = INJECTION_MENU[choice]
        state, logrow = irm_step(state, obs)
        logrow["tick"] = tick
        history.append(logrow)
        print(f"\n  [{label:<28}]  ", end="")
        _print_tick(tick, logrow)
        tick += 1

    if history:
        print_session_summary(history)


def main() -> None:
    ap = argparse.ArgumentParser(description="IRM Probe — regime explorer")
    ap.add_argument("--auto",   action="store_true", help="Run automated stress sequence")
    ap.add_argument("--seed",   type=int, default=42, help="RNG seed")
    args = ap.parse_args()

    if args.auto:
        run_auto(seed=args.seed)
    else:
        run_interactive(seed=args.seed)


if __name__ == "__main__":
    main()
