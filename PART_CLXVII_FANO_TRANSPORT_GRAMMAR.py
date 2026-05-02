#!/usr/bin/env python3
"""
PART CLXVII - Fano Transport Grammar
====================================

CLXVI built the Fano plane as the projective completion of the mod-12 wheel:

    affine J-cycle: {1,5,12,8}
    q-axis infinity: {3,6,9}

with affine coordinates

    1  -> (0,0)
    5  -> (1,0)
    12 -> (0,1)
    8  -> (1,1)

and directions at infinity

    3 -> horizontal q-direction
    6 -> vertical 2q-direction
    9 -> diagonal q^2-direction.

CLXVII turns this incidence geometry into a transport grammar.

The two horizontal affine lines have affine-pair product

    1*5 = 5,       12*8 = 96 = 5 mod 13.

So q-horizontal transport carries the threshold residue J=5.

The two diagonal affine lines have affine-pair product

    1*8 = 8,       5*12 = 60 = 8 mod 13.

So q^2-diagonal transport carries the carrier residue J^{-1}=8.

The two vertical affine lines are additive-inverse pairs

    1+12 = 0 mod 13,
    5+8  = 0 mod 13.

So 2q-vertical transport carries the rank/opposition involution.

Thus the Fano bridge is not only incidence: it is a transport grammar for
threshold, rank/opposition, and carrier motion.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parent

Q = 3
RANK_SEED = 2 * Q
Q2 = Q * Q
K = 12
PHI3 = 13
PHI4 = 10
PHI6 = 7
J = 5
J_INV = 8
HASHIMOTO_NORM = 11

AFFINE_POINTS = [1, J, K, J_INV]
INFINITY_POINTS = [Q, RANK_SEED, Q2]

FANO_LINES: Dict[str, Tuple[int, int, int]] = {
    "horizontal_y0": (1, J, Q),
    "horizontal_y1": (K, J_INV, Q),
    "vertical_x0": (1, K, RANK_SEED),
    "vertical_x1": (J, J_INV, RANK_SEED),
    "diagonal_main": (1, J_INV, Q2),
    "diagonal_shift": (J, K, Q2),
    "line_at_infinity": (Q, RANK_SEED, Q2),
}

DIRECTION_GROUPS = {
    "threshold_horizontal_q": ["horizontal_y0", "horizontal_y1"],
    "rank_vertical_2q": ["vertical_x0", "vertical_x1"],
    "carrier_diagonal_q2": ["diagonal_main", "diagonal_shift"],
    "q_axis_infinity": ["line_at_infinity"],
}


def mod13(x: int) -> int:
    return x % PHI3


def affine_pair(line: Tuple[int, int, int]) -> Tuple[int, int]:
    return tuple(p for p in line if p in AFFINE_POINTS)  # type: ignore[return-value]


@dataclass(frozen=True)
class TransportLine:
    name: str
    points: List[int]
    direction: int
    affine_pair: List[int]
    affine_pair_sum_mod13: int
    affine_pair_product_mod13: int
    total_sum_mod13: int
    total_product_mod13: int
    interpretation: str


def transport_lines() -> List[TransportLine]:
    interpretations = {
        "horizontal_y0": "unit-to-threshold transport with q at infinity",
        "horizontal_y1": "k-to-carrier transport with q at infinity",
        "vertical_x0": "unit-to-k opposition with 2q at infinity",
        "vertical_x1": "threshold-to-carrier opposition with 2q at infinity",
        "diagonal_main": "unit-to-carrier transport with q^2 at infinity",
        "diagonal_shift": "threshold-to-k transport with q^2 at infinity",
        "line_at_infinity": "q-axis closure / missing decimal axis",
    }
    rows = []
    for name, line in FANO_LINES.items():
        aff = list(affine_pair(line))
        direction = [p for p in line if p in INFINITY_POINTS][0]
        rows.append(
            TransportLine(
                name=name,
                points=list(line),
                direction=direction,
                affine_pair=aff,
                affine_pair_sum_mod13=mod13(sum(aff)) if aff else 0,
                affine_pair_product_mod13=mod13(aff[0] * aff[1]) if len(aff) == 2 else 0,
                total_sum_mod13=mod13(sum(line)),
                total_product_mod13=mod13(line[0] * line[1] * line[2]),
                interpretation=interpretations[name],
            )
        )
    return rows


@dataclass(frozen=True)
class DirectionTransport:
    direction_name: str
    direction_residue: int
    line_names: List[str]
    invariant: str
    value: str
    interpretation: str


def direction_transports() -> List[DirectionTransport]:
    by_name = {r.name: r for r in transport_lines()}
    return [
        DirectionTransport(
            direction_name="threshold_horizontal_q",
            direction_residue=Q,
            line_names=DIRECTION_GROUPS["threshold_horizontal_q"],
            invariant="affine-pair product",
            value=str(J),
            interpretation="q-horizontal transport preserves threshold residue J=5",
        ),
        DirectionTransport(
            direction_name="rank_vertical_2q",
            direction_residue=RANK_SEED,
            line_names=DIRECTION_GROUPS["rank_vertical_2q"],
            invariant="affine-pair sum",
            value="0 mod 13",
            interpretation="2q-vertical transport pairs additive inverses / opposition",
        ),
        DirectionTransport(
            direction_name="carrier_diagonal_q2",
            direction_residue=Q2,
            line_names=DIRECTION_GROUPS["carrier_diagonal_q2"],
            invariant="affine-pair product",
            value=str(J_INV),
            interpretation="q^2-diagonal transport preserves carrier residue J^{-1}=8",
        ),
        DirectionTransport(
            direction_name="q_axis_infinity",
            direction_residue=0,
            line_names=DIRECTION_GROUPS["q_axis_infinity"],
            invariant="line sum/product",
            value=f"sum={J}, product={RANK_SEED}",
            interpretation="line at infinity closes q-axis: sum gives J, product gives 2q",
        ),
    ]


def fano_transport_grammar_audit() -> Dict[str, object]:
    rows = {r.name: r for r in transport_lines()}

    horizontal_products = [rows[name].affine_pair_product_mod13 for name in DIRECTION_GROUPS["threshold_horizontal_q"]]
    vertical_sums = [rows[name].affine_pair_sum_mod13 for name in DIRECTION_GROUPS["rank_vertical_2q"]]
    diagonal_products = [rows[name].affine_pair_product_mod13 for name in DIRECTION_GROUPS["carrier_diagonal_q2"]]
    infinity = rows["line_at_infinity"]

    checks = {
        "horizontal_affine_products_are_threshold": horizontal_products == [J, J],
        "vertical_affine_sums_are_zero": vertical_sums == [0, 0],
        "diagonal_affine_products_are_carrier": diagonal_products == [J_INV, J_INV],
        "line_at_infinity_sum_is_threshold": infinity.total_sum_mod13 == J,
        "line_at_infinity_product_is_rank": infinity.total_product_mod13 == RANK_SEED,
        "threshold_and_carrier_inverse": mod13(J * J_INV) == 1,
        "threshold_plus_carrier_closes_phi3": J + J_INV == PHI3,
        "threshold_minus_carrier_abs_is_q": abs(J_INV - J) == Q,
        "horizontal_direction_is_q": rows["horizontal_y0"].direction == rows["horizontal_y1"].direction == Q,
        "vertical_direction_is_2q": rows["vertical_x0"].direction == rows["vertical_x1"].direction == RANK_SEED,
        "diagonal_direction_is_q2": rows["diagonal_main"].direction == rows["diagonal_shift"].direction == Q2,
        "vertical_pairs_are_additive_inverses": set(rows["vertical_x0"].affine_pair) == {1, K} and set(rows["vertical_x1"].affine_pair) == {J, J_INV},
        "diagonal_total_products_are_phi6": rows["diagonal_main"].total_product_mod13 == rows["diagonal_shift"].total_product_mod13 == PHI6,
        "horizontal_total_products_are_binary_duality": rows["horizontal_y0"].total_product_mod13 == rows["horizontal_y1"].total_product_mod13 == Q - 1,
    }
    assert all(checks.values())

    return {
        "module": "PART_CLXVII_FANO_TRANSPORT_GRAMMAR",
        "source_links": {
            "CLXVI": "Fano affine completion",
            "CLXI_CLXII": "stabilizer residue and finite-field dynamics",
        },
        "w33_atoms": {
            "q": Q,
            "rank_seed_2q": RANK_SEED,
            "q_square": Q2,
            "k": K,
            "Phi3": PHI3,
            "Phi4": PHI4,
            "Phi6": PHI6,
            "J_threshold": J,
            "J_inverse_carrier": J_INV,
            "Hashimoto_norm": HASHIMOTO_NORM,
        },
        "transport_lines": [asdict(r) for r in transport_lines()],
        "direction_transports": [asdict(r) for r in direction_transports()],
        "checks": checks,
        "theorem_statement": (
            "The Fano affine completion carries a transport grammar: q-horizontal lines "
            "preserve affine-pair product J=5, giving threshold transport; 2q-vertical "
            "lines pair additive inverses, giving rank/opposition transport; and q^2-diagonal "
            "lines preserve affine-pair product J^{-1}=8, giving carrier transport. "
            "The line at infinity {3,6,9} closes the q-axis with sum J and product 2q."
        ),
        "interpretive_note": (
            "This is the first explicit transport law on the Fano bridge.  The affine "
            "square is not just a diagram: its parallel classes encode the threshold, "
            "rank/opposition, and carrier operations that have been appearing separately "
            "in the mixer, decimal, and toroidal analyses."
        ),
    }


def main() -> int:
    audit = fano_transport_grammar_audit()
    out = ROOT / "PART_CLXVII_fano_transport_grammar_results.json"
    out.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(json.dumps(audit, indent=2))
    print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
