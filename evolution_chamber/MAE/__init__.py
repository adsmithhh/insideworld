# evolution_chamber/MAE/__init__.py

"""
Multi-Agent Environment (MAE) for evolution_chamber.

This package wires:
- Environment (shared world)
- Agents (some IRM-backed)
- Message bus
- Logging and KPIs
"""

from .sim.rollout import run_scenario  # convenience re-export

__all__ = ["run_scenario"]
