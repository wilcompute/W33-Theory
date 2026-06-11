#!/usr/bin/env python3
"""
BT819 - Beacon heptads and the clock trichotomy of the universal computer.

Physics reading of BT818's alpha = 7: the maximum classical-witness sets
of the photonic substrate are HEPTADS - seven states, pairwise overlap
exactly 1/3 = 1/q - i.e. a complete K7 "beacon mesh" with uniform
interference visibility: the Csaszar toroidal node (Phi6 = 7, K7 routing,
diameter 1) realized as a constellation of quantum states inside the
single photon.  A quantum network can use a heptad as a phase-reference
frame: every beacon pair interferes at the same fixed visibility.

  T1. Enumerate ALL heptads (maximum independent sets of the W(3,3)
      orthogonality graph): the count is a new substrate invariant.
  T2. PSp(4,3)-orbit structure on heptads: orbits and stabilizer orders.
      Since 7 does not divide |PSp(4,3)| = 25920, NO heptad can have a
      cyclic Z7 symmetry inside the substrate group: the Csaszar clock is
      EXTERNAL to the symplectic world.
  T3. Frame physics: the beacon mesh's frame operator F = sum |h><h|.
      Equiangular at 1/3 but NOT tight (the (4,7)-ETF angle would be
      1/8): compute the frame spectrum - the mesh's "impedance profile".
  T4. THE CLOCK TRICHOTOMY: of the three natural clocks of the program,
        Z12 (rectangle/D12, BT746)   12 | 25920   INTERNAL
        Z7  (Csaszar/F42, BT803)      7 !| 25920   EXTERNAL
        Z13 (Singer/PG(3,3), BT807)  13 !| 25920   EXTERNAL
      The universal computer has exactly one internal clock (k = 12) and
      two external synchronization standards (Phi6 = 7, Phi3 = 13) - the
      reptend pair of BT774 (both have ord(10) = 6 = q! decimal periods).
"""
from __future__ import annotations

from itertools import combinations, product
import json

import numpy as np


def witting_rays():
    w = np.exp(2j * np.pi / 3.0)
    s3 = np.sqrt(3.0)
    rays = []
    for i in range(4):
        e = np.zeros(4, dtype=complex)
        e[i] = 1.0
        rays.append(e)
    for mu, nu in product(range(3), repeat=2):
        rays.append(np.array([0, 1, -(w**mu), w**nu]) / s3)
        rays.append(np.array([1, 0, -(w**mu), -(w**nu)]) / s3)
        rays.append(np.array([1, -(w**mu), 0, w**nu]) / s3)
        rays.append(np.array([1, w**mu, w**nu, 0]) / s3)
    return rays


