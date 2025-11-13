# evolution_chamber/MAE/env/world.py

from typing import Dict
from .spaces import Obs, Act


class Environment:
    """
    Minimal shared world for MAE.

    - Tracks per-agent local state in self.state["agents"]
    - Provides observations
    - Applies agent actions each tick
    """

    def __init__(self, task_cfg: dict, rng) -> None:
        self.task_cfg = task_cfg
        self.rng = rng
        self.tick = 0
        self.state: Dict[str, Dict] = {}

    def reset(self, agent_ids) -> None:
        """
        Initialize world state for all agents.
        """
        self.tick = 0
        self.state = {
            "agents": {aid: {"score": 0.0} for aid in agent_ids},
            "resources": {},
        }

    def observe(self, agent_id: str) -> Obs:
        """
        Construct an observation for a given agent.
        """
        return Obs(
            tick=self.tick,
            world_state=self._world_view_for(agent_id),
            local_state=self.state["agents"][agent_id],
            messages_in=[],  # scheduler fills this
        )

    def step(self, actions: Dict[str, Act]) -> None:
        """
        Apply world_actions from each agent and progress the simulation.
        """
        # Example: treat a 'delta_score' world_action as additive.
        for agent_id, act in actions.items():
            delta = act.world_actions.get("delta_score", 0.0)
            self.state["agents"][agent_id]["score"] += float(delta)

        self.tick += 1

    def _world_view_for(self, agent_id: str) -> Dict:
        """
        Optionally restrict or mask world info per agent.
        For now, all agents see everything.
        """
        return self.state
