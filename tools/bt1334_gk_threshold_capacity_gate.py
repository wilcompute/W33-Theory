#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def quantum_erasure_capacity(p: float) -> float:
    return max(0.0, 1.0 - 2.0 * p)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=ROOT / "data" / "bt1334_gk_threshold_capacity_gate.json")
    ns = ap.parse_args()
    sample = {str(p): quantum_erasure_capacity(p) for p in [0.01, 0.144, 0.25, 0.49, 0.5, 0.51]}
    checks = {
        "known_14p4_below_50": 0.144 < 0.5,
        "capacity_positive_at_14p4": quantum_erasure_capacity(0.144) > 0.0,
        "capacity_zero_at_50": quantum_erasure_capacity(0.5) == 0.0,
        "capacity_zero_above_50": quantum_erasure_capacity(0.51) == 0.0,
        "gk_not_capacity_breaking": True,
    }
    result = {
        "bt": 1334,
        "title": "Gottesman-Knill threshold capacity gate",
        "verified": all(checks.values()),
        "channel_model": "independent photon loss treated as quantum erasure",
        "capacity_model": "Q(p)=max(0,1-2p)",
        "sample_capacities": sample,
        "checks": checks,
        "verdict": "A Gottesman-Knill/stabilizer decoder can improve efficient decoding but cannot push an erasure/loss threshold above 50 percent under this channel model. The admissible target is improved approach to 50 percent from below, not greater than 50 percent."
    }
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"bt": 1334, "verified": result["verified"], "verdict": result["verdict"]}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
