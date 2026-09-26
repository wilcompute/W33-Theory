#!/usr/bin/env python3
"""Pass 10963: Clifford-grade stabilizer chain and tetrahedral packet geometry."""
from __future__ import annotations

import importlib.util
import itertools
import json
from collections import Counter
from pathlib import Path

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/w33_pass10963_clifford_grade_stabilizer_chain.json"
EXACT = ROOT / "data/w33_pass10963_exact_stabilizer_generators.json"

_spec = importlib.util.spec_from_file_location(
    "p55", ROOT / "analysis/w33_pass10955_d4_halfspin_clock_bridge.py")
P55 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(P55)
MM = P55.p51.mm
DET = P55.P46.det2
ID = ((1, 0), (0, 1))
def inv(m):
    a, b = m[0]
    c, d = m[1]
    di = 1 if DET(m) == 1 else 2
    return ((d * di % 3, -b * di % 3),
            (-c * di % 3, a * di % 3))


def mpow(m, n):
    x = ID
    for _ in range(n):
        x = MM(x, m)
    return x


def order(m):
    x = ID
    for n in range(1, 49):
        x = MM(x, m)
        if x == ID:
            return n
    raise AssertionError("order > 48")


def conj(a, x):
    return MM(MM(a, x), inv(a))


def closure(gens):
    h = {ID}
    changed = True
    while changed:
        changed = False
        for a in list(h):
            for b in gens + list(h):
                c = MM(a, b)
                if c not in h:
                    h.add(c)
                    changed = True
    return h
def all_gl23():
    out = []
    for e in itertools.product(range(3), repeat=4):
        m = ((e[0], e[1]), (e[2], e[3]))
        if DET(m):
            out.append(m)
    assert len(out) == 48
    return out


def conjugate_subgroups(G, H):
    out = []
    for a in G:
        K = frozenset(conj(a, h) for h in H)
        if K not in out:
            out.append(K)
    return out


def left_cosets(G, H):
    out = []
    for a in G:
        C = frozenset(MM(a, h) for h in H)
        if C not in out:
            out.append(C)
    return out


def line_canon(v):
    a, b = v
    choices = [(a % 3, b % 3), ((2*a) % 3, (2*b) % 3)]
    return min(choices)


def line_action(m, v):
    a, b = v
    return line_canon((
        (m[0][0]*a + m[0][1]*b) % 3,
        (m[1][0]*a + m[1][1]*b) % 3,
    ))
def subspace_basis(A):
    q, _ = np.linalg.qr(A)
    return q


def same_subspace(A, B, tol=1e-8):
    qa = subspace_basis(A)
    qb = subspace_basis(B)
    return np.linalg.norm(
        (np.eye(A.shape[0]) - qa @ qa.conj().T) @ qb
    ) < tol


def image_basis(m, A, Jf, Ji):
    r4 = P55.signed_matrix(m).astype(complex)
    rho = Jf @ np.kron(np.eye(8), r4) @ Ji
    ri = np.linalg.inv(rho)
    cols = []
    for k in range(A.shape[1]):
        X = A[:, k].reshape(32, 32)
        cols.append((rho @ X @ ri).reshape(-1))
    return np.column_stack(cols)


def interdim(A, B, tol=1e-8):
    return A.shape[1] + B.shape[1] - np.linalg.matrix_rank(
        np.column_stack([A, B]), tol)


