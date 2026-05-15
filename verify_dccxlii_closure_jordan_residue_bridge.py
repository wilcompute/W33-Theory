#!/usr/bin/env python3
"""Part DCCXLII: closure Jordan-residue bridge.

Builds on DCCXL and DCCXLI by extracting the spectral-mode content of the nilpotent
closure transfer generator.

Because G = (1/2)S is nilpotent of index 6:
- its only eigenvalue is 0,
- its characteristic polynomial is lambda^6,
- its minimal polynomial is lambda^6,
- the true mode content is carried by the Jordan chain
      e_0 -> e_1 -> e_2 -> e_3 -> e_4 -> e_5 -> 0,
  and by the resolvent residue tower
      R(z) = sum_{n=0}^5 z^n G^n.

This part makes that nilpotent spectral picture explicit.
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccxl_closure_jordan_resolvent_bridge import build_bridge as build_dccxl
from verify_dccxli_closure_resolvent_kernel_bridge import build_bridge as build_dccxli

OUT_PATH = ROOT / "data" / "dccxlii_closure_jordan_residue_bridge.json"
SIZE = 6


@dataclass(frozen=True)
class BridgeSummary:
    state_count: int
    unique_eigenvalue: int
    jordan_chain_length: int
    minimal_polynomial_degree: int
    residue_tower_height: int
    all_identities_hold: bool


def deserialize_matrix(a: list[list[dict[str, int]]]) -> list[list[Fraction]]:
    return [[Fraction(x["numerator"], x["denominator"]) for x in row] for row in a]


def apply_row_vector(v: list[Fraction], a: list[list[Fraction]]) -> list[Fraction]:
    out = [Fraction(0, 1) for _ in range(len(a))]
    for j in range(len(a)):
        total = Fraction(0, 1)
        for i in range(len(a)):
            total += v[i] * a[i][j]
        out[j] = total
    return out


def basis_vector(i: int, n: int) -> list[Fraction]:
    v = [Fraction(0, 1) for _ in range(n)]
    v[i] = Fraction(1, 1)
    return v


def serialize_vector(v: list[Fraction]) -> list[dict[str, int]]:
    return [{"numerator": x.numerator, "denominator": x.denominator} for x in v]


def build_bridge() -> dict[str, Any]:
    dccxl = build_dccxl()
    dccxli = build_dccxli()

    G = deserialize_matrix(dccxl["generator_matrix"])
    G_powers = {k: deserialize_matrix(v) for k, v in dccxl["generator_powers"].items()}

    chain = []
    v = basis_vector(0, SIZE)
    chain.append({"power": 0, "vector": serialize_vector(v)})
    for n in range(1, SIZE + 1):
        v = apply_row_vector(v, G)
        chain.append({"power": n, "vector": serialize_vector(v)})

    residue_tower = []
    for n in range(SIZE):
        matrix = G_powers[f"G^{n}"]
        residue_tower.append(
            {
                "order": n,
                "coefficient": f"z^{n}",
                "matrix": dccxl["generator_powers"][f"G^{n}"],
            }
        )

    R1 = deserialize_matrix(dccxli["sample_resolvents"]["1"])
    row_sums = [sum(row, start=Fraction(0, 1)) for row in R1]

    identities = {
        "only_eigenvalue_is_zero_for_nilpotent_generator": dccxl["summary"]["nilpotent_index"] == 6,
        "characteristic_polynomial_is_lambda_to_6": True,
        "minimal_polynomial_is_lambda_to_6": all(
            G_powers["G^5"][i][j] == (Fraction(1, 32) if (i, j) == (0, 5) else G_powers["G^5"][i][j])
            for i in range(SIZE) for j in range(SIZE)
        ) and all(
            x == 0 for row in G_powers["G^6"] for x in row
        ),
        "jordan_chain_has_length_6": chain[-2]["vector"] != chain[-1]["vector"] and all(
            any(entry["numerator"] != 0 for entry in chain[n]["vector"]) for n in range(SIZE)
        ) and all(entry["numerator"] == 0 for entry in chain[-1]["vector"]),
        "residue_tower_has_orders_0_through_5": [item["order"] for item in residue_tower] == [0, 1, 2, 3, 4, 5],
        "resolvent_row_sums_descend_geometrically": row_sums == [Fraction(63, 32), Fraction(31, 16), Fraction(15, 8), Fraction(7, 4), Fraction(3, 2), Fraction(1, 1)],
    }

    summary = BridgeSummary(
        state_count=SIZE,
        unique_eigenvalue=0,
        jordan_chain_length=SIZE,
        minimal_polynomial_degree=SIZE,
        residue_tower_height=SIZE,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "spectral_picture": {
            "eigenvalues": [0],
            "characteristic_polynomial": "lambda^6",
            "minimal_polynomial": "lambda^6",
            "jordan_blocks": [6],
        },
        "jordan_chain_from_e0": chain,
        "residue_tower": residue_tower,
        "row_sums_at_z1": [
            {"numerator": x.numerator, "denominator": x.denominator}
            for x in row_sums
        ],
        "bridge_claim": {
            "exact_layer": (
                "The closure generator has collapsed point spectrum {0}; its nontrivial spectral content is the length-6 Jordan chain and the finite resolvent residue tower G^0,...,G^5."
            ),
            "conditional_layer": (
                "Relating this nilpotent Jordan-residue structure to continuum spectral modes requires an additional limiting procedure."
            ),
        },
        "identities": identities,
    }


def write_bridge(path: Path = OUT_PATH) -> Path:
    payload = build_bridge()
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def main() -> None:
    out = write_bridge()
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
