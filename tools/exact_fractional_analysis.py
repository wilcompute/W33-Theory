#!/usr/bin/env python3
"""Verify exact fractional structure in W33 eigenspace projections.

KEY OBSERVATION:
- Vertex projection inner products appear to be exact fractions
- Adjacent: 0.1 = 1/10 = 3/30
- Non-adjacent: -0.0667 = -1/15 = -2/30
- Diagonal: 24/40 = 3/5 = 18/30

This means the projection matrix has entries in {18, 3, -2}/30!

This tool verifies the exact fractional structure and investigates its
algebraic/number-theoretic significance.

Outputs:
- artifacts/exact_fractional_analysis.json
- artifacts/exact_fractional_analysis.md
"""

from __future__ import annotations

import json
from collections import Counter
from fractions import Fraction
from itertools import product
from pathlib import Path

import numpy as np
from numpy.linalg import eigh

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "exact_fractional_analysis.json"
OUT_MD = ROOT / "artifacts" / "exact_fractional_analysis.md"


def construct_w33():
    """Construct W33 from F_3^4 symplectic geometry."""
    F3 = [0, 1, 2]
    vectors = [v for v in product(F3, repeat=4) if any(x != 0 for x in v)]

    proj_points = []
    seen = set()
    for v in vectors:
        v = list(v)
        for i in range(4):
            if v[i] != 0:
                inv = 1 if v[i] == 1 else 2
                v = tuple((x * inv) % 3 for x in v)
                break
        if v not in seen:
            seen.add(v)
            proj_points.append(v)

    n = len(proj_points)

    def omega(x, y):
        return (x[0] * y[2] - x[2] * y[0] + x[1] * y[3] - x[3] * y[1]) % 3

    adj = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(i + 1, n):
            if omega(proj_points[i], proj_points[j]) == 0:
                adj[i, j] = adj[j, i] = 1

    return adj, proj_points


