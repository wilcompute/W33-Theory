#!/usr/bin/env python3
"""
Pass 73 -- The Prime Geodesic Spectrum of W(3,3).

Pass 71 (Track E) computed the Ihara-zeta POLES of the W(3,3) collinearity graph and
confirmed the graph Riemann Hypothesis (all non-trivial poles on |u| = 1/sqrt(k-1)).
This pass builds the object that MAKES those poles mean something dynamical -- the
non-backtracking (Hashimoto) edge operator B -- and derives the PRIME GEODESIC THEOREM:
the exact counting law for closed primitive routes (periodic orbits) on the Holonet
fabric, with the Ramanujan property upgraded from a spectral fact to a hard ERROR BOUND.

Everything here is proved by exact finite computation and cross-checked two independent
ways (spectral closed form vs. direct integer walk counting; and pi(3) vs. the triangle
count of the strongly regular graph). ASCII-only output.

Objects
-------
* Graph G = collinearity graph of the symplectic generalized quadrangle W(3,3):
  points = 40 projective points of PG(3,3); x ~ y iff the symplectic form B(x,y)=0.
  This is SRG(40,12,2,4), adjacency spectrum {12^1, 2^24, (-4)^15}. (verified)
* Hashimoto operator B on the 480 directed edges (arcs): B[(u,v),(v,w)] = 1 iff w != u.
* N_m = tr(B^m) = # closed non-backtracking tailless walks of length m (with base arc).
* Primes p = equivalence classes of primitive closed backtrackless tailless cycles;
  pi(d) = # primes of length d. Relation:  N_m = sum_{d | m} d * pi(d),
  hence  m * pi(m) = sum_{d | m} mobius(m/d) * N_d   (Mobius inversion).

Theorems verified
-----------------
T1  Bass spectrum: eig(B) = { roots of mu^2 - lambda*mu + (k-1)=0 : lambda in spec(A) }
    union {+1, -1} each with multiplicity |E|-|V| = 200.  (k-1 = 11)
T2  Prime geodesic / graph-PNT: pi(m) is a positive integer ~ (k-1)^m / m, and
    m*pi(m) = sum_{d|m} mobius(m/d) N_d holds exactly for all tested m.
T3  Ramanujan error bound (graph RH made quantitative):
        | N_m - (k-1)^m - 1 - 200*(1 + (-1)^m) | <= 78 * (k-1)^(m/2)
    because every non-Perron, non-(+/-1) eigenvalue of B has modulus exactly sqrt(k-1).
T4  Combinatorial cross-check: pi(3) = 2 * (number of triangles of G).
"""

from __future__ import annotations

import json
import math
from itertools import product

import numpy as np

Q = 3
K = 12  # degree
KM1 = K - 1  # 11


# ---------- 1. build W(3,3) collinearity graph from the symplectic form ----------


def projective_points():
    """40 projective points of PG(3,3): nonzero GF(3)^4 vectors up to scale,
    canonicalized so the first nonzero coordinate is 1."""
    pts = []
    seen = set()
    for v in product(range(Q), repeat=4):
        if all(c == 0 for c in v):
            continue
        # canonical representative: scale so first nonzero coord == 1
        for c in v:
            if c != 0:
                inv = pow(c, Q - 2, Q)  # inverse mod 3
                break
        canon = tuple((inv * c) % Q for c in v)
        if canon not in seen:
            seen.add(canon)
            pts.append(canon)
    return pts


def symplectic(x, y):
    """Standard symplectic form on GF(3)^4: x1y2 - x2y1 + x3y4 - x4y3 (mod 3)."""
    return (x[0] * y[1] - x[1] * y[0] + x[2] * y[3] - x[3] * y[2]) % Q


def build_graph():
    pts = projective_points()
    n = len(pts)
    A = np.zeros((n, n), dtype=np.int64)
    for i in range(n):
        for j in range(n):
            if i != j and symplectic(pts[i], pts[j]) == 0:
                A[i, j] = 1
    return pts, A


def srg_params(A):
    n = A.shape[0]
    deg = int(A[0].sum())
    A2 = A @ A
    lam = None
    mu = None
    ok = True
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            common = int(A2[i, j])
            if A[i, j] == 1:
                if lam is None:
                    lam = common
                elif common != lam:
                    ok = False
            else:
                if mu is None:
                    mu = common
                elif common != mu:
                    ok = False
    return n, deg, lam, mu, ok


# ---------- 2. non-backtracking (Hashimoto) operator ----------


def build_hashimoto(A):
    n = A.shape[0]
    arcs = [(u, v) for u in range(n) for v in range(n) if A[u, v]]
    idx = {a: i for i, a in enumerate(arcs)}
    m = len(arcs)
    B = np.zeros((m, m), dtype=np.int64)
    for u, v in arcs:
        i = idx[(u, v)]
        for w in range(n):
            if A[v, w] and w != u:  # no backtrack
                B[i, idx[(v, w)]] = 1
    return arcs, B


# ---------- 3. prime counting via Mobius inversion ----------


