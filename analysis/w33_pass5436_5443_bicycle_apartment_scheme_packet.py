#!/usr/bin/env python3
"""Passes 5436--5443: bicycle filtration, apartment orbitals, Tanner fusion,
minimum apartment bases, critical determinant, stabilizer fixed points, and the
q=3 BFS-basis Gram spectrum.

Everything promoted here is exact finite combinatorics / linear algebra.  The
q=3 orbital calculation constructs W(3,3) and PSp(4,3) directly from the
standard symplectic form; it does not rely on a precomputed group table.
"""
from __future__ import annotations

from collections import Counter, defaultdict, deque
from fractions import Fraction
from itertools import combinations, product
import hashlib
import json
import math
from pathlib import Path

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PART_W33_PASS5436_5443_BICYCLE_APARTMENT_SCHEME.json"


def inv_mod(a: int, q: int) -> int:
    return pow(int(a), -1, q)


def norm_vec(v, q: int):
    v = tuple(int(x) % q for x in v)
    for x in v:
        if x:
            z = inv_mod(x, q)
            return tuple((z * y) % q for y in v)
    raise ValueError("zero vector")


def symp(u, v, q: int) -> int:
    return (u[0]*v[2] + u[1]*v[3] - u[2]*v[0] - u[3]*v[1]) % q


def build_W_prime(q: int):
    pts = sorted({norm_vec(v, q) for v in product(range(q), repeat=4) if any(v)})
    pidx = {p: i for i, p in enumerate(pts)}
    lines = set()
    for i, j in combinations(range(len(pts)), 2):
        p, r = pts[i], pts[j]
        if symp(p, r, q) != 0:
            continue
        L = set()
        for a in range(q):
            for b in range(q):
                if a or b:
                    vv = tuple((a*p[k] + b*r[k]) % q for k in range(4))
                    L.add(pidx[norm_vec(vv, q)])
        if len(L) == q + 1:
            lines.add(tuple(sorted(L)))
    lines = sorted(lines)
    v = (q + 1)*(q*q + 1)
    assert len(pts) == len(lines) == v
    incP = [[] for _ in pts]
    for li, L in enumerate(lines):
        for p in L:
            incP[p].append(li)
    assert {len(z) for z in incP} == {q + 1}
    return pts, lines, incP


def enumerate_q3_apartments():
    q = 3
    pts, lines, incP = build_W_prime(q)
    nP = len(pts)
    adj = [[] for _ in range(2*nP)]
    flags = []
    edgeid = {}
    for p, lis in enumerate(incP):
        for li in lis:
            u, v = p, nP + li
            adj[u].append(v)
            adj[v].append(u)
            eid = len(flags)
            flags.append((p, li))
            edgeid[(min(u, v), max(u, v))] = eid
    for a in adj:
        a.sort()

    cycles = set()
    for s in range(2*nP):
        def dfs(path):
            cur = path[-1]
            if len(path) == 8:
                if s in adj[cur] and min(path) == s:
                    rev = [s] + list(reversed(path[1:]))
                    cycles.add(min(tuple(path), tuple(rev)))
                return
            for nb in adj[cur]:
                if nb == s or nb in path or nb < s:
                    continue
                dfs(path + [nb])
        dfs([s])

    cycles = sorted(cycles)
    apartments = []
    for cyc in cycles:
        eids = []
        for i in range(8):
            a, b = cyc[i], cyc[(i+1) % 8]
            eids.append(edgeid[(min(a, b), max(a, b))])
        apartments.append(frozenset(eids))
    assert len(flags) == 160 and len(apartments) == 1620
    return pts, lines, flags, adj, edgeid, cycles, apartments


def compose(p, q):
    """Permutation p after q."""
    return tuple(p[q[i]] for i in range(len(p)))


def invperm(p):
    z = [0]*len(p)
    for i, j in enumerate(p):
        z[j] = i
    return tuple(z)


def group_closure(gens):
    identity = tuple(range(len(gens[0])))
    G = {identity}
    todo = [identity]
    while todo:
        g = todo.pop()
        for h in gens:
            x = compose(h, g)
            if x not in G:
                G.add(x)
                todo.append(x)
    return G


def perm_order(p):
    seen = [False]*len(p)
    out = 1
    for i in range(len(p)):
        if seen[i]:
            continue
        j, n = i, 0
        while not seen[j]:
            seen[j] = True
            n += 1
            j = p[j]
        out = math.lcm(out, n)
    return out


