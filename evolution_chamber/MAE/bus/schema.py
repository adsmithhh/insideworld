# evolution_chamber/MAE/bus/schema.py

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class Message:
    """
    Message passed over the MAE bus.

    src:   agent id that sent the message
    dst:   target agent id, or None for broadcast
    topic: logical channel name
    tick:  simulation tick at send time
    payload: arbitrary JSON-serializable dict
    taint_level: integer for future firewall / taint tracking
    """
    src: str
    dst: Optional[str]
    topic: str
    tick: int
    payload: Dict[str, Any]
    taint_level: int = 0
