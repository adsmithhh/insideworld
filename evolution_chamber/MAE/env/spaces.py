# evolution_chamber/MAE/env/spaces.py

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class Obs:
    """
    Observation delivered to an agent at each tick.

    tick:        global simulation tick
    world_state: environment state visible to this agent
    local_state: agent's own state inside the environment
    messages_in: messages delivered from the bus
    """
    tick: int
    world_state: Dict[str, Any]
    local_state: Dict[str, Any]
    messages_in: List[Any] = field(default_factory=list)


@dataclass
class Act:
    """
    Action returned by an agent at each tick.

    world_actions: dict of environment-facing actions
    messages_out: list of outgoing bus messages
    """
    world_actions: Dict[str, Any] = field(default_factory=dict)
    messages_out: List[Any] = field(default_factory=list)
