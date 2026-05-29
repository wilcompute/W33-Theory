#!/usr/bin/env python3
"""
Prepare a SLURM CNF bundle for transport CSP seeds 0..127 with strong/full lex-leader.

This is a convenience wrapper around scripts/transport_job_generator.py that
preconfigures the common options operators want for farm submission.

Run locally inside the repo venv.

Usage:
  python scripts/prepare_transport_slurm_bundle_full.py

"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = ROOT / ".venv" / "Scripts" / "python.exe"
if not PY.exists():
    PY = Path("python")

SCRIPT = ROOT / "scripts" / "transport_job_generator.py"
OUT_DIR = ROOT / "data"

def main():
    args = [
        str(PY),
        str(SCRIPT),
        "--seeds", "0-127",
        "--time_limit", "600",
        "--workers", "8",
        "--slurm",
        "--bundle",
        "--lexleader-strong",
        "--lexleader-full",
        "--lexleader-prefix-length", "0",
        "--out_dir", str(OUT_DIR),
    ]
    print("Running:", " ".join(args))
    try:
        subprocess.check_call(args)
    except subprocess.CalledProcessError as exc:
        print("transport_job_generator failed:", exc)
        sys.exit(2)
    print("Bundle generation complete. Inspect data/ for the bundle and manifest.")

if __name__ == '__main__':
    main()
