#!/usr/bin/env python3
"""Deterministic replay runner for the corrected Pass5699--5703 packet.

The five Python sources are the only certificate owners.  The q=5 GAP file in
this packet is an executable tombstone that redirects to Pass5667--5674; it is
not a sixth producer and therefore is not replayed here.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = [
    "analysis/w33_pass5699_tower_artin_L_factorization.py",
    "analysis/w33_pass5700_girth_cycle_group_order_identity.py",
    "analysis/w33_pass5701_exact_psd_ramanujan_certificates.py",
    "analysis/w33_pass5702_kestent_mckay_equidistribution.py",
    "analysis/w33_pass5703_w39_independence_replication.py",
]


def main() -> None:
    for script in SCRIPTS:
        print(f"=== {script} ===", flush=True)
        subprocess.run([sys.executable, str(ROOT / script)], cwd=ROOT, check=True)
    print("PASS5699_5703_CORRECTED_REPLAY_OK", flush=True)


if __name__ == "__main__":
    main()
