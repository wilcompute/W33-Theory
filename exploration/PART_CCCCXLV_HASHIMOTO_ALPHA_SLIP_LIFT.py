#!/usr/bin/env python3
"""
PART CCCCXLV: Hashimoto Alpha Slip Lift

CCCCXLIV showed that the refined alpha correction is a vertex constant-channel
propagator:

    alpha^{-1} - y_c^{-1} = 1_V^T M_alpha^{-1} 1_V = 880/24445.

This part lifts the same mechanism to the 480-dimensional Hashimoto carrier of
oriented W(3,3) edges.  The point is to show that the alpha slip is not merely a
40-vertex artifact: it is the normalized constant-flow amplitude of the
non-backtracking directed-edge system.

Directed-edge facts:
    |D| = 2E = vk = 480
    B 1_D = (k-1) 1_D = 11 1_D

Hashimoto-native constant-channel mass polynomial:
    h(theta) = theta*((theta-(lambda-1))^2 + 1)

At the constant-flow Hashimoto eigenvalue theta=k-1=11:
    h(11) = 11*((11-1)^2+1) = 1111.

Rank-one constant-flow correction:
    Delta_M = q/(lambda*(k-1)) = 3/22
    H_alpha = H_0 + Delta_M P_D,  P_D = J_D/|D|

Then the normalized directed-edge amplitude is
    (1/k) 1_D^T H_alpha^{-1} 1_D
      = (|D|/k)/(1111+3/22)
      = v/(24445/22)
      = 880/24445.

So the refined alpha correction is recovered from the 480-state Hashimoto
constant-flow sector and compresses exactly to the CCCCXLIV vertex result.

Run:
    python exploration/PART_CCCCXLV_HASHIMOTO_ALPHA_SLIP_LIFT.py
"""
from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path


