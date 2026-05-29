"""Automated runner: try pysat -> OR-Tools -> CNF export and instruct user.

This wrapper calls the existing `transport_solve_harness.py` with a preferred
sequence of modes. It returns the path to any resulting JSON assignment file
or raises if none produced.

Usage:
  python scripts/transport_automated_runner.py --seed 0 --time_limit 300
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Optional


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def run_cmd(cmd):
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = proc.communicate()
    return proc.returncode, out, err


def try_mode(mode: str, seed: int, time_limit: int, workers: int) -> Optional[Path]:
    cmd = [sys.executable, str(SCRIPTS / "transport_solve_harness.py"), "--seed", str(seed), "--mode", mode, "--time_limit", str(time_limit), "--workers", str(workers)]
    rc, out, err = run_cmd(cmd)
    print(out)
    if rc != 0:
        print(f"Mode {mode} failed: rc={rc}\nstderr={err}")
        return None
    # heuristics: look for expected output files
    if mode == "pysat":
        path = ROOT / "data" / f"transport_csp_pysat_seed{seed}.json"
        if path.exists():
            return path
    if mode == "or":
        path = ROOT / "data" / f"transport_csp_or_tools_seed{seed}.json"
        if path.exists():
            return path
    return None


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--time_limit", type=int, default=300)
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()

    seed = args.seed
    print("Attempting pysat flow...")
    res = try_mode("pysat", seed, args.time_limit, args.workers)
    if res:
        print("Found result:", res)
        return

    print("Pysat failed or missing; trying OR-Tools flow...")
    res = try_mode("or", seed, args.time_limit, args.workers)
    if res:
        print("Found result:", res)
        return

    print("Both pysat and OR-Tools flows failed or produced no assignment. Exporting CNF for manual solve...")
    cmd = [sys.executable, str(SCRIPTS / "transport_csp_cnf_export.py"), "--out", str(ROOT / "data" / f"transport_seed{seed}.cnf"), "--seeds", str(seed)]
    rc, out, err = run_cmd(cmd)
    if rc != 0:
        print("CNF export failed:\n", out, err)
        raise SystemExit(1)
    print("Wrote CNF; run your preferred SAT solver on the produced file and then run the verifier:")
    print(f"python scripts/transport_result_verify.py data/<solver_result.json>")


if __name__ == "__main__":
    main()