def q3_orbital_certificate():
    pts, lines, flags, adj, edgeid, cycles, apartments = enumerate_q3_apartments()
    pidx = {p: i for i, p in enumerate(pts)}
    line_lookup = {tuple(L): i for i, L in enumerate(lines)}
    flag_lookup = {f: i for i, f in enumerate(flags)}
    apt_lookup = {A: i for i, A in enumerate(apartments)}
    bits = [sum(1 << e for e in A) for A in apartments]

    def transvection(v):
        ans = []
        for x in pts:
            c = symp(x, v, 3)
            y = tuple((x[i] + c*v[i]) % 3 for i in range(4))
            ans.append(pidx[norm_vec(y, 3)])
        return tuple(ans)

    G = group_closure([transvection(v) for v in pts])
    assert len(G) == 25920

    base_cycle = cycles[0]
    base_points = {x for x in base_cycle if x < 40}
    base_line_ids = {x - 40 for x in base_cycle if x >= 40}
    base_line_sets = {tuple(lines[i]) for i in base_line_ids}

    H = []
    for g in G:
        if {g[p] for p in base_points} != base_points:
            continue
        mapped = {tuple(sorted(g[p] for p in lines[li])) for li in base_line_ids}
        if mapped == base_line_sets:
            H.append(g)
    assert len(H) == 16

    def lineperm(g):
        return tuple(line_lookup[tuple(sorted(g[p] for p in L))] for L in lines)

    def aptperm(g):
        lp = lineperm(g)
        fp = [flag_lookup[(g[p], lp[l])] for p, l in flags]
        return tuple(apt_lookup[frozenset(fp[e] for e in A)] for A in apartments)

    Hapt = [aptperm(g) for g in H]
    unseen = set(range(1620))
    orbits = []
    while unseen:
        a = min(unseen)
        orb = sorted({h[a] for h in Hapt})
        orbits.append(orb)
        unseen -= set(orb)
    assert len(orbits) == 131
    size_census = Counter(map(len, orbits))
    assert size_census == Counter({16: 84, 8: 25, 4: 17, 2: 3, 1: 2})

    orb_of = {}
    for oi, orb in enumerate(orbits):
        for a in orb:
            orb_of[a] = oi

    baseA = apartments[0]
    def base_image(g):
        lp = lineperm(g)
        fp = [flag_lookup[(g[p], lp[l])] for p, l in flags]
        return apt_lookup[frozenset(fp[e] for e in baseA)]

    rep = [None]*1620
    for g in G:
        a = base_image(g)
        if rep[a] is None:
            rep[a] = g
    assert all(g is not None for g in rep)
    invrep = [invperm(g) for g in rep]

    def relation(a, b):
        return orb_of[base_image(compose(invrep[a], rep[b]))]

    transpose = [relation(orb[0], 0) for orb in orbits]
    symmetric = sum(i == transpose[i] for i in range(131))
    assert symmetric == 25
    assert (131 - symmetric)//2 == 53

    fusion = defaultdict(Counter)
    for orb in orbits:
        s = (bits[0] & bits[orb[0]]).bit_count()
        fusion[s][len(orb)] += 1
    fusion_expected = {
        8: {1: 1},
        4: {4: 2, 8: 1},
        3: {16: 2},
        2: {4: 2, 8: 3, 16: 4},
        1: {16: 18},
        0: {1: 1, 2: 3, 4: 13, 8: 21, 16: 60},
    }
    assert {k: dict(v) for k, v in fusion.items()} == fusion_expected

    # Complete orbital intersection tensor p_{ij}^k.  For a representative b
    # of orbital k, classify every intermediate apartment c.
    tensor = []
    for k, orb in enumerate(orbits):
        b = orb[0]
        cnt = Counter()
        for c in range(1620):
            i = orb_of[c]
            j = relation(c, b)
            cnt[(i, j)] += 1
        assert sum(cnt.values()) == 1620
        tensor.append(cnt)

    sparse = []
    for k, cnt in enumerate(tensor):
        for (i, j), value in sorted(cnt.items()):
            if value:
                sparse.append([k, i, j, value])
    payload = json.dumps(sparse, separators=(",", ":")).encode()
    tensor_sha = hashlib.sha256(payload).hexdigest()
    assert len(sparse) == 159065
    assert tensor_sha == "868ffd6ea89ab41b95557cdd97b4ffca6198771238a0bb0f8c006974c7885b19"

    # Center of the 131-dimensional orbital algebra.  The equations for
    # z=sum_i z_i A_i to commute with each A_j are
    # sum_i z_i(p_{ij}^k-p_{ji}^k)=0.  A deterministic 114-row subsystem has
    # nullity 17; its 17 exact null vectors annihilate every full equation.
    center_rows = []
    for j in range(131):
        for k in range(131):
            row = {}
            for i in range(131):
                d = tensor[k].get((i, j), 0) - tensor[k].get((j, i), 0)
                if d:
                    row[i] = d
            if row:
                center_rows.append(row)
    selected = [474,603,1103,1481,1610,1739,1993,2122,2251,2505,2634,2763,2892,3021,3404,3533,3662,3920,4295,4545,4795,4924,5053,5182,5813,5942,6958,7725,7979,8109,8238,9777,10035,10421,8937,9578,10093,13647,13903,14415,1796,2308,2562,2691,3078,4224,8819,8904,8295,10221,13180,8910,13620,1676,1764,402,531,1667,5684,6100,6141,6213,6446,9670,13876,9551,1418,3687,13656,10110,13616,9656,13730,13741,3046,5078,974,345,7343,13615,8906,2829,6148,8911,4870,2703,6009,6513,3860,8980,10448,11723,5455,7401,5490,8812,604,1093,15690,6095,8984,6096,8686,3523,10199,8890,1994,10993,5696,8780,13203,1707,9984,5968]
    assert len(selected) == 114 and max(selected) < len(center_rows)
    Msel = sp.Matrix([[center_rows[r].get(i, 0) for i in range(131)] for r in selected])
    null = Msel.nullspace()
    assert len(null) == 17  # hence selected subsystem has rank 114
    integer_null = []
    for vec in null:
        den = sp.ilcm(*[x.q for x in vec])
        integer_null.append([int(x*den) for x in vec])
    for row in center_rows:
        for vec in integer_null:
            assert sum(value*vec[i] for i, value in row.items()) == 0
    center_dimension = 17

    # Stabilizer/Burnside fixed-point fingerprint.
    fixed = Counter()
    for g, hp in zip(H, Hapt):
        fixed[(perm_order(g), sum(i == hp[i] for i in range(1620)))] += 1
    fixed_expected = Counter({(1,1620):1, (2,108):3, (2,24):4, (4,12):4, (4,2):4})
    assert fixed == fixed_expected
    assert sum(mult*fix for (order, fix), mult in fixed.items()) == 16*131

    return {
        "group_order": 25920,
        "apartments": 1620,
        "stabilizer_order": 16,
        "orbital_rank": 131,
        "orbital_size_census": {str(k): v for k, v in sorted(size_census.items())},
        "symmetric_orbitals": 25,
        "directed_transpose_pairs": 53,
        "overlap_fusion_orbital_census": {
            str(s): {str(k): v for k, v in sorted(c.items())}
            for s, c in sorted(fusion.items(), reverse=True)
        },
        "tensor_nonzero_entries": len(sparse),
        "tensor_sha256": tensor_sha,
        "orbital_algebra_center_dimension": center_dimension,
        "orbital_algebra_center_codimension": 131-center_dimension,
        "stabilizer_fixed_apartment_fingerprint": [
            {"element_order": o, "fixed_apartments": f, "multiplicity": m}
            for (o, f), m in sorted(fixed.items())
        ],
        "burnside_sum": 16*131,
        "geometry": (pts, lines, flags, adj, edgeid, cycles, apartments),
    }


