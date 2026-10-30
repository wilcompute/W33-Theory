#!/usr/bin/env python3
"""
TOE phase diagram postprocess (v5-style): critical boundary + symmetry reselection.

This mirrors the "v5 report" concept from More New Work (v3p48), but runs directly
on the reproducible output of `tools/toe_phase_diagram.py`.

Definitions (heuristic, but deterministic):
  - ordered cell: (best_charge.mean_drift <= median drift) AND
                  (holonomy.union_weighted_entropy_nats <= median holonomy entropy)
  - critical sigma for a fixed firewall row: midpoint between the last ordered sigma
    and the first disordered sigma (if such a transition exists)
  - symmetry reselection index at a cell: 1 - mean cosine similarity between the
    optimized best_charge coefficient vector and its grid neighbors

Outputs:
  - artifacts/toe_phase_diagram_v5_summary.json
  - artifacts/toe_phase_diagram_v5_report.md
  - optional PPM heatmaps (no matplotlib dependency)
"""

from __future__ import annotations

import argparse
import json
from math import sqrt
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def _load_json(path: Path) -> Dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, data: Dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")


def _write_md(path: Path, lines: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def _write_ppm_heatmap(path: Path, grid: np.ndarray, *, invert: bool = False) -> None:
    if grid.ndim != 2:
        raise ValueError("Expected 2D grid")
    h, w = grid.shape
    finite = grid[np.isfinite(grid)]
    if finite.size == 0:
        vmin, vmax = 0.0, 1.0
    else:
        vmin = float(np.min(finite))
        vmax = float(np.max(finite))
    denom = (vmax - vmin) if vmax > vmin else 1.0

    def scale(x: float) -> int:
        if not np.isfinite(x):
            return 0
        t = (float(x) - vmin) / denom
        if invert:
            t = 1.0 - t
        t = min(1.0, max(0.0, t))
        return int(round(255 * t))

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="ascii") as f:
        f.write(f"P3\n{w} {h}\n255\n")
        for i in range(h):
            row = []
            for j in range(w):
                g = scale(float(grid[i, j]))
                row.append(f"{g} {g} {g}")
            f.write(" ".join(row) + "\n")


def _cosine(a: np.ndarray, b: np.ndarray) -> float:
    na = float(np.linalg.norm(a))
    nb = float(np.linalg.norm(b))
    if na == 0.0 or nb == 0.0:
        return 0.0
    return float(np.dot(a, b) / (na * nb))


def main(argv: Sequence[str] | None = None) -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--in-json",
        type=Path,
        default=ROOT / "artifacts" / "toe_phase_diagram_summary.json",
    )
    p.add_argument(
        "--out-json",
        type=Path,
        default=ROOT / "artifacts" / "toe_phase_diagram_v5_summary.json",
    )
    p.add_argument(
        "--out-md",
        type=Path,
        default=ROOT / "artifacts" / "toe_phase_diagram_v5_report.md",
    )
    p.add_argument("--write-ppm", action="store_true")
    args = p.parse_args(list(argv) if argv is not None else None)

    inp = _load_json(args.in_json)
    fw_vals = [float(x) for x in inp["grid"]["firewall_strength"]]
    sig_vals = [float(x) for x in inp["grid"]["phase_noise_sigma"]]
    cells = inp["cells"]
    if not (isinstance(cells, list) and cells and isinstance(cells[0], list)):
        raise RuntimeError("Invalid input: cells grid missing")

    n_fw = len(fw_vals)
    n_sig = len(sig_vals)

    drift = np.zeros((n_fw, n_sig), dtype=float)
    hol = np.zeros((n_fw, n_sig), dtype=float)
    coeffs = np.zeros((n_fw, n_sig, 6), dtype=float)
    for i in range(n_fw):
        row = cells[i]
        for j in range(n_sig):
            cell = row[j]
            drift[i, j] = float(cell["best_charge"]["mean_drift"])
            hol[i, j] = float(cell["holonomy"]["union_weighted_entropy_nats"])
            coeffs[i, j] = np.array(cell["best_charge"]["coeffs"], dtype=float)

    drift_med = float(np.median(drift))
    hol_med = float(np.median(hol))
    ordered = np.logical_and(drift <= drift_med, hol <= hol_med)

    # Critical sigma per fw row.
    critical: Dict[str, float] = {}
    for i, fw in enumerate(fw_vals):
        row = ordered[i]
        if not np.any(row):
            critical[str(fw)] = 0.0
            continue
        if np.all(row):
            critical[str(fw)] = float(sig_vals[-1])
            continue
        last_ord = int(np.max(np.nonzero(row)[0]))
        first_dis = int(last_ord + 1)
        if first_dis >= len(sig_vals):
            critical[str(fw)] = float(sig_vals[-1])
            continue
        critical[str(fw)] = float(0.5 * (sig_vals[last_ord] + sig_vals[first_dis]))

    # Symmetry reselection index: neighbor dissimilarity of best-charge direction.
    reselection = np.zeros((n_fw, n_sig), dtype=float)
    for i in range(n_fw):
        for j in range(n_sig):
            v = coeffs[i, j]
            ds = []
            for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                ii, jj = i + di, j + dj
                if 0 <= ii < n_fw and 0 <= jj < n_sig:
                    w = coeffs[ii, jj]
                    c = abs(_cosine(v, w))  # sign-invariant
                    ds.append(1.0 - c)
            reselection[i, j] = float(np.mean(ds)) if ds else 0.0

    out: Dict[str, object] = {
        "thresholds": {"drift_median": drift_med, "holonomy_entropy_median": hol_med},
        "critical_sigma_by_firewall": critical,
        "notes": [
            "Ordered region defined as (drift <= median drift) AND (holonomy entropy <= median holonomy entropy).",
            "Critical sigma per firewall row defined as the midpoint between the last ordered sigma bin and the first disordered bin.",
            "Symmetry reselection index is 1 - mean cosine similarity of best-charge coeffs with neighboring grid points (absolute cosine).",
        ],
    }
    _write_json(args.out_json, out)

    lines: List[str] = []
    lines.append("# TOE Phase Diagram v5 (postprocess)")
    lines.append("")
    lines.append("## Thresholds")
    lines.append(f"- drift median threshold: `{drift_med:.4e}`")
    lines.append(f"- holonomy entropy median threshold: `{hol_med:.4e}`")
    lines.append("")
    lines.append("## Critical boundary (σ*)")
    for fw in fw_vals:
        lines.append(f"- firewall {fw:.2f}: σ* ≈ {critical[str(fw)]:.3f}")
    lines.append("")
    lines.append("## Outputs")
    lines.append(f"- summary JSON: `{args.out_json}`")
    if args.write_ppm:
        lines.append(
            "- heatmaps: `artifacts/phase_diagram_ordered_mask.ppm`, `artifacts/phase_diagram_symmetry_reselection.ppm`"
        )
    _write_md(args.out_md, lines)

    if args.write_ppm:
        out_dir = args.out_json.parent
        _write_ppm_heatmap(
            out_dir / "phase_diagram_ordered_mask.ppm",
            ordered.astype(float),
            invert=False,
        )
        _write_ppm_heatmap(
            out_dir / "phase_diagram_symmetry_reselection.ppm", reselection, invert=True
        )

    print(f"Wrote {args.out_json}")
    print(f"Wrote {args.out_md}")


if __name__ == "__main__":
    main()
