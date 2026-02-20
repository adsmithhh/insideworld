# evolution_chamber/IRM/models/primitives.py
"""
Core IRM state primitives.

IRMState is the data carrier for one agent's internal reality model.
It holds the latent vectors, covariance, regime, and timers —
everything needed to run one step of the IRM engine.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict

import numpy as np


@dataclass
class IRMState:
    """
    Complete state of one IRM instance at a single point in time.

    Fields:
        z_L       Low-level latent vector  (shape: d_L)
        z_H       High-level latent vector (shape: d_H)
        Sigma_H   Covariance of z_H belief (shape: d_H × d_H)
        regime    Current regime name: DORMANT | SAFE_AWARE | ACTIVE |
                                       DESTABILIZED | CORRECTIVE
        timers    Phase counters per regime (for min_duration enforcement)
        rng_state Seeded RNG for reproducibility
    """
    z_L: np.ndarray
    z_H: np.ndarray
    Sigma_H: np.ndarray
    regime: str = "DORMANT"
    timers: Dict[str, int] = field(default_factory=dict)
    rng_state: Any = None

    def indices(self, scale_s_u: float = 1.0) -> Dict[str, float]:
        """
        Compute the six core IRM indices from current state.

        Returns a dict with keys matching irm.yaml section 4:
            Δ_proto, PT_u, DP_u, CC_index, RCI, E
        """
        delta = self.z_L - self.z_H
        dim = len(delta)

        # PT_u: Mahalanobis-style uncertainty pressure
        sigma_diag = np.maximum(np.diag(self.Sigma_H), 1e-12)
        pt_u = float(np.sqrt(np.sum(delta ** 2 / sigma_diag)))

        # DP_u: normalized uncertainty pressure [0, 1]
        dp_u = min(1.0, pt_u / max(scale_s_u, 1e-12))

        # CC_index: coherence — how aligned are z_L and z_H?
        v_norm = float(np.linalg.norm(delta)) / (np.sqrt(dim) + 1e-12)
        cc_index = 1.0 - min(1.0, v_norm)

        # RCI: reality consistency — mean absolute residual
        r_norm = float(np.mean(np.abs(delta)))
        rci = 1.0 - min(1.0, r_norm)

        return {
            "Δ_proto": float(np.linalg.norm(delta)),
            "PT_u":    pt_u,
            "DP_u":    dp_u,
            "CC_index": cc_index,
            "RCI":     rci,
            "E":       1.0,  # compute cost; caller sets this
        }

    def regime_label(self) -> str:
        """Return current regime with a one-line functional description."""
        descriptions = {
            "DORMANT":       "DORMANT      — low input, no commits",
            "SAFE_AWARE":    "SAFE_AWARE   — observer mode, log only",
            "ACTIVE":        "ACTIVE       — normal operation, commits on",
            "DESTABILIZED":  "DESTABILIZED — pressure detected, guarded commits",
            "CORRECTIVE":    "CORRECTIVE   — rollback mode, stabilizing",
        }
        return descriptions.get(self.regime, self.regime)
