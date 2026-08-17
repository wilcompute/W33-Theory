#!/usr/bin/env python3
"""Pass 4878 correction tombstone, owned by the exact Pass-4948 audit.

The eigenvalue congruence ``2 == -4 (mod 3)`` survives. The historical
inference that the full modular adjacency algebra has dimension two, or that
this congruence causes the unrelated quadratic Hom dimension, does not.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUTHORITATIVE = ROOT / "data" / "PART_W33_PASS4948_MODULAR_BOSE_MESNER_CORRECTION.json"
OUTPUT = ROOT / "data" / "PART_W33_PASS4878_BOSE_MESNER_F3_COLLAPSE.json"


def main() -> int:
    audit = json.loads(AUTHORITATIVE.read_text())
    characteristic_three = audit["characteristic_three"]
    assert audit["status"] == "PASS"
    assert characteristic_three["bose_mesner_vector_space_dimension"] == 3
    assert characteristic_three["semisimple_quotient_dimension"] == 2
    assert characteristic_three["augmentation_layer_dimensions"] == [10, 19, 10]
    assert characteristic_three["rank_24_or_15_modular_scheme_idempotent_exists"] is False

    out = {
        "pass": 4878,
        "schema": "w33.pass4878.correction_tombstone.v1",
        "status": "CORRECTED_BY_PASS4948",
        "surviving_statement": (
            "The rational nontrivial eigenvalues 2 and -4 are congruent modulo 3, "
            "so the 39-dimensional nontrivial rational sector becomes a generalized "
            "characteristic-three block."
        ),
        "withdrawn_statements": [
            "The full F3 Bose-Mesner adjacency algebra has dimension two.",
            "The eigenvalue congruence causes dim Hom_PSp(Sym^2 H2,Q10)=2.",
            "A marked F2 chart canonically restores modular rank-24 and rank-15 scheme idempotents.",
        ],
        "authoritative_replacement": {
            "certificate": AUTHORITATIVE.name,
            "algebra_dimension": 3,
            "semisimple_quotient_dimension": 2,
            "minimal_polynomial": "x(x+1)^2",
            "augmentation_layers": [10, 19, 10],
            "scheme_idempotent_ranks": [0, 1, 39, 40],
        },
        "boundary": (
            "This legacy entry point is a fail-closed correction tombstone. It does "
            "not derive a quadratic Hom dimension or a cross-characteristic splitting."
        ),
    }
    OUTPUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print("Pass 4878 correction tombstone: status=CORRECTED_BY_PASS4948")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
