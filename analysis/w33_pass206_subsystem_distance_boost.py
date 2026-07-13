#!/usr/bin/env python3
"""Compatibility launcher for the GAP-owned Pass 206 withdrawal ledger."""

from __future__ import annotations

from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
GAP_CERTIFICATE = ROOT / "analysis" / "w33_pass206_subsystem_claim_withdrawal.g"


def main() -> int:
    completed = subprocess.run(
        ["gap", "-q", str(GAP_CERTIFICATE)],
        cwd=ROOT,
        check=False,
    )
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