def main():
    G = all_gl23()
    g = ((0, 1), (1, 1))
    b = ((1, 0), (1, 2))
    g2 = mpow(g, 2)
    z = mpow(g, 4)
    assert order(g) == 8
    assert order(b) == 2
    assert z == ((2, 0), (0, 2))
    assert conj(b, g) == mpow(g, 3)

    H19 = closure([g, b])
    H10 = closure([g2, b])
    assert len(H19) == 16 and len(H10) == 8
    assert H10 < H19
    assert conj(b, g2) == mpow(g2, 3)

    C8 = {mpow(g, k) for k in range(8)}
    normalizer = {
        a for a in G
        if {conj(a, x) for x in C8} == C8
    }
    assert normalizer == H19

    assert Counter(order(x) for x in H19) == Counter(
        {1: 1, 2: 5, 4: 6, 8: 4})
    assert Counter(order(x) for x in H10) == Counter(
        {1: 1, 2: 5, 4: 2})

    C10 = conjugate_subgroups(G, H10)
    C19 = conjugate_subgroups(G, H19)
    core10 = set.intersection(*map(set, C10))
    core19 = set.intersection(*map(set, C19))
    assert core10 == {ID, z}
    assert len(core19) == 8
    assert Counter(order(x) for x in core19) == Counter(
        {1: 1, 2: 1, 4: 6})
    # Exact projective-line action: GL(2,3)/{+-I} = S4.
    points = sorted({
        line_canon(v)
        for v in itertools.product(range(3), repeat=2)
        if v != (0, 0)
    })
    assert len(points) == 4
    edges = sorted(itertools.combinations(range(4), 2))
    matchings = [
        ((0, 1), (2, 3)),
        ((0, 2), (1, 3)),
        ((0, 3), (1, 2)),
    ]

    def perm4(m):
        return tuple(points.index(line_action(m, p)) for p in points)

    image4 = {perm4(m) for m in G}
    assert len(image4) == 24
    kernel4 = {m for m in G if perm4(m) == (0, 1, 2, 3)}
    assert kernel4 == core10

    def edge_image(m, edge):
        p = perm4(m)
        return tuple(sorted((p[edge[0]], p[edge[1]])))

    def matching_image(m, matching):
        return tuple(sorted(edge_image(m, e) for e in matching))
    fixed_edges = [
        e for e in edges
        if all(edge_image(h, e) == e for h in H10)
    ]
    assert len(fixed_edges) == 2
    base_edge = min(fixed_edges)

    fixed_matchings = [
        M for M in matchings
        if all(matching_image(h, M) == M for h in H19)
    ]
    assert len(fixed_matchings) == 1
    base_matching = fixed_matchings[0]
    assert base_edge in base_matching

    cos10 = left_cosets(G, H10)
    cos19 = left_cosets(G, H19)
    assert len(cos10) == 6 and len(cos19) == 3

    edge_labels = []
    for C in cos10:
        a = next(iter(C))
        e = edge_image(a, base_edge)
        assert all(edge_image(x, base_edge) == e for x in C)
        edge_labels.append(e)
    assert sorted(edge_labels) == edges

    matching_labels = []
    for C in cos19:
        a = next(iter(C))
        M = matching_image(a, base_matching)
        assert all(matching_image(x, base_matching) == M for x in C)
        matching_labels.append(M)
    assert sorted(matching_labels) == sorted(matchings)

    coset_pairs = []
    for D in cos19:
        ids = [i for i, C in enumerate(cos10) if C <= D]
        assert len(ids) == 2
        coset_pairs.append(ids)
    for pair, M in zip(coset_pairs, matching_labels):
        assert set(edge_labels[i] for i in pair) == set(M)

    # Packet orbit/intersection census from the committed 32D intertwiner.
    jd = json.loads(
        (ROOT / "data/w33_pass10959_doubled_albert_gl23_intertwiner.json")
        .read_text(encoding="utf-8"))
    J = sp.Matrix([
        [sp.sympify(x) for x in row] for row in jd["intertwiner_J"]
    ])
    Jf = np.array(J.evalf(), dtype=complex)
    Ji = np.linalg.inv(Jf)

    gd = json.loads(
        (ROOT / "data/w33_pass10961_albert_clifford9_gammas.json")
        .read_text(encoding="utf-8"))
    g9 = [
        sp.Matrix([[sp.Rational(x) for x in row] for row in M])
        for M in gd["gamma9"]
    ]
    I16 = sp.eye(16)
    Z16 = sp.zeros(16)
    Vms = [
        sp.Matrix.vstack(
            sp.Matrix.hstack(Z16, x),
            sp.Matrix.hstack(x, Z16),
        )
        for x in g9
    ]
    G10 = sp.diag(I16, -I16)
    Vms.append(G10)
    MIX = [G10 * Vms[i] for i in range(9)]
    V = np.column_stack([
        np.array(x.evalf(), dtype=complex).reshape(-1) for x in Vms
    ])
    P19 = np.column_stack([
        np.array(x.evalf(), dtype=complex).reshape(-1)
        for x in Vms + MIX
    ])

    Vorbit, Porbit = [], []
    for m in G:
        A = image_basis(m, V, Jf, Ji)
        if not any(same_subspace(A, B) for B in Vorbit):
            Vorbit.append(A)
        A = image_basis(m, P19, Jf, Ji)
        if not any(same_subspace(A, B) for B in Porbit):
            Porbit.append(A)
    assert len(Vorbit) == 6 and len(Porbit) == 3

    vinter = Counter()
    vcross = Counter()
    for i in range(6):
        for j in range(i + 1, 6):
            vinter[interdim(Vorbit[i], Vorbit[j])] += 1
            qi = subspace_basis(Vorbit[i])
            qj = subspace_basis(Vorbit[j])
            vcross[np.linalg.matrix_rank(qi.conj().T @ qj, 1e-8)] += 1
    assert vinter == Counter({0: 12, 1: 3})
    assert vcross == Counter({9: 12, 1: 3})

    pinter = Counter()
    pcross = Counter()
    for i in range(3):
        for j in range(i + 1, 3):
            pinter[interdim(Porbit[i], Porbit[j])] += 1
            qi = subspace_basis(Porbit[i])
            qj = subspace_basis(Porbit[j])
            pcross[np.linalg.matrix_rank(qi.conj().T @ qj, 1e-8)] += 1
    assert pinter == Counter({8: 3})
    assert pcross == Counter({9: 3})

    v_hull_rank = np.linalg.matrix_rank(np.column_stack(Vorbit), 1e-8)
    p_hull_rank = np.linalg.matrix_rank(np.column_stack(Porbit), 1e-8)
    assert v_hull_rank == p_hull_rank == 33
    contain = []
    for P in Porbit:
        q = subspace_basis(P)
        ids = []
        for i, A in enumerate(Vorbit):
            a = subspace_basis(A)
            err = np.linalg.norm(
                (np.eye(1024) - q @ q.conj().T) @ a)
            if err < 1e-8:
                ids.append(i)
        assert len(ids) == 2
        contain.append(ids)

    # Exact packet stabilizer certificate, generated independently.
    ex = json.loads(EXACT.read_text(encoding="utf-8"))
    assert ex["exact_zero_tests"] is True
    assert ex["b_preserves_all_10_vectors"] is True
    assert ex["b_preserves_all_19_packet_generators"] is True
    assert ex["outsider_preserves_vector_generators"] == 0
    assert ex["outsider_preserves_packet_generators"] == 0

    # 10961 supplies the other exact generator facts:
    # g preserves the 19D packet but not V10; g^2 preserves V10.
    p61 = json.loads(
        (ROOT / "data/w33_pass10961_albert_clifford10_doubled_clock.json")
        .read_text(encoding="utf-8"))
    o61 = p61["clifford_normalizer_obstruction"]
    assert o61["full_C8_normalizes_vector_space"] is False
    assert o61["two_ticks_normalize_vector_space"] is True
    out = {
        "schema": "w33.pass10963.clifford-grade-stabilizer-chain.v1",
        "status": "PASS_CLIFFORD_GRADE_STABILIZER_TETRAHEDRAL_CHAIN",
        "group": {
            "G": "GL(2,3)",
            "order": 48,
            "center": "C2={+I,-I}",
            "clock_generator": [list(r) for r in g],
            "clock_order": 8,
            "determinant_character": "GL(2,3)->C2",
        },
        "packet_stabilizers": {
            "V10": {
                "dimension": 10,
                "order": len(H10),
                "generators": ["g^2", "b"],
                "presentation": "<r,b | r^4=b^2=1, b r b=r^-1>",
                "group": "D8",
                "exact": True,
            },
            "P19": {
                "dimension": 19,
                "order": len(H19),
                "generators": ["g", "b"],
                "presentation": "<g,b | g^8=b^2=1, b g b=g^3>",
                "group": "QD16 = SD16",
                "clock_normalizer": True,
                "sylow_2_subgroup": True,
                "exact": True,
            },
            "chain": "C8 < QD16; D8 < QD16 < GL(2,3)",
        },
        "cores_and_quotients": {
            "core_V10_stabilizer_order": len(core10),
            "core_V10_stabilizer": "central C2",
            "V10_packet_action_image": "S4",
            "V10_packet_orbit_size": len(cos10),
            "core_P19_stabilizer_order": len(core19),
            "core_P19_stabilizer": "Q8",
            "P19_packet_action_image": "S3",
            "P19_packet_orbit_size": len(cos19),
            "projective_line_points": points,
        },
        "tetrahedral_dictionary": {
            "four_vertices": points,
            "six_V10_packets": "six edges of a tetrahedron/K4",
            "three_P19_packets":
                "three perfect matchings = three opposite-edge pairs",
            "base_edge": base_edge,
            "base_matching": base_matching,
            "coset_edge_labels": edge_labels,
            "coset_matching_labels": matching_labels,
            "coset_pairs": coset_pairs,
            "equivariant": True,
        },
        "packet_intersections": {
            "V10_pair_intersection_histogram": {
                str(k): v for k, v in sorted(vinter.items())
            },
            "V10_cross_gram_rank_histogram": {
                str(k): v for k, v in sorted(vcross.items())
            },
            "reading_V10":
                "12 adjacent edge-pairs are transverse (intersection 0) with cross-Gram rank 9; 3 opposite pairs intersect in dimension 1 with cross-Gram rank 1",
            "P19_pair_intersection_histogram": {
                str(k): v for k, v in sorted(pinter.items())
            },
            "P19_cross_gram_rank_histogram": {
                str(k): v for k, v in sorted(pcross.items())
            },
            "reading_P19":
                "all three pairs of perfect-matching packets intersect in dimension 8 and have cross-Gram rank 9",
            "common_orbit_hull_dimension": int(v_hull_rank),
            "V10_orbit_hull_equals_P19_orbit_hull": bool(
                v_hull_rank == p_hull_rank == 33
            ),
            "each_P19_contains_exactly_two_V10_packets": True,
            "containment_pairs_numeric_orbit_order": contain,
            "numerical_tolerance": 1e-8,
        },
        "external_group_anchor": {
            "sylow2":
                "GL(2,3) has semidihedral Sylow-2 subgroups of order 16",
            "projective_quotient":
                "GL(2,3)/{+-I}=PGL(2,3)=S4",
        },
        "theorem": (
            "The exact stabilizer of the canonical Cl(10) vector packet V10 "
            "inside the transported GL(2,3) action is D8=<g^2,b>. The exact "
            "stabilizer of the 19D vector-plus-mixed-bivector packet is "
            "QD16=<g,b>, the normalizer of the clock C8 and a Sylow-2 subgroup. "
            "Their cores are the central C2 and Q8, so the induced packet "
            "actions are S4 on six V10 packets and S3 on three P19 packets. "
            "These actions are equivariantly the S4 action on the six edges "
            "of a tetrahedron and the S3 action on its three perfect matchings. "
            "Each P19 packet contains exactly the two V10 packets in one "
            "opposite-edge pair. Adjacent V10 packets are transverse but have "
            "cross-Gram rank 9; opposite packets meet in a 1D line with "
            "cross-Gram rank 1. The six V10 packets and three P19 packets "
            "generate the same 33-dimensional operator hull."
        ),
        "boundary": (
            "The S4/S3 tetrahedral packet geometry is an exact finite "
            "Clifford-grade statement for this transported GL(2,3) action. "
            "It is not by itself the D4 triality outer action, a physical "
            "gauge symmetry, or a spacetime identification. The intersection "
            "dimensions are replayed numerically from exact committed matrices "
            "with tolerance 1e-8; the stabilizer groups and quotient actions "
            "are certified independently by exact finite-field and symbolic "
            "generator checks."
        ),
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(json.dumps({
        "status": out["status"],
        "V10_stabilizer": out["packet_stabilizers"]["V10"]["group"],
        "P19_stabilizer": out["packet_stabilizers"]["P19"]["group"],
        "quotients": {
            "six_packets": "S4",
            "three_packets": "S3",
        },
        "V_intersections": out["packet_intersections"][
            "V10_pair_intersection_histogram"],
    }, indent=2))


if __name__ == "__main__":
    main()
