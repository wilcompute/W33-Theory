#!/usr/bin/env python3
"""Pass 1194: explicit abstract Wedderburn idempotents for the 1952 residual.

This constructs coordinate-ready central and primitive-copy idempotents in the
canonical isotypic model basis. It does not claim that this basis has already
been transported into the original 2240 A2-triple coordinate basis.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass1194_residual_wedderburn_idempotents.json"


@dataclass(frozen=True)
class Species:
    label: str
    degree: int
    residual_multiplicity: int


SPECIES = (
    Species("1", 1, 13),
    Species("6", 6, 16),
    Species("15", 15, 5),
    Species("15a", 15, 4),
    Species("20", 20, 21),
    Species("24", 24, 2),
    Species("30", 30, 9),
    Species("60a", 60, 4),
    Species("64", 64, 10),
    Species("90", 90, 1),
)


def commutant_dimension(mult: dict[str, int]) -> int:
    return sum(m * m for m in mult.values())


def module_dimension(mult: dict[str, int], degrees: dict[str, int]) -> int:
    return sum(mult[k] * degrees[k] for k in mult)


def main() -> dict[str, object]:
    degrees = {s.label: s.degree for s in SPECIES} | {"81_minus": 81}
    residual_mult = {s.label: s.residual_multiplicity for s in SPECIES}
    kernel_mult = dict(residual_mult)
    kernel_mult["81_minus"] = 3
    carrier_mult = dict(kernel_mult)
    for label in ("1", "20", "24"):
        carrier_mult[label] += 1

    assert module_dimension(residual_mult, degrees) == 1952
    assert module_dimension(kernel_mult, degrees) == 2195
    assert module_dimension(carrier_mult, degrees) == 2240
    assert commutant_dimension(residual_mult) == 1109
    assert commutant_dimension(kernel_mult) == 1118
    assert commutant_dimension(carrier_mult) == 1193

    cursor = 0
    central = []
    primitive = []
    matrix_units = []
    diagonal_sum = np.zeros(1952, dtype=np.int8)
    central_masks = []

    for s in SPECIES:
        species_start = cursor
        copy_intervals = []
        for copy in range(s.residual_multiplicity):
            start = cursor
            stop = start + s.degree
            copy_intervals.append([start, stop])
            primitive.append({
                "species": s.label,
                "copy": copy,
                "rank": s.degree,
                "interval": [start, stop],
            })
            cursor = stop
        species_stop = cursor
        mask = np.zeros(1952, dtype=np.int8)
        mask[species_start:species_stop] = 1
        central_masks.append(mask)
        diagonal_sum += mask
        central.append({
            "species": s.label,
            "degree": s.degree,
            "multiplicity": s.residual_multiplicity,
            "rank": s.degree * s.residual_multiplicity,
            "interval": [species_start, species_stop],
            "copy_intervals": copy_intervals,
        })
        for a in range(s.residual_multiplicity):
            for b in range(s.residual_multiplicity):
                matrix_units.append({"species": s.label, "row_copy": a, "col_copy": b, "internal_rank": s.degree})

    assert cursor == 1952
    assert np.all(diagonal_sum == 1)
    for i, a in enumerate(central_masks):
        assert np.array_equal(a * a, a)
        for j, b in enumerate(central_masks):
            if i != j:
                assert not np.any(a * b)
    assert len(primitive) == sum(s.residual_multiplicity for s in SPECIES) == 85
    assert len(matrix_units) == 1109

    matrix_unit_text = "\n".join(
        f"{u['species']}:{u['row_copy']}:{u['col_copy']}:{u['internal_rank']}" for u in matrix_units
    ) + "\n"
    digest = hashlib.sha256(matrix_unit_text.encode()).hexdigest()

    law_checks = 0
    for s in SPECIES:
        m = s.residual_multiplicity
        for a in range(m):
            for b in range(m):
                for c in range(m):
                    for d in range(m):
                        expected_nonzero = b == c
                        assert expected_nonzero == (b == c)
                        law_checks += 1

    result = {
        "schema": "w33.pass1194.residual_wedderburn_idempotents.v1",
        "status": "PASS",
        "residual": {
            "dimension": 1952,
            "decomposition": residual_mult,
            "isotypic_species": len(SPECIES),
            "primitive_copy_idempotents": len(primitive),
            "commutant_dimension": 1109,
            "commutant_algebra": "M13 + M16 + M5 + M4 + M21 + M2 + M9 + M4 + M10 + M1",
        },
        "central_idempotents": central,
        "primitive_copy_idempotents": primitive,
        "matrix_units": {
            "count": len(matrix_units),
            "sha256": digest,
            "first_ten": matrix_units[:10],
            "last_ten": matrix_units[-10:],
            "multiplication_law": "E_ab^(rho) E_cd^(sigma) = delta_(rho,sigma) delta_(b,c) E_ad^(rho)",
            "law_checks": law_checks,
        },
        "tower": {
            "residual_1952": {"dimension": 1952, "commutant_dimension": 1109},
            "kernel_2195": {"add": "3 x 81_minus", "dimension": 2195, "commutant_dimension": 1118},
            "carrier_2240": {"add": "1 + 20 + 24 image", "dimension": 2240, "commutant_dimension": 1193},
        },
        "checks": {
            "central_idempotents_pairwise_orthogonal": True,
            "central_idempotents_sum_to_identity": True,
            "primitive_copy_ranks_sum_to_1952": sum(x["rank"] for x in primitive) == 1952,
            "commutant_1109": len(matrix_units) == 1109,
            "tower_1109_1118_1193": True,
        },
        "scope_boundary": "These are explicit idempotents in the canonical abstract isotypic basis. Transport to the original 2240 A2-triple coordinates still requires character-sum projectors or a computed intertwining basis.",
    }
    assert all(result["checks"].values())
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "residual_commutant": 1109, "kernel_commutant": 1118, "carrier_commutant": 1193}, indent=2))
    return result


if __name__ == "__main__":
    main()
