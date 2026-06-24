#!/usr/bin/env python3
"""
The substrate's spectrum as a periodic-orbit trace formula: closed geodesics are
particle worldlines, and the Ihara zeta's zeros sit on |u| = 1/sqrt(11) -- a
Riemann Hypothesis the substrate satisfies because it is Ramanujan.

Gutzwiller/Selberg: a quantum spectrum is dual to a sum over classical periodic
orbits. On a graph this duality is exact (Ihara-Bass): the closed non-backtracking
geodesics (the 'graph primes') are counted by the Hashimoto operator B, and
  N_m = Tr(B^m) = number of closed non-backtracking walks of length m,
while the spectral determinant factorizes as
  det(I - uB) = (1-u^2)^{|E|-|V|} det(I - uA + (k-1)u^2 I).
Each adjacency eigenvalue lambda contributes B-eigenvalues 1/u with
  (k-1)u^2 - lambda u + 1 = 0  =>  product of roots = 1/(k-1),
so a NON-TRIVIAL lambda (discriminant lambda^2 - 4(k-1) < 0) gives |u| = 1/sqrt(k-1)
and |B-eigenvalue| = sqrt(k-1). For W(3,3), k-1 = 11 (the Ihara prime), and the
non-trivial adjacency eigenvalues 2 and -4 satisfy 4,16 < 44, so EVERY non-trivial
zeta zero lies on the critical circle |u| = 1/sqrt(11): the graph Riemann
Hypothesis, equivalent to W(3,3) being Ramanujan.

Physics reading: the closed geodesics are the substrate's periodic orbits
(particle worldlines); the Ihara prime 11 = k-1 sets the topological entropy
ln(11) (max operator growth / butterfly rate); and the substrate satisfies an
exact Riemann Hypothesis -- its 'energy levels' (zeta zeros) all sit on one line.

Builds the Hashimoto B, verifies the spectrum (Perron k-1=11, the Euler factor
+-1, the non-trivial shell at |.|=sqrt(11)), and the periodic-orbit counts.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter

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
    adj = [[] for _ in range(n)]
    for i, j in itertools.combinations(range(n), 2):
        if sform(pts[i], pts[j]) == 0:
            adj[i].append(j)
            adj[j].append(i)
    k = len(adj[0])
    assert k == 12

    # directed edges and Hashimoto non-backtracking operator B
    edges = [(u, v) for u in range(n) for v in adj[u]]
    idx = {e: m for m, e in enumerate(edges)}
    E = len(edges)
    assert E == 480
    B = np.zeros((E, E))
    for a, b in edges:
        for c in adj[b]:
            if c != a:  # non-backtracking
                B[idx[(a, b)], idx[(b, c)]] = 1

    # spectrum of B
    bev = np.linalg.eigvals(B)
    mods = np.abs(bev)
    perron = mods.max()
    kk = k - 1
    sqrt_kk = np.sqrt(kk)
    # classify: Perron ~ 11, Euler shell ~1, non-trivial shell ~ sqrt(11)
    n_perron = int(np.sum(np.abs(mods - kk) < 1e-6))
    n_one = int(np.sum(np.abs(mods - 1.0) < 1e-6))
    n_sqrt = int(np.sum(np.abs(mods - sqrt_kk) < 1e-6))
    print(
        f"[Hashimoto B on W(3,3)]  {E}x{E}, Perron eigenvalue = {perron:.4f} "
        f"= k-1 = {kk}"
    )
    print(
        f"  spectral shells: |.|={kk} x{n_perron} (Perron), |.|=1 x{n_one} "
        f"(Euler factor |E|-|V|={E-n}), |.|=sqrt(11)={sqrt_kk:.4f} x{n_sqrt} "
        f"(non-trivial)"
    )
    assert abs(perron - kk) < 1e-6
    out["perron"] = kk
    out["euler_pm1_count"] = n_one
    out["nontrivial_sqrt11_count"] = n_sqrt

    # graph Riemann Hypothesis: all non-trivial zeros on |u|=1/sqrt(11)
    # i.e. all non-Perron, non-(+-1) B-eigenvalues have modulus sqrt(11)
    other = mods[(np.abs(mods - kk) > 1e-6) & (np.abs(mods - 1.0) > 1e-6)]
    on_circle = bool(np.all(np.abs(other - sqrt_kk) < 1e-6))
    print(
        f"\n[graph Riemann Hypothesis]  every non-trivial zeta zero on "
        f"|u|=1/sqrt(11): {on_circle}  (<=> Ramanujan)"
    )
    assert on_circle
    out["graph_RH_holds"] = on_circle

    # periodic-orbit (closed non-backtracking walk) counts N_m = Tr(B^m)
    print(f"\n[periodic orbits]  N_m = Tr(B^m) = closed non-backtracking walks:")
    Bp = np.eye(E)
    Ns = []
    for m in range(1, 9):
        Bp = Bp @ B
        Nm = int(round(np.trace(Bp).real))
        Ns.append(Nm)
        print(f"  m={m}: N_m = {Nm}")
    out["periodic_orbit_counts_N1_8"] = Ns
    # topological entropy = ln(Perron) = ln(k-1)
    h_top = np.log(kk)
    print(
        f"\n[topological entropy]  h = ln(k-1) = ln(11) = {h_top:.4f} "
        f"(max operator-growth / butterfly rate; the Ihara prime is 11)"
    )
    out["topological_entropy"] = round(float(h_top), 4)

    print("\nRESULT: the substrate is a Gutzwiller/Selberg system whose periodic")
    print("  orbits are the closed non-backtracking geodesics (particle worldlines)")
    print("  counted by N_m = Tr(B^m). Its Ihara zeta factorizes into a trivial")
    print("  Euler part (eigenvalues +-1) and a non-trivial part whose zeros ALL sit")
    print("  on the critical circle |u| = 1/sqrt(11): an exact Riemann Hypothesis,")
    print("  equivalent to W(3,3) being Ramanujan. The Ihara prime 11 = k-1 sets the")
    print("  topological entropy ln(11). So the substrate's 'energy levels' lie on a")
    print("  single line and its particle content is a periodic-orbit trace formula.")

    out["summary"] = (
        "Hashimoto B on W(3,3): Perron k-1=11, Euler shell +-1, all "
        "non-trivial zeta zeros on |u|=1/sqrt(11) (graph Riemann "
        "Hypothesis <=> Ramanujan); periodic orbits N_m=Tr(B^m) = "
        "closed geodesics = particle worldlines; topological entropy "
        "ln(11), Ihara prime 11=k-1. Gutzwiller/Selberg trace-formula "
        "reading of the substrate spectrum."
    )
    out["sources"] = [
        "Ihara zeta / Ihara-Bass formula; Terras, Zeta functions of "
        "graphs; Gutzwiller & Selberg trace formulas; Ramanujan graphs "
        "(graph Riemann Hypothesis)"
    ]
    with open("data/w33_periodic_orbit_spectrum.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_periodic_orbit_spectrum.json")


if __name__ == "__main__":
    main()
