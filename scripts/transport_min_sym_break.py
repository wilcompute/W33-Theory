"""Generate minimally symmetry-broken CNF variants by fixing first-k reps.

This helper exports a base CNF (no seed) then produces copies with unit
clauses that fix the first `k` representative indices to all combinations
of branch labels (limited by max_jobs). It is useful to search for
solutions that break symmetry only on a small set of orbit representatives.

Run inside the repo venv:
  python scripts/transport_min_sym_break.py --k 2 --max_jobs 20
"""

from __future__ import annotations

import argparse
import itertools
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
DATA = ROOT / "data"


def run_cmd(cmd: List[str]) -> None:
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\nstdout:\n{out}\nstderr:\n{err}")


def export_base_cnf(out_fn: Path) -> Path:
    cmd = [sys.executable, str(SCRIPTS / "transport_csp_cnf_export.py"), "--out", str(out_fn), "--seeds", ""]
    print("Exporting base CNF to", out_fn)
    run_cmd(cmd)
    # exporter should write the file exactly as out_fn
    if not out_fn.exists():
        raise FileNotFoundError("Base CNF not found: " + str(out_fn))
    return out_fn


def append_unit_clauses(base_cnf: Path, combos: List[List[int]], per_cell: int, out_dir: Path) -> List[Path]:
    out_paths = []
    with base_cnf.open("r", encoding="utf-8") as fh:
        header = []
        body = []
        for line in fh:
            if line.startswith("p cnf") or line.startswith("c "):
                header.append(line)
            else:
                body.append(line)

    for idx, combo in enumerate(combos):
        fname = out_dir / f"transport_symbreak_k{len(combo)}_job{idx}.cnf"
        with fname.open("w", encoding="utf-8") as fh:
            fh.writelines(header)
            fh.writelines(body)
            # append unit clauses for rep indices 0..k-1
            for rep_i, label in enumerate(combo):
                var = rep_i * per_cell + label + 1
                fh.write(f"{var} 0\n")
        out_paths.append(fname)
    return out_paths


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--k", type=int, default=1, help="number of reps to fix (first k reps)")
    parser.add_argument("--per_cell", type=int, default=3)
    parser.add_argument("--max_jobs", type=int, default=100, help="limit number of generated jobs")
    parser.add_argument("--out_dir", default=str(DATA))
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    base_cnf = out_dir / "transport_base.cnf"
    export_base_cnf(base_cnf)

    # generate all combos of per_cell labels for k reps
    all_combos = list(itertools.product(range(args.per_cell), repeat=args.k))
    if len(all_combos) > args.max_jobs:
        print(f"Truncating {len(all_combos)} combos to max_jobs={args.max_jobs}")
        combos = all_combos[: args.max_jobs]
    else:
        combos = all_combos

    out_paths = append_unit_clauses(base_cnf, combos, args.per_cell, out_dir)
    manifest = {"generated": [str(p) for p in out_paths], "count": len(out_paths)}
    manifest_path = out_dir / "transport_symbreak_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
