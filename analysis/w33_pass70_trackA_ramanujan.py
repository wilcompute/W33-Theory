"""Pass 70 Track A: W33 Ramanujan impossibility witness.

Computes the explicit non-Ramanujan excess for the claimed W33/360-vertex
cheap-channel spectrum and writes a machine-readable witness.
"""
from __future__ import annotations

import json
import math
from pathlib import Path


def main() -> None:
    d = 8
    lambda2 = (1 + math.sqrt(97)) / 2
    ramanujan_bound = 2 * math.sqrt(d - 1)
    delta = lambda2 - ramanujan_bound

    payload = {
        "track": "A",
        "title": "W33 Ramanujan impossibility theorem witness",
        "degree": d,
        "lambda2": lambda2,
        "ramanujan_bound": ramanujan_bound,
        "delta": delta,
        "is_ramanujan": lambda2 <= ramanujan_bound,
        "minimal_polynomial": "x^2 - x - 24",
        "quadratic_fields": ["Q(sqrt(97))", "Q(sqrt(7))"],
        "claim": "Any 8-regular graph with second eigenvalue (1+sqrt(97))/2 violates the Ramanujan bound.",
    }

    out = Path("w33_pass70_trackA_ramanujan.json")
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
