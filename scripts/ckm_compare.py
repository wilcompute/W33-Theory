#!/usr/bin/env python3
"""
Compare CKM overlap matrix (data/ckm_from_grams.json) to experimental magnitudes
and write a small JSON report to data/ckm_comparison.json
"""
from __future__ import annotations

import json
from pathlib import Path
import numpy as np


def main():
    p = Path("data/ckm_from_grams.json")
    if not p.exists():
        print("ERROR: data/ckm_from_grams.json not found. Run scripts/ckm_from_grams.py first.")
        return 1

    d = json.loads(p.read_text(encoding="utf-8"))
    overlap = np.array(d["overlap_matrix"], dtype=float)
    exp = np.array(d.get("experimental", []), dtype=float)

    diff = overlap - exp
    frob = float(np.linalg.norm(diff))
    max_abs = float(np.max(np.abs(diff)))
    mean_abs = float(np.mean(np.abs(diff)))
    row_rms = [float(np.sqrt(np.mean((overlap[i] - exp[i]) ** 2))) for i in range(3)]

    report = {
        "frobenius_diff": frob,
        "max_abs_diff": max_abs,
        "mean_abs_diff": mean_abs,
        "row_rms": row_rms,
        "overlap": overlap.tolist(),
        "experimental": exp.tolist(),
    }

    out = Path("data/ckm_comparison.json")
    out.write_text(json.dumps(report, indent=2))
    print("Wrote data/ckm_comparison.json")
    print(f"Frobenius norm of difference: {frob:.6f}")
    print(f"Max abs diff: {max_abs:.6f}, Mean abs diff: {mean_abs:.6f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
