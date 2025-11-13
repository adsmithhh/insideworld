# evolution_chamber/MAE/policies/__init__.py

"""
Policy implementations for MAE agents.

Includes:
- RandomPolicy: stochastic baseline
- ScriptedPolicy: simple deterministic baseline
- IRMPolicy: IRM-backed agent bridge
"""

from .random import RandomPolicy
from .scripted import ScriptedPolicy
from .bridge import IRMPolicy

__all__ = ["RandomPolicy", "ScriptedPolicy", "IRMPolicy"]
