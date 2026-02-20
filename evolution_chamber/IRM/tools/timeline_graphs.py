# evolution_chamber/IRM/tools/timeline_graphs.py
"""
ASCII timeline renderer for IRM regime history and index trends.

Takes a list of tick records and prints:
  - A regime bar over time
  - Trend lines for the six core indices

No external dependencies.
"""

# Regime display characters
REGIME_CHARS = {
    "DORMANT":      "·",
    "SAFE_AWARE":   "○",
    "ACTIVE":       "█",
    "DESTABILIZED": "▒",
    "CORRECTIVE":   "▓",
}

INDEX_KEYS = ["DP_u", "CC_index", "RCI", "E", "PT_u", "Δ_proto"]
INDEX_THRESHOLDS = {
    "DP_u":    (0.20, 0.60),   # (warn, danger)
    "CC_index":(0.85, 0.60),   # (ok, bad) — inverted scale
    "RCI":     (0.80, 0.60),   # (ok, bad) — inverted scale
    "E":       (1.30, 1.80),   # (soft, hard)
    "PT_u":    (0.5,  1.0),
    "Δ_proto": (0.5,  1.0),
}


def print_regime_timeline(history: list, width: int = 60) -> None:
    """
    Print a one-line regime timeline.

    history: list of dicts with at least {"tick": int, "regime": str}
    """
    if not history:
        print("  (no history)")
        return

    step = max(1, len(history) // width)
    sampled = history[::step][:width]

    line = "".join(REGIME_CHARS.get(r.get("regime", "DORMANT"), "?") for r in sampled)

    print("\n  Regime timeline:")
    print("  " + line)
    print("  Legend: · DORMANT  ○ SAFE_AWARE  █ ACTIVE  ▒ DESTAB.  ▓ CORRECT.")


def print_index_trends(history: list, index_key: str, width: int = 50) -> None:
    """
    Print a sparkline for a single index over time.
    """
    values = [r.get("indices", {}).get(index_key, 0.0) for r in history]
    if not values:
        return

    step = max(1, len(values) // width)
    sampled = values[::step][:width]

    lo, hi = min(sampled), max(sampled)
    if hi - lo < 1e-9:
        hi = lo + 1.0

    chars = " ▁▂▃▄▅▆▇█"
    sparkline = ""
    for v in sampled:
        idx = int((v - lo) / (hi - lo) * (len(chars) - 1))
        sparkline += chars[max(0, min(len(chars)-1, idx))]

    warn, danger = INDEX_THRESHOLDS.get(index_key, (0.5, 1.0))
    current = values[-1]
    flag = "  ✓" if current < warn else ("  !" if current < danger else "  ✗")

    print(f"  {index_key:<12} {sparkline}  [{current:.3f}]{flag}")


def print_session_summary(history: list) -> None:
    """
    Full session summary: regime timeline + all index trends.

    history: list of dicts:
        {
          "tick": int,
          "regime": str,
          "indices": {"DP_u": float, "CC_index": float, ...},
          "transition": str | None
        }
    """
    if not history:
        print("  No session data.")
        return

    ticks = len(history)
    transitions = [r for r in history if r.get("transition")]

    print(f"\n{'─'*62}")
    print(f"  SESSION SUMMARY  ({ticks} ticks)")
    print(f"{'─'*62}")

    print_regime_timeline(history)

    print(f"\n  Index trends  (▁=low → █=high)  ✓ ok  ! warn  ✗ danger")
    print(f"  {'─'*58}")
    for key in INDEX_KEYS:
        print_index_trends(history, key)

    if transitions:
        print(f"\n  Regime transitions ({len(transitions)}):")
        for r in transitions:
            print(f"    tick {r['tick']:>3}  {r['transition']}")

    final = history[-1]
    print(f"\n  Final regime : {final.get('regime', '?')}")
    final_idx = final.get("indices", {})
    if final_idx:
        print(f"  Final indices: " + "  ".join(
            f"{k}={v:.3f}" for k, v in final_idx.items()
            if k in ("DP_u", "CC_index", "RCI", "E")
        ))
    print(f"{'─'*62}\n")