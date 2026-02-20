import yaml
from dataclasses import dataclass, field
from typing import Dict, Optional
import os


@dataclass
class KB:
    path: str
    terms: Dict = field(default_factory=dict)
    predicates: Dict = field(default_factory=dict)

    def load(self):
        if not os.path.exists(self.path):
            raise FileNotFoundError(self.path)

        with open(self.path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        self.terms = data.get("terms", {})
        self.predicates = data.get("predicates", {})

    def save(self):
        data = {
            "version": 0.1,
            "terms": self.terms,
            "predicates": self.predicates,
            "meta": {
                "auto_generated": True
            }
        }

        with open(self.path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, sort_keys=False)

    def has_term(self, term: str) -> bool:
        return term.lower() in self.terms

    def get_term(self, term: str) -> Optional[dict]:
        return self.terms.get(term.lower())

    def ensure_term(self, term: str):

        term = term.lower()

        if term in self.terms:
            return False

        # auto-create stub
        self.terms[term] = {
            "type": "unknown",
            "requires": [
                "definition",
                "measurement_protocol"
            ],
            "status": "auto_stub",
            "confidence": 0.0
        }

        return True