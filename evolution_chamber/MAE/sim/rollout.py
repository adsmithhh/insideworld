# evolution_chamber/MAE/sim/rollout.py

from pathlib import Path
import yaml

from ..env.tasks import make_env
from ..bus.broker import Broker
from ..agents.registry import build_agent_registry
from .scheduler import Scheduler
from ..logging.writers import LogRouter
from ..logging.kpis import compute_kpis


def run_scenario(config_path: str) -> None:
    """
    High-level helper: run a MAE scenario from a YAML config.
    """
    cfg_path = Path(config_path)
    cfg = yaml.safe_load(cfg_path.read_text())

    scenario_name = cfg["scenario"]["name"]
    seed = int(cfg["scenario"]["seed"])
    ticks = int(cfg["scenario"]["ticks"])

    env = make_env(cfg["task"])
    broker = Broker(cfg.get("bus_acl", {}), cfg.get("bus_rate_limits", {}))
    agents = build_agent_registry(cfg["agents"], cfg.get("irm_params", {}))

    logger = LogRouter(scenario=scenario_name, seed=seed)
    sched = Scheduler(env=env, broker=broker, agents=agents, logger=logger)

    sched.reset(seed=seed, task_cfg=cfg["task"])

    for _ in range(ticks):
        sched.step()

    logger.close()
    compute_kpis(scenario_name, seed)
