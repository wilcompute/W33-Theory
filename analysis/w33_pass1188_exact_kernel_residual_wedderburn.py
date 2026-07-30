#!/usr/bin/env python3
"""Pass 1188: recover the exact 1952-dimensional residual from Pass 1135.

This is a lightweight certificate for the exact character decomposition already
computed by the E8-root/W(E6) class-algebra pipeline.  It replaces the speculative
``1952 = 1920 + 32`` arithmetic split with the actual isotypic decomposition and
computes the corresponding Wedderburn/commutant dimensions.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass1188_exact_kernel_residual_wedderburn.json"

# Exact multiplicities from analysis/w33_pass1135_cubic_kernel_decomposition.py.
DOMAIN = {
    "1": (1, 14),
    "6": (6, 16),
    "15": (15, 5),
    "15a": (15, 4),
    "20": (20, 22),
    "24": (24, 3),
    "30": (30, 9),
    "60a": (60, 4),
    "64": (64, 10),
    "81_minus": (81, 3),
    "90": (90, 1),
}
IMAGE = {"1": (1, 1), "20": (20, 1), "24": (24, 1)}
KERNEL = {
    name: (degree, mult - IMAGE.get(name, (degree, 0))[1])
    for name, (degree, mult) in DOMAIN.items()
}
KERNEL = {name: pair for name, pair in KERNEL.items() if pair[1]}
RESIDUAL = {name: pair for name, pair in KERNEL.items() if name != "81_minus"}


def dimension(module: dict[str, tuple[int, int]]) -> int:
    return sum(degree * multiplicity for degree, multiplicity in module.values())


def commutant_dimension(module: dict[str, tuple[int, int]]) -> int:
    return sum(multiplicity * multiplicity for _, multiplicity in module.values())


def compact(module: dict[str, tuple[int, int]]) -> str:
    return " + ".join(
        f"{multiplicity}*{name}" for name, (_, multiplicity) in module.items()
    )


def main() -> dict:
    assert dimension(DOMAIN) == 2240
    assert dimension(IMAGE) == 45
    assert dimension(KERNEL) == 2195
    assert KERNEL["81_minus"] == (81, 3)
    assert dimension(RESIDUAL) == 1952
    assert "81_minus" not in RESIDUAL

    domain_comm = commutant_dimension(DOMAIN)
    image_comm = commutant_dimension(IMAGE)
    kernel_comm = commutant_dimension(KERNEL)
    residual_comm = commutant_dimension(RESIDUAL)

    assert domain_comm == 1193
    assert image_comm == 3
    assert kernel_comm == 1118
    assert residual_comm == 1109
    assert kernel_comm - residual_comm == 3**2

    result = {
        "schema": "w33.pass1188.exact_kernel_residual_wedderburn.v1",
        "status": "PASS",
        "source_of_truth": "analysis/w33_pass1135_cubic_kernel_decomposition.py",
        "domain": {
            "dimension": dimension(DOMAIN),
            "decomposition": compact(DOMAIN),
            "isotypic_species": len(DOMAIN),
            "commutant_dimension": domain_comm,
        },
        "cubic_image": {
            "dimension": dimension(IMAGE),
            "decomposition": compact(IMAGE),
            "multiplicity_free": True,
            "commutant_dimension": image_comm,
        },
        "cubic_kernel": {
            "dimension": dimension(KERNEL),
            "decomposition": compact(KERNEL),
            "isotypic_species": len(KERNEL),
            "commutant_dimension": kernel_comm,
        },
        "steinberg_block": {
            "irrep": "81_minus",
            "multiplicity": 3,
            "dimension": 243,
            "endomorphism_block": "M_3",
            "commutant_dimension": 9,
        },
        "residual_after_steinberg": {
            "dimension": dimension(RESIDUAL),
            "decomposition": compact(RESIDUAL),
            "isotypic_species": len(RESIDUAL),
            "commutant_dimension": residual_comm,
            "center_dimension": len(RESIDUAL),
        },
        "correction": {
            "rejected_unproved_split": "1952 = 1920 + 32",
            "reason": "Pass 1135 already determines the exact W(E6)-isotypic decomposition; dimension factorization is not module decomposition.",
        },
        "checks": {
            "domain_dimension_2240": dimension(DOMAIN) == 2240,
            "image_is_1_plus_20_plus_24": compact(IMAGE) == "1*1 + 1*20 + 1*24",
            "kernel_dimension_2195": dimension(KERNEL) == 2195,
            "steinberg_packet_243": 3 * 81 == 243,
            "residual_dimension_1952": dimension(RESIDUAL) == 1952,
            "domain_commutant_1193": domain_comm == 1193,
            "kernel_commutant_1118": kernel_comm == 1118,
            "residual_commutant_1109": residual_comm == 1109,
        },
    }
    assert all(result["checks"].values())
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("PASS 1188 residual=1952 commutant=1109")
    return result


if __name__ == "__main__":
    main()
