# evolution_chamber/MAE/logging/__init__.py

"""
Logging layer for MAE.

- LogRouter: routes per-agent logs to the correct IRM line
- compute_kpis: placeholder for multi-agent KPIs
"""

from .writers import LogRouter
from .kpis import compute_kpis

__all__ = ["LogRouter", "compute_kpis"]
