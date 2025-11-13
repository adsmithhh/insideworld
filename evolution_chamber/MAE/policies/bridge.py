# evolution_chamber/MAE/policies/bridge.py

from typing import Any, Dict

import numpy as np

from ..env.spaces import Obs, Act

# Default: main IRM line. You can later parameterise this import per line.
from evolution_chamber.IRM.step_engine import step as irm_step
from evolution_chamber.IRM.models.primitives import IRMState


class IRMPolicy:
    """
    IRM-backed agent policy.

    One instance per agent; carries its own IRMState.
    """

    def __init__(self, agent_id: str, line: str, params: Dict[str, Any]) -> None:
        self.id = agent_id
        self.line = line
        self.params = params
        self.state: IRMState | None = None
        self._last_obs: Obs | None = None
        self.last_logrow: Dict[str, Any] = {}

    def reset(self, seed: int, task_cfg: dict) -> None:
        rng = np.random.default_rng(seed + hash(self.id) % 10_000)
        z_dim = int(self.params.get("z_dim", 8))
        self.state = IRMState(
            z_L=rng.normal(size=z_dim),
            z_H=rng.normal(size=z_dim),
            Sigma_H=np.eye(z_dim),
            regime="ACTIVE",
            timers={},
            rng_state=rng,
        )

    def observe(self, obs: Obs) -> None:
        self._last_obs = obs

    def decide(self) -> Act:
        assert self.state is not None
        assert self._last_obs is not None

        obs_dict = {
            "world_state": self._last_obs.world_state,
            "local_state": self._last_obs.local_state,
            "messages": [
                getattr(m, "payload", m) for m in self._last_obs.messages_in
            ],
        }

        self.state, logrow = irm_step(self.state, obs_dict, self.params)
        self.last_logrow = logrow

        # Minimal placeholder: push delta proportional to -E (if present)
        E = float(logrow.get("E", 0.0))
        delta = -0.01 * E

        return Act(
            world_actions={"delta_score": delta},
            messages_out=[],
        )
