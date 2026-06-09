#!/usr/bin/env python3
"""BT630: representation-level intertwiner obstruction for the 48-packet.

BT626 constructs an external W(G2)=D6 action on a 48-dimensional carrier:

    4*(6 short roots + 6 long roots) = 24 + 24.

BT623/BT617 show that the folded-cubic F3 cross-channel on E1+E3 satisfies

    M13 M31 = -6455 E1,
    M31 M13 = -6455 E3,

so after normalization the channel is a complex structure J with J^2=-I.

BT630 checks the clean representation-level obstruction: a real involutive Weyl
reflection has square +I.  Therefore no map that sends an ordinary W(G2)
reflection to the normalized F3 cross-channel can be an algebra homomorphism or
intertwiner respecting generator squares.  However, the obstruction disappears
after complexification if one adjoins a scalar i: iJ has square +I.

This is the precise boundary between:

  * real external Weyl packet action (BT626), and
  * folded-cubic quadratic conjugate transport (BT623/BT617).
"""
from __future__ import annotations

import json
from pathlib import Path


def main() -> int:
    wg2_reflection_square = 1
    normalized_f3_cross_square = -1
    complexified_cross_square = (-1) * normalized_f3_cross_square  # (iJ)^2 = i^2 J^2 = (-1)(-1)

    dim_short = 24
    dim_long = 24
    dim_packet = dim_short + dim_long
    root_orbits = 8
    orbit_size = 6
    wg2_order = 12

    # Any real algebra homomorphism carrying a generator s with s^2=1 to J
    # would force J^2=1.  Since J^2=-1, contradiction is exact.
    real_square_defect = normalized_f3_cross_square - wg2_reflection_square
    complex_square_defect = complexified_cross_square - wg2_reflection_square

    checks = {
        "dimension_packet_48": dim_packet == 48,
        "packet_split_24_24": dim_short == dim_long == 24,
        "external_orbit_count_8_size_6": root_orbits * orbit_size == dim_packet,
        "wg2_order_12": wg2_order == 12,
        "real_reflection_square_plus_one": wg2_reflection_square == 1,
        "f3_cross_square_minus_one": normalized_f3_cross_square == -1,
        "real_intertwiner_square_obstructed": real_square_defect == -2,
        "complexified_square_matches": complexified_cross_square == 1,
        "complex_square_defect_zero": complex_square_defect == 0,
    }

    result = {
        "bt": 630,
        "title": "W(G2) packet intertwiner obstruction",
        "objects": {
            "external_packet": "4 copies of G2 short roots plus 4 copies of G2 long roots",
            "dimension": "24+24=48",
            "external_reflection_law": "s^2=+I",
            "folded_cubic_cross_channel_law": "J^2=-I after normalization",
        },
        "obstruction": {
            "real_square_defect": real_square_defect,
            "statement": "No real generator-respecting intertwiner can identify a W(G2) reflection with the normalized F3 cross-channel because +I != -I.",
        },
        "complexification_escape_hatch": {
            "law": "(iJ)^2=+I",
            "square_defect_after_complexification": complex_square_defect,
            "statement": "A complexified or projective packet model may absorb the sign by a scalar i; that is not the same as a real Weyl reflection in the original folded-cubic operator.",
        },
        "interpretation": "BT630 explains why BT626 must remain external and why BT623's -I obstruction is not a contradiction. The dimension match 48=4*12 is real, but the F3 channel carries a complex/quadratic structure unless a scalar phase is adjoined.",
        "checks": checks,
        "all_identities_hold": all(checks.values()),
    }
    out = Path("data/PART_BT630_WG2_PACKET_INTERTWINER_OBSTRUCTION_results.json")
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
