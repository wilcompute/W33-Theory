#!/usr/bin/env python3
"""Pass 4880 withdrawal tombstone for the cross-characteristic chart claim."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUTHORITATIVE = ROOT / "data" / "PART_W33_PASS4948_MODULAR_BOSE_MESNER_CORRECTION.json"
OUTPUT = ROOT / "data" / "PART_W33_PASS4880_SYMPLECTIC_CHART_CANONICAL_BASIS.json"


def main() -> int:
    audit = json.loads(AUTHORITATIVE.read_text())
    assert audit["status"] == "PASS"
    assert audit["characteristic_three"]["scheme_idempotent_ranks"] == [0, 1, 39, 40]
    assert audit["characteristic_three"]["rank_24_or_15_modular_scheme_idempotent_exists"] is False

    out = {
        "pass": 4880,
        "schema": "w33.pass4880.withdrawal_tombstone.v1",
        "status": "WITHDRAWN_BY_PASS4948",
        "surviving_statement": (
            "The marked double-six F2^6 chart is a useful finite coordinate system on its native binary carrier."
        ),
        "withdrawn_statement": (
            "The binary chart canonically splits the characteristic-three generalized block into modular rank-24 and rank-15 scheme sectors."
        ),
        "reason": (
            "No cross-characteristic map was constructed, and exhaustive enumeration "
            "of the F3 scheme algebra finds idempotent ranks only 0,1,39,40."
        ),
        "authoritative_certificate": AUTHORITATIVE.name,
        "boundary": (
            "No F2-to-F3 splitting or canonical quadratic-Hom basis follows from the chart alone."
        ),
    }
    OUTPUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print("Pass 4880 withdrawal tombstone: status=WITHDRAWN_BY_PASS4948")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
