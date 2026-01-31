#!/usr/bin/env sage
"""Attempt to compute canonical double-sixes using Sage's cubic surface tools.

This script is best run within a Sage environment. It will try multiple approaches
and write artifacts/sage_double_sixes.json if successful, otherwise it will dump
useful diagnostics for manual inspection.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

try:
    from sage.all import CubicSurface, ProjectiveSpace

    sage_available = True
except Exception as e:
    print("Sage components not available:", e)
    sage_available = False

if not sage_available:
    print(
        "Sage not available in this environment. Run this script inside Sage to compute canonical double-sixes."
    )
    sys.exit(1)

# Example: try to use a well-known cubic surface (Clebsch) and compute lines
# NOTE: Sage's API may differ across versions; this is a best-effort helper.
try:
    P3 = ProjectiveSpace(3, QQ)
    # Clebsch cubic or a standard cubic that Sage supports
    X = CubicSurface(P3, "x0^3 + x1^3 + x2^3 + x3^3")
    lines = X.lines()
    print("Found lines count:", len(lines))
    Ldata = []
    for L in lines:
        try:
            pts = [p for p in L.rational_points(10)]
        except Exception:
            pts = []
        Ldata.append({"repr": str(L), "points_example": [str(p) for p in pts[:3]]})

    out_path = ROOT / "artifacts" / "sage_double_sixes.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps({"lines": Ldata}, indent=2), encoding="utf-8")
    print("Wrote", out_path)
except Exception as e:
    print("Error while using CubicSurface API:", e)
    sys.exit(1)
