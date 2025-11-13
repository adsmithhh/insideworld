# evolution_chamber/MAE/cli.py

import argparse
import yaml
from pathlib import Path

from .env.tasks import make_env
from .bus.broker import Broker
from .agents.registry import build_agent_registry
from .sim.scheduler import Scheduler
from .logging.writers import LogRouter
from .logging.kpis import compute_kpis


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True, help="Path to MAE scenario YAML")
    args = ap.parse_args()

    cfg_path = Path(args.config)
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


if __name__ == "__main__":
    main()