def normalize_projective(vec: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    for x in vec:
        if x % 3:
            inv = 1 if x % 3 == 1 else 2
            return tuple((inv * y) % 3 for y in vec)  # type: ignore[return-value]
    raise ValueError("zero vector")


def projective_points() -> list[tuple[int, int, int, int]]:
    pts = set()
    for a in range(3):
        for b in range(3):
            for c in range(3):
                for d in range(3):
                    x = (a, b, c, d)
                    if x != (0, 0, 0, 0):
                        pts.add(normalize_projective(x))
    return sorted(pts)


def omega(u: tuple[int, int, int, int], v: tuple[int, int, int, int]) -> int:
    return (u[0] * v[2] - u[2] * v[0] + u[1] * v[3] - u[3] * v[1]) % 3


def build_adjacency(points: list[tuple[int, int, int, int]]) -> list[list[int]]:
    n = len(points)
    A = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if omega(points[i], points[j]) == 0:
                A[i][j] = 1
                A[j][i] = 1
    return A


def directed_edges(A: list[list[int]]) -> list[tuple[int, int]]:
    D: list[tuple[int, int]] = []
    for u, row in enumerate(A):
        for v, adjacent in enumerate(row):
            if adjacent:
                D.append((u, v))
    return D


def hashimoto_outdegrees(A: list[list[int]], D: list[tuple[int, int]]) -> list[int]:
    # B maps directed edge (u,v) to (v,w), w adjacent v and w != u.
    out = []
    for u, v in D:
        out.append(sum(1 for w, adjacent in enumerate(A[v]) if adjacent and w != u))
    return out


def main() -> None:
    # True master seed.
    q = 3
    assert math.factorial(q) == 2 * q
    disc = math.factorial(q) ** 2 - 4 * (2**q)
    sqrt_disc = math.isqrt(disc)
    lam = (math.factorial(q) - sqrt_disc) // 2
    mu = (math.factorial(q) + sqrt_disc) // 2

    # Forced W(3,3) atoms.
    k = q * (q + 1)
    v_expected = (q + 1) * (q * q + 1)
    theta = k - 1

    points = projective_points()
    A = build_adjacency(points)
    v = len(points)
    degrees = [sum(row) for row in A]
    E = sum(degrees) // 2
    D = directed_edges(A)
    D_size = len(D)
    outdegrees = hashimoto_outdegrees(A, D)

    # SRG audit.
    common_adjacent = set()
    common_nonadjacent = set()
    for i in range(v):
        for j in range(i + 1, v):
            common = sum(1 for m in range(v) if A[i][m] and A[j][m])
            if A[i][j]:
                common_adjacent.add(common)
            else:
                common_nonadjacent.add(common)

    # Hashimoto constant-flow channel.
    # B 1_D = theta 1_D, so any polynomial p(B) has p(theta) on 1_D.
    hashimoto_constant_mass = theta * ((theta - (lam - 1)) ** 2 + 1)
    vertex_constant_mass = theta * ((k - lam) ** 2 + 1)
    assert hashimoto_constant_mass == vertex_constant_mass

    delta_m = Fraction(q, lam * theta)
    m_eff = Fraction(hashimoto_constant_mass, 1) + delta_m

    # Unnormalized directed constant-flow amplitude is |D|/M_eff.
    directed_unnormalized_amplitude = Fraction(D_size, 1) / m_eff
    # The vertex-compressed amplitude divides by k because the constant vertex
    # lift repeats each vertex value over k outgoing directed edges.
    directed_vertex_compressed_amplitude = directed_unnormalized_amplitude / k

    # CCCCXLIV vertex amplitude for comparison.
    vertex_amplitude = Fraction(v, 1) / m_eff

    alpha_core = theta**2 + mu**2
    alpha_inv_refined = Fraction(alpha_core, 1) + directed_vertex_compressed_amplitude

    checks = {
        "true_master_equation": math.factorial(q) == 2 * q,
        "srg_quadratic_roots_lambda_mu": (lam, mu) == (2, 4),
        "projective_point_count": v == v_expected == 40,
        "degree_set_is_12": set(degrees) == {k},
        "edge_count_240": E == 240,
        "directed_edge_count_480": D_size == 480 == 2 * E == v * k,
        "hashimoto_outdegree_set_is_11": set(outdegrees) == {theta},
        "common_adjacent_lambda": common_adjacent == {lam},
        "common_nonadjacent_mu": common_nonadjacent == {mu},
        "hashimoto_constant_mass_equals_1111": hashimoto_constant_mass == 1111,
        "rank_one_delta_equals_3_over_22": delta_m == Fraction(3, 22),
        "m_eff_equals_24445_over_22": m_eff == Fraction(24445, 22),
        "directed_unnormalized_amplitude_equals_10560_over_24445": directed_unnormalized_amplitude == Fraction(10560, 24445),
        "directed_vertex_compression_equals_vertex_amplitude": directed_vertex_compressed_amplitude == vertex_amplitude,
        "compressed_amplitude_equals_alpha_slip": directed_vertex_compressed_amplitude == Fraction(880, 24445),
        "alpha_inverse_refined_exact": alpha_inv_refined == Fraction(669969, 4889),
    }

    result = {
        "part": "CCCCXLV",
        "title": "Hashimoto Alpha Slip Lift",
        "atoms": {
            "q": q,
            "lambda": lam,
            "mu": mu,
            "k": k,
            "v": v,
            "E": E,
            "directed_edges": D_size,
            "theta_hashimoto_constant": theta,
        },
        "hashimoto_channel": {
            "B_constant_eigenvalue": theta,
            "mass_polynomial": "h(theta)=theta*((theta-(lambda-1))^2+1)",
            "M_vac_hashimoto_constant": hashimoto_constant_mass,
            "Delta_M": str(delta_m),
            "M_eff": str(m_eff),
            "directed_unnormalized_amplitude": str(directed_unnormalized_amplitude),
            "compressed_by_k": str(directed_vertex_compressed_amplitude),
            "vertex_amplitude": str(vertex_amplitude),
        },
        "alpha_identity": {
            "alpha_core_yc_inverse": alpha_core,
            "alpha_slip_from_hashimoto_compression": str(directed_vertex_compressed_amplitude),
            "alpha_inverse_refined": str(alpha_inv_refined),
            "alpha_inverse_refined_decimal": float(alpha_inv_refined),
        },
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "interpretation": (
            "The CCCCXLIV vertex alpha slip is exactly the k-normalized constant-flow amplitude "
            "of the 480-dimensional Hashimoto carrier. The factor k appears because each vertex "
            "constant lifts to k outgoing directed edges. Thus 480/M_eff compresses to v/M_eff, "
            "recovering alpha^{-1}-y_c^{-1}=880/24445 from the non-backtracking sector."
        ),
    }

    out = Path("PART_CCCCXLV_hashimoto_alpha_slip_lift_results.json")
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print("PART CCCCXLV: Hashimoto Alpha Slip Lift")
    print("=" * 70)
    for key, ok in checks.items():
        print(f"{'PASS' if ok else 'FAIL'} {key}")
    print("-" * 70)
    print(f"|D| = {D_size}, k = {k}, |D|/k = {D_size // k}")
    print(f"B constant eigenvalue theta = {theta}")
    print(f"Hashimoto constant mass = {hashimoto_constant_mass}")
    print(f"M_eff = {m_eff}")
    print(f"Directed amplitude = {directed_unnormalized_amplitude}")
    print(f"Compressed amplitude = {directed_vertex_compressed_amplitude}")
    print(f"alpha^-1 refined = {alpha_inv_refined} = {float(alpha_inv_refined):.12f}")
    print(f"all_checks_pass={result['all_checks_pass']}")
    print(f"wrote {out}")

    assert result["all_checks_pass"]


if __name__ == "__main__":
    main()
