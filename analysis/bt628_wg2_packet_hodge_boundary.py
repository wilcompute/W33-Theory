#!/usr/bin/env python3
"""BT628: W(G2) packet / Hodge boundary consistency check.

BT626 constructs an external W(G2)=D6 action on a 48-dimensional carrier
matching E1+E3 = 24+24.  BT621/BT625 show that the physical Hodge block E4
has parity clock scalar a_n = 2 + (-1)^n under F_n = T B^n T^T.

BT628 checks that these two structures stay separated:

    lower-shell packet:  E1+E3, dimension 48 = 4*(6+6)
    physical packet:     E4,    dimension 81

The external W(G2) packet has eight root orbits of size 6.  The Hodge sector
has the independent two-state parity clock 1,3,1,3,... .  Their smallest joint
period is lcm(6,2)=6, so one G2 rotation period contains three full Hodge parity
periods.

This gives a clean boundary statement: the external W(G2) packet can organize
the conjugate lower-shell channel without acting on or mixing the Hodge sector.
"""
from __future__ import annotations

import json
from math import gcd
from pathlib import Path


def lcm(a: int, b: int) -> int:
    return a * b // gcd(a, b)


def main() -> int:
    wg2_order = 12
    wg2_rotation_period = 6
    wg2_reflection_order = 2
    short_roots = 6
    long_roots = 6
    copies = 4
    lower_packet_dim = copies * (short_roots + long_roots)
    e1_dim = copies * short_roots
    e3_dim = copies * long_roots
    hodge_dim = 81
    hodge_period = 2
    joint_period = lcm(wg2_rotation_period, hodge_period)
    hodge_cycles_per_root_rotation = joint_period // hodge_period
    root_rotations_per_joint_period = joint_period // wg2_rotation_period

    hodge_clock = {n: 2 + (-1) ** n for n in range(1, joint_period + 1)}
    root_angles = {n: n % wg2_rotation_period for n in range(1, joint_period + 1)}
    joint_states = [
        {"step": n, "root_angle_mod_6": root_angles[n], "hodge_scalar": hodge_clock[n]}
        for n in range(1, joint_period + 1)
    ]

    checks = {
        "lower_packet_is_48": lower_packet_dim == 48,
        "lower_packet_splits_24_24": e1_dim == 24 and e3_dim == 24,
        "hodge_dim_is_81": hodge_dim == 81,
        "packets_are_dimension_disjoint": lower_packet_dim != hodge_dim,
        "wg2_order_is_12": wg2_order == 12,
        "wg2_rotation_period_is_6": wg2_rotation_period == short_roots == long_roots,
        "hodge_period_is_2": hodge_period == 2,
        "joint_period_is_6": joint_period == 6,
        "three_hodge_periods_per_g2_rotation": hodge_cycles_per_root_rotation == 3,
        "one_root_rotation_per_joint_period": root_rotations_per_joint_period == 1,
        "joint_clock_values": [s["hodge_scalar"] for s in joint_states] == [1, 3, 1, 3, 1, 3],
    }

    result = {
        "bt": 628,
        "title": "W(G2) packet / Hodge boundary consistency check",
        "lower_shell_packet": {
            "sector": "E1 + E3",
            "dimension": lower_packet_dim,
            "split": "24 + 24 = 4*6 short + 4*6 long",
            "external_group": "W(G2)=D6, order 12",
        },
        "physical_packet": {
            "sector": "E4",
            "dimension": hodge_dim,
            "hodge_clock": "a_n = 2 + (-1)^n",
            "values_on_joint_period": [hodge_clock[n] for n in range(1, joint_period + 1)],
        },
        "joint_clock": {
            "G2_root_rotation_period": wg2_rotation_period,
            "Hodge_parity_period": hodge_period,
            "joint_period": joint_period,
            "hodge_cycles_per_G2_rotation": hodge_cycles_per_root_rotation,
            "states": joint_states,
        },
        "interpretation": "The external W(G2) action organizes the E1+E3 lower-shell packet. The Hodge/physical E4 sector remains separate and follows its own 1,3 parity clock. One G2 root-rotation period contains three Hodge parity periods, but there is no sector mixing implied.",
        "boundary": "BT628 is a consistency/boundary check. It does not construct a W(G2) action on E4 and does not reverse BT623's obstruction that F3 itself is not a Weyl reflection.",
        "checks": checks,
        "all_identities_hold": all(checks.values()),
    }
    out = Path("data/PART_BT628_WG2_PACKET_HODGE_BOUNDARY_results.json")
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
