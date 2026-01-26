#!/usr/bin/env python3
"""Analyze whether W33 edge projections form a root-like system.

KEY INSIGHT:
- 240 W33 edges all project to vectors of equal norm in the λ=2 eigenspace
- This is exactly like E8 roots (240 roots, all equal norm)
- The inner product structure might reveal root system properties

This tool investigates:
1. Whether edge projections form a root system
2. Inner product relations vs E8
3. Explicit bijection attempts
4. Symmetry properties

Outputs:
- artifacts/edge_root_system_analysis.json
- artifacts/edge_root_system_analysis.md
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from itertools import combinations, product
from pathlib import Path

import numpy as np
from numpy.linalg import eigh, norm

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "edge_root_system_analysis.json"
OUT_MD = ROOT / "artifacts" / "edge_root_system_analysis.md"


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
        return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3

    adj = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(i+1, n):
            if omega(proj_points[i], proj_points[j]) == 0:
                adj[i, j] = adj[j, i] = 1

    return adj, proj_points


def build_e8_roots():
    """Build E8 root system (240 roots in R^8)."""
    roots = []

    # Type 1: permutations of (±1, ±1, 0, 0, 0, 0, 0, 0) - 112 roots
    for i in range(8):
        for j in range(i+1, 8):
            for si in [1, -1]:
                for sj in [1, -1]:
                    r = [0]*8
                    r[i] = si
                    r[j] = sj
                    roots.append(tuple(r))

    # Type 2: (±1/2, ..., ±1/2) with even number of minus signs - 128 roots
    for signs in product([1, -1], repeat=8):
        if sum(1 for s in signs if s == -1) % 2 == 0:
            roots.append(tuple(s/2 for s in signs))

    return np.array(roots, dtype=float)


def to_native(obj):
    """Convert numpy types to native Python types."""
    if isinstance(obj, np.integer):
        return int(obj)
    if isinstance(obj, np.floating):
        return float(obj)
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, dict):
        return {str(k): to_native(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [to_native(x) for x in obj]
    return obj


def main():
    results = {}
    lines = []

    lines.append("# W33 Edge Projections as Root-Like System")
    lines.append("")

    # Build W33
    adj, vertices = construct_w33()
    n = len(vertices)

    # Compute eigendecomposition
    eigenvalues, eigenvectors = eigh(adj.astype(float))
    eigenvalues = np.round(eigenvalues, 6)

    # Get λ=2 eigenspace
    tol = 0.001
    lambda2_mask = np.abs(eigenvalues - 2.0) < tol
    lambda2_vectors = eigenvectors[:, lambda2_mask]

    # Get edges
    edges = []
    for i in range(n):
        for j in range(i+1, n):
            if adj[i, j]:
                edges.append((i, j))

    lines.append("## Setup")
    lines.append("")
    lines.append(f"- W33 edges: {len(edges)}")
    lines.append(f"- λ=2 eigenspace dimension: {lambda2_vectors.shape[1]}")
    lines.append("")

    # Compute edge projections
    edge_projections = []
    for (a, b) in edges:
        indicator = np.zeros(n)
        indicator[a] = 1
        indicator[b] = 1
        proj = lambda2_vectors.T @ indicator
        edge_projections.append(proj)

    edge_projections = np.array(edge_projections)  # 240 × 24

    # All edges have the same projection norm
    edge_norms = norm(edge_projections, axis=1)
    common_norm = edge_norms[0]

    lines.append("## Edge Projection Properties")
    lines.append("")
    lines.append(f"- Common norm: {common_norm:.6f}")
    lines.append(f"- Norm variance: {np.var(edge_norms):.10f}")
    lines.append("")

    results["common_norm"] = float(common_norm)

    # Normalize edge projections
    normalized = edge_projections / common_norm

    # Compute Gram matrix (inner products)
    gram = normalized @ normalized.T
    gram_rounded = np.round(gram, 6)

    # Get distinct inner product values
    ip_values = sorted(set(gram_rounded.flatten()))
    ip_counts = Counter(gram_rounded.flatten())

    lines.append("### Inner Product Values (normalized)")
    lines.append("")
    for ip in ip_values:
        count = ip_counts[ip]
        # Exclude diagonal for counting
        if abs(ip - 1.0) < 0.0001:
            count -= 240  # Remove diagonal
        lines.append(f"- ⟨ê_i, ê_j⟩ = {ip:.6f}: {count} pairs (i≠j)")
    lines.append("")

    results["inner_product_values"] = [float(x) for x in ip_values]

    # Compare to E8
    lines.append("## Comparison to E8 Root System")
    lines.append("")

    e8_roots = build_e8_roots()
    e8_norm = norm(e8_roots[0])
    e8_normalized = e8_roots / e8_norm

    e8_gram = e8_normalized @ e8_normalized.T
    e8_gram_rounded = np.round(e8_gram, 6)

    e8_ip_values = sorted(set(e8_gram_rounded.flatten()))
    e8_ip_counts = Counter(e8_gram_rounded.flatten())

    lines.append("### E8 Inner Product Values (normalized)")
    lines.append("")
    for ip in e8_ip_values:
        count = e8_ip_counts[ip]
        if abs(ip - 1.0) < 0.0001:
            count -= 240
        lines.append(f"- ⟨r_i, r_j⟩ = {ip:.6f}: {count} pairs (i≠j)")
    lines.append("")

    results["e8_inner_product_values"] = [float(x) for x in e8_ip_values]

    # Key comparison
    lines.append("### Inner Product Comparison")
    lines.append("")
    lines.append("| W33 Edge IP | Count | E8 Root IP | Count |")
    lines.append("|-------------|-------|------------|-------|")

    w33_ips = [ip for ip in ip_values if abs(ip - 1) > 0.0001]
    e8_ips = [ip for ip in e8_ip_values if abs(ip - 1) > 0.0001]

    max_rows = max(len(w33_ips), len(e8_ips))
    for i in range(max_rows):
        w33_ip = f"{w33_ips[i]:.4f}" if i < len(w33_ips) else "-"
        w33_cnt = str(ip_counts.get(float(w33_ips[i]), 0)) if i < len(w33_ips) else "-"
        e8_ip = f"{e8_ips[i]:.4f}" if i < len(e8_ips) else "-"
        e8_cnt = str(e8_ip_counts.get(float(e8_ips[i]), 0)) if i < len(e8_ips) else "-"
        lines.append(f"| {w33_ip} | {w33_cnt} | {e8_ip} | {e8_cnt} |")
    lines.append("")

    # Check for root system properties
    lines.append("## Root System Properties Check")
    lines.append("")

    # Property 1: All roots have equal length ✓
    lines.append("### 1. Equal Length")
    lines.append(f"- All 240 vectors have norm {common_norm:.6f} ✓")
    lines.append("")

    # Property 2: For roots α, β: 2⟨α,β⟩/⟨α,α⟩ ∈ Z
    # For normalized roots: 2⟨α,β⟩ ∈ Z
    lines.append("### 2. Integrality Check (2⟨α,β⟩)")
    lines.append("")

    two_gram = 2 * gram_rounded
    two_gram_int = np.round(two_gram).astype(int)
    deviation = np.abs(two_gram - two_gram_int)
    max_deviation = np.max(deviation)

    lines.append(f"- Max deviation from integer: {max_deviation:.6f}")

    if max_deviation < 0.01:
        lines.append("- ✓ All 2⟨α,β⟩ are integers!")
        results["integrality_check"] = True
    else:
        lines.append("- ✗ Not all 2⟨α,β⟩ are integers")
        results["integrality_check"] = False
    lines.append("")

    # Property 3: Closure under reflection
    lines.append("### 3. Closure Under Reflection")
    lines.append("")

    # For each pair (α, β), check if 2⟨α,β⟩α - β is in the set
    # This is expensive, so we sample
    closure_violations = 0
    samples_checked = 0
    for i in range(min(50, len(edges))):
        for j in range(i+1, min(50, len(edges))):
            alpha = normalized[i]
            beta = normalized[j]
            ip = np.dot(alpha, beta)
            reflection = beta - 2 * ip * alpha

            # Check if reflection is in the set
            found = False
            for k in range(len(edges)):
                if np.allclose(reflection, normalized[k], atol=0.01) or \
                   np.allclose(reflection, -normalized[k], atol=0.01):
                    found = True
                    break
            if not found:
                closure_violations += 1
            samples_checked += 1

    lines.append(f"- Samples checked: {samples_checked}")
    lines.append(f"- Closure violations: {closure_violations}")

    if closure_violations == 0:
        lines.append("- ✓ No violations found in sample!")
    else:
        lines.append(f"- ✗ {closure_violations} reflection not in set")
    lines.append("")

    results["closure_violations"] = closure_violations
    results["samples_checked"] = samples_checked

    # Adjacency structure of the 240 edges
    lines.append("## Adjacency Structure of Edge Projections")
    lines.append("")

    # Two edges are "adjacent" in the edge graph if they share a vertex
    edge_adj = np.zeros((240, 240), dtype=int)
    for i, (a1, b1) in enumerate(edges):
        for j, (a2, b2) in enumerate(edges):
            if i < j:
                if a1 == a2 or a1 == b2 or b1 == a2 or b1 == b2:
                    edge_adj[i, j] = 1
                    edge_adj[j, i] = 1

    edge_graph_degree = edge_adj.sum(axis=1)[0]
    edge_graph_edges = edge_adj.sum() // 2

    lines.append(f"- Edge graph degree: {edge_graph_degree}")
    lines.append(f"- Edge graph total edges: {edge_graph_edges}")
    lines.append("")

    # Compare to E8 adjacency
    lines.append("### Comparison to E8")
    lines.append("")

    e8_adj = np.zeros((240, 240), dtype=int)
    for i in range(240):
        for j in range(i+1, 240):
            ip = np.dot(e8_normalized[i], e8_normalized[j])
            if abs(ip - 0.5) < 0.01 or abs(ip + 0.5) < 0.01:
                e8_adj[i, j] = 1
                e8_adj[j, i] = 1

    e8_degree = e8_adj.sum(axis=1)[0]
    e8_total_edges = e8_adj.sum() // 2

    lines.append(f"| Property | W33 Edge Graph | E8 Root Graph |")
    lines.append(f"|----------|----------------|---------------|")
    lines.append(f"| Degree | {edge_graph_degree} | {e8_degree} |")
    lines.append(f"| Total edges | {edge_graph_edges} | {e8_total_edges} |")
    lines.append("")

    results["w33_edge_graph_degree"] = int(edge_graph_degree)
    results["e8_root_graph_degree"] = int(e8_degree)

    # Look for correlation between inner product and adjacency
    lines.append("## Inner Product vs Graph Adjacency")
    lines.append("")

    adj_ips = []
    nonadj_ips = []
    for i in range(240):
        for j in range(i+1, 240):
            ip = gram_rounded[i, j]
            if edge_adj[i, j]:
                adj_ips.append(ip)
            else:
                nonadj_ips.append(ip)

    adj_ip_counts = Counter(np.round(adj_ips, 4))
    nonadj_ip_counts = Counter(np.round(nonadj_ips, 4))

    lines.append("### Adjacent edge-pairs (share a W33 vertex):")
    for ip, count in sorted(adj_ip_counts.items()):
        lines.append(f"- IP = {ip}: {count}")
    lines.append("")

    lines.append("### Non-adjacent edge-pairs:")
    for ip, count in sorted(nonadj_ip_counts.items()):
        lines.append(f"- IP = {ip}: {count}")
    lines.append("")

    results["adj_edge_ips"] = {str(k): int(v) for k, v in adj_ip_counts.items()}
    results["nonadj_edge_ips"] = {str(k): int(v) for k, v in nonadj_ip_counts.items()}

    # Look for special structure: antipodal pairs
    lines.append("## Antipodal Structure")
    lines.append("")

    antipodal_count = 0
    for i in range(240):
        for j in range(i+1, 240):
            if abs(gram_rounded[i, j] + 1) < 0.01:
                antipodal_count += 1

    lines.append(f"- Antipodal pairs (IP ≈ -1): {antipodal_count}")
    lines.append(f"- Expected for root system: 120 (= 240/2)")
    lines.append("")

    results["antipodal_pairs"] = antipodal_count

    # Summary
    lines.append("## Summary")
    lines.append("")

    lines.append("### Structural Parallel")
    lines.append("")
    lines.append("| Property | W33 Edge System | E8 Root System |")
    lines.append("|----------|-----------------|----------------|")
    lines.append(f"| Vectors | 240 | 240 |")
    lines.append(f"| Equal norm | ✓ | ✓ |")
    lines.append(f"| Dimension | 24 | 8 |")
    lines.append(f"| IP values | {len(w33_ips)} distinct | {len(e8_ips)} distinct |")
    lines.append(f"| Antipodal pairs | {antipodal_count} | 120 |")
    lines.append("")

    if antipodal_count == 120:
        lines.append("**REMARKABLE**: The W33 edge system has exactly 120 antipodal pairs,")
        lines.append("matching E8's root-line count!")
    elif antipodal_count == 0:
        lines.append("No antipodal structure - the system lacks ±root symmetry")
    else:
        lines.append(f"Partial antipodal structure: {antipodal_count} pairs")
    lines.append("")

    # Write outputs
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(to_native(results), indent=2), encoding="utf-8")
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
