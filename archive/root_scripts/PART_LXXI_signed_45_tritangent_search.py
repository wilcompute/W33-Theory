#!/usr/bin/env python3
"""PART LXXI — Signed 45-tritangent cubic search.

Part LXX proved that the unsigned 36-internal-triangle cubic on H27 has
infinitesimal stabilizer dimension 6, not 78, so it is not the E6 Cartan
cubic.  The next target is the full 45-tritangent structure:

    45 = 36 internal W33 triangles + 9 missing Heisenberg fibers.

This script performs the first finite search: keep the 36 internal terms with
coefficient +1, add the 9 missing fiber triples with all possible +/- signs,
and compute the infinitesimal stabilizer dimension of each resulting cubic.

If a candidate with stabilizer dimension 78 appears, that is a concrete E6
cubic candidate.  If no such candidate appears, then the true cubic requires
more than simply +/- signs on the 9 fiber terms: e.g. phases, signs on the 36
terms, or a different tritangent coordinatization.
"""
from __future__ import annotations

from collections import Counter
from itertools import combinations, combinations_with_replacement
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parent
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from w33_homology import build_w33
from w33_heisenberg_qutrit import compute_local_structure, build_f3_cube


def rank_mod_prime_sparse(rows, ncols, prime=1000003):
    """Sparse Gaussian elimination over GF(prime)."""
    pivots = {}
    rank = 0
    for row in rows:
        row = {k: v % prime for k, v in row.items() if v % prime}
        while row:
            pivot = min(row)
            coeff = row[pivot] % prime
            if pivot not in pivots:
                inv = pow(coeff, prime - 2, prime)
                pivots[pivot] = {k: (v * inv) % prime for k, v in row.items()}
                rank += 1
                break
            factor = coeff
            prow = pivots[pivot]
            for k, v in prow.items():
                nv = (row.get(k, 0) - factor * v) % prime
                if nv:
                    row[k] = nv
                elif k in row:
                    del row[k]
    return rank


def cubic_stabilizer_nullity_weighted(terms, dim=27):
    """Compute infinitesimal stabilizer nullity for a weighted cubic.

    terms: iterable of ((a,b,c), coeff), with distinct indices in each triple.
    Variables are X_{i,a}, the entries of a dim x dim matrix X.  The linear
    equation for each unordered triple (a,b,c) is

        sum_i X_{i,a} c_{i,b,c}
      + sum_i X_{i,b} c_{a,i,c}
      + sum_i X_{i,c} c_{a,b,i} = 0.
    """
    coeff = {}
    for tri, value in terms:
        tri = tuple(sorted(tri))
        coeff[tri] = coeff.get(tri, 0) + int(value)

    coeff = {k: v for k, v in coeff.items() if v != 0}

    def C(a, b, c):
        if len({a, b, c}) != 3:
            return 0
        return coeff.get(tuple(sorted((a, b, c))), 0)

    rows = []
    for a, b, c in combinations_with_replacement(range(dim), 3):
        row = {}
        for i in range(dim):
            value = C(i, b, c)
            if value:
                row[i * dim + a] = row.get(i * dim + a, 0) + value
            value = C(a, i, c)
            if value:
                row[i * dim + b] = row.get(i * dim + b, 0) + value
            value = C(a, b, i)
            if value:
                row[i * dim + c] = row.get(i * dim + c, 0) + value
        if row:
            rows.append(row)

    rank = rank_mod_prime_sparse(rows, dim * dim)
    return dim * dim - rank


def build_h27_terms(base_vertex=0):
    n, vertices, adj, edges = build_w33()
    adj_s = [set(row) for row in adj]
    N12, H27, n12_triangles, _ = compute_local_structure(base_vertex, n, adj_s)
    fibers, vertex_to_xyz = build_f3_cube(N12, H27, n12_triangles, adj_s)
    local = {v: i for i, v in enumerate(H27)}

    internal = []
    for a, b, c in combinations(H27, 3):
        if b in adj_s[a] and c in adj_s[a] and c in adj_s[b]:
            internal.append(tuple(sorted((local[a], local[b], local[c]))))
    internal = sorted(set(internal))

    fiber_terms = []
    fiber_labels = []
    for label, verts in sorted(fibers.items()):
        tri = tuple(sorted(local[v] for v in verts))
        fiber_terms.append(tri)
        fiber_labels.append(label)

    return {
        "base_vertex": base_vertex,
        "internal": internal,
        "fibers": fiber_terms,
        "fiber_labels": fiber_labels,
    }


def search_fiber_signs(base_vertex=0):
    data = build_h27_terms(base_vertex)
    internal = data["internal"]
    fibers = data["fibers"]
    assert len(internal) == 36
    assert len(fibers) == 9
    assert len(set(internal) & set(fibers)) == 0

    # Baseline: unsigned 36 cubic.
    nullity_36 = cubic_stabilizer_nullity_weighted([(t, 1) for t in internal])

    # First finite search: internal signs fixed +1, fiber signs vary +/-1.
    histogram = Counter()
    hits_78 = []
    best = []
    started = time.time()
    for mask in range(1 << len(fibers)):
        signs = [1 if ((mask >> i) & 1) == 0 else -1 for i in range(len(fibers))]
        terms = [(t, 1) for t in internal] + [(t, s) for t, s in zip(fibers, signs)]
        nullity = cubic_stabilizer_nullity_weighted(terms)
        histogram[nullity] += 1
        record = {"mask": mask, "signs": signs, "stabilizer_dim": nullity}
        if nullity == 78:
            hits_78.append(record)
        best.append(record)

    best_sorted = sorted(best, key=lambda r: (-r["stabilizer_dim"], r["mask"]))[:20]

    return {
        "base_vertex": base_vertex,
        "internal_terms": len(internal),
        "fiber_terms": len(fibers),
        "total_terms": len(internal) + len(fibers),
        "baseline_36_stabilizer_dim": nullity_36,
        "search_space": 1 << len(fibers),
        "histogram": dict(sorted(histogram.items())),
        "max_stabilizer_dim": max(histogram),
        "hits_78_count": len(hits_78),
        "hits_78": hits_78[:20],
        "best_candidates": best_sorted,
        "elapsed_seconds": round(time.time() - started, 6),
        "interpretation": (
            "If hits_78_count>0, a signed 45-term E6-cubic candidate was found. "
            "If hits_78_count=0, +/- signs on the 9 fibers are insufficient and the "
            "search must allow phases/signs on the 36 internal tritangent terms or a "
            "different tritangent coordinatization."
        ),
    }


def main():
    payload = search_fiber_signs(base_vertex=0)
    out = ROOT / "checks"
    out.mkdir(exist_ok=True)
    path = out / f"PART_LXXI_signed_45_tritangent_search_{int(time.time())}.json"
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
