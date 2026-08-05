#!/usr/bin/env python3
"""Passes 3535--3541: clique recertification source, Borel-M57 collapse,
Perkel Fourier projectors, coupled factorization design, and exact
W33/Gewirtz polynomial transplantation.

All promoted finite claims are regenerated with the Python standard library.
The independent 3,720-instance clique rerun is implemented by a companion
heavy source and remains a separate workflow result until that job completes.
"""
from __future__ import annotations
import collections
import hashlib
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PART_BT3535_BT3541_CLIQUE_BOREL_FOURIER_FACTORIZATION_PORTS_results.json"


def canon(x: Any) -> str:
    return json.dumps(x, sort_keys=True, separators=(",", ":"))


def semantic_sha(x: Any) -> str:
    return hashlib.sha256(canon(x).encode()).hexdigest()


def matmul(A, B):
    BT = list(zip(*B))
    return [[sum(a*b for a, b in zip(row, col)) for col in BT] for row in A]


def matadd(*Ms):
    return [[sum(M[i][j] for M in Ms) for j in range(len(Ms[0][0]))]
            for i in range(len(Ms[0]))]


def matscale(c, A):
    return [[c*x for x in row] for row in A]


def eye(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def zeros(n, m=None):
    if m is None:
        m = n
    return [[0]*m for _ in range(n)]


def rank_fraction(A):
    M = [[Fraction(x) for x in row] for row in A]
    n = len(M)
    m = len(M[0]) if n else 0
    r = 0
    for c in range(m):
        p = next((i for i in range(r, n) if M[i][c]), None)
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]
        q = M[r][c]
        M[r] = [x/q for x in M[r]]
        for i in range(n):
            if i != r and M[i][c]:
                q = M[i][c]
                M[i] = [M[i][j]-q*M[r][j] for j in range(m)]
        r += 1
        if r == n:
            break
    return r


PUBLISHED_HIST = {
    2: 6, 3: 2, 4: 13, 5: 32, 6: 18, 7: 173, 8: 358, 9: 403,
    10: 131, 11: 220, 12: 502, 13: 400, 14: 58, 15: 123, 16: 303,
    29: 19, 30: 49, 31: 910,
}


def clique_recertification_contract():
    assert sum(PUBLISHED_HIST.values()) == 3720
    assert max(PUBLISHED_HIST) == 31
    return {
        "companion_source": "analysis/bt3535_star_clique_recertify.py",
        "candidate_source": "analysis/bt3529_star_complement_census.py",
        "instances": 3720,
        "required_clique": 38,
        "published_histogram": {str(k): v for k, v in sorted(PUBLISHED_HIST.items())},
        "published_maximum": 31,
        "independent_engine": [
            "exact inverse of 2I-C",
            "exact admissible reconstruction-column enumeration",
            "exact compatibility graph construction",
            "bitset maximum clique with greedy-color upper bounds",
            "witness clique and deterministic proof digest per candidate",
        ],
        "quick_self_tests": {
            "complete_graph_9": 9,
            "cycle_5": 2,
            "complete_bipartite_5_7": 2,
        },
        "boundary": (
            "The source and fail-closed comparison are installed. No fresh all-3720 "
            "histogram is promoted before the heavy workflow artifact is observed."
        ),
    }


def moore_fixed_subgraph_theorem():
    return {
        "prime_fixed_subgraph_law": (
            "For prime p dividing degree 57, a nontrivial fixed set is closed under "
            "unique common neighbors and, if nontrivial, is itself a Moore graph "
            "whose fixed degree is 57 mod p."
        ),
        "p19": "fixed degree 0, hence every order-19 automorphism fixes exactly one vertex",
        "p3": "fixed graph is one vertex or the Petersen graph on ten vertices",
        "admissible_Moore_degrees": [2, 3, 7, 57],
    }