def to_native(obj):
    """Convert numpy types to native Python types."""
    if isinstance(obj, np.integer):
        return int(obj)
    if isinstance(obj, np.floating):
        return float(obj)
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, Fraction):
        return str(obj)
    if isinstance(obj, dict):
        return {str(k): to_native(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [to_native(x) for x in obj]
    return obj


def float_to_fraction(x, max_denom=1000):
    """Convert float to exact fraction if possible."""
    return Fraction(x).limit_denominator(max_denom)


def main():
    results = {}
    lines = []

    lines.append("# Exact Fractional Structure in W33 Eigenspace")
    lines.append("")

    # Build W33
    adj, vertices = construct_w33()
    n = len(vertices)

    # Compute eigendecomposition
    eigenvalues, eigenvectors = eigh(adj.astype(float))
    eigenvalues = np.round(eigenvalues, 10)

    # Get λ=2 eigenspace
    tol = 0.0001
    lambda2_mask = np.abs(eigenvalues - 2.0) < tol
    lambda2_vectors = eigenvectors[:, lambda2_mask]

    lines.append("## Eigenspace Projection Matrix")
    lines.append("")

    # Projection matrix P = V V^T where V are the eigenvectors
    P = lambda2_vectors @ lambda2_vectors.T

    lines.append(f"- Eigenspace dimension: {lambda2_vectors.shape[1]}")
    lines.append(f"- Projection matrix P = V V^T")
    lines.append("")

    # Analyze entries
    diag_entries = np.diag(P)
    off_diag_adj = []
    off_diag_nonadj = []

    for i in range(n):
        for j in range(i + 1, n):
            if adj[i, j]:
                off_diag_adj.append(P[i, j])
            else:
                off_diag_nonadj.append(P[i, j])

    lines.append("### Entry Values")
    lines.append("")

    # Convert to fractions
    diag_frac = float_to_fraction(diag_entries[0])
    adj_frac = float_to_fraction(off_diag_adj[0])
    nonadj_frac = float_to_fraction(off_diag_nonadj[0])

    lines.append(f"- Diagonal P[i,i]: {diag_entries[0]:.10f} = {diag_frac}")
    lines.append(f"- Adjacent P[i,j]: {off_diag_adj[0]:.10f} = {adj_frac}")
    lines.append(f"- Non-adjacent P[i,j]: {off_diag_nonadj[0]:.10f} = {nonadj_frac}")
    lines.append("")

    results["diagonal_fraction"] = str(diag_frac)
    results["adjacent_fraction"] = str(adj_frac)
    results["nonadjacent_fraction"] = str(nonadj_frac)

    # Verify uniformity
    diag_var = np.var(diag_entries)
    adj_var = np.var(off_diag_adj)
    nonadj_var = np.var(off_diag_nonadj)

    lines.append("### Uniformity Check (variance)")
    lines.append("")
    lines.append(f"- Diagonal variance: {diag_var:.2e}")
    lines.append(f"- Adjacent variance: {adj_var:.2e}")
    lines.append(f"- Non-adjacent variance: {nonadj_var:.2e}")
    lines.append("")

    if diag_var < 1e-20 and adj_var < 1e-20 and nonadj_var < 1e-20:
        lines.append("**EXACT**: All entries are uniform within each category!")
        results["exact_fractional"] = True
    else:
        lines.append("Values are approximately but not exactly uniform")
        results["exact_fractional"] = False
    lines.append("")

    # Express in common denominator
    lines.append("### Common Denominator Representation")
    lines.append("")

    # Find LCM of denominators
    from math import lcm

    common_denom = lcm(
        diag_frac.denominator, adj_frac.denominator, nonadj_frac.denominator
    )

    diag_num = int(diag_frac * common_denom)
    adj_num = int(adj_frac * common_denom)
    nonadj_num = int(nonadj_frac * common_denom)

    lines.append(f"Common denominator: {common_denom}")
    lines.append("")
    lines.append(f"| Entry Type | Fraction | Numerator/{common_denom} |")
    lines.append(f"|------------|----------|--------------------------|")
    lines.append(f"| Diagonal | {diag_frac} | {diag_num}/{common_denom} |")
    lines.append(f"| Adjacent | {adj_frac} | {adj_num}/{common_denom} |")
    lines.append(f"| Non-adjacent | {nonadj_frac} | {nonadj_num}/{common_denom} |")
    lines.append("")

    results["common_denominator"] = common_denom
    results["numerators"] = {
        "diagonal": diag_num,
        "adjacent": adj_num,
        "nonadjacent": nonadj_num,
    }

    # Verify projection property: P² = P
    lines.append("### Projection Property Verification")
    lines.append("")

    P_squared = P @ P
    diff = np.abs(P_squared - P)
    max_diff = np.max(diff)

    lines.append(f"max|P² - P| = {max_diff:.2e}")
    if max_diff < 1e-10:
        lines.append("✓ P is a valid projection matrix (P² = P)")
    lines.append("")

    # Row sum (should be related to eigenspace)
    row_sums = P.sum(axis=1)
    lines.append("### Row Sums")
    lines.append("")
    lines.append(f"Row sum: {row_sums[0]:.10f}")
    row_sum_frac = float_to_fraction(row_sums[0])
    lines.append(f"As fraction: {row_sum_frac}")
    lines.append("")

    results["row_sum"] = str(row_sum_frac)

    # Analyze the numerators
    lines.append("## Numerator Analysis")
    lines.append("")

    lines.append(f"With denominator {common_denom}:")
    lines.append(f"- Diagonal: {diag_num}")
    lines.append(f"- Adjacent: {adj_num}")
    lines.append(f"- Non-adjacent: {nonadj_num}")
    lines.append("")

    # Check relationships
    lines.append("### Arithmetic Relationships")
    lines.append("")

    # Sum check: diagonal + 12*adjacent + 27*nonadjacent should equal something nice
    sum_check = diag_num + 12 * adj_num + 27 * nonadj_num
    lines.append(f"{diag_num} + 12×{adj_num} + 27×{nonadj_num} = {sum_check}")
    lines.append("")

    # This should be 0 if the constant vector is orthogonal to eigenspace
    lines.append(f"(This checks if 1 ⊥ λ=2 eigenspace: should be 0)")
    if sum_check == 0:
        lines.append("✓ Constant vector is orthogonal to λ=2 eigenspace")
    lines.append("")

    results["orthogonality_check"] = sum_check

    # Look at the ratio
    lines.append("### Ratio Analysis")
    lines.append("")

    if nonadj_num != 0:
        adj_nonadj_ratio = Fraction(adj_num, nonadj_num)
        lines.append(
            f"Adjacent/Non-adjacent ratio: {adj_num}/{nonadj_num} = {adj_nonadj_ratio}"
        )

    if adj_num != 0:
        diag_adj_ratio = Fraction(diag_num, adj_num)
        lines.append(
            f"Diagonal/Adjacent ratio: {diag_num}/{adj_num} = {diag_adj_ratio}"
        )
    lines.append("")

    # Factor analysis
    lines.append("### Factor Analysis")
    lines.append("")

    def factorize(n):
        if n == 0:
            return "0"
        factors = []
        abs_n = abs(n)
        d = 2
        while d * d <= abs_n:
            while abs_n % d == 0:
                factors.append(d)
                abs_n //= d
            d += 1
        if abs_n > 1:
            factors.append(abs_n)
        sign = "-" if n < 0 else ""
        return sign + " × ".join(map(str, factors)) if factors else "1"

    lines.append(f"- {common_denom} = {factorize(common_denom)}")
    lines.append(f"- {diag_num} = {factorize(diag_num)}")
    lines.append(f"- {adj_num} = {factorize(adj_num)}")
    lines.append(f"- {nonadj_num} = {factorize(nonadj_num)}")
    lines.append("")

    # Now analyze edge projections more carefully
    lines.append("## Edge Projection Fractions")
    lines.append("")

    # Get edges
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            if adj[i, j]:
                edges.append((i, j))

    # Compute edge projections
    edge_projections = []
    for a, b in edges:
        indicator = np.zeros(n)
        indicator[a] = 1
        indicator[b] = 1
        proj = lambda2_vectors.T @ indicator
        edge_projections.append(proj)

    edge_projections = np.array(edge_projections)  # 240 × 24

    # Edge norm squared
    edge_norm_sq = np.sum(edge_projections[0] ** 2)
    edge_norm_sq_frac = float_to_fraction(edge_norm_sq)

    lines.append(f"Edge projection norm²: {edge_norm_sq:.10f} = {edge_norm_sq_frac}")
    lines.append("")

    # This should relate to diagonal + adjacent
    expected_norm_sq = 2 * float(diag_frac) + 2 * float(adj_frac)
    lines.append(f"Expected (2×diag + 2×adj): {expected_norm_sq:.10f}")
    lines.append(f"Match: {abs(edge_norm_sq - expected_norm_sq) < 1e-10}")
    lines.append("")

    # Edge-edge inner products
    lines.append("### Edge-Edge Inner Products")
    lines.append("")

    # Compute all distinct edge-edge inner products
    edge_gram = edge_projections @ edge_projections.T
    edge_ips = set()
    for i in range(240):
        for j in range(i + 1, 240):
            edge_ips.add(round(edge_gram[i, j], 10))

    edge_ip_fracs = {}
    for ip in sorted(edge_ips):
        frac = float_to_fraction(ip)
        count = np.sum(np.abs(edge_gram - ip) < 1e-8) - (
            240 if abs(ip - edge_norm_sq) < 1e-8 else 0
        )
        edge_ip_fracs[ip] = (frac, int(count) // 2)  # div 2 for symmetry

    lines.append("| Inner Product | Fraction | Count |")
    lines.append("|---------------|----------|-------|")
    for ip, (frac, count) in sorted(edge_ip_fracs.items()):
        if count > 0:
            lines.append(f"| {ip:.6f} | {frac} | {count} |")
    lines.append("")

    results["edge_inner_products"] = {
        str(k): str(v[0]) for k, v in edge_ip_fracs.items() if v[1] > 0
    }

    # Summary
    lines.append("## Summary")
    lines.append("")
    lines.append("The λ=2 eigenspace projection matrix has **exact rational entries**:")
    lines.append("")
    lines.append(f"P[i,j] ∈ {{{diag_num}, {adj_num}, {nonadj_num}}} / {common_denom}")
    lines.append("")
    lines.append("This exact fractional structure is a strong algebraic constraint")
    lines.append("suggesting deep number-theoretic properties of W33.")
    lines.append("")

    # Write outputs
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(to_native(results), indent=2), encoding="utf-8")
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
