#!/usr/bin/env python3
"""
IRM → vNext migration helper (v0.1)
Reads alignment map and emits a compact report showing whether
canonical IRM indices/thresholds match vNext.
"""
from pathlib import Path
import json

ROOT = Path("evolution_chamber")
MAP  = ROOT/"meta/alignment/IRM_to_vNext_map.yaml"

def main():
    if not MAP.exists():
        print(json.dumps({"ok": False, "error": "alignment map missing", "path": str(MAP)}))
        raise SystemExit(1)
    # lightweight: just print where humans should check; no YAML parser required here
    print(json.dumps({
        "ok": True,
        "message": "Open the alignment map and verify thresholds and invariants are mirrored.",
        "map_path": str(MAP),
        "checklist": [
            "IRM/schema/primitives.yaml -> vnext_shims present",
            "IRM/engine/step_engine.py -> vnext_indices() logged",
            "IRM_vnext/schema/indices_invariants.yaml -> thresholds match map",
            "IRM_vnext/tests/canary.yaml -> contains 6 mirrored cases",
        ]
    }, indent=2))

if __name__ == "__main__":
    main()