def borel_orbit_archetypes():
    profiles = []
    for x19 in range(172):
        for x57 in range(58):
            rem = 3250-1-19*x19-57*x57
            if rem < 0 or rem % 171:
                continue
            x171 = rem//171
            f3 = 1+x19+3*x57
            if f3 not in (1, 10):
                continue
            if f3 == 1:
                continue
            f9 = 1+x19
            if f9 not in (1, 10):
                continue
            profiles.append((x19, x57, x171, f3, f9))
    assert profiles == [(0, 3, 18, 10, 1), (9, 0, 18, 10, 10)]

    feasible = []
    for a19 in range(172):
        a1 = 1729-18*a19
        if a1 < 0:
            continue
        for b19 in range(172):
            b1 = 1520-18*b19
            if b1 < 0:
                continue
            if a1+b1 != 171 or a19+b19 != 171:
                continue
            chi7 = a1-a19
            chim8 = b1-b19
            g = 57+7*chi7-8*chim8
            if 0 <= g <= 3250:
                feasible.append(g)
    feasible = sorted(set(feasible))
    assert feasible == [57, 342, 627, 912, 1197]

    surviving = [g for g in feasible if g % 19 == 0 and 9*(g//19) <= 171]
    assert surviving == [57, 342]
    archetypes = []
    for x19, x57, x171, f3, f9 in profiles:
        profile = "P57" if x57 else "P19"
        for g in surviving:
            archetypes.append({
                "name": f"{profile}-{'low' if g == 57 else 'high'}",
                "orbits": {"1": 1, "19": x19, "57": x57, "171": x171},
                "fixed_order3": f3,
                "fixed_order9": f9,
                "order19_displacement_g": g,
                "edge_bearing_C19_orbits": g//19,
                "regular_B_orbits_with_internal_C19_step": g//19,
            })
    assert len(archetypes) == 4
    return {
        "conditional_assumption": "B=C19 semidirect C9 acts on a hypothetical M57",
        "order_bound_consequence": (
            "If Aut(M57) is odd of order at most 375, the presence of B forces Aut(M57)=B."
        ),
        "fixed_subgraph": moore_fixed_subgraph_theorem(),
        "orbit_profiles": [
            {
                "name": "P19",
                "decomposition": "1 + 9*19 + 18*171",
                "neighborhood_of_global_fixed_vertex": "three 19-orbits",
            },
            {
                "name": "P57",
                "decomposition": "1 + 3*57 + 18*171",
                "neighborhood_of_global_fixed_vertex": "one 57-orbit",
            },
        ],
        "raw_order19_displacement_values": feasible,
        "girth_and_power_balance_survivors": surviving,
        "four_action_archetypes": archetypes,
        "boundary": "The four archetypes are necessary conditions, not constructions or a contradiction.",
    }


def perkel_graph():
    vertices = [(i, j) for i in range(3) for j in range(19)]
    idx = {v: i for i, v in enumerate(vertices)}
    A = zeros(57)
    for i, j in vertices:
        rhs = pow(2, 6*i, 19)
        for k in range(19):
            if pow((k-j) % 19, 3, 19) == rhs:
                u = idx[(i, j)]
                v = idx[((i+1) % 3, k)]
                A[u][v] = A[v][u] = 1
    assert all(sum(r) == 6 for r in A)
    return vertices, idx, A


def perkel_fourier_projectors():
    _, _, A = perkel_graph()
    I = eye(57)
    J = [[1]*57 for _ in range(57)]
    B19 = zeros(57)
    for block in range(3):
        for a in range(19):
            for b in range(19):
                B19[19*block+a][19*block+b] = 1
    A2 = matmul(A, A)
    A3 = matmul(A2, A)
    N = matadd(matscale(-1, A3), matscale(9, A2), matscale(-19, A), matscale(6, I))
    P1 = matscale(3, J)
    P2 = matadd(matscale(9, B19), matscale(-3, J))
    P18 = matadd(N, matscale(-9, B19), matscale(3, J))
    P36 = matadd(matscale(171, I), matscale(-3, J), matscale(-1, N))
    Ps = [P1, P2, P18, P36]
    ranks = [rank_fraction(P) for P in Ps]
    assert ranks == [1, 2, 18, 36]
    assert matadd(*Ps) == matscale(171, I)
    for i, P in enumerate(Ps):
        for j, Q in enumerate(Ps):
            lhs = matmul(P, Q)
            rhs = matscale(171, P) if i == j else zeros(57)
            assert lhs == rhs
    assert matmul(A, P1) == matscale(6, P1)
    assert matmul(A, P2) == matscale(-3, P2)
    assert matmul(A, P18) == matscale(-3, P18)
    golden_poly = matadd(A2, matscale(-3, A), I)
    assert matmul(golden_poly, P36) == zeros(57)
    P54 = matadd(P18, P36)
    cubic = matadd(A3, matscale(-8, A), matscale(3, I))
    assert matmul(cubic, P54) == zeros(57)
    assert P54 == matadd(matscale(171, I), matscale(-9, B19))

    def reduce_cubic(coeffs):
        c = list(map(int, coeffs))
        while len(c) > 3:
            n = len(c)-1
            z = c.pop()
            if z:
                c[n-2] += 8*z
                c[n-3] -= 3*z
        c += [0]*(3-len(c))
        return c[:3]

    examples = {}
    for n in (3, 4, 19):
        examples[f"x^{n}"] = reduce_cubic([0]*n+[1])
    assert examples["x^3"] == [-3, 8, 0]
    assert examples["x^4"] == [0, -3, 8]
    assert examples["x^19"] == [-69144384, 201730265, -54214032]
    return {
        "rational_module": "Q^57 = 1 + 3*V18 + V2",
        "common_denominator": 171,
        "integer_projector_numerators": {
            "rank1": "3J",
            "rank2": "9B19-3J",
            "rank18": "(-A^3+9A^2-19A+6I)-9B19+3J",
            "rank36": "171I-3J-(-A^3+9A^2-19A+6I)",
        },
        "ranks": ranks,
        "orthogonal_idempotent_law": "Pi*Pj = 171*delta_ij*Pi",
        "spectral_actions": {
            "rank1": "A=6",
            "rank2": "A=-3",
            "rank18": "A=-3",
            "rank36": "A^2-3A+I=0",
        },
        "conductor19_projector": "P54=171I-9B19=P18+P36",
        "conductor19_minimal_polynomial": "x^3-8x+3",
        "compiler_normal_form": "p(A)=p(6)E1+p(-3)E2+(c0I+c1A+c2A^2)E54",
        "cubic_reductions": examples,
    }


def perfect_matchings(items):
    items = tuple(items)
    if not items:
        yield ()
        return
    a = items[0]
    for i in range(1, len(items)):
        b = items[i]
        rest = items[1:i]+items[i+1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted(((min(a, b), max(a, b)),)+tail))


def all_factorizations_k6():
    edges = {tuple(sorted(e)) for e in itertools.combinations(range(6), 2)}
    matchings = sorted(set(perfect_matchings(range(6))))
    facts = []

    def rec(chosen, remaining, start):
        if not remaining:
            facts.append(tuple(chosen))
            return
        e = min(remaining)
        for i in range(start, len(matchings)):
            M = matchings[i]
            if e not in M:
                continue
            s = set(M)
            if s <= remaining:
                rec(chosen+[M], remaining-s, i+1)

    rec([], edges, 0)
    facts = sorted(set(tuple(sorted(F)) for F in facts))
    assert len(matchings) == 15
    assert len(facts) == 6
    return matchings, facts


def hs_graph():
    g = {("p", i, j): set() for i in range(5) for j in range(5)}
    g.update({("q", i, j): set() for i in range(5) for j in range(5)})

    def add(u, v):
        g[u].add(v)
        g[v].add(u)

    for i in range(5):
        for j in range(5):
            add(("p", i, j), ("p", i, (j+1) % 5))
            add(("q", i, j), ("q", i, (j+2) % 5))
    for i in range(5):
        for j in range(5):
            for k in range(5):
                add(("p", i, j), ("q", k, (i*k+j) % 5))
    assert len(g) == 50 and all(len(g[v]) == 7 for v in g)
    return g


def edge_chart(g, edge):
    x, y = edge
    rows = sorted(g[x]-{y}, key=repr)
    cols = sorted(g[y]-{x}, key=repr)
    residual = set(g)-{x, y}-set(rows)-set(cols)
    cell = {}
    for v in residual:
        rr = [i for i, r in enumerate(rows) if v in g[r]]
        cc = [a for a, c in enumerate(cols) if v in g[c]]
        assert len(rr) == len(cc) == 1
        cell[rr[0], cc[0]] = v
    n = len(rows)
    assert n == 6 and len(cell) == 36
    perms = {}
    for i, j in itertools.permutations(range(n), 2):
        p = []
        for a in range(n):
            v = cell[i, a]
            ns = [b for b in range(n) if cell[j, b] in g[v]]
            assert len(ns) == 1
            p.append(ns[0])
        perms[i, j] = tuple(p)
    return rows, cols, cell, perms


def matching_from_perm(p):
    assert all(p[p[a]] == a and p[a] != a for a in range(len(p)))
    return tuple(sorted(tuple(sorted((a, p[a]))) for a in range(len(p)) if a < p[a]))


def compose(p, q):
    return tuple(p[q[i]] for i in range(len(p)))


def cycles(p):
    seen = set()
    out = []
    for i in range(len(p)):
        if i in seen:
            continue
        c = []
        j = i
        while j not in seen:
            seen.add(j)
            c.append(j)
            j = p[j]
        out.append(len(c))
    return tuple(sorted(out))


def factorization_design():
    _, facts = all_factorizations_k6()
    fact_index = {F: i for i, F in enumerate(facts)}
    g = hs_graph()
    root = (("p", 0, 0), ("p", 0, 1))
    _, _, _, perms = edge_chart(g, root)
    row_facts = []
    for i in range(6):
        F = tuple(sorted(matching_from_perm(perms[i, j]) for j in range(6) if j != i))
        assert F in fact_index
        row_facts.append(fact_index[F])
    assert sorted(row_facts) == list(range(6))

    base = facts[0]
    base_perms = []
    for M in base:
        p = list(range(6))
        for a, b in M:
            p[a] = b
            p[b] = a
        base_perms.append(tuple(p))
    triangle_fixed_hist = collections.Counter()
    successful = 0
    for color_map in itertools.permutations(range(5)):
        edge_color = {}
        for color, M in enumerate(base):
            for e in M:
                edge_color[e] = color
        good = True
        for i, j, k in itertools.combinations(range(6), 3):
            sij = base_perms[color_map[edge_color[tuple(sorted((i, j)))]]]
            sjk = base_perms[color_map[edge_color[tuple(sorted((j, k)))]]]
            ski = base_perms[color_map[edge_color[tuple(sorted((k, i)))]]]
            H = compose(ski, compose(sjk, sij))
            f = sum(H[a] == a for a in range(6))
            triangle_fixed_hist[f] += 1
            if f:
                good = False
        successful += int(good)
    assert successful == 0
    assert triangle_fixed_hist == {2: 2400}

    hs_hol = collections.Counter()
    for i, j, k in itertools.combinations(range(6), 3):
        H = compose(perms[k, i], compose(perms[j, k], perms[i, j]))
        hs_hol[cycles(H)] += 1
    assert hs_hol == {(2, 2, 2): 20}
    return {
        "K6_perfect_matchings": 15,
        "K6_labeled_one_factorizations": 6,
        "HS_row_factorization_indices": row_facts,
        "HS_uses_complete_factorization_atlas": True,
        "HS_triangle_holonomy_cycle_histogram": {"2+2+2": 20},
        "global_separable_ansatz": {
            "color_bijections_exhausted": 120,
            "row_triangles_per_bijection": 20,
            "successful_bijections": 0,
            "fixed_points_histogram": {"2": 2400},
            "verdict": "Every global-factorization ansatz fails every triangle in the Hoffman-Singleton control.",
        },
        "M57_design_consequence": (
            "The involutive n=56 branch must use genuinely row-dependent, "
            "reciprocity-coupled one-factorizations of K56."
        ),
        "M57_pencils": 56,
        "matchings_per_pencil": 55,
        "edges_per_matching": 28,
        "edges_covered_per_pencil": 1540,
    }


def w33_graph():
    reps = []
    seen = set()
    for v in itertools.product(range(3), repeat=4):
        if v == (0, 0, 0, 0):
            continue
        nv = tuple((-x) % 3 for x in v)
        r = min(v, nv)
        if r not in seen:
            seen.add(r)
            reps.append(r)
    reps = sorted(reps)
    assert len(reps) == 40
    A = zeros(40)

    def sp(u, v):
        return (u[0]*v[2]-u[2]*v[0]+u[1]*v[3]-u[3]*v[1]) % 3

    for i, j in itertools.combinations(range(40), 2):
        if sp(reps[i], reps[j]) == 0:
            A[i][j] = A[j][i] = 1
    assert all(sum(r) == 12 for r in A)
    return A


def extended_golay_words():
    gp = [11, 9, 7, 6, 5, 1, 0]
    words = []
    for m in range(1 << 12):
        w = 0
        for s in range(12):
            if (m >> s) & 1:
                for p in gp:
                    w ^= 1 << (p+s)
        words.append(w | ((w.bit_count() & 1) << 23))
    return words


def gewirtz_graph():
    hexads = set()
    for w in extended_golay_words():
        if w.bit_count() == 8 and ((w >> 22) & 1) and ((w >> 23) & 1):
            hexads.add(frozenset(i for i in range(22) if (w >> i) & 1))
    H = sorted(hexads, key=lambda x: tuple(sorted(x)))
    assert len(H) == 77
    V = [h for h in H if 0 not in h]
    assert len(V) == 56
    A = zeros(56)
    for i, j in itertools.combinations(range(56), 2):
        if V[i].isdisjoint(V[j]):
            A[i][j] = A[j][i] = 1
    assert all(sum(r) == 10 for r in A)
    return A


def reduce_quadratic(coeffs):
    c = list(map(int, coeffs))
    while len(c) > 2:
        n = len(c)-1
        z = c.pop()
        if z:
            c[n-1] += -2*z
            c[n-2] += 8*z
    c += [0]*(2-len(c))
    return c[:2]


def verify_srg_relation(A, k, v, m2, mm4):
    n = len(A)
    I = eye(n)
    J = [[1]*n for _ in range(n)]
    lhs = matmul(matadd(A, matscale(-2, I)), matadd(A, matscale(4, I)))
    rhs = matscale((k-2)*(k+4)//v, J)
    assert lhs == rhs
    Rnum = matadd(matscale(k+1, J), matscale(-v, I), matscale(-v, A))
    assert matmul(Rnum, Rnum) == matadd(matscale(9*v*v, I), matscale(-9*v, J))
    Q3num = matadd(matscale(3*v, I), matscale(-3, J))
    E2num = matadd(Q3num, matscale(-1, Rnum))
    Em4num = matadd(Q3num, Rnum)
    assert rank_fraction(E2num) == m2
    assert rank_fraction(Em4num) == mm4
    return {
        "parameters": [v, k],
        "restricted_multiplicities": {"2": m2, "-4": mm4},
        "full_identity": "(A-2I)(A+4I)=((k-2)(k+4)/v)J",
        "reflection": "R=((k+1)J/v-I-A)/3; R^2=I-J/v",
        "projectors": "E2=(Q-R)/2, E-4=(Q+R)/2",
    }


def polynomial_ports():
    W = w33_graph()
    G = gewirtz_graph()
    rows = {
        "W33": verify_srg_relation(W, 12, 40, 24, 15),
        "Gewirtz": verify_srg_relation(G, 10, 56, 35, 20),
    }
    examples = {}
    for n in (2, 3, 4, 5, 19):
        examples[f"x^{n}"] = reduce_quadratic([0]*n+[1])
    theorem = {
        "augmentation_quotient": "Q[x]/(x^2+2x-8)",
        "normal_form": "p(A)Q=(aA+bI)Q where [b,a]=reduce(p)",
        "full_graph_compiler": "p(A)=p(k)P+(aA+bI)Q",
        "constant_channel_correction": "equivalently p(A)=aA+bI+[p(k)-ak-b]P",
        "reductions": examples,
        "trace_formula": "tr p(A)=p(k)+m2*p(2)+m_4*p(-4)",
        "determinant_formula": "det p(A)=p(k)*p(2)^m2*p(-4)^m_4",
        "inverse_formula": "if p(k),p(2),p(-4) are nonzero, invert the three scalar channels",
    }
    return {
        "graphs_regenerated_exactly": rows,
        "portable_theorem_package": theorem,
        "policy": {
            "automatic": "adjacency-polynomial and functional-calculus claims",
            "typed_graph_data_required": "k,v,multiplicities for full trace/determinant/rank statements",
            "fresh_geometry_required": [
                "incidence", "lines", "codes", "automorphisms", "Smith forms",
                "descendant maps", "intertwiners",
            ],
        },
    }


def build():
    data = {
        "schema": "w33.pass3535_3541.clique_borel_fourier_factorization_ports.v1",
        "status": "PASS_7_FRONTS",
        "pass3535_clique_recertification": clique_recertification_contract(),
        "pass3536_m57_borel_fixed_subgraphs": moore_fixed_subgraph_theorem(),
        "pass3537_bonkers_four_archetypes": borel_orbit_archetypes(),
        "pass3538_perkel_fourier_projectors": perkel_fourier_projectors(),
        "pass3539_factorization_first_m57": factorization_design(),
        "pass3540_bonkers_HS_complete_atlas": {
            "statement": (
                "The six residual rows of the Hoffman-Singleton edge chart realize "
                "all six labeled one-factorizations of K6 exactly once."
            ),
            "design_consequence": (
                "The smallest nontrivial Moore control is maximally nonseparable "
                "at the factorization level."
            ),
        },
        "pass3541_w33_gewirtz_polynomial_ports": polynomial_ports(),
        "boundaries": {
            "M57": "open; four conditional Borel archetypes only",
            "star_cliques": "engine installed; no full independent histogram promoted before observed artifact",
            "physical": "no particle, spacetime, hardware, or laboratory claim",
        },
    }
    data["semantic_sha256"] = semantic_sha(data)
    return data


def main():
    data = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    print(data["status"], data["semantic_sha256"])


if __name__ == "__main__":
    main()
