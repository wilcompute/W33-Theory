#!/usr/bin/env python3
"""Passes 3274-3275: exact rank-two twisted cohomology of the port complex.

Pass 3240 proved that the filled finite-port complex is homotopy-equivalent to a
wedge of 436 circles.  This script computes H^0 and H^1 for rank-two local
systems over F_3 from the reduced cellular complex

    V --d0--> V^436,
    d0(v)=((rho(g_i)-I)v)_i.

The nontrivial control sends one free generator to the mod-three D4 quarter-turn
J=[[0,-1],[1,0]] and all remaining generators to identity.  Since J-I is
invertible over F_3, the local system has no global invariant vector.
"""
from __future__ import annotations

import json
from pathlib import Path

P = 3
FREE_RANK = 436
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_BT3274_BT3275_TWISTED_PORT_LOCAL_SYSTEM_results.json"

I = ((1, 0), (0, 1))
J = ((0, 2), (1, 0))  # quarter turn over F_3; J^2=-I, J^4=I


def matmul(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(2)) % P for j in range(2)) for i in range(2))


def matsub(a, b):
    return tuple(tuple((a[i][j] - b[i][j]) % P for j in range(2)) for i in range(2))


def det(a):
    return (a[0][0] * a[1][1] - a[0][1] * a[1][0]) % P


def rank2(a):
    if all(x % P == 0 for row in a for x in row):
        return 0
    return 2 if det(a) else 1


def local_system(name: str, first_monodromy):
    delta = matsub(first_monodromy, I)
    d0_rank = rank2(delta)
    c0_dim = 2
    c1_dim = 2 * FREE_RANK
    h0 = c0_dim - d0_rank
    h1 = c1_dim - d0_rank
    euler = h0 - h1
    return {
        "name": name,
        "field": "F3",
        "fiber_rank": 2,
        "free_generators": FREE_RANK,
        "first_generator_monodromy": [list(row) for row in first_monodromy],
        "remaining_generator_monodromy": "identity",
        "rank_d0": d0_rank,
        "dim_C0": c0_dim,
        "dim_C1": c1_dim,
        "dim_H0": h0,
        "dim_H1": h1,
        "dim_H2": 0,
        "twisted_euler_characteristic": euler,
    }


def main():
    assert matmul(J, J) == ((2, 0), (0, 2))
    assert matmul(matmul(J, J), matmul(J, J)) == I
    assert det(J) == 1
    assert det(matsub(J, I)) == 2  # no nonzero fixed vector

    trivial = local_system("trivial_rank_two", I)
    quarter = local_system("d4_quarter_turn", J)
    assert trivial["dim_H0"] == 2 and trivial["dim_H1"] == 872
    assert quarter["dim_H0"] == 0 and quarter["dim_H1"] == 870
    assert trivial["twisted_euler_characteristic"] == quarter["twisted_euler_characteristic"] == -870

    payload = {
        "schema": "w33.pass3274_3275.twisted_port_local_system.v1",
        "status": "EXACT_REDUCED_CELLULAR_THEOREM",
        "port_complex": {
            "vertices": 45,
            "edges": 720,
            "filled_triangles": 240,
            "fundamental_group": "F_436",
            "homotopy_model": "wedge of 436 circles",
        },
        "controls": [trivial, quarter],
        "exact_conclusion": "A single fixed-point-free D4 quarter-turn monodromy lowers rank-two H1 from 872 to 870 and kills H0. The transport effect is two dimensions, not a second copy of the constant 436-dimensional ambiguity.",
        "negative_control": "Replacing J by identity restores H0=2 and H1=872.",
        "boundary": "This is exact cellular cohomology for the stated F3 local system on the proved F_436 homotopy model. It is not an optical phase measurement, a complete contextuality invariant, or a fault-tolerance theorem.",
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"trivial_h1": 872, "twisted_h1": 870, "twisted_h0": 0}, sort_keys=True))


if __name__ == "__main__":
    main()
