# evolution_chamber/MAE/sim/__init__.py

"""
Simulation layer for MAE.

Provides:
- Scheduler: deterministic tick loop
- run_scenario helper (see rollout.py)
"""

from .scheduler import Scheduler

__all__ = ["Scheduler"]
