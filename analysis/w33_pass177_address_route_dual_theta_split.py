#!/usr/bin/env python3
"""Pass 177: the address--route dual theta split.

Pass 173 proved that the address and route kernel codes

    C_A = ker_F2(N)       = [40,15,8],
    C_R = ker_F2(N^T)     = [40,15,10]

are inequivalent, while their dual context codes first differ at weight
eight.  This witness lifts that code obstruction to the two rank-40
parity constructions

    K_A = {x in Z^40 : x mod 2 in C_A^perp},
    K_R = {x in Z^40 : x mod 2 in C_R^perp},

using the scaled theta exponent |x|^2/2.  Their first two nontrivial
shells agree exactly, then their third shells split:

    Theta_KA = 1 + 720 q^2 + 15360 q^3 + 1350960 q^4 + ...,
    Theta_KR = 1 + 720 q^2 + 15360 q^3 +  982320 q^4 + ....

The common 720 is objectwise: 80 coordinate doubles plus 16 sign lifts
of each of the 40 W(3,3) lines on the address side, or of each of the 40
point stars on the route side.  The q^4 difference is exactly

    (5085 - 3645) * 2^8 = 368640.

Thus incidence non-self-duality is invisible in the first two dual
shells and becomes measurable at the first weight-eight sector.
"""

from __future__ import annotations

from collections import Counter
import json
from math import comb
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_pass158_chiral_trade_lattice_two_480s import (
    build_w33,
    saturated_kernel,
    w33_lines,
)
from analysis.w33_pass167_sentinel_theta_macwilliams import poly_mul, poly_pow
from analysis.w33_pass173_incidence_transceiver_route_dark_lattice import (
    binary_kernel_code,
    macwilliams_dual,
    rank_mod2,
)

OUT = ROOT / "data" / "w33_pass177_address_route_dual_theta_split.json"


