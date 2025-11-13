# evolution_chamber/MAE/logging/writers.py

from pathlib import Path
import csv
from typing import Dict, Any


class LogRouter:
    """
    Routes logs to:

        evolution_chamber/<LINE>/meta/runs/<scenario>/seed_XXX/agent_<ID>.csv

    where LINE ∈ {"IRM", "IRM_cn", "IRM_vnext"}.
    """

    def __init__(self, scenario: str, seed: int, repo_root: Path | None = None) -> None:
        self.scenario = scenario
        self.seed = seed
        # parents[2] of this file is: evolution_chamber/
        self.repo_root = repo_root or Path(__file__).resolve().parents[2]

        self._files: Dict[str, Any] = {}
        self._writers: Dict[str, csv.DictWriter] = {}
        self._fieldnames: Dict[str, list[str]] = {}

    def _agent_log_path(self, line: str, agent_id: str) -> Path:
        if line not in ("IRM", "IRM_cn", "IRM_vnext"):
            raise ValueError(f"Unknown line {line}")

        run_root = (
            self.repo_root
            / line
            / "meta"
            / "runs"
            / self.scenario
            / f"seed_{self.seed:03d}"
        )
        run_root.mkdir(parents=True, exist_ok=True)
        return run_root / f"agent_{agent_id}.csv"

    def record_tick(
        self,
        tick: int,
        agent_logs: Dict[str, Dict[str, Any]],
        agent_lines: Dict[str, str],
    ) -> None:
        """
        agent_logs:  {agent_id: {col: value, ...}}
        agent_lines: {agent_id: "IRM" | "IRM_cn" | "IRM_vnext"}
        """
        for agent_id, logrow in agent_logs.items():
            line = agent_lines[agent_id]
            path = self._agent_log_path(line, agent_id)

            if agent_id not in self._writers:
                f = path.open("w", newline="")
                fieldnames = ["tick"] + sorted(logrow.keys())
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()

                self._files[agent_id] = f
                self._writers[agent_id] = writer
                self._fieldnames[agent_id] = fieldnames

            writer = self._writers[agent_id]
            row = {"tick": tick}
            row.update(logrow)
            writer.writerow(row)

    def close(self) -> None:
        for f in self._files.values():
            f.close()
        self._files.clear()
        self._writers.clear()
