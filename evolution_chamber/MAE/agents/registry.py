# evolution_chamber/MAE/agents/registry.py

from typing import Dict, List
from .base import Agent
from ..policies.random import RandomPolicy
from ..policies.scripted import ScriptedPolicy
from ..policies.bridge import IRMPolicy


def build_agent_registry(
    agent_cfgs: List[dict],
    irm_params_by_line: Dict[str, dict],
) -> Dict[str, Agent]:
    """
    Build all agents from config.

    agent_cfgs example:
      - id: A
        kind: irm | random | scripted
        line: IRM | IRM_cn | IRM_vnext
        delta: 0.05      # for scripted, optional
    """
    agents: Dict[str, Agent] = {}

    for cfg in agent_cfgs:
        agent_id = cfg["id"]
        kind = cfg["kind"]
        line = cfg.get("line", "IRM")

        if kind == "random":
            agent = RandomPolicy(agent_id=agent_id, line=line)
        elif kind == "scripted":
            delta = float(cfg.get("delta", 0.05))
            agent = ScriptedPolicy(agent_id=agent_id, line=line, delta=delta)
        elif kind == "irm":
            params = irm_params_by_line.get(line, {})
            agent = IRMPolicy(agent_id=agent_id, line=line, params=params)
        else:
            raise ValueError(f"Unknown agent kind {kind}")

        agents[agent_id] = agent

    return agents