def mobius(k):
    if k == 1:
        return 1
    result = 1
    d = 2
    kk = k
    while d * d <= kk:
        if kk % d == 0:
            kk //= d
            if kk % d == 0:
                return 0
            result = -result
        d += 1
    if kk > 1:
        result = -result
    return result


def divisors(m):
    return [d for d in range(1, m + 1) if m % d == 0]


def main():
    pts, A = build_graph()
    n, deg, lam, mu, srg_ok = srg_params(A)
    evals = sorted(np.rint(np.linalg.eigvalsh(A.astype(float))).astype(int).tolist())
    spec = {}
    for e in evals:
        spec[e] = spec.get(e, 0) + 1
    spec_ok = (
        n == 40
        and deg == 12
        and lam == 2
        and mu == 4
        and spec.get(12) == 1
        and spec.get(2) == 24
        and spec.get(-4) == 15
    )

    arcs, B = build_hashimoto(A)
    m_arcs = len(arcs)
    num_edges = m_arcs // 2

    # T1: Bass spectrum prediction from adjacency eigenvalues
    predicted = []
    for e in evals:
        disc = complex(e * e - 4 * KM1)
        r = math.sqrt(abs(disc)) if disc.real >= 0 else 0
        root1 = (e + (disc) ** 0.5) / 2
        root2 = (e - (disc) ** 0.5) / 2
        predicted.append(root1)
        predicted.append(root2)
    predicted += [1.0] * (num_edges - n) + [-1.0] * (num_edges - n)
    B_eig = np.linalg.eigvals(B.astype(float))

    # compare multisets by sorted modulus+phase (robust: sort by (round(re),round(im)))
    def canon(z):
        return (round(z.real, 4), round(z.imag, 4))

    pred_sorted = sorted((canon(complex(z)) for z in predicted))
    beig_sorted = sorted((canon(complex(z)) for z in B_eig))
    bass_ok = pred_sorted == beig_sorted

    # non-Perron, non +/-1 eigenvalues should have modulus sqrt(11) exactly
    moduli = sorted({round(abs(complex(z)), 6) for z in predicted})
    ramanujan_modulus_ok = all(
        (
            abs(abs(complex(z)) - math.sqrt(KM1)) < 1e-9
            or abs(abs(complex(z)) - 1.0) < 1e-9
            or abs(abs(complex(z)) - KM1) < 1e-9
        )
        for z in predicted
    )

    # T2/T3: N_m by exact integer trace of B^m
    MAXM = 12
    Bp = np.identity(m_arcs, dtype=np.int64)
    N = {}
    for mm in range(1, MAXM + 1):
        Bp = Bp @ B
        N[mm] = int(np.trace(Bp))

    # cross-check N_m against spectral sum (float)
    spectral_N = {}
    for mm in range(1, MAXM + 1):
        s = sum((complex(z)) ** mm for z in predicted)
        spectral_N[mm] = s.real
    spectral_ok = all(
        abs(N[mm] - spectral_N[mm]) < 1e-3 * max(1, abs(N[mm])) for mm in N
    )

    # prime counts
    pi = {}
    pi_int_ok = True
    pnt = {}
    for mm in range(1, MAXM + 1):
        s = sum(mobius(mm // d) * N[d] for d in divisors(mm))
        if s % mm != 0:
            pi_int_ok = False
        pval = s // mm
        pi[mm] = pval
        pnt[mm] = KM1**mm / mm
    pi_positive_ok = all(pi[mm] >= 0 for mm in pi if mm >= 3)

    # T3 error bound: |N_m - 11^m - 1 - 200(1+(-1)^m)| <= 78*11^(m/2)
    err_ok = True
    err_rows = []
    for mm in range(1, MAXM + 1):
        main_term = KM1**mm + 1 + 200 * (1 + (-1) ** mm)
        resid = abs(N[mm] - main_term)
        bound = 78 * KM1 ** (mm / 2)
        err_rows.append(
            {
                "m": mm,
                "residual": resid,
                "bound": round(bound, 3),
                "ok": resid <= bound + 1e-6,
            }
        )
        if resid > bound + 1e-6:
            err_ok = False

    # T4: triangle cross-check.  #triangles = trace(A^3)/6.
    A3 = np.linalg.matrix_power(A, 3)
    triangles = int(np.trace(A3) // 6)
    pi3_expected = 2 * triangles
    triangle_ok = pi[3] == pi3_expected

    # bonus: non-backtracking mixing gap vs simple-random-walk gap
    nb_second = math.sqrt(KM1)  # second-largest |eig(B)|
    nb_gap = KM1 - nb_second  # spectral gap of B (Perron 11)
    srw_gap = K - 2  # adjacency gap 12 - 2

    all_ok = (
        spec_ok
        and srg_ok
        and bass_ok
        and ramanujan_modulus_ok
        and spectral_ok
        and pi_int_ok
        and pi_positive_ok
        and err_ok
        and triangle_ok
    )

    print("=" * 74)
    print("PASS 73 -- PRIME GEODESIC SPECTRUM OF W(3,3)")
    print("=" * 74)
    print(
        f"[graph] SRG params (n,k,lambda,mu) = ({n},{deg},{lam},{mu})  regular&SRG={srg_ok}"
    )
    print(
        f"[graph] adjacency spectrum = 12^{spec.get(12)} 2^{spec.get(2)} (-4)^{spec.get(-4)}  ok={spec_ok}"
    )
    print(
        f"[edges] directed arcs={m_arcs}  undirected edges={num_edges}  |E|-|V|={num_edges-n}"
    )
    print(
        f"[T1] Bass spectrum of B matches mu^2 - lambda*mu + 11 roots (+/-1 x200): {bass_ok}"
    )
    print(
        f"[T1] all non-Perron/non-(+/-1) eigenvalues have modulus sqrt(11): {ramanujan_modulus_ok}"
    )
    print(f"[T2] N_m = tr(B^m) matches spectral sum: {spectral_ok}")
    print(
        f"[T2] m*pi(m) = sum mobius(m/d) N_d integer & pi>=0: {pi_int_ok and pi_positive_ok}"
    )
    print(f"[T3] Ramanujan error bound |N_m - 11^m - low| <= 78*11^(m/2): {err_ok}")
    print(
        f"[T4] pi(3) = 2 * #triangles: pi(3)={pi[3]}  2*tri={pi3_expected}  {triangle_ok}"
    )
    print()
    print(
        f"{'m':>3} {'N_m=tr(B^m)':>16} {'pi(m) primes':>14} {'(k-1)^m/m':>16} {'pi*m/(k-1)^m':>14}"
    )
    for mm in range(1, MAXM + 1):
        ratio = pi[mm] * mm / KM1**mm
        print(f"{mm:>3} {N[mm]:>16} {pi[mm]:>14} {pnt[mm]:>16.1f} {ratio:>14.5f}")
    print()
    print(f"[mixing] non-backtracking gap = 11 - sqrt(11) = {nb_gap:.5f}")
    print(f"[mixing] simple-random-walk adjacency gap = 12 - 2 = {srw_gap}")
    print(
        f"[mixing] Perron(B)=11=k-1, second modulus=sqrt(11)={nb_second:.5f} (Ramanujan/optimal)"
    )
    print()
    print("=" * 74)
    print(
        f"STATUS: {'PASS' if all_ok else 'FAIL'} -- prime geodesic theorem for W(3,3) verified,"
    )
    print("Ramanujan property upgraded to a quantitative periodic-orbit error bound.")
    print("=" * 74)

    payload = {
        "schema": "w33.pass73.prime_geodesics.v1",
        "status": "PASS" if all_ok else "FAIL",
        "graph": {
            "n": n,
            "k": deg,
            "lambda": lam,
            "mu": mu,
            "spectrum": {"12": spec.get(12), "2": spec.get(2), "-4": spec.get(-4)},
            "srg_verified": bool(srg_ok and spec_ok),
        },
        "hashimoto": {
            "arcs": m_arcs,
            "edges": num_edges,
            "genus_rank_EminusV": num_edges - n,
            "bass_spectrum_ok": bool(bass_ok),
            "all_nontrivial_modulus_sqrt11": bool(ramanujan_modulus_ok),
        },
        "N_m_trace_Bm": {str(k): v for k, v in N.items()},
        "pi_primes": {str(k): v for k, v in pi.items()},
        "graph_PNT_ratio": {str(k): round(pi[k] * k / KM1**k, 6) for k in pi},
        "ramanujan_error_bound": {
            "formula": "|N_m - 11^m - 1 - 200(1+(-1)^m)| <= 78*11^(m/2)",
            "rows": err_rows,
            "all_hold": bool(err_ok),
        },
        "triangle_crosscheck": {
            "triangles": triangles,
            "pi_3": pi[3],
            "expected_2x": pi3_expected,
            "ok": bool(triangle_ok),
        },
        "mixing": {
            "nonbacktracking_gap": round(nb_gap, 6),
            "srw_adjacency_gap": srw_gap,
            "perron": KM1,
            "second_modulus": round(nb_second, 6),
        },
        "interpretation": (
            "Closed non-backtracking routes on W(3,3) are the periodic orbits of "
            "the Holonet router; their count obeys the graph prime number theorem "
            "pi(m) ~ 11^m/m, and Ramanujan-ness bounds the fluctuation by "
            "78*11^(m/2) exactly -- the tightest possible (RH) error."
        ),
        "paper_reconciliation": (
            "Corrects w33_paper.tex 'Prime-Geodesic Expansion': pi_G(3) is 320 "
            "(oriented triangles = 2T), not the undirected triangle count T=160. "
            "Forced by the paper's own N_3=tr(B^3)=960 via N_m=sum_{d|m} d*pi(d) "
            "=> N_3=3*pi_G(3). This pass supplies the full pi_G(m) and the exact "
            "Ramanujan error bound, both absent from the paper (which stops at N_n~11^n)."
        ),
    }
    with open("w33_pass73_prime_geodesics.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print("[wrote] w33_pass73_prime_geodesics.json")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
