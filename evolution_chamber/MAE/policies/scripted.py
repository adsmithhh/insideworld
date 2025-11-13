# evolution_chamber/MAE/policies/scripted.py

from ..env.spaces import Obs, Act


class ScriptedPolicy:
    """
    Deterministic baseline policy.

    Each tick, adds a fixed delta to its score.
    """

    def __init__(self, agent_id: str, line: str, delta: float = 0.05) -> None:
        self.id = agent_id
        self.line = line
        self.delta = float(delta)
        self._last_obs: Obs | None = None
        self.last_logrow: dict = {}

    def reset(self, seed: int, task_cfg: dict) -> None:
        # no-op: fully deterministic
        pass

    def observe(self, obs: Obs) -> None:
        self._last_obs = obs

    def decide(self) -> Act:
        self.last_logrow = {
            "policy": "scripted",
            "delta_score": self.delta,
        }
        return Act(world_actions={"delta_score": self.delta}, messages_out=[])
