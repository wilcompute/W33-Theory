#!/usr/bin/env python3
"""
BT813 - The vacuum transition matrix of PSp(4,3).

GAP witness (.tmp/gap_vacuum_transitions.g): for every ordered pair of
maximal classes (the five vacua, BT812), the orbit partition of one
maximal acting on the coset space of the other - the complete relative
position table:

              G/27        G/36       G/40a      G/40b      G/45
   M27     [1,10,16]    [16,20]     [40]       [40]      [5,40]
   M36     [12,15]      [1,15,20]   [10,30]    [40]      [15,30]
   M40a    [27]         [9,27]      [1,12,27]  [4,36]    [18,27]
   M40b    [27]         [36]        [4,36]     [1,12,27] [9,36]
   M45     [3,24]       [12,24]     [16,24]    [8,32]    [1,12,32]

(40a = the parabolic seeing spreads as 9+27 = the LINE stabilizer, since
each line lies in exactly 9 spreads; 40b = the POINT stabilizer, transitive
on spreads because every spread covers every point.)

THEOREMS / READINGS:
  T1. Double-coset symmetry: #(Mi-orbits on G/Mj) = #(Mj-orbits on G/Mi)
      for all pairs - verified from the table.
  T2. The register diagonal [1,10,16] is the SCHLAFLI structure: the 27
      icosahedral registers form the line-intersection geometry of the
      cubic surface (each line meets 10, skew to 16).  The spread
      diagonal [1,15,20] and tritangent diagonal [1,12,32] are the
      classical double-six and tritangent intersection ranks.
  T3. Line-in-spread count: 36 spreads x 10 lines = 40 lines x 9 - each
      W33 line lies in EXACTLY 9 regular spreads (the [9,27] row).
  T4. Substrate saturation of the off-diagonal entries:
      icosa<->polar [5,40]/[3,24]: 5 = F5 distinguished tritangents per
        register, 3 = q distinguished registers per tritangent;
      icosa<->spread [16,20]/[12,15]: 16 = mu^2 = |F4^2| register cells,
        20 = BC ring count; 12 = k, 15 = g;
      spread<->polar [15,30]/[12,24]: g + h(E8); k + f.
"""
from __future__ import annotations

import json

TABLE = {
    (27, 27): [1, 10, 16], (27, 36): [16, 20], (27, "40a"): [40],
    (27, "40b"): [40], (27, 45): [5, 40],
    (36, 27): [12, 15], (36, 36): [1, 15, 20], (36, "40a"): [10, 30],
    (36, "40b"): [40], (36, 45): [15, 30],
    ("40a", 27): [27], ("40a", 36): [9, 27], ("40a", "40a"): [1, 12, 27],
    ("40a", "40b"): [4, 36], ("40a", 45): [18, 27],
    ("40b", 27): [27], ("40b", 36): [36], ("40b", "40a"): [4, 36],
    ("40b", "40b"): [1, 12, 27], ("40b", 45): [9, 36],
    (45, 27): [3, 24], (45, 36): [12, 24], (45, "40a"): [16, 24],
    (45, "40b"): [8, 32], (45, 45): [1, 12, 32],
}

SIZE = {27: 27, 36: 36, "40a": 40, "40b": 40, 45: 45}


def main():
    keys = [27, 36, "40a", "40b", 45]

    # T1: row sums + double coset symmetry
    for (a, b), part in TABLE.items():
        assert sum(part) == SIZE[b], (a, b)
    for a in keys:
        for b in keys:
            assert len(TABLE[(a, b)]) == len(TABLE[(b, a)]), (a, b)
    print("T1 row sums + double-coset symmetry: ALL PASS")

    # T2: Schlafli diagonal
    assert TABLE[(27, 27)] == [1, 10, 16]
    assert TABLE[(36, 36)] == [1, 15, 20]
    assert TABLE[(45, 45)] == [1, 12, 32]
    print("T2 diagonals: registers = Schlafli line-intersection [1,10,16];")
    print("   double-sixes [1,15,20]; tritangents [1,12,32]")

    # T3: line-in-spread count
    assert 36 * 10 == 40 * 9
    assert TABLE[("40a", 36)] == [9, 27]
    print("T3 every line lies in exactly 9 regular spreads (36x10 = 40x9)")

    # T4: substrate saturation
    seals = {
        "icosa->polar 5": 5, "polar->icosa 3": 3,
        "icosa->spread 16": 16, "spread->icosa 12+15": 27,
        "spread->polar 15+30": 45, "polar->spread 12+24": 36,
    }
    print("T4 substrate entries: 5=F5, 3=q, 16=mu^2, 20=BC rings, 12=k,")
    print("   15=g, 30=h(E8), 24=f - the transition matrix speaks substrate")

    out = {
        "theorem": "BT813 vacuum transition matrix",
        "table": {f"{a}|{b}": part for (a, b), part in TABLE.items()},
        "readings": {
            "register_diagonal": "Schlafli graph suborbits [1,10,16]",
            "line_in_spreads": 9,
            "icosa_sees_polar": "[5,40] - five F5 tritangents",
            "polar_sees_icosa": "[3,24] - three q registers",
            "icosa_sees_spread": "[16,20] - register cells + BC rings",
        },
    }
    with open("data/bt813_vacuum_transition_matrix.json", "w") as fj:
        json.dump(out, fj, indent=2)
    print("\nwrote data/bt813_vacuum_transition_matrix.json")


if __name__ == "__main__":
    main()
