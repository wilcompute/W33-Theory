#!/usr/bin/env python3
"""
BT817 - The self-entangled photon atlas: vacuum decompositions as
        entanglement strata, and spreads as measurement schedules.

Quantum network reading (user direction): the network IS the computer and
the carrier is a SINGLE PHOTON self-entangled across its own degrees of
freedom: path qubit (x) polarization qubit = C2 (x) C2 = C4.  The Witting
polytope's 40 rays realize W(3,3) in that C4 (Penrose/Waegell-Aravind).

  T1. The 40 Witting rays' orthogonality graph is SRG(40,12,2,4) and
      isomorphic to W(3,3) (networkx certificate).
  T2. The 40 orthonormal tetrads (= maximal measurement contexts) match
      the 40 lines; each ray lies in exactly 4 contexts.
  T3. SELF-ENTANGLEMENT = THE PARABOLIC VACUUM.  Under C4 = C2 (x) C2
      (reshape to 2x2, Schmidt rank = matrix rank):
        rays:   4 product + 36 self-entangled   = the [4,36] line vacuum
        bases:  1 all-product + 12 one-product + 27 fully-entangled
                = THE HOLONET SPLIT 1 + 12 + 27 on measurement contexts.
      Choosing a qubit factorization of the photon IS choosing a
      parabolic vacuum; the holonet decomposition is the physical
      entanglement stratification of the contexts.
  T4. SPREADS = MEASUREMENT SCHEDULES.  Exact-cover search for all
      partitions of the 40 rays into 10 disjoint contexts: each schedule
      measures every ray exactly once.  Count them all (the 36 regular
      spreads of BT809 are the prediction; the search decides whether
      any non-regular schedules exist).
"""
from __future__ import annotations

from itertools import combinations, product
import json

import numpy as np
import networkx as nx


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
    assert len(rays) == 40
    n = 40
    orth = [[abs(np.vdot(rays[i], rays[j])) < 1e-9 for j in range(n)]
            for i in range(n)]

    G = nx.Graph()
    G.add_nodes_from(range(n))
    for i, j in combinations(range(n), 2):
        if orth[i][j]:
            G.add_edge(i, j)
    degs = set(dict(G.degree()).values())
    print(f"T1 orthogonality graph: degrees {degs}")
    assert degs == {12}
    # SRG parameters
    lam = set()
    mu_ = set()
    A = nx.to_numpy_array(G)
    A2 = A @ A
    for i, j in combinations(range(n), 2):
        (lam if A[i, j] else mu_).add(int(A2[i, j]))
    print(f"T1 lambda = {lam}, mu = {mu_}  (expect 2, 4)")
    assert lam == {2} and mu_ == {4}

    # W33 from symplectic F3^4
    def canon(v):
        for x in v:
            if x % 3:
                c = 1 if x % 3 == 1 else 2
                return tuple((c * y) % 3 for y in v)
        raise ValueError

    pts = sorted({canon(v) for v in product(range(3), repeat=4) if any(v)})

    def symp(x, y):
        return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3

    W = nx.Graph()
    W.add_nodes_from(range(40))
    for i, j in combinations(range(40), 2):
        if symp(pts[i], pts[j]) == 0:
            W.add_edge(i, j)
    iso = nx.is_isomorphic(G, W)
    print(f"T1 orthogonality graph isomorphic to W(3,3): {iso}")
    assert iso

    # T2: contexts = 4-cliques
    contexts = [c for c in nx.find_cliques(G) if len(c) == 4]
    contexts = [tuple(sorted(c)) for c in contexts]
    print(f"T2 orthonormal tetrads (contexts): {len(contexts)}")
    assert len(contexts) == 40
    per_ray = [sum(1 for c in contexts if r in c) for r in range(n)]
    assert set(per_ray) == {4}
    print("T2 each ray in exactly 4 contexts")

    # T3: self-entanglement census (path (x) polarization split)
    def schmidt_rank(v):
        M = v.reshape(2, 2)
        return int(np.linalg.matrix_rank(M, tol=1e-9))

    ranks = [schmidt_rank(r) for r in rays]
    n_prod = ranks.count(1)
    n_ent = ranks.count(2)
    print(f"T3 rays: {n_prod} product + {n_ent} self-entangled "
          f"(the [4,36] parabolic line vacuum)")
    assert (n_prod, n_ent) == (4, 36)

    profile = {}
    for c in contexts:
        k = sum(1 for r in c if ranks[r] == 1)
        profile[k] = profile.get(k, 0) + 1
    print(f"T3 contexts by product-ray count: {dict(sorted(profile.items(), reverse=True))}")
    assert profile == {4: 1, 1: 12, 0: 27}
    print("T3 = THE HOLONET SPLIT 1 + 12 + 27 as entanglement strata:")
    print("   1 all-product context, 12 partially entangled, 27 fully")
    print("   self-entangled contexts")

    # T4: exact cover - all 10-context measurement schedules
    ctx_of_ray = [[ci for ci, c in enumerate(contexts) if r in c]
                  for r in range(n)]
    schedules = []

    def cover(used_rays, chosen):
        if len(chosen) == 10:
            schedules.append(tuple(sorted(chosen)))
            return
        r = min(set(range(n)) - used_rays)
        for ci in ctx_of_ray[r]:
            c = contexts[ci]
            if used_rays & set(c):
                continue
            cover(used_rays | set(c), chosen + [ci])

    cover(set(), [])
    print(f"\nT4 complete measurement schedules (spreads): {len(schedules)}")
    per_ctx = [sum(1 for s in schedules if ci in s) for ci in range(40)]
    print(f"T4 each context in {set(per_ctx)} schedules")

    out = {
        "theorem": "BT817 self-entangled photon atlas",
        "orthogonality_iso_W33": bool(iso),
        "contexts": len(contexts),
        "ray_split_product_entangled": [n_prod, n_ent],
        "context_entanglement_strata": {str(k): v
                                        for k, v in profile.items()},
        "measurement_schedules": len(schedules),
        "context_in_schedules": sorted(set(per_ctx)),
        "statement": (
            "qubit factorization of the photon = parabolic vacuum; "
            "1+12+27 = entanglement stratification of contexts; "
            "spreads = complete single-photon measurement schedules"),
    }
    with open("data/bt817_self_entangled_photon_atlas.json", "w") as fj:
        json.dump(out, fj, indent=2)
    print("\nwrote data/bt817_self_entangled_photon_atlas.json")


if __name__ == "__main__":
    main()
