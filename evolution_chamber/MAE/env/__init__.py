# evolution_chamber/MAE/env/__init__.py

"""
Environment layer for MAE.

Provides:
- Obs / Act dataclasses
- Environment base class (ticks, reset/step)
- Task factory
"""

from .spaces import Obs, Act
from .world import Environment
from .tasks import make_env

__all__ = ["Obs", "Act", "Environment", "make_env"]
