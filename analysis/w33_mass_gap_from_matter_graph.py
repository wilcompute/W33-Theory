#!/usr/bin/env python3
"""
The mass gap of the substrate's su(2) gauge theory is f = 24 -- exactly, finitely.

The matter graph Q (non-collinear pairs of W(3,3)) is the lattice of the
substrate's su(2) (2T) gauge theory (w33_lattice_to_continuum_ym.py). A discrete
gauge theory on a finite graph is automatically GAPPED: the kinetic operator is
the graph Laplacian, whose smallest nonzero eigenvalue is the spectral gap = the
discrete mass gap (glueball scale). Because Q is strongly regular -- an expander
-- this gap is large and EXACT.

Computed here: Q = SRG(40,27,18,18) has adjacency spectrum {27^1, 3^g, (-3)^f}
with g=15, f=24, so the Laplacian L_Q = 27 I - A_Q has spectrum
  {0^1, 24^{15}, 30^{24}},
and the spectral gap (smallest nonzero Laplacian eigenvalue, the algebraic
connectivity = discrete mass gap) is exactly
  gap = 24 = f,
with multiplicity g = 15 (the gauge-sector dimension), while the top eigenvalue
30 has multiplicity f = 24 (the matter-sector dimension). The eigenvalue
multiplicities ARE the Standard-Model sector sizes, and the mass gap IS the matter
count f. Confinement / a mass gap is forced by the expander (SRG) structure of
the matter graph; the substrate fixes the gap to f, exactly, with no continuum
limit needed to see that it is nonzero. (Honest: this is the gap of the discrete
finite theory on Q -- the substrate's exact shadow of the Yang-Mills mass gap --
not a continuum proof of the Millennium problem.)
"""
from __future__ import annotations

import itertools
import json

import numpy as np

F = 3


def sform(u, v):
    return (u[0] * v[2] - u[2] * v[0] + u[1] * v[3] - u[3] * v[1]) % F


def projective_points():
    pts, seen = [], set()
    for vec in itertools.product(range(F), repeat=4):
        if vec == (0, 0, 0, 0):
            continue
        for i in range(4):
            if vec[i] != 0:
                inv = pow(vec[i], F - 2, F)
                rep = tuple((inv * x) % F for x in vec)
                break
        if rep not in seen:
            seen.add(rep)
            pts.append(rep)
    return pts


def main():
    out = {}
    pts = projective_points()
    n = len(pts)
    assert n == 40
    # collinearity graph W (SRG(40,12,2,4)): p~q iff <v_p,v_q>=0
    # matter graph Q (complement): non-collinear, <v_p,v_q> != 0
    A_W = np.zeros((n, n))
    A_Q = np.zeros((n, n))
    for i, j in itertools.combinations(range(n), 2):
        if sform(pts[i], pts[j]) == 0:
            A_W[i, j] = A_W[j, i] = 1
        else:
            A_Q[i, j] = A_Q[j, i] = 1
    degW = int(A_W[0].sum())
    degQ = int(A_Q[0].sum())
    print(f"[graphs] W collinearity SRG(40,{degW},...), Q matter SRG(40,{degQ},...)")
    assert degW == 12 and degQ == 27

    def spectrum(A):
        ev = np.linalg.eigvalsh(A)
        # round and tally
        from collections import Counter

        c = Counter(int(round(x)) for x in ev)
        return dict(sorted(c.items(), reverse=True))

    specQ = spectrum(A_Q)
    print(f"\n[matter graph Q adjacency spectrum] {specQ}")
    # expect {27:1, 3:15, -3:24}
    assert specQ == {27: 1, 3: 15, -3: 24}
    out["Q_adjacency_spectrum"] = {str(k): v for k, v in specQ.items()}

    # Laplacian L_Q = degQ I - A_Q
    L = degQ * np.eye(n) - A_Q
    Lev = np.linalg.eigvalsh(L)
    from collections import Counter

    Lspec = dict(sorted(Counter(int(round(x)) for x in Lev).items()))
    print(f"[matter graph Q Laplacian spectrum] {Lspec}")
    assert Lspec == {0: 1, 24: 15, 30: 24}
    out["Q_laplacian_spectrum"] = {str(k): v for k, v in Lspec.items()}

    gap = sorted(k for k in Lspec if k > 0)[0]
    gap_mult = Lspec[gap]
    top = max(Lspec)
    print(
        f"\n[mass gap] smallest nonzero Laplacian eigenvalue = {gap} = f "
        f"(mult {gap_mult} = g, the gauge-sector dim)"
    )
    print(f"  top eigenvalue = {top} (mult {Lspec[top]} = f, the matter-sector dim)")
    assert gap == 24 and gap_mult == 15
    out["mass_gap"] = gap
    out["mass_gap_mult"] = gap_mult

    # cross-check: collinearity graph W Laplacian {0, 10^24, 16^15} (corpus)
    LW = degW * np.eye(n) - A_W
    LWspec = dict(
        sorted(Counter(int(round(x)) for x in np.linalg.eigvalsh(LW)).items())
    )
    print(
        f"\n[cross-check] W collinearity Laplacian spectrum {LWspec} "
        f"(corpus {{0,10^24,16^15}})"
    )
    out["W_laplacian_spectrum"] = {str(k): v for k, v in LWspec.items()}

    print("\nRESULT: the substrate's su(2) gauge theory on the matter graph Q has")
    print("  an EXACT, finite MASS GAP = f = 24 (the smallest nonzero Laplacian")
    print("  eigenvalue), forced by the strongly-regular/expander structure of Q.")
    print("  The Laplacian multiplicities ARE the Standard-Model sector sizes:")
    print("  gap eigenvalue 24=f at multiplicity g=15 (gauge), top 30 at f=24")
    print("  (matter). Confinement is structural -- the substrate fixes the gap to")
    print("  f with no continuum limit needed to see it is nonzero. The gauge")
    print("  (su(2)/Q) and gravity (whole spectrum) sectors share one finite")
    print("  spectrum whose gaps and multiplicities are substrate primitives.")

    out["result"] = (
        "matter-graph Q Laplacian spectrum {0, 24^15, 30^24}; mass "
        "gap = 24 = f at mult g=15; top 30 at mult f=24; the discrete "
        "su(2) gauge theory is exactly gapped (confining) by the SRG "
        "expander structure. Honest: discrete finite-theory gap, the "
        "substrate's exact shadow of the YM mass gap, not a continuum "
        "Millennium-problem proof."
    )
    out["sources"] = [
        "SRG(40,27,18,18) parameters; graph Laplacian = discrete "
        "gauge kinetic operator; Wilson lattice gauge theory"
    ]
    with open("data/w33_mass_gap_from_matter_graph.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_mass_gap_from_matter_graph.json")


if __name__ == "__main__":
    main()
