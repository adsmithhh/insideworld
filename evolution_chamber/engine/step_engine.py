def vnext_indices(state):
    # Minimal parity export; use existing computed indices when available
    d_proto = state["indices"].get("Δ_proto", 0.0)
    pt_u    = state["indices"].get("PT_u", 0.0)
    scale   = state.get("params", {}).get("scale_s_u", 1.0) or 1.0
    dp_u    = min(1.0, pt_u / max(scale, 1e-12))
    cc_idx  = state["indices"].get("CC_index", 1.0)
    rci     = state["indices"].get("RCI", 1.0)
    E       = state["indices"].get("E", 1.0)
    return {"Δ_proto": d_proto, "PT_u": pt_u, "DP_u": dp_u, "CC_index": cc_idx, "RCI": rci, "E": E}
