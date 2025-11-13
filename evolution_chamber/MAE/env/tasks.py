# evolution_chamber/MAE/env/tasks.py

from numpy.random import default_rng
from .world import Environment


def make_env(task_cfg: dict) -> Environment:
    """
    Factory for Environment instances.
    Creates the shared world with a seeded RNG.
    """
    seed = int(task_cfg.get("seed", 0))
    rng = default_rng(seed)
    return Environment(task_cfg=task_cfg, rng=rng)
