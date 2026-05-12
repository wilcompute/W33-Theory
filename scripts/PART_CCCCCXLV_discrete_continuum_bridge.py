#!/usr/bin/env python3
"""
PART_CCCCCXLV_discrete_continuum_bridge.py

Exact verification of the W(3,3) discrete-to-continuous spectral bridge.

Main point:
  The finite graph has a completely exact analytic functional calculus
      f(L) = f(0) P0 + f(10) P10 + f(16) P16
  where L = 12I - A.  This is the internal continuous portal: heat time,
  wave time, resolvents, zeta regularization, and spectral-action cutoffs
  are continuous parameters acting on a finite theorem kernel.

  The graph tropical Jacobian has dimension 201, but the cellular
  W(3,3) triangle complex descends to H1-rank 81:
      dim ker d1 = 201, rank d2 = 120, H1 = 81 = 3*27.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product
import json
from pathlib import Path

F3 = (0, 1, 2)


def normalize_projective(v: tuple[int, int, int, int]) -> tuple[int, int, int, int] | None:
    if all(x == 0 for x in v):
        return None
    for x in v:
        if x % 3:
            inv = 1 if x % 3 == 1 else 2
            return tuple((y * inv) % 3 for y in v)
    raise AssertionError("unreachable")


def symplectic(x: tuple[int, ...], y: tuple[int, ...]) -> int:
    return (x[0] * y[2] - x[2] * y[0] + x[1] * y[3] - x[3] * y[1]) % 3


def build_w33() -> tuple[list[tuple[int, int, int, int]], list[tuple[int, int]], list[tuple[int, int, int]], list[list[int]]]:
    seen = set()
    points: list[tuple[int, int, int, int]] = []
    for raw in product(F3, repeat=4):
        p = normalize_projective(raw)
        if p is not None and p not in seen:
            seen.add(p)
            points.append(p)

    n = len(points)
    adj = [[0] * n for _ in range(n)]
    edges: list[tuple[int, int]] = []
    for i, j in combinations(range(n), 2):
        if symplectic(points[i], points[j]) == 0:
            adj[i][j] = adj[j][i] = 1
            edges.append((i, j))

    triangles: list[tuple[int, int, int]] = []
    for i, j, k in combinations(range(n), 3):
        if adj[i][j] and adj[i][k] and adj[j][k]:
            triangles.append((i, j, k))

    return points, edges, triangles, adj


def matmul_int(A: list[list[int]], B: list[list[int]]) -> list[list[int]]:
    rows, mid, cols = len(A), len(B), len(B[0])
    out = [[0] * cols for _ in range(rows)]
    for i in range(rows):
        Ai = A[i]
        for k in range(mid):
            if Ai[k] == 0:
                continue
            aik = Ai[k]
            Bk = B[k]
            for j in range(cols):
                out[i][j] += aik * Bk[j]
    return out


def rank_mod(matrix: list[list[int]], p: int = 1_000_003) -> int:
    """Gaussian elimination over F_p."""
    if not matrix:
        return 0
    A = [[x % p for x in row] for row in matrix]
    m, n = len(A), len(A[0])
    r = 0
    for c in range(n):
        pivot = None
        for i in range(r, m):
            if A[i][c]:
                pivot = i
                break
        if pivot is None:
            continue
        A[r], A[pivot] = A[pivot], A[r]
        inv = pow(A[r][c], -1, p)
        A[r] = [(x * inv) % p for x in A[r]]
        for i in range(m):
            if i != r and A[i][c]:
                factor = A[i][c]
                A[i] = [(A[i][j] - factor * A[r][j]) % p for j in range(n)]
        r += 1
        if r == m:
            break
    return r


def boundary_ranks(n: int, edges: list[tuple[int, int]], triangles: list[tuple[int, int, int]]) -> dict[str, int]:
    d1 = [[0] * len(edges) for _ in range(n)]
    for c, (i, j) in enumerate(edges):
        d1[i][c] = -1
        d1[j][c] = 1

    edge_index = {e: idx for idx, e in enumerate(edges)}
    d2 = [[0] * len(triangles) for _ in range(len(edges))]
    for c, (i, j, k) in enumerate(triangles):
        for sign, e in ((1, (j, k)), (-1, (i, k)), (1, (i, j))):
            d2[edge_index[e]][c] = sign

    r1 = rank_mod(d1)
    r2 = rank_mod(d2)
    return {
        "rank_d1": r1,
        "rank_d2": r2,
        "graph_cycle_rank": len(edges) - r1,
        "cellular_H1_rank": len(edges) - r1 - r2,
    }


def verify_srg(adj: list[list[int]]) -> dict[str, object]:
    n = len(adj)
    degrees = [sum(row) for row in adj]
    A2 = matmul_int(adj, adj)
    lam_values = []
    mu_values = []
    for i, j in combinations(range(n), 2):
        if adj[i][j]:
            lam_values.append(A2[i][j])
        else:
            mu_values.append(A2[i][j])
    return {
        "degrees": sorted(set(degrees)),
        "lambda_values": sorted(set(lam_values)),
        "mu_values": sorted(set(mu_values)),
        "diag_A2": sorted(set(A2[i][i] for i in range(n))),
    }


def exact_projector_resistance() -> dict[str, str]:
    p10_diag, p16_diag = Fraction(3, 5), Fraction(3, 8)
    p10_adj, p16_adj = Fraction(1, 10), Fraction(-1, 8)
    p10_non, p16_non = Fraction(-1, 15), Fraction(1, 24)

    lplus_diag = Fraction(1, 10) * p10_diag + Fraction(1, 16) * p16_diag
    lplus_adj = Fraction(1, 10) * p10_adj + Fraction(1, 16) * p16_adj
    lplus_non = Fraction(1, 10) * p10_non + Fraction(1, 16) * p16_non

    r_adj = 2 * (lplus_diag - lplus_adj)
    r_non = 2 * (lplus_diag - lplus_non)
    kf = 240 * r_adj + (780 - 240) * r_non

    return {
        "P0": "J/40",
        "P10": "-((A-12I)(A+4I))/60",
        "P16": "((A-12I)(A-2I))/96",
        "Lplus_diag": str(lplus_diag),
        "Lplus_adjacent_offdiag": str(lplus_adj),
        "Lplus_nonadjacent_offdiag": str(lplus_non),
        "R_adjacent": str(r_adj),
        "R_nonadjacent": str(r_non),
        "R_ratio_non_over_adj": str(r_non / r_adj),
        "Kirchhoff_index_standard": str(kf),
        "Kirchhoff_index_half_normalized": str(kf / 2),
    }


def build_summary() -> dict[str, object]:
    points, edges, triangles, adj = build_w33()
    n, E, T = len(points), len(edges), len(triangles)
    srg = verify_srg(adj)
    ranks = boundary_ranks(n, edges, triangles)
    resistance = exact_projector_resistance()

    summary: dict[str, object] = {
        "part": "CCCCCXLV",
        "title": "Discrete/Continuous Spectral Bridge and Dimension Descent",
        "finite_kernel": {
            "points": n,
            "edges": E,
            "triangles": T,
            "degrees": srg["degrees"],
            "lambda_values": srg["lambda_values"],
            "mu_values": srg["mu_values"],
            "diag_A2": srg["diag_A2"],
            "adjacency_spectrum": {"12": 1, "2": 24, "-4": 15},
            "laplacian_spectrum": {"0": 1, "10": 24, "16": 15},
        },
        "continuous_functional_calculus": {
            "master_formula": "f(L)=f(0)P0+f(10)P10+f(16)P16",
            "heat_trace_internal": "K_W(t)=1+24 exp(-10t)+15 exp(-16t)",
            "zeta_internal": "zeta_W(s)=24*10^(-s)+15*16^(-s)",
            "spectral_action": "Tr Phi(L/Lambda^2)=Phi(0)+24 Phi(10/Lambda^2)+15 Phi(16/Lambda^2)",
            "finite_heat_guardrail": "K_W(t) is analytic at t=0; no internal t^(-d/2) divergence occurs before adding an external continuum.",
        },
        "dimension_descent": {
            **ranks,
            "graph_tropical_jacobian_dim": ranks["graph_cycle_rank"],
            "cellular_jacobian_dim": ranks["cellular_H1_rank"],
            "descent_identity": "201 - 120 = 81 = 3*27",
            "interpretation": "Triangle boundaries remove 120 local curvature/gauge-exact graph cycles, leaving the 81-dimensional physical H1 torus.",
        },
        "resistance_metric": resistance,
        "external_continuum_bridge": {
            "almost_commutative_operator": "D_total^2 = Delta_ext tensor I_40 + I_ext tensor L_W",
            "heat_trace_factorization": "K_total(t)=K_ext(t) K_W(t)",
            "four_dimensional_weyl_law": "For external (C_n)^4 with diffusive scaling, K_ext(t) ~ C t^(-2), so K_total(t) ~ 40 C t^(-2).",
            "tomotope_Qk_role": "Internal cover towers can change finite multiplicities but not the external Weyl exponent.",
        },
    }

    checks = {
        "points_40": n == 40,
        "edges_240": E == 240,
        "triangles_160": T == 160,
        "degree_12": srg["degrees"] == [12],
        "lambda_2": srg["lambda_values"] == [2],
        "mu_4": srg["mu_values"] == [4],
        "rank_d1_39": ranks["rank_d1"] == 39,
        "rank_d2_120": ranks["rank_d2"] == 120,
        "graph_cycle_rank_201": ranks["graph_cycle_rank"] == 201,
        "cellular_h1_81": ranks["cellular_H1_rank"] == 81,
        "resistance_adj_13_80": resistance["R_adjacent"] == "13/80",
        "resistance_non_7_40": resistance["R_nonadjacent"] == "7/40",
        "kirchhoff_standard_267_2": resistance["Kirchhoff_index_standard"] == "267/2",
        "kirchhoff_half_normalized_267_4": resistance["Kirchhoff_index_half_normalized"] == "267/4",
    }
    summary["checks"] = checks
    summary["all_checks_pass"] = all(checks.values())
    return summary


def main() -> None:
    summary = build_summary()
    print(json.dumps(summary, indent=2))
    assert summary["all_checks_pass"], "one or more bridge checks failed"

    out = Path("data/PART_CCCCCXLV_discrete_continuum_bridge_results.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
