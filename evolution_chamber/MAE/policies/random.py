# evolution_chamber/MAE/policies/random.py

from numpy.random import default_rng
from ..env.spaces import Obs, Act


class RandomPolicy:
    """
    Random baseline policy.

    Each tick, adds a small Gaussian delta to its score.
    """

    def __init__(self, agent_id: str, line: str) -> None:
        self.id = agent_id
        self.line = line
        self._rng = default_rng()
        self._last_obs: Obs | None = None
        self.last_logrow: dict = {}

    def reset(self, seed: int, task_cfg: dict) -> None:
        # jittered seed so different agents differ
        self._rng = default_rng(seed + hash(self.id) % 10_000)

    def observe(self, obs: Obs) -> None:
        self._last_obs = obs

    def decide(self) -> Act:
        delta = float(self._rng.normal(loc=0.0, scale=0.1))
        self.last_logrow = {
            "policy": "random",
            "delta_score": delta,
        }
        return Act(world_actions={"delta_score": delta}, messages_out=[])
