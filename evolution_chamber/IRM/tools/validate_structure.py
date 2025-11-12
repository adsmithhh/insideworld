#!/usr/bin/env python3
"""
Evolution Chamber — Structure Validator (v0.1)
Checks minimal invariants:
- evolution_chamber/README.md exists
- evolution_chamber/meta/index.yaml exists and has required keys
- Listed IRM line paths exist and contain a README.md (and optionally inout.yaml)
- Numeric thresholds are sane
"""
import argparse
from __future__ import annotations
import sys, json, re
from pathlib import Path

# Tiny YAML reader (safe) without PyYAML: supports the subset we need
def _miniyaml(text: str):
    # extremely small YAML subset: key: value, nested via two-space indent, lists with "- "
    # converts to dict/list/str/float/bool/null where obvious
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
                # list item can be scalar k or start of nested map
                item = l[2:]
                if re.match(r"^[^:]+:\s*.*$", item):  # inline map head -> recurse next indent
                 
                    def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true", help="enforce tests/ and inout.yaml schema")
    args = ap.parse_args()
    strict = args.strict

                 if strict:
                check((lp/"tests").exists(), f"{name}: tests/ folder present (strict)", str(lp/"tests"), findings)
                # minimal inout.yaml schema check (version/status/scope)
                ino = lp/"inout.yaml"
                if ino.exists():
                    try:
                        ino_data = _miniyaml(ino.read_text(encoding="utf-8"))
                        okv = all(k in (ino_data or {}) for k in ("version","status","scope"))
                        check(okv, f"{name}: inout.yaml has version/status/scope (strict)", str(ino), findings)
                    except Exception as e:
                        check(False, f"{name}: inout.yaml parseable ({e})", str(ino), findings)

#