def bfs_basis_q3(geometry):
    pts, lines, flags, adj, edgeid, cycles, apartments = geometry
    nV = len(adj)
    parent = [None]*nV
    dist = [None]*nV
    dist[0] = 0
    todo = deque([0])
    tree = set()
    while todo:
        u = todo.popleft()
        for v in adj[u]:
            if dist[v] is None:
                dist[v] = dist[u] + 1
                parent[v] = u
                todo.append(v)
                tree.add((min(u, v), max(u, v)))
    assert max(dist) == 4 and len(tree) == nV-1
    all_edges = set(edgeid)
    cotree = sorted(all_edges - tree)
    assert len(cotree) == 81

    def root_path(u):
        out = [u]
        while parent[u] is not None:
            u = parent[u]
            out.append(u)
        return out

    def tree_path(u, v):
        pu, pv = root_path(u), root_path(v)
        pos = {x: i for i, x in enumerate(pu)}
        j = next(j for j, x in enumerate(pv) if x in pos)
        w = pv[j]
        i = pos[w]
        return pu[:i+1] + list(reversed(pv[:j]))

    flag_lookup = {f: i for i, f in enumerate(flags)}
    A = np.zeros((len(flags), len(cotree)), dtype=np.int64)
    apartment_sets = set(apartments)
    for col, (u, v) in enumerate(cotree):
        path = tree_path(u, v)
        directed = [(path[i], path[i+1]) for i in range(len(path)-1)] + [(v, u)]
        assert len(directed) == 8
        support = set()
        for a, b in directed:
            p, l = (a, b-40) if a < 40 else (b, a-40)
            eid = flag_lookup[(p, l)]
            support.add(eid)
            A[eid, col] = 1 if a < 40 else -1
        assert frozenset(support) in apartment_sets
    assert np.linalg.matrix_rank(A.astype(float)) == 81

    G = sp.Matrix((A.T @ A).tolist())
    x = sp.symbols("x")
    charpoly = sp.factor(G.charpoly(x).as_expr())
    expected = (x-160)*(x-40)**4*(x-4)**12*(x-1)**28*(x**2-17*x+40)**12*(x**2-8*x+10)**6
    assert sp.expand(charpoly-expected) == 0
    determinant = int(G.det())
    assert determinant == 2**83 * 5**23
    return {
        "root": 0,
        "tree_edges": 79,
        "cotree_edges_apartment_basis": 81,
        "basis_rank": 81,
        "gram_charpoly": str(charpoly),
        "gram_eigenvalue_extremes": ["1", "160"],
        "basis_condition_number": "sqrt(160)",
        "gram_determinant": str(determinant),
        "gram_determinant_factorization": "2^83*5^23",
    }


