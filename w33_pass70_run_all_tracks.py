"""Pass 70 master runner: executes Tracks A, B, C and emits all JSON witnesses.

This is the canonical single-entry-point for the entire Pass 70 execution.
Run:
    python w33_pass70_run_all_tracks.py
Outputs three JSON files and prints a pass/fail summary.
"""
from __future__ import annotations

import importlib
import json
import math
import sys
from pathlib import Path

TRACKS = [
    "w33_pass70_trackA_ramanujan",
    "w33_pass70_trackB_qec",
    "w33_pass70_trackC_partition",
]

OUTPUTS = [
    "w33_pass70_trackA_ramanujan.json",
    "w33_pass70_trackB_qec.json",
    "w33_pass70_trackC_partition.json",
]


def run_all() -> None:
    for module_name in TRACKS:
        mod = importlib.import_module(module_name)
        mod.main()

    results = {}
    for fname in OUTPUTS:
        p = Path(fname)
        if p.exists():
            results[fname] = json.loads(p.read_text())
            print(f"[PASS] {fname}")
        else:
            print(f"[FAIL] {fname} not written", file=sys.stderr)
            sys.exit(1)

    # Cross-track consistency check:
    # Track B length_n must equal 360
    assert results[OUTPUTS[1]]["length_n"] == 360, "Track B n mismatch"
    # Track A lambda2 must equal Track C lambda2
    tol = 1e-12
    assert abs(results[OUTPUTS[0]]["lambda2"] - results[OUTPUTS[2]]["lambda2"]) < tol, \
        "lambda2 mismatch between Track A and Track C"
    # Track A is_ramanujan must be False
    assert results[OUTPUTS[0]]["is_ramanujan"] is False, "Ramanujan bound should be violated"

    print("\nAll Pass 70 tracks completed and cross-validated.")


if __name__ == "__main__":
    run_all()
