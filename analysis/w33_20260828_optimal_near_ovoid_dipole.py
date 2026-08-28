#!/usr/bin/env python3
"""Exact W(3,3) optimal near-ovoid classification (2026-08-28).

This is deliberately independent of the CP-SAT proof in Holotrade.  It builds
W(3,3) from the standard symplectic form, uses the exact -4 line-graph
projector numerator to classify every possible deficiency <= 3, and then uses
an exact backtracker plus the projective PSp(4,3) action to count/classify all
optima.

The theorem proved here is stronger than def(W(3,3))=3:

* every optimal 10-set has line profile 0^3 1^34 2^3;
* the three missed lines are the three non-hinge lines through a unique point a;
* the three doubled lines are the three non-hinge lines through a unique point b;
* a and b are collinear and their common line is singly hit;
* each ordered collinear pair (a,b) has exactly six completions;
* there are 40*12*6 = 2880 optimal 10-sets;
* PSp(4,3) is transitive on them, with stabilizer C3 x C3;
* the oriented-edge stabilizer (order 54) acts transitively on the six local
  completions through C3 x S3 (order 18), with kernel C3.

No physics interpretation is made.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter, defaultdict
from math import gcd, lcm
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_W33_20260828_OPTIMAL_NEAR_OVOID_DIPOLE.json"

Q = 3


def norm(v):
    i = next(k for k, x in enumerate(v) if x % Q)
    z = pow(v[i] % Q, -1, Q)
    return tuple((z * x) % Q for x in v)


def form(u, v):
    return (u[0]*v[1] - u[1]*v[0] + u[2]*v[3] - u[3]*v[2]) % Q


def build_geometry():
    pts = sorted({norm(v) for v in itertools.product(range(Q), repeat=4) if any(v)})
    idx = {v: i for i, v in enumerate(pts)}
    lines = set()
    for ia, ib in itertools.combinations(range(len(pts)), 2):
        a, b = pts[ia], pts[ib]
        if form(a, b):
            continue
        span = set()
        for s, t in itertools.product(range(Q), repeat=2):
            if s == t == 0:
                continue
            span.add(idx[norm(tuple((s*a[k] + t*b[k]) % Q for k in range(4)))])
        if len(span) == 4:
            lines.add(tuple(sorted(span)))
    lines = sorted(lines)
    assert len(pts) == len(lines) == 40
    assert all(len(L) == 4 for L in lines)
    return pts, lines


def matmul(A, B):
    return [[sum(A[i][k]*B[k][j] for k in range(len(B)))
             for j in range(len(B[0]))] for i in range(len(A))]


def matvec(A, v):
    return tuple(sum(a*x for a, x in zip(row, v)) for row in A)


def addmat(A, scalar_diag):
    return [[A[i][j] + (scalar_diag if i == j else 0)
             for j in range(len(A))] for i in range(len(A))]


def line_graph(lines):
    n = len(lines)
    A = [[0]*n for _ in range(n)]
    for i, j in itertools.combinations(range(n), 2):
        if set(lines[i]) & set(lines[j]):
            A[i][j] = A[j][i] = 1
    assert {sum(r) for r in A} == {12}
    # SRG(40,12,2,4), checked without floating point.
    A2 = matmul(A, A)
    lam = {A2[i][j] for i in range(n) for j in range(i+1, n) if A[i][j]}
    mu = {A2[i][j] for i in range(n) for j in range(i+1, n) if not A[i][j]}
    assert lam == {2} and mu == {4}
    return A


def incidence(lines):
    N = [[0]*40 for _ in range(40)]
    for li, L in enumerate(lines):
        for p in L:
            N[li][p] = 1
    return N


def projector_numerator(A):
    # K=(A-12I)(A-2I)=96 E_{-4}.  Since NN^T=A+4I, K annihilates im(N).
    return matmul(addmat(A, -12), addmat(A, -2))


def line_pencils(lines):
    out = [[] for _ in range(40)]
    for li, L in enumerate(lines):
        for p in L:
            out[p].append(li)
    assert all(len(x) == 4 for x in out)
    return out


def intersection_center(lines, triple):
    z = set(lines[triple[0]])
    for li in triple[1:]:
        z &= set(lines[li])
    assert len(z) == 1
    return next(iter(z))


def exact_binary_solutions(lines, point_lines, target, limit=1000):
    """Enumerate all x in {0,1}^40 with line occupancies exactly target."""
    allowed = [p for p in range(40)
               if all(target[li] > 0 for li in point_lines[p])]
    allowed_set = set(allowed)
    cand = [[p for p in L if p in allowed_set] for L in lines]
    counts = [0]*40
    chosen = []
    sols = set()

    def rec():
        if len(sols) >= limit or len(chosen) > 10:
            return
        unmet = []
        for li, t in enumerate(target):
            if counts[li] > t:
                return
            need = t - counts[li]
            if need:
                feasible = [p for p in cand[li]
                            if p not in chosen and
                            all(counts[lj] < target[lj] for lj in point_lines[p])]
                if len(feasible) < need:
                    return
                unmet.append((len(feasible), -need, li, feasible))
        if not unmet:
            if len(chosen) == 10:
                sols.add(tuple(sorted(chosen)))
            return
        remaining = sum(target[li] - counts[li] for li in range(40))
        if len(chosen) + (remaining + 3)//4 > 10:
            return
        _, negneed, _, feasible = min(unmet)
        need = -negneed
        for subset in itertools.combinations(feasible, need):
            delta = Counter()
            for p in subset:
                for lj in point_lines[p]:
                    delta[lj] += 1
            if any(counts[lj] + d > target[lj] for lj, d in delta.items()):
                continue
            chosen.extend(subset)
            for lj, d in delta.items():
                counts[lj] += d
            rec()
            for lj, d in delta.items():
                counts[lj] -= d
            del chosen[-len(subset):]
    rec()
    return sorted(sols)


def compose(a, b):
    return tuple(a[b[i]] for i in range(len(a)))


def perm_order(p):
    seen = set(); out = 1
    for i in range(len(p)):
        if i in seen:
            continue
        j = i; n = 0
        while j not in seen:
            seen.add(j); n += 1; j = p[j]
        out = lcm(out, n)
    return out


def generated_group(gens, degree):
    e = tuple(range(degree))
    G = {e}; front = [e]
    while front:
        h = front.pop()
        for g in gens:
            z = compose(g, h)
            if z not in G:
                G.add(z); front.append(z)
    return G


def transvection_perm(pts, idx, v):
    out = []
    for x in pts:
        s = form(x, v)
        y = tuple((x[k] + s*v[k]) % Q for k in range(4))
        out.append(idx[norm(y)])
    return tuple(out)


def main():
    pts, lines = build_geometry()
    N = incidence(lines)
    A = line_graph(lines)
    K = projector_numerator(A)
    one = (1,)*40
    assert matvec(K, one) == (0,)*40
    # Exact annihilator identity: K N = 0.
    KN = matmul(K, N)
    assert all(x == 0 for row in KN for x in row)

    pencils = line_pencils(lines)
    point_lines = [[] for _ in range(40)]
    for li, L in enumerate(lines):
        for p in L:
            point_lines[p].append(li)

    # d=0: direct exact-cover search proves W(3,3) has no 10-point ovoid.
    assert exact_binary_solutions(lines, point_lines, [1]*40, limit=1) == []

    # If Nx=1+d then Kd=0.  Use that necessary condition to kill deficiency 1 and 2.
    cols = [tuple(K[r][c] for r in range(40)) for c in range(40)]
    assert len(set(cols)) == 40  # no d=1 cancellation
    pair_sig = {}
    for a, b in itertools.combinations(range(40), 2):
        sig = tuple(cols[a][r] + cols[b][r] for r in range(40))
        assert sig not in pair_sig
        pair_sig[sig] = (a, b)
    assert not any(tuple(2*x for x in cols[a]) in pair_sig for a in range(40))
    # Pair signatures are unique, so two distinct +/- pairs cannot cancel either.

    # d=3.  Missed-line triples have 9760 signatures: 9720 singletons and 40 classes of 4.
    triple_groups = defaultdict(list)
    for T in itertools.combinations(range(40), 3):
        sig = tuple(sum(cols[c][r] for c in T) for r in range(40))
        triple_groups[sig].append(T)
    hist = Counter(map(len, triple_groups.values()))
    assert hist == Counter({1: 9720, 4: 40})

    # The other partitions of excess 3 (+2,+1 or +3) never match a missed triple.
    triple_sigs = set(triple_groups)
    assert not any(tuple(2*cols[a][r] + cols[b][r] for r in range(40)) in triple_sigs
                   for a in range(40) for b in range(40) if a != b)
    assert not any(tuple(3*cols[a][r] for r in range(40)) in triple_sigs
                   for a in range(40))

    # Every size-4 signature class is exactly the four punctured pencils on one W33 line.
    collision_classes = [v for v in triple_groups.values() if len(v) == 4]
    expected = []
    for Lidx, L in enumerate(lines):
        C = sorted(tuple(sorted(set(pencils[p]) - {Lidx})) for p in L)
        expected.append(C)
    assert sorted(map(tuple, map(sorted, collision_classes))) == sorted(map(tuple, expected))

    # Pick one ordered pair of distinct punctured pencils from one class.
    C = sorted(collision_classes[0])
    missed, doubled = C[0], C[1]
    a = intersection_center(lines, missed)
    b = intersection_center(lines, doubled)
    shared = set(pencils[a]) & set(pencils[b])
    assert len(shared) == 1
    hinge = next(iter(shared))
    assert hinge not in missed and hinge not in doubled
    target = [1]*40
    for li in missed:
        target[li] = 0
    for li in doubled:
        target[li] = 2
    local = exact_binary_solutions(lines, point_lines, target)
    assert len(local) == 6
    for S in local:
        occ = [sum(p in S for p in L) for L in lines]
        assert Counter(occ) == Counter({1: 34, 0: 3, 2: 3})
        assert occ[hinge] == 1

    # Build the projective PSp(4,3) action from four deterministic transvections.
    idx = {v: i for i, v in enumerate(pts)}
    trans = [transvection_perm(pts, idx, v) for v in pts]
    G = generated_group([trans[i] for i in (17, 26, 23, 2)], 40)
    assert len(G) == 25920
    adj = {(u, v) for u in range(40) for v in range(40)
           if u != v and any(u in L and v in L for L in lines)}
    assert len(adj) == 480
    edge_orbit = {(g[a], g[b]) for g in G}
    assert edge_orbit == adj

    sample = frozenset(local[0])
    orbit = {frozenset(g[p] for p in sample) for g in G}
    assert len(orbit) == 2880 == 480*6
    stab_sample = [g for g in G if frozenset(g[p] for p in sample) == sample]
    assert len(stab_sample) == 9
    assert Counter(perm_order(g) for g in stab_sample) == Counter({3: 8, 1: 1})

    edge_stab = [g for g in G if g[a] == a and g[b] == b]
    assert len(edge_stab) == 54
    local_sets = [frozenset(S) for S in local]
    image = set()
    for g in edge_stab:
        p = tuple(local_sets.index(frozenset(g[x] for x in S)) for S in local_sets)
        image.add(p)
    assert len(image) == 18
    assert {p[0] for p in image} == set(range(6))
    orders = Counter(perm_order(p) for p in image)
    assert orders == Counter({3: 8, 6: 6, 2: 3, 1: 1})
    center = [g for g in image if all(compose(g, h) == compose(h, g) for h in image)]
    assert len(center) == 3
    # Exhibit an S3 complement, proving image ~= C3 x S3.
    s3 = None
    for r in image:
        if perm_order(r) != 3 or r in center:
            continue
        for s in image:
            if perm_order(s) != 2:
                continue
            H = generated_group([r, s], 6)
            if len(H) == 6 and all(z not in center or perm_order(z) == 1 for z in H):
                s3 = H; break
        if s3:
            break
    assert s3 is not None
    products = {compose(z, h) for z in center for h in s3}
    assert products == image

    out = {
        "schema": "w33.20260828.optimal-near-ovoid-dipole.v1",
        "status": "PASS",
        "geometry": {"points": 40, "lines": 40, "line_size": 4,
                     "line_graph": "SRG(40,12,2,4)"},
        "spectral_certificate": {
            "annihilator": "K=(A_line-12I)(A_line-2I)=96 E_{-4}",
            "K_times_incidence_zero": True,
            "deficiency_0_exact_cover_solutions": 0,
            "deficiency_1_spectral_candidates": 0,
            "deficiency_2_spectral_candidates": 0,
            "triple_signature_histogram": {"singleton": 9720, "size4": 40},
            "excess_partition_2plus1_candidates": 0,
            "excess_partition_3_candidates": 0,
        },
        "theorem": {
            "deficiency": 3,
            "optimal_line_profile": {"0": 3, "1": 34, "2": 3},
            "defect_shape": "missed and doubled triples are punctured line-pencils at two distinct collinear points; their common line is singly hit",
            "defect_patterns": 480,
            "completions_per_oriented_collinear_pair": 6,
            "optimal_10_sets": 2880,
        },
        "group_action": {
            "PSp4_3_order": 25920,
            "optimal_set_orbit": 2880,
            "optimal_set_stabilizer_order": 9,
            "optimal_set_stabilizer": "C3 x C3",
            "oriented_edge_stabilizer_order": 54,
            "local_six_completion_image_order": 18,
            "local_six_completion_image": "C3 x S3",
            "local_kernel_order": 3,
        },
        "representative": {
            "miss_center": a, "double_center": b, "hinge_line": hinge,
            "missed_lines": list(missed), "doubled_lines": list(doubled),
            "six_completions": [list(S) for S in local],
        },
        "boundary": "Exact finite-combinatorial theorem. The six local completions are not identified with any other six-state carrier without an explicit intertwiner. No physics claim."
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": "PASS", "deficiency": 3, "optima": 2880,
                      "local": 6, "stabilizer": "C3^2",
                      "local_action": "C3xS3"}, sort_keys=True))


if __name__ == "__main__":
    main()