def parity_theta_shells(enumerator: Counter[int], cap: int) -> list[int]:
    """Theta coefficients at |x|^2/2=0..cap/2 for a parity construction."""
    even = [0] * (cap + 1)
    odd = [0] * (cap + 1)
    even[0] = 1
    for value in range(1, int(cap**0.5) + 1):
        square = value * value
        if value % 2:
            odd[square] += 2
        else:
            even[square] += 2

    shells = [0] * (cap // 2 + 1)
    for weight, multiplicity in enumerator.items():
        odd_part = poly_pow(odd, weight, cap) if weight else [1] + [0] * cap
        even_part = poly_pow(even, 40 - weight, cap)
        contribution = poly_mul(odd_part, even_part, cap)
        for norm_squared in range(0, cap + 1, 2):
            shells[norm_squared // 2] += multiplicity * contribution[norm_squared]
    return shells


def main():
    checks = {}
    _, adjacency, _ = build_w33()
    lines = w33_lines(adjacency)
    incidence = np.zeros((40, 40), dtype=np.int64)
    for line_id, line in enumerate(lines):
        incidence[line_id, list(line)] = 1

    address_kernel = saturated_kernel(incidence)
    route_kernel = saturated_kernel(incidence.T)
    address_generators, _, address_weights = binary_kernel_code(
        address_kernel, incidence
    )
    route_generators, _, route_weights = binary_kernel_code(
        route_kernel, incidence.T
    )
    checks["kernel_codes_40_15"] = (
        address_generators.shape == (15, 40)
        and route_generators.shape == (15, 40)
    )

    address_dual = macwilliams_dual(address_weights, 40, 15)
    route_dual = macwilliams_dual(route_weights, 40, 15)
    checks["dual_enumerators_complete"] = (
        sum(address_dual.values()) == 2**25
        and sum(route_dual.values()) == 2**25
    )
    checks["dual_heads_40_240_then_split"] = (
        address_dual[4] == route_dual[4] == 40
        and address_dual[6] == route_dual[6] == 240
        and address_dual[8] == 5085
        and route_dual[8] == 3645
    )

    # The forty exhibited minimum words exhaust each A_4=40 sector.
    line_words = incidence % 2
    point_star_words = incidence.T % 2
    checks["address_min_words_are_lines"] = (
        len({tuple(row) for row in line_words}) == 40
        and set(line_words.sum(axis=1)) == {4}
        and np.all((line_words @ address_generators.T) % 2 == 0)
    )
    checks["route_min_words_are_point_stars"] = (
        len({tuple(row) for row in point_star_words}) == 40
        and set(point_star_words.sum(axis=1)) == {4}
        and np.all((point_star_words @ route_generators.T) % 2 == 0)
    )

    address_shells = parity_theta_shells(address_dual, 12)
    route_shells = parity_theta_shells(route_dual, 12)
    checks["first_two_nontrivial_shells_agree"] = (
        address_shells[:4] == route_shells[:4] == [1, 0, 720, 15360]
    )
    checks["third_shell_split_exact"] = (
        address_shells[4] == 1350960
        and route_shells[4] == 982320
        and address_shells[4] - route_shells[4] == 368640
    )

    coordinate_sector = 4 * comb(40, 2)
    weight4_plus_coordinate = 40 * 2**4 * (40 - 4) * 2
    address_weight8_sector = address_dual[8] * 2**8
    route_weight8_sector = route_dual[8] * 2**8
    checks["q4_sector_decomposition"] = (
        coordinate_sector == 3120
        and weight4_plus_coordinate == 46080
        and coordinate_sector + weight4_plus_coordinate + address_weight8_sector
        == address_shells[4]
        and coordinate_sector + weight4_plus_coordinate + route_weight8_sector
        == route_shells[4]
    )
    checks["split_is_1440_weight8_words_times_256_signs"] = (
        address_dual[8] - route_dual[8] == 1440
        and 1440 * 2**8 == 368640
    )
    checks["non_self_duality_already_visible_in_kernel_gram"] = (
        rank_mod2(address_generators @ address_generators.T) == 0
        and rank_mod2(route_generators @ route_generators.T) == 6
    )

    all_pass = all(checks.values())
    payload = {
        "schema": "w33.pass177.address_route_dual_theta_split.v1",
        "status": "PASS" if all_pass else "FAIL",
        "codes": {
            "address": "C_A=ker_F2(N)=[40,15,8]",
            "route": "C_R=ker_F2(N^T)=[40,15,10]",
            "address_dual_A4_A6_A8": [
                address_dual[4],
                address_dual[6],
                address_dual[8],
            ],
            "route_dual_A4_A6_A8": [
                route_dual[4],
                route_dual[6],
                route_dual[8],
            ],
        },
        "theta": {
            "convention": "coefficient of q^m counts |x|^2/2=m",
            "address_scaled_0_to_6": [int(value) for value in address_shells],
            "route_scaled_0_to_6": [int(value) for value in route_shells],
            "common_q2": {
                "count": 720,
                "address": "80 coordinate doubles + 16 lifts * 40 lines",
                "route": "80 coordinate doubles + 16 lifts * 40 point stars",
            },
            "common_q3": {
                "count": 15360,
                "decomposition": "2^6 sign lifts * 240 weight-6 context words",
            },
            "q4_split": {
                "common_coordinate_sector": coordinate_sector,
                "common_weight4_plus_coordinate_sector": weight4_plus_coordinate,
                "address_weight8_sector": address_weight8_sector,
                "route_weight8_sector": route_weight8_sector,
                "address_total": address_shells[4],
                "route_total": route_shells[4],
                "difference": address_shells[4] - route_shells[4],
            },
        },
        "reading": (
            "the point-line non-self-duality is spectrally delayed: lines and "
            "point stars give identical 720 openings, and the weight-6 sectors "
            "also agree, but 1440 extra address weight-8 words create exactly "
            "368640 extra signed vectors in the next shell"
        ),
        "checks": {name: bool(value) for name, value in checks.items()},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
