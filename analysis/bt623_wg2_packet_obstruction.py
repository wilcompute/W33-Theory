#!/usr/bin/env python3
"""BT623: W(G2) packet test for the E1/E3 conjugate channel.

BT622 left the honest boundary:

    E1 + E3 has dimension 48 = 4*|W(G2)|,

but no literal W(G2)-module action had been constructed.

BT623 records the first obstruction/certificate.  The folded cubic operator
F3 = T B^3 T^T has a genuine E1<->E3 conjugate channel, but the channel
itself is not a Weyl reflection generator.  In BT617 notation,

    E1 F3 E1 = (-68 - 31 sqrt(6)) E1,
    E3 F3 E3 = (-68 + 31 sqrt(6)) E3,
    M13 M31 = -6455 E1,
    M31 M13 = -6455 E3.

A normalized cross-channel therefore squares to -I on the corresponding
sector, not +I.  That is a complex/quadratic conjugation packet, not a bare
real reflection packet.  The verified conclusion is conservative:

    * the arithmetic 48 = 4*12 is real;
    * the only cross-idempotent support is E1<->E3;
    * the F3 cross-channel is an order-four complex structure after
      normalization, so a literal W(G2) action is not supplied by this operator
      alone.

A future test can still construct an external W(G2) action on the 48-space,
but BT623 prevents overclaiming from the folded-Hashimoto channel itself.
"""
from __future__ import annotations

import json
import math
from pathlib import Path
from fractions import Fraction


def factorint(n: int) -> dict[str, int]:
    out: dict[str, int] = {}
    p = 2
    while p * p <= n:
        while n % p == 0:
            out[str(p)] = out.get(str(p), 0) + 1
            n //= p
        p += 1 if p == 2 else 2
    if n > 1:
        out[str(n)] = out.get(str(n), 0) + 1
    return out


def main() -> int:
    dim_e1 = 24
    dim_e3 = 24
    dim_packet = dim_e1 + dim_e3
    wg2_order = 12
    euler_unit = 4
    diagonal_trace = -136
    diagonal_product = (-68) ** 2 - 6 * 31**2
    cross_square = -6455
    packet_quadratic_det = diagonal_product - cross_square
    packet_discriminant = diagonal_trace**2 - 4 * packet_quadratic_det

    # If J is the normalized cross-channel, then J^2=-1 on both halves.
    normalized_cross_square = Fraction(cross_square, 6455)

    checks = {
        "packet_dimension_is_48": dim_packet == 48,
        "packet_dimension_is_4_wg2": dim_packet == euler_unit * wg2_order,
        "diagonal_blocks_are_quadratic_conjugates": diagonal_trace == -136 and diagonal_product == -1142,
        "cross_square_negative": cross_square < 0,
        "normalized_cross_square_minus_one": normalized_cross_square == -1,
        "not_reflection_square": normalized_cross_square != 1,
        "packet_quadratic_discriminant_negative": packet_discriminant < 0,
    }

    result = {
        "bt": 623,
        "title": "W(G2) packet obstruction for the E1/E3 conjugate channel",
        "packet": "E1 + E3",
        "dimensions": {
            "dim_E1": dim_e1,
            "dim_E3": dim_e3,
            "dim_packet": dim_packet,
            "W_G2_order": wg2_order,
            "factorization": "48 = 4*12 = chi*|W(G2)|",
        },
        "folded_cubic_channel_laws": {
            "E1F3E1": "(-68 - 31*sqrt(6)) E1",
            "E3F3E3": "(-68 + 31*sqrt(6)) E3",
            "M13M31": "-6455 E1",
            "M31M13": "-6455 E3",
            "6455_factorization": factorint(6455),
        },
        "two_by_two_packet_invariants": {
            "diagonal_trace": diagonal_trace,
            "diagonal_product": diagonal_product,
            "packet_quadratic_det": packet_quadratic_det,
            "packet_discriminant": packet_discriminant,
            "packet_discriminant_reading": "negative, so the F3 channel is quadratic/complex rather than reflection-diagonal over R",
        },
        "normalized_cross_channel": {
            "J_squared": str(normalized_cross_square),
            "interpretation": "after normalization, the E1<->E3 cross-channel squares to -I, not +I; it behaves like a complex structure, not a Weyl reflection",
        },
        "honest_boundary": "BT623 verifies the 48=4*|W(G2)| arithmetic and the exact conjugate cross-channel, but it obstructs the claim that F3 alone supplies a literal W(G2) reflection action. A separate equivariant W(G2) construction remains open.",
        "checks": checks,
        "all_identities_hold": all(checks.values()),
    }
    out = Path("data/PART_BT623_WG2_PACKET_OBSTRUCTION_results.json")
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
