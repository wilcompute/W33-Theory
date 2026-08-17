#!/usr/bin/env python3
"""Pass 4879 correction tombstone for the dual-code covering radius.

The historical lower bound 10 used a nonexistent covering-radius/minimum-
distance duality. Pass 4948 replaces it with the exact sphere-volume crossing
and the syndrome-basis ceiling: 6 <= rho(K^perp) <= 36.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUTHORITATIVE = ROOT / "data" / "PART_W33_PASS4948_MODULAR_BOSE_MESNER_CORRECTION.json"
OUTPUT = ROOT / "data" / "PART_W33_PASS4879_DUAL_CODE_COVERING_RADIUS.json"


def main() -> int:
    audit = json.loads(AUTHORITATIVE.read_text())
    assert audit["status"] == "PASS"
    assert audit["corrected_finite_values"]["dual_radius_interval"] == [6, 36]
    checks = audit["checks"]
    assert checks["sphere_covering_lower_bound_is_6"]
    assert checks["syndrome_basis_upper_bound_is_36"]

    out = {
        "pass": 4879,
        "schema": "w33.pass4879.correction_tombstone.v1",
        "status": "CORRECTED_BY_PASS4948",
        "code": "K^perp=[360,324,3]_2",
        "rho_interval": [6, 36],
        "lower_bound": (
            "The Hamming-ball volume through radius 5 is below 2^36, so radius "
            "at most 5 cannot cover all syndromes."
        ),
        "upper_bound": (
            "Thirty-six independent parity-check columns form a syndrome basis, "
            "so every syndrome has a representative of weight at most 36."
        ),
        "withdrawn_statement": (
            "rho(K^perp)>=ceil(d(K)/2)=10; no such general lower-bound duality was established."
        ),
        "authoritative_certificate": AUTHORITATIVE.name,
        "boundary": (
            "Only 6<=rho(K^perp)<=36 is certified. The exact dual covering radius "
            "is not determined, and this is separate from the primal-code radius."
        ),
    }
    OUTPUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print("Pass 4879 correction tombstone: rho(K^perp) in [6,36]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