def allq_formula_certificate():
    anchors = {}
    for q in (2,3,4,5,7,8,9,11,13):
        N = (q+1)**2*(q*q+1)              # flags / Levi edges
        V = 2*(q+1)*(q*q+1)               # Levi vertices
        E = N
        beta = E-V+1
        assert beta == q**4
        apartments = N*q**4//8

        # Pass5079 plus Pass5422: R4 apartment-intersection graph.
        k4 = 8*(q-1)
        roots = q**3*(q+1)**2*(q*q+1)
        theta = q**3*(q+1)*(q*q+1)*math.comb(q+1, 3)
        tanner6 = roots*math.comb(q, 3)
        assert tanner6 == theta*(q-2)
        total_triangles = theta+tanner6
        assert total_triangles == theta*(q-1)
        # Every R4 edge is in exactly one theta triangle and q-2 root triangles.
        r4_edges = apartments*k4//2
        assert 3*total_triangles == r4_edges*(q-1)

        f = q*(q+1)**2//2
        g = q*(q*q+1)//2
        tree_order = (q*q+1)**(f-1) * (q+1)**(2*g)

        anchors[str(q)] = {
            "q": q,
            "levi_vertices": V,
            "levi_edges": E,
            "cycle_rank": beta,
            "minimum_apartment_basis_size": beta,
            "all_apartments": apartments,
            "R4_degree": k4,
            "R4_adjacent_common_neighbors": q-1,
            "theta_triangles": theta,
            "root_tanner_triangles": tanner6,
            "R4_total_triangles": total_triangles,
            "levi_spanning_tree_order": str(tree_order),
        }

    q3_tau = int(anchors["3"]["levi_spanning_tree_order"])
    assert q3_tau == 2**83 * 5**23
    return {
        "bfs_apartment_basis": {
            "theorem": "For any GQ(q,q), a BFS geodesic spanning tree of the Levi graph has exactly q^4 cotree edges; every cotree fundamental cycle has length 8 and is therefore an apartment. These q^4 apartments are a basis of H1 and are cardinality-minimal.",
            "proof_key": "Levi diameter is 4 and girth is 8. A cotree fundamental cycle has length at most 8 and is nonzero, hence exactly 8. Fundamental cycles of a spanning tree form a basis.",
        },
        "R4_edge_regular_graph": {
            "vertices": "M=Nq^4/8 apartments",
            "degree": "8(q-1)",
            "adjacent_common_neighbors": "q-1",
            "triangle_split": "each R4 edge is in 1 theta triangle and q-2 root/Tanner triangles",
            "total_triangles": "T(q)(q-1)",
            "Tanner_six_cycles": "T(q)(q-2), already Pass5079",
            "boundary": "edge-regular is asserted; strong regularity is not. q=3 refines into 131 orbitals.",
        },
        "cycle_lattice_determinant": {
            "f": "q(q+1)^2/2",
            "g": "q(q^2+1)/2",
            "levi_tree_number": "tau=(q^2+1)^(f-1)(q+1)^(2g)",
            "fundamental_apartment_gram_determinant": "det(F^T F)=tau",
            "proof_key": "Cauchy-Binet for an integral fundamental cycle matrix: nonzero maximal minors are +/-1 and are indexed by complements of spanning trees. The Levi Laplacian spectrum gives tau.",
            "q3": "tau=2^83*5^23",
        },
        "anchors": anchors,
    }


