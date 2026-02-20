# evolution_chamber.IRM.engine package
from .entropy_calc import entropy_bits, prediction_salience
from .anchor_resolver import classify_conflict, resolve

__all__ = ["entropy_bits", "prediction_salience", "classify_conflict", "resolve"]
