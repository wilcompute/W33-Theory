#!/usr/bin/env python3
"""
(R3, clarifying) The K3_16 level-2 boundary ranks are topologically forced;
the R3 convergence lives in the MASSIVE spectrum, not the ranks.

The edgewise refinement program (BT984-BT1029) is grinding the K3_16 level-2
middle boundary ranks d2, d3 via sharded F2 elimination in CI. This note
observes that all four ranks are EXACTLY determined by the f-vector and the
(level-independent) K3 Betti numbers, so the heavy middle-rank computation is
a triangulation-validity consistency check, not new convergence data.

WHY the Betti numbers are level-independent: each edgewise refinement of the
K3_16 seed is again a triangulation of the SAME smooth 4-manifold K3, so by the
de Rham theorem (combinatorially: Dodziuk; the simplicial cohomology of any
triangulation equals the de Rham cohomology) its homology is K3's,
b = (1,0,22,0,1), at EVERY level. Given the f-vector, that pins every boundary
rank via b_k = dim C_k - rank d_k - rank d_{k+1}.

Consequence for R3: the spectral action splits into
  - a HARMONIC (zero-mode) sector = the homology = topology: exact at every
    level, so it 'converges' trivially (it is already correct at level 1), and
  - a MASSIVE (nonzero-spectrum) sector that carries the Seeley-DeWitt
    coefficient a_2 ~ (1/6) int R sqrt(g) = the Einstein-Hilbert term.
The refinement limit is needed ONLY for the massive sector. So the R3-relevant
quantity is the massive heat trace (stochastic estimators, BT1004), not the
exact ranks (which the cheap pseudomanifold + connectivity + Euler checks
already pin).
"""
from __future__ import annotations

import json


def forced_ranks(fvec, betti):
    """rank d_k for k=1..n from b_k = C_k - rank d_k - rank d_{k+1}, top-down."""
    n = len(fvec) - 1
    ranks = {}
    rd_next = 0  # rank d_{n+1} = 0
    for k in range(n, 0, -1):
        ranks[k] = fvec[k] - betti[k] - rd_next
        rd_next = ranks[k]
    return ranks


def main():
    # K3_16 edgewise level-2 (BT993/BT1000) and CP2_9 level-2 (BT998), with the
    # level-independent Betti numbers of the underlying smooth 4-manifolds.
    cases = {
        "K3_16 level-2": {
            "f": [2776, 45120, 152960, 184320, 73728],
            "betti": [1, 0, 22, 0, 1],
            "agent_targets": {1: 2775, 2: 42345, 3: 110593, 4: 73727},
        },
        "CP2_9 level-2": {
            "f": [459, 5976, 19344, 23040, 9216],
            "betti": [1, 0, 1, 0, 1],
            "agent_targets": None,
        },
    }
    out = {}
    for name, c in cases.items():
        r = forced_ranks(c["f"], c["betti"])
        chi = sum((-1)**k * c["f"][k] for k in range(len(c["f"])))
        chi_b = sum((-1)**k * c["betti"][k] for k in range(len(c["betti"])))
        bottom_ok = r[1] == c["f"][0] - c["betti"][0]
        print(f"=== {name} ===")
        print(f"  f-vector = {c['f']}")
        print(f"  Betti    = {c['betti']}  (de Rham: same at EVERY level)")
        print(f"  forced ranks d1..d4 = {[r[k] for k in (1,2,3,4)]}")
        if c["agent_targets"]:
            match = all(r[k] == c["agent_targets"][k] for k in (1, 2, 3, 4))
            print(f"  parallel-agent targets = "
                  f"{[c['agent_targets'][k] for k in (1,2,3,4)]}  MATCH={match}")
        print(f"  Euler chi (f) = {chi}; alt-sum Betti = {chi_b}; "
              f"bottom consistency = {bottom_ok}")
        print()
        out[name] = {
            "f": c["f"], "betti": c["betti"],
            "forced_ranks": {str(k): r[k] for k in (1, 2, 3, 4)},
            "euler": chi, "euler_from_betti": chi_b,
            "matches_agent_targets": (None if not c["agent_targets"] else
                                      all(r[k] == c["agent_targets"][k]
                                          for k in (1, 2, 3, 4))),
        }

    print("READING:")
    print(" - All four K3_16 level-2 ranks are forced by (f-vector, Betti);")
    print("   they match the BT1005/1006 targets exactly. The middle-rank F2")
    print("   grind (BT1015-1029) re-derives topologically-fixed numbers: a")
    print("   triangulation-validity check, not R3 convergence data.")
    print(" - Validity is already pinned cheaply: closed pseudomanifold")
    print("   (every 3-face in exactly two 4-faces, BT1006), connectivity, and")
    print("   chi=24 -- plus the fact that each level is a refinement of the")
    print("   known K3_16 triangulation. Given validity, the ranks follow.")
    print(" - R3's convergence is in the MASSIVE spectrum: a_2 ~ (1/6) int R")
    print("   = the Einstein-Hilbert coefficient. Compute should target the")
    print("   massive heat trace (stochastic estimators), not exact ranks.")

    out["reading"] = ("K3 level-2 boundary ranks are topologically forced "
                      "(de Rham/Dodziuk); the exact middle-rank grind is a "
                      "validity check, not convergence data. R3's quantity is "
                      "the massive-spectrum Seeley-DeWitt a_2 ~ (1/6) int R.")
    with open("data/bt1030_k3_ranks_topologically_forced.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nwrote data/bt1030_k3_ranks_topologically_forced.json")


if __name__ == "__main__":
    main()
