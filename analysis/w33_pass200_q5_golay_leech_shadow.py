#!/usr/bin/env python3
"""Thin launcher for the GAP-owned corrected Pass 200 certificate."""

from __future__ import annotations

from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
GAP_CERTIFICATE = ROOT / "analysis" / "w33_pass200_q5_golay_leech_shadow.g"


def main() -> int:
    completed = subprocess.run(
        ["gap", "-q", str(GAP_CERTIFICATE)],
        cwd=ROOT,
        check=False,
    )
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
