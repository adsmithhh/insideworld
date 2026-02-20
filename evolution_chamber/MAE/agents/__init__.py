# evolution_chamber/MAE/agents/__init__.py

"""
Agent layer for MAE.

Defines:
- Agent protocol (interface)
- Helpers for constructing agents from config
"""

from .base import Agent  # Protocol

__all__ = ["Agent"]
