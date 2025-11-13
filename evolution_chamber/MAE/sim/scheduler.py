# evolution_chamber/MAE/sim/scheduler.py

from typing import Dict
from ..env.world import Environment
from ..env.spaces import Act
from ..bus.broker import Broker


class Scheduler:
    """
    Deterministic tick scheduler for MAE.

    Per tick:
    - build observations (incl. messages from bus)
    - let each agent decide an Act
    - publish messages to bus
    - apply world_actions to Environment
    - send log rows to LogRouter
    """

    def __init__(
        self,
        env: Environment,
        broker: Broker,
        agents: Dict[str, object],
        logger,
    ) -> None:
        self.env = env
        self.broker = broker
        self.agents = agents
        self.logger = logger
        self.tick = 0

    def reset(self, seed: int, task_cfg: dict) -> None:
        agent_ids = list(self.agents.keys())
        self.env.reset(agent_ids)
        for agent in self.agents.values():
            agent.reset(seed, task_cfg)
        self.tick = 0

    def step(self) -> None:
        actions: Dict[str, Act] = {}
        agent_logs: Dict[str, dict] = {}
        agent_lines: Dict[str, str] = {}

        # 1) observations, decisions, messages
        for agent_id, agent in self.agents.items():
            obs = self.env.observe(agent_id)
            obs.messages_in = self.broker.deliver(agent_id)
            agent.observe(obs)
            act = agent.decide()
            actions[agent_id] = act

            for msg in act.messages_out:
                self.broker.publish(msg)

            agent_logs[agent_id] = getattr(agent, "last_logrow", {})
            agent_lines[agent_id] = getattr(agent, "line", "IRM")

        # 2) world update
        self.env.step(actions)

        # 3) logging
        self.logger.record_tick(self.tick, agent_logs, agent_lines)

        self.tick += 1
