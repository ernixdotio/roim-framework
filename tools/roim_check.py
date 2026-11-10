#!/usr/bin/env python3
"""
roim_check.py - RoIM readiness checker (v0.1)

Reads an IFC model, finds every element that declares a RoIM level in
Pset_RobotReadiness, and checks that it carries every property required
up to that level (see spec/pset/Pset_RobotReadiness_v0.1.json).

Usage:
    python tools/roim_check.py model.ifc [--report report.csv]

Requires: pip install ifcopenshell
Licence: MIT (see LICENSE-CODE)
"""
import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path

import ifcopenshell
import ifcopenshell.util.element as eu

LEVELS = ["R0", "R1", "R2", "R3", "R4"]
SPEC_PATH = Path(__file__).resolve().parent.parent / "spec" / "pset" / "Pset_RobotReadiness_v0.1.json"


def load_spec(path=SPEC_PATH):
    with open(path, encoding="utf-8") as f:
        spec = json.load(f)
    return spec["name"], spec["properties"]


def required_for(level, props):
    """Properties required at `level` (cumulative from R1)."""
    i = LEVELS.index(level)
    return [p for p in props if LEVELS.index(p["fromLevel"]) <= i and p["name"] != "RoIM_Level"]


def check_value(prop, value):
    if value is None or (isinstance(value, str) and not value.strip()):
        return "missing"
    allowed = prop.get("allowedValues")
    if allowed and str(value) not in allowed:
        return f"invalid value '{value}'"
    return None


def check(model_path, report_path=None):
    pset_name, props = load_spec()
    model = ifcopenshell.open(model_path)
    rows, summary = [], Counter()

    for el in model.by_type("IfcElement"):
        pset = eu.get_pset(el, pset_name)
        if not pset or "RoIM_Level" not in pset:
            continue
        level = str(pset["RoIM_Level"]).strip()
        if level not in LEVELS:
            rows.append([el.GlobalId, el.is_a(), el.Name or "", level, "FAIL", "RoIM_Level", "invalid level"])
            summary["FAIL"] += 1
            continue
        problems = []
        for p in required_for(level, props):
            err = check_value(p, pset.get(p["name"]))
            if err:
                problems.append((p["name"], err))
        status = "FAIL" if problems else "PASS"
        summary[status] += 1
        summary[f"{level}:{status}"] += 1
        if problems:
            for name, err in problems:
                rows.append([el.GlobalId, el.is_a(), el.Name or "", level, status, name, err])
        else:
            rows.append([el.GlobalId, el.is_a(), el.Name or "", level, status, "", ""])

    total = summary["PASS"] + summary["FAIL"]
    print(f"RoIM check: {model_path}")
    print(f"  Elements declaring a RoIM level: {total}")
    print(f"  PASS: {summary['PASS']}   FAIL: {summary['FAIL']}")
    for lv in LEVELS:
        p, f = summary[f"{lv}:PASS"], summary[f"{lv}:FAIL"]
        if p or f:
            print(f"    {lv}: {p} pass, {f} fail")

    if report_path:
        with open(report_path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["GlobalId", "IfcClass", "Name", "DeclaredLevel", "Status", "Property", "Issue"])
            w.writerows(rows)
        print(f"  Report written to {report_path}")
    return summary["FAIL"] == 0


def main():
    ap = argparse.ArgumentParser(description="Check an IFC model against RoIM levels (Pset_RobotReadiness v0.1).")
    ap.add_argument("model", help="Path to the IFC file")
    ap.add_argument("--report", help="Write a CSV report to this path")
    a = ap.parse_args()
    sys.exit(0 if check(a.model, a.report) else 1)


if __name__ == "__main__":
    main()
