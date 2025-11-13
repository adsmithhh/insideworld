# evolution_chamber/MAE/bus/__init__.py

"""
Message bus layer for MAE.

Provides:
- Message dataclass
- In-process Broker with simple ACL and rate limiting
"""

from .schema import Message
from .broker import Broker

__all__ = ["Message", "Broker"]