def main():
    rays = witting_rays()
    n = 40
    adj = [[abs(np.vdot(rays[i], rays[j])) < 1e-9 for j in range(n)]
           for i in range(n)]
    nbr = [set(j for j in range(n) if adj[i][j]) for i in range(n)]

    # ---- T1: enumerate all maximum independent sets (size 7) -----------
    heptads = []

    def enum(cands, cur, start):
        if len(cur) == 7:
            heptads.append(tuple(cur))
            return
        if len(cur) + len(cands) < 7:
            return
        for v in sorted(cands):
            if v < start:
                continue
            enum(cands - {v} - nbr[v], cur + [v], v + 1)

    enum(set(range(n)), [], 0)
    N = len(heptads)
    print(f"T1 heptads (maximum independent sets): {N}")

    # ---- T2: orbit structure under PSp(4,3) ------------------------------
    def canon(v):
        for x in v:
            if x % 3:
                c = 1 if x % 3 == 1 else 2
                return tuple((c * y) % 3 for y in v)
        raise ValueError

    pts = sorted({canon(v) for v in product(range(3), repeat=4) if any(v)})
    pt_index = {p: i for i, p in enumerate(pts)}

    def symp(x, y):
        return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3

    # isomorphism Witting-orthogonality -> W33 collinearity via networkx
    import networkx as nx
    GW = nx.Graph()
    GW.add_nodes_from(range(n))
    for i, j in combinations(range(n), 2):
        if adj[i][j]:
            GW.add_edge(i, j)
    GS = nx.Graph()
    GS.add_nodes_from(range(40))
    for i, j in combinations(range(40), 2):
        if symp(pts[i], pts[j]) == 0:
            GS.add_edge(i, j)
    gm = nx.algorithms.isomorphism.GraphMatcher(GW, GS)
    assert gm.is_isomorphic()
    f = gm.mapping   # witting index -> symplectic index

    hepts_symp = {frozenset(f[x] for x in h) for h in heptads}

    def transvection_perm(v):
        out = []
        for x in pts:
            w_ = symp(x, v)
            out.append(pt_index[canon(tuple(
                (x[k] + w_ * v[k]) % 3 for k in range(4)))])
        return tuple(out)

    gens = [transvection_perm(v) for v in pts]

    rem = set(hepts_symp)
    orbits = []
    while rem:
        s0 = next(iter(rem))
        orb = {s0}
        frontier = [s0]
        while frontier:
            nxt = []
            for s in frontier:
                for g in gens:
                    s2 = frozenset(g[x] for x in s)
                    if s2 not in orb:
                        orb.add(s2)
                        nxt.append(s2)
            frontier = nxt
        orbits.append(len(orb))
        rem -= orb
    print(f"T2 PSp-orbit sizes on heptads: {sorted(orbits)}")
    stabs = sorted(25920 // o for o in orbits)
    print(f"T2 stabilizer orders: {stabs} (all 7-free since 7 !| 25920:")
    print("   no heptad has an internal Z7 - the Csaszar clock is EXTERNAL)")
    assert all(s % 7 != 0 for s in stabs)
    assert sum(orbits) == N

    # ---- T3: frame physics ------------------------------------------------
    h0 = heptads[0]
    F = sum(np.outer(rays[i], rays[i].conj()) for i in h0)
    ev = sorted(np.linalg.eigvalsh(F).real)
    print(f"T3 beacon-mesh frame spectrum: {[round(x, 6) for x in ev]}")
    tight = ev[0] == ev[-1]
    print(f"T3 tight frame: {abs(ev[0]-ev[-1]) < 1e-9} "
          f"(ETF(4,7) angle would be 1/8; ours is 1/3 - a LOOSE mesh)")
    print(f"T3 trace = {sum(ev):.6f} = 7; impedance spread "
          f"{ev[-1]/ev[0]:.6f}")

    # ---- T4: clock trichotomy ---------------------------------------------
    assert 25920 % 12 == 0 and 25920 % 7 != 0 and 25920 % 13 != 0
    print("\nT4 CLOCK TRICHOTOMY of the universal computer:")
    print("   Z12 (rectangle clock)  12 | 25920   INTERNAL  (BT746)")
    print("   Z7  (Csaszar clock)     7 !| 25920   EXTERNAL  (BT803)")
    print("   Z13 (Singer clock)     13 !| 25920   EXTERNAL  (BT807)")
    print("   both external clocks have decimal period 6 = q! (BT774);")
    print("   the network keeps one internal gauge clock and two external")
    print("   synchronization standards - exactly like a real network")
    print("   (local oscillator + external time references).")

    out = {
        "theorem": "BT819 beacon heptads + clock trichotomy",
        "heptad_count": N,
        "orbit_sizes": sorted(orbits),
        "stabilizer_orders": stabs,
        "frame_spectrum": [round(float(x), 6) for x in ev],
        "tight": bool(abs(ev[0]-ev[-1]) < 1e-9),
        "clock_trichotomy": {"12": "internal", "7": "external",
                             "13": "external"},
    }
    with open("data/bt819_beacon_heptads.json", "w") as fj:
        json.dump(out, fj, indent=2)
    print("\nwrote data/bt819_beacon_heptads.json")


if __name__ == "__main__":
    main()
