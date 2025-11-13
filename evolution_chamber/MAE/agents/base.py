# evolution_chamber/MAE/agents/base.py

from typing import Protocol
from ..env.spaces import Obs, Act


class Agent(Protocol):
    """
    Minimal interface all MAE agents must implement.
    """

    id: str       # agent id
    line: str     # IRM line: "IRM", "IRM_cn", "IRM_vnext"

    def reset(self, seed: int, task_cfg: dict) -> None:
        """
        Called once per scenario run.
        """
        ...

    def observe(self, obs: Obs) -> None:
        """
        Receives the observation for this tick.
        """
        ...

    def decide(self) -> Act:
        """
        Returns the action for this tick.
        """
        ...
