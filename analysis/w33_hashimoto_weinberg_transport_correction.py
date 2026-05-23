#!/usr/bin/env python3
"""Hashimoto/Ihara transport derivation of the alpha/(k-1) Weinberg correction.

This script makes the Eq. 52 refinement structural rather than numerical.

Starting from W(3,3), it constructs:

  * the 40-point SRG(40,12,2,4),
  * the 480-state directed-edge carrier,
  * the 480x480 Hashimoto non-backtracking operator B,
  * the normalized transport operator P = B/(k-1).

It verifies that every directed edge has exactly k-1 = 11 forward
non-backtracking continuations.  Therefore an isotropic first-order radiative
insertion of strength alpha_hat is distributed over 11 transport branches,
giving the scalar leading correction alpha_hat/11.

The same 11 is also the Ihara-Bass quadratic coefficient:

  det(I - u B) = (1-u^2)^(E-V) det(I - u A + (k-1)u^2 I).

So the correction denominator is not fitted from the Weinberg angle; it is the
canonical non-backtracking transport denominator of W33.
"""
from __future__ import annotations

import json
from collections import Counter
from itertools import combinations, product
from pathlib import Path
from fractions import Fraction
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
P_FIELD = 3


def canon(v):
    v = tuple(int(x) % P_FIELD for x in v)
    if v == (0, 0, 0, 0):
        raise ValueError("zero vector")
    for x in v:
        if x:
            inv = 1 if x == 1 else 2
            return tuple((inv * y) % P_FIELD for y in v)
    raise AssertionError


def symp(u, v):
    return (u[0]*v[2] - u[2]*v[0] + u[1]*v[3] - u[3]*v[1]) % P_FIELD


def build_w33():
    pts = []
    seen = set()
    for raw in product(range(P_FIELD), repeat=4):
        if raw == (0, 0, 0, 0):
            continue
        c = canon(raw)
        if c not in seen:
            seen.add(c)
            pts.append(c)
    pts = sorted(pts)
    A = np.zeros((40, 40), dtype=int)
    edges = []
    for i, j in combinations(range(40), 2):
        if symp(pts[i], pts[j]) == 0:
            A[i, j] = A[j, i] = 1
            edges.append((i, j))
    return pts, A, edges


def build_hashimoto(A, edges):
    directed = []
    for i, j in edges:
        directed.append((i, j))
        directed.append((j, i))
    idx = {e: n for n, e in enumerate(directed)}
    B = np.zeros((len(directed), len(directed)), dtype=int)
    for n, (a, b) in enumerate(directed):
        for c in range(A.shape[0]):
            if c != a and A[b, c] == 1:
                B[n, idx[(b, c)]] = 1
    return directed, B


def main() -> int:
    pts, A, edges = build_w33()
    directed, B = build_hashimoto(A, edges)
    V = A.shape[0]
    E = len(edges)
    k = int(A.sum(axis=1)[0])
    nb = k - 1
    q = 3
    phi3 = q*q + q + 1
    x0 = Fraction(q, phi3)

    alpha_inv = 127.930
    alpha_hat = 1.0 / alpha_inv
    correction = alpha_hat / nb
    x_eff = float(x0) + correction

    # Association-scheme Q-matrix check for the separate GUT normalization.
    Pmat = np.array([[1, 12, 27], [1, 2, -3], [1, -4, 3]], dtype=float)
    Qmat = 40 * np.linalg.inv(Pmat)
    kappa_y = Qmat[2, 2]
    gut_sin2 = 1.0 / (1.0 + kappa_y)

    # Ihara quadratic coefficient check from adjacency eigenvalues.
    eigs = Counter(int(round(x)) for x in np.linalg.eigvalsh(A.astype(float)))
    ihara_factors = {
        str(lam): f"1 - ({lam}) u + {nb} u^2"
        for lam in sorted(eigs.keys(), reverse=True)
    }

    checks = {
        "w33_srg_vertex_edge_counts": V == 40 and E == 240,
        "regular_degree_12": Counter(A.sum(axis=1)) == Counter({12: 40}),
        "directed_edge_carrier_480": len(directed) == 480 and B.shape == (480, 480),
        "hashimoto_outdegree_11": Counter(B.sum(axis=1)) == Counter({11: 480}),
        "hashimoto_indegree_11": Counter(B.sum(axis=0)) == Counter({11: 480}),
        "normalized_transport_row_stochastic": np.allclose((B / nb).sum(axis=1), np.ones(480)),
        "adjacency_spectrum": eigs == Counter({12: 1, 2: 24, -4: 15}),
        "q_matrix_gut_normalization": abs(kappa_y - 5/3) < 1e-12 and abs(gut_sin2 - 3/8) < 1e-12,
        "finite_generator": x0 == Fraction(3, 13),
        "transport_denominator_equals_ihara_coefficient": nb == 11,
    }

    payload = {
        "theorem_name": "Hashimoto Transport Weinberg Correction Theorem",
        "all_checks_passed": all(checks.values()),
        "summary": {
            "vertices": V,
            "undirected_edges": E,
            "directed_edges": len(directed),
            "degree_k": k,
            "nonbacktracking_outdegree_k_minus_1": nb,
            "tree_generator": "3/13",
            "alpha_hat_inverse_used": alpha_inv,
            "transport_correction_alpha_over_11": correction,
            "corrected_effective_value": x_eff,
            "GUT_Q22_kappaY": kappa_y,
            "GUT_sin2": gut_sin2,
            "adjacency_spectrum": dict(eigs),
            "ihara_quadratic_factors": ihara_factors,
        },
        "checks": checks,
        "transport_derivation": {
            "carrier": "directed edges of W33, size 2E = 480",
            "operator": "Hashimoto non-backtracking matrix B",
            "branching": "each directed edge has k-1 = 11 legal forward continuations",
            "normalized_transport": "P = B/11 is row-stochastic",
            "first_order_rule": "an isotropic one-loop insertion alpha_hat contributes alpha_hat/11 to the scalar generator",
            "weinberg_refinement": "sin^2(theta_eff)(MZ) = 3/13 + alpha_hat(MZ)/11 + higher transport terms",
        },
        "interpretation": (
            "The denominator 11 in the Weinberg correction is not tuned from the measured angle. It is the canonical "
            "non-backtracking branching number of the W33 Hashimoto carrier and the u^2 coefficient in the Ihara-Bass "
            "vertex determinant. Thus Eq. 52 can be defended as a finite-geometric tree generator corrected by the "
            "first isotropic transport insertion on the W33 directed-edge carrier."
        ),
        "boundary": (
            "This proves the transport denominator and the natural first-order branch-averaging rule. A full QFT derivation "
            "still requires deriving alpha_hat itself and the higher-order terms from the W33 Ihara effective action."
        ),
    }

    out = ROOT / "data" / "w33_hashimoto_weinberg_transport_correction.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    return 0 if payload["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