def main():
    orb = q3_orbital_certificate()
    geometry = orb.pop("geometry")
    bfs = bfs_basis_q3(geometry)
    allq = allq_formula_certificate()

    # Pass5436: exact q=3 refinement forced by Pass5426 + Pass5068.
    bicycle = {
        "odd_q_amalgam_input": "Bike=P_g+L_g with P_g cap L_g=<J> and dim Bike=q(q^2+1)-1 (Pass5426).",
        "q3_input": "Pass5068 has dim P15=15, J<L9<L15 with dimensions 1<9<15, and W23=P15+L9.",
        "q3_filtration": "0 < J < P15 < W23=P15+L9 < Bike29=P15+L15",
        "dimensions": [0,1,15,23,29],
        "successive_factor_dimensions": [1,14,8,6],
        "quotients": ["P15/J:14", "W23/P15 ~= L9/J:8", "Bike29/W23 ~= L15/L9:6"],
        "proof": "P15 cap L15=J implies P15 cap L9=J; apply the dimension formula and the second isomorphism theorem.",
        "boundary": "The numbers 14,8,6 are exact quotient dimensions. Irreducibility is not newly asserted here.",
    }

    out = {
        "schema": "w33.pass5436_5443.bicycle_apartment_scheme.v1",
        "status": "THEOREM_PACKET_SOURCE_COMPLETE",
        "pass_range": [5436,5443],
        "5436_q3_bicycle_filtration": bicycle,
        "5437_q3_apartment_orbital_coherent_configuration": orb,
        "5438_allq_R4_edge_regular_tanner_fusion": allq["R4_edge_regular_graph"],
        "5439_allq_minimum_BFS_apartment_basis": allq["bfs_apartment_basis"],
        "5440_evidence_boundary": {
            "prior_run": 31888221806,
            "observed_status_at_packet_start": "queued",
            "claim": "No remote CI success is inferred from registration or queueing."
        },
        "5441_bonkers_cycle_lattice_critical_determinant": allq["cycle_lattice_determinant"],
        "5442_bonkers_H16_Burnside_fingerprint": {
            "stabilizer_order": 16,
            "fixed_point_types": orb["stabilizer_fixed_apartment_fingerprint"],
            "Burnside_identity": "sum_h Fix(h)=2096=16*131",
            "reading": "The 131 apartment orbitals are independently recovered as the Burnside orbit count of the apartment stabilizer. Four order-4 elements fix only two apartments each."
        },
        "5443_bonkers_q3_BFS_basis_Gram_spectrum": bfs,
        "allq_anchors": allq["anchors"],
        "cross_regressions": [
            "Pass5426 footprint/bicycle amalgam",
            "Pass5068 Bike29/P15/L9/W23 filtration",
            "Pass5422 apartment intersection counts",
            "Pass5079 all-q Tanner six-cycle theorem",
            "Pass5031 q=3 Levi critical-group tree order 2^83*5^23",
            "Pass5069/5072 apartment stabilizer order 16"
        ],
        "boundary": "No physical threshold, code-distance, optimal numerical conditioning, strong-regularity, irreducibility, broad novelty, or remote-CI-success claim is made. The five overlap-size relations are explicitly NOT an association scheme at q=3; the correct Schurian refinement has rank 131."
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))
    return out


if __name__ == "__main__":
    main()
