#!/usr/bin/env python3
"""Pass 1194: explicit central Wedderburn projectors for the 1952 residual."""
from __future__ import annotations

from fractions import Fraction
import hashlib
import json
from pathlib import Path

from w33_pass1135_cubic_kernel_decomposition import ATLAS, CLASS_SIZES, IRR
from w33_pass1188_exact_kernel_residual_wedderburn import RESIDUAL

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass1194_residual_central_idempotents.json"
GROUP_ORDER = 51840


def fraction_text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def main() -> dict:
    rows = {name: (degree, tuple(character)) for degree, character, _, name in IRR}
    names = tuple(RESIDUAL)
    assert set(names) <= set(rows)

    orthogonality = []
    for left in names:
        _, chil = rows[left]
        for right in names:
            _, chir = rows[right]
            inner_numerator = sum(
                int(size) * int(a) * int(b)
                for size, a, b in zip(CLASS_SIZES, chil, chir)
            )
            expected = GROUP_ORDER if left == right else 0
            assert inner_numerator == expected
            if left <= right:
                orthogonality.append({"pair": [left, right], "inner_product": inner_numerator // GROUP_ORDER})

    projectors = []
    total_coefficients = [Fraction(0) for _ in ATLAS]
    for name in names:
        degree, character = rows[name]
        expected_degree, multiplicity = RESIDUAL[name]
        assert degree == expected_degree
        coefficients = [Fraction(degree * value, GROUP_ORDER) for value in character]
        total_coefficients = [a + b for a, b in zip(total_coefficients, coefficients)]
        numerator_vector = [degree * value for value in character]
        projectors.append({
            "irrep": name,
            "degree": degree,
            "multiplicity": multiplicity,
            "residual_rank": degree * multiplicity,
            "commutant_block": f"M_{multiplicity}(Q)",
            "central_idempotent_formula": f"e_{name} = ({degree}/51840) * sum_C chi_{name}(C) K_C",
            "class_sum_coefficients": {
                ATLAS[i][0]: fraction_text(coefficients[i])
                for i in range(len(ATLAS)) if coefficients[i]
            },
            "denominator_cleared": {
                "common_denominator": GROUP_ORDER,
                "numerators_in_atlas_order": numerator_vector,
                "sha256": hashlib.sha256(json.dumps(numerator_vector, separators=(",", ":")).encode()).hexdigest(),
            },
        })

    residual_dimension = sum(item[0] * item[1] for item in RESIDUAL.values())
    commutant_dimension = sum(item[1] ** 2 for item in RESIDUAL.values())
    assert residual_dimension == 1952
    assert commutant_dimension == 1109
    assert len(projectors) == 10
    assert sum(p["residual_rank"] for p in projectors) == 1952

    result = {
        "schema": "w33.pass1194.residual_central_idempotents.v1",
        "status": "PASS",
        "headline": "The 1952 residual has ten explicit rational central idempotents and commutant algebra of dimension 1109.",
        "atlas_class_order": [row[0] for row in ATLAS],
        "residual_dimension": residual_dimension,
        "center_dimension": len(projectors),
        "commutant_dimension": commutant_dimension,
        "wedderburn_commutant": " ⊕ ".join(f"M_{multiplicity}(Q)" for _, multiplicity in RESIDUAL.values()),
        "projectors": projectors,
        "residual_central_projector": {
            "formula": "P_res = sum_chi e_chi over the ten residual species",
            "class_sum_coefficients": {
                ATLAS[i][0]: fraction_text(value)
                for i, value in enumerate(total_coefficients) if value
            },
        },
        "orthogonality_certificate": orthogonality,
        "checks": {
            "ten_isotypic_blocks": len(projectors) == 10,
            "residual_rank_1952": sum(p["residual_rank"] for p in projectors) == 1952,
            "commutant_dimension_1109": commutant_dimension == 1109,
            "character_rows_orthonormal": all(item["inner_product"] == (1 if item["pair"][0] == item["pair"][1] else 0) for item in orthogonality),
        },
        "boundary": "These are canonical central/isotypic projectors. Matrix units inside each multiplicity block require a noncanonical choice of copy basis and are intentionally not claimed.",
    }
    assert all(result["checks"].values())
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("PASS 1194 residual central idempotents=10 commutant=1109")
    return result


if __name__ == "__main__":
    main()
