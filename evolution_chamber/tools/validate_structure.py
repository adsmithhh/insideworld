#!/usr/bin/env python3
"""
Evolution Chamber — Structure Validator (v0.1)
Checks minimal invariants:
- evolution_chamber/README.md exists
- evolution_chamber/meta/index.yaml exists and has required keys
- Listed IRM line paths exist and contain a README.md (and optionally inout.yaml)
- Numeric thresholds are sane
"""
from __future__ import annotations
import sys, json, re
from pathlib import Path
import argparse

# Tiny YAML reader (safe) without PyYAML: supports the subset we need
def _miniyaml(text: str):
    lines = [l.rstrip() for l in text.splitlines() if l.strip() and not l.strip().startswith("#")]
    def parse_block(i, indent=0):
        obj = {}
        arr = None
        while i < len(lines):
            line = lines[i]
            if not line.startswith(" " * indent):
                break
            l = line[indent:]
            if l.startswith("- "):  # list item
                if arr is None:
                    arr = []
                item = l[2:]
                if re.match(r"^[^:]+:\s*.*$", item):
                    lines[i] = " " * (indent) + item
                    subtree, i2 = parse_block(i, indent)
                    arr.append(subtree)
                    i = i2
                else:
                    arr.append(_coerce_scalar(item))
                    i += 1
            else:
                m = re.match(r"^([^:]+):\s*(.*)$", l)
                if not m:
                    raise ValueError(f"YAML parse error near: {l}")
                key, val = m.group(1).strip(), m.group(2).strip()
                if val == "":
                    i += 1
                    subtree, i = parse_block(i, indent + 2)
                    obj[key] = subtree
                else:
                    obj[key] = _coerce_scalar(val)
                    i += 1
            if arr is not None and obj:
                raise ValueError("Mixed list/map at same level is not supported by miniyaml.")
        return (arr if arr is not None else obj), i

    def _coerce_scalar(s: str):
        s = s.strip()
        if s.lower() in ("true","false"): return s.lower()=="true"
        if s.lower() in ("null","~"): return None
        try:
            if "." in s or "e" in s.lower(): return float(s)
            return int(s)
        except ValueError:
            return s

    return parse_block(0,0)[0]

OK = "PASS"
FAIL = "FAIL"

def check(cond, msg, ctx, findings):
    findings.append({"status": OK if cond else FAIL, "check": msg, "context": ctx})
    return cond

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true", help="enforce tests/ and inout.yaml schema")
    args = ap.parse_args()
    strict = args.strict

    root = Path("evolution_chamber")
    findings = []
    summary = {"passes":0, "fails":0}

    # 1) essential files
    readme = root/"README.md"
    idx = root/"meta"/"index.yaml"
    check(readme.exists(), "chamber README present", str(readme), findings)
    check(idx.exists(), "meta/index.yaml present", str(idx), findings)

    # 2) parse index.yaml and required keys
    index_data = {}
    if idx.exists():
        try:
            index_data = _miniyaml(idx.read_text(encoding="utf-8"))
            check(True, "index.yaml parsed", "miniyaml", findings)
        except Exception as e:
            check(False, f"index.yaml parseable ({e})", "miniyaml", findings)

    req_chamber_keys = ["id","version","status","readme","access_protocol","continuity_requirements"]
    chamber = (index_data.get("chamber") or {}) if index_data else {}
    for k in req_chamber_keys:
        check(k in chamber, f"chamber.{k} present", "index.yaml", findings)

    # 3) continuity numeric sanity
    cr = chamber.get("continuity_requirements",{}) if chamber else {}
    if cr:
        check(isinstance(cr.get("energy_limit", None),(int,float)) and cr["energy_limit"]<=1.30,
              "energy_limit ≤ 1.30", "continuity_requirements", findings)
        check(isinstance(cr.get("f1_min", None),(int,float)) and cr["f1_min"]>=0.80,
              "f1_min ≥ 0.80", "continuity_requirements", findings)
        check(isinstance(cr.get("drift_norm_max", None),(int,float)) and cr["drift_norm_max"]<=0.10,
              "drift_norm_max ≤ 0.10", "continuity_requirements", findings)

    # 4) lines exist & have README (and try inout.yaml)
    lines = index_data.get("lines") or []
    for line in lines:
        name = line.get("name")
        path = (line.get("path") or "").replace("../","")
        lp = root / path
        okp = check(lp.exists(), f"line path exists: {name}", str(lp), findings)
        if okp:
            check((lp/"README.md").exists(), f"{name}: README.md present", str(lp/"README.md"), findings)
            check((lp/"inout.yaml").exists(), f"{name}: inout.yaml present (recommended)", str(lp/"inout.yaml"), findings)
            if strict:
                check((lp/"tests").exists(), f"{name}: tests/ folder present (strict)", str(lp/"tests"), findings)
                ino = lp/"inout.yaml"
                if ino.exists():
                    try:
                        ino_data = _miniyaml(ino.read_text(encoding="utf-8"))
                        okv = all(k in (ino_data or {}) for k in ("version","status","scope"))
                        check(okv, f"{name}: inout.yaml has version/status/scope (strict)", str(ino), findings)
                    except Exception as e:
                        check(False, f"{name}: inout.yaml parseable ({e})", str(ino), findings)

    # tally
    for f in findings:
        if f["status"]==OK: summary["passes"]+=1
        else: summary["fails"]+=1

    print(json.dumps({"summary":summary,"findings":findings}, indent=2))
    hard_fail = any(f["status"]==FAIL and ("present" in f["check"] or "parseable" in f["check"]) for f in findings)
    sys.exit(1 if hard_fail else 0)

if __name__ == "__main__":
    main()
