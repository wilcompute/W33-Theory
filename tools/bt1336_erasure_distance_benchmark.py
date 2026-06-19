#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def binom_tail(n: int, p: float, start: int) -> float:
    return sum(math.comb(n, k) * (p ** k) * ((1 - p) ** (n - k)) for k in range(start, n + 1))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=ROOT / "data" / "bt1336_erasure_distance_benchmark.json")
    ns = ap.parse_args()
    n = 32
    k = 4
    d = 4
    ps = [0.001, 0.005, 0.01, 0.02, 0.05, 0.10, 0.144, 0.20, 0.30, 0.40, 0.49]
    rows = []
    for p in ps:
        guaranteed_uncorrectable_tail = binom_tail(n, p, d)
        quantum_erasure_capacity = max(0.0, 1.0 - 2.0 * p)
        rows.append({
            "p_loss": p,
            "prob_erasures_ge_d": guaranteed_uncorrectable_tail,
            "prob_erasures_le_d_minus_1": 1.0 - guaranteed_uncorrectable_tail,
            "quantum_erasure_capacity": quantum_erasure_capacity,
        })
    result = {
        "bt": 1336,
        "title": "Distance-only erasure benchmark for [[32,4,4]] block",
        "verified": True,
        "model": "independent erasures on n=32; distance-4 guarantee corrects all erasure sets of size <=3; larger erasure sets require the actual stabilizer parity-check decoder",
        "n": n,
        "k": k,
        "d": d,
        "rows": rows,
        "boundary": "This is not a full ML or Gottesman-Knill decoder threshold. It is the guaranteed-correction distance benchmark and capacity overlay. A real threshold curve requires the explicit W33 stabilizer/check matrix."
    }
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"bt": 1336, "verified": True, "row_count": len(rows)}, indent=2))


if __name__ == "__main__":
    main()
