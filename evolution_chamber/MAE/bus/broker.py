# evolution_chamber/MAE/bus/broker.py

from collections import defaultdict
from typing import Dict, List, Tuple
from .schema import Message


class Broker:
    """
    In-process pub/sub message broker.

    - Simple ACL on topics
    - Per-topic rate limiting per (src, topic, tick)
    - Delivery by agent_id, with '*' as broadcast bucket
    """

    def __init__(self, acl: dict, rate_limits: dict) -> None:
        self.acl = acl
        self.rate_limits = rate_limits
        self._outbox: Dict[str, List[Message]] = defaultdict(list)
        self._sent_counts: Dict[Tuple[str, str, int], int] = defaultdict(int)

    def publish(self, msg: Message) -> None:
        """
        Publish a message into the broker. It will be available
        for delivery on the next scheduler step.
        """
        key = (msg.src, msg.topic, msg.tick)
        self._sent_counts[key] += 1

        # simple per-topic rate limiting
        if self._sent_counts[key] > self.rate_limits.get(msg.topic, 10_000):
            return

        if not self._allowed(msg):
            return

        target_key = msg.dst or "*"
        self._outbox[target_key].append(msg)

    def _allowed(self, msg: Message) -> bool:
        """
        Check ACL for this topic: ACL format:
          { topic: { "allow_src": [ids...] } }
        """
        spec = self.acl.get(msg.topic, {})
        allow_src = spec.get("allow_src")
        if allow_src and msg.src not in allow_src:
            return False
        return True

    def deliver(self, agent_id: str) -> List[Message]:
        """
        Collect all messages targeted to this agent id plus broadcast.
        Clears them from the outbox.
        """
        msgs = self._outbox.pop(agent_id, [])
        msgs += self._outbox.pop("*", [])
        return msgs
