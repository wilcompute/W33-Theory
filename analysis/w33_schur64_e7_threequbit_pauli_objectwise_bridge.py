#!/usr/bin/env python3
"""Objectwise bridge from the Schur64 real three-qubit Pauli phase quotient to E7.

Nurowski (arXiv:2609.10751) identifies the normal order-128 subgroup of the
64-line Schur incidence automorphism group as the real three-qubit Pauli group

    E3 = <-I, X1,Z1,X2,Z2,X3,Z3> ~= 2_+^{1+6}.

Projectivizing by its center gives E3/Z(E3) ~= F2^6, with the standard
three-qubit symplectic form on coordinates

    (x1,z1,x2,z2,x3,z3).

Independently, Pass8489-8496 proves that the 63 antipodal E7 root pairs exhaust
the 63 nonzero vectors of a six-dimensional symplectic quotient of the E7
lattice, with root-inner-product parity equal to the quotient symplectic form.

This certificate constructs an explicit symplectic basis change between those
two F2^6 models, then freezes an objectwise 63-entry dictionary

    Schur/Pauli direction <-> Pauli word <-> E7 antipodal root pair.

It verifies every pairwise symplectic/root-parity relation and all 336 closed
anticommuting XOR triangles.  This is a phase-quotient bridge; it does NOT yet
identify the 64 Schur lines or 64 ordinary Schur triple points with E7 objects.
"""
from __future__ import annotations

from collections import defaultdict
from itertools import combinations, product
import json
from pathlib import Path

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_schur64_e7_threequbit_pauli_objectwise_bridge.json"

S = [
    (1,-1,-1,-1,-1,-1,-1,1),
    (2,2,0,0,0,0,0,0),
    (-2,2,0,0,0,0,0,0),
    (0,-2,2,0,0,0,0,0),
    (0,0,-2,2,0,0,0,0),
    (0,0,0,-2,2,0,0,0),
    (0,0,0,0,-2,2,0,0),
    (0,0,0,0,0,-2,2,0),
]
JSTD = np.array([
    [0,1,0,0,0,0],
    [1,0,0,0,0,0],
    [0,0,0,1,0,0],
    [0,0,1,0,0,0],
    [0,0,0,0,0,1],
    [0,0,0,0,1,0],
], dtype=np.uint8)


def e8_roots():
    roots = []
    for i, j in combinations(range(8), 2):
        for a in (2, -2):
            for b in (2, -2):
                v = [0] * 8
                v[i] = a
                v[j] = b
                roots.append(tuple(v))
    for signs in product((1, -1), repeat=8):
        if sum(x < 0 for x in signs) % 2 == 0:
            roots.append(tuple(signs))
    assert len(roots) == 240
    return roots


def rank2(A):
    A = np.array(A, dtype=np.uint8) % 2
    m, n = A.shape
    r = 0
    for c in range(n):
        pivot = next((i for i in range(r, m) if A[i, c]), None)
        if pivot is None:
            continue
        A[[r, pivot]] = A[[pivot, r]]
        for i in range(m):
            if i != r and A[i, c]:
                A[i] ^= A[r]
        r += 1
    return r


def root_pair_key(r):
    r = tuple(map(int, r))
    nr = tuple(-x for x in r)
    return min(r, nr)


def omega(v, w, J):
    a = np.array(v, dtype=np.uint8)
    b = np.array(w, dtype=np.uint8)
    return int(a @ J @ b) % 2


def vec_xor(a, b):
    return tuple(x ^ y for x, y in zip(a, b))


def mat_vec(P, v):
    return tuple(int(x) for x in ((P @ np.array(v, dtype=np.uint8)) % 2).tolist())


def symplectic_basis(J):
    """Deterministically choose columns e1,f1,e2,f2,e3,f3 with Gram JSTD."""
    vectors = sorted(v for v in product((0, 1), repeat=6) if any(v))
    chosen = []
    for _ in range(3):
        e = next(v for v in vectors if all(omega(v, b, J) == 0 for b in chosen))
        prev = tuple(chosen)
        f = next(
            v for v in vectors
            if omega(v, e, J) == 1
            and all(omega(v, b, J) == 0 for b in prev)
        )
        chosen.extend((e, f))
    P = np.array(chosen, dtype=np.uint8).T
    assert rank2(P) == 6
    assert np.array_equal((P.T @ J @ P) % 2, JSTD)
    return P, tuple(chosen)


def pauli_word(v):
    lut = {(0,0): "I", (1,0): "X", (0,1): "Z", (1,1): "Y"}
    return "".join(lut[(v[2*i], v[2*i+1])] for i in range(3))


def build_e7_model():
    roots = e8_roots()
    r0 = np.array(S[1], dtype=int)
    e7 = [np.array(r, dtype=int) for r in roots if int(np.dot(r, r0)) == 0]
    assert len(e7) == 126

    A = sp.Matrix(np.array(S, dtype=int).T)
    G = np.array([[np.dot(x, y) // 4 for y in S] for x in S], dtype=int)
    B = np.zeros((8, 7), dtype=int)
    for j, i in enumerate([0, 2, 4, 5, 6, 7]):
        B[i, j] = 1
    B[1, 6] = 1
    B[3, 6] = 2
    GE = B.T @ G @ B
    assert round(np.linalg.det(GE)) == 2

    Ai = A.inv()
    mods = defaultdict(list)
    for r in e7:
        c = Ai * sp.Matrix(r.tolist())
        assert all(x.q == 1 for x in c)
        c = np.array([int(x) for x in c])
        d = np.array([c[0], c[2], c[4], c[5], c[6], c[7], c[1]], dtype=int)
        assert np.array_equal(B @ d, c)
        mods[tuple((d % 2).tolist())].append(tuple(map(int, r)))
    assert len(mods) == 63 and set(map(len, mods.values())) == {2}

    G2 = GE % 2
    assert rank2(G2) == 6 and not np.any(G2[-1])
    J = G2[:6, :6].astype(np.uint8)
    assert rank2(J) == 6

    qmap = {tuple(v[:6]): v for v in mods}
    assert len(qmap) == 63
    rootpair = {
        q: root_pair_key(mods[qmap[q]][0])
        for q in qmap
    }
    return J, rootpair


def build_result():
    J, rootpair = build_e7_model()
    P, symp_basis = symplectic_basis(J)

    labels = sorted(v for v in product((0, 1), repeat=6) if any(v))
    dictionary = []
    mapped_rootpairs = set()
    for v in labels:
        q = mat_vec(P, v)
        r = rootpair[q]
        mapped_rootpairs.add(r)
        dictionary.append({
            "standard_bits_x1z1x2z2x3z3": list(v),
            "pauli_word_projective": pauli_word(v),
            "e7_quotient_bits": list(q),
            "e7_antipodal_root_pair_representative": list(r),
        })
    assert len(mapped_rootpairs) == 63

    # Every pairwise commutation/anticommutation relation agrees with E7 root parity.
    pair_checks = 0
    commuting = 0
    anticommuting = 0
    label_to_root = {v: rootpair[mat_vec(P, v)] for v in labels}
    for a, b in combinations(labels, 2):
        lhs = omega(a, b, JSTD)
        ra = np.array(label_to_root[a], dtype=int)
        rb = np.array(label_to_root[b], dtype=int)
        dot = int(np.dot(ra, rb))
        assert dot % 4 == 0
        rhs = (dot // 4) % 2
        assert lhs == rhs
        pair_checks += 1
        if lhs:
            anticommuting += 1
        else:
            commuting += 1
    assert pair_checks == 1953
    assert anticommuting == 1008
    assert commuting == 945

    # Closed anticommuting Pauli XOR triangles are preserved objectwise.
    triangles = set()
    for a, b in combinations(labels, 2):
        if omega(a, b, JSTD) != 1:
            continue
        c = vec_xor(a, b)
        assert any(c)
        T = frozenset((a, b, c))
        triangles.add(T)
    assert len(triangles) == 336

    e7_triangles = set()
    for T in triangles:
        qs = tuple(mat_vec(P, v) for v in T)
        # In the E7 quotient the same closed triangle relation is q1+q2+q3=0.
        z = tuple(qs[0][i] ^ qs[1][i] ^ qs[2][i] for i in range(6))
        assert z == (0, 0, 0, 0, 0, 0)
        rs = frozenset(rootpair[q] for q in qs)
        assert len(rs) == 3
        e7_triangles.add(rs)
    assert len(e7_triangles) == 336

    checks = {
        "E7_symplectic_form_rank6": rank2(J) == 6,
        "basis_change_is_GL6F2": rank2(P) == 6,
        "basis_change_is_symplectic_to_standard_threequbit_gauge": np.array_equal((P.T @ J @ P) % 2, JSTD),
        "all_63_nonzero_standard_Pauli_directions_mapped": len(dictionary) == 63,
        "all_63_E7_root_pairs_hit_once": len(mapped_rootpairs) == 63,
        "all_1953_pair_relations_checked": pair_checks == 1953,
        "anticommuting_pair_count_1008": anticommuting == 1008,
        "commuting_pair_count_945": commuting == 945,
        "all_336_closed_anticommuting_XOR_triangles_preserved": len(e7_triangles) == 336,
    }

    return {
        "schema": "w33.schur64-e7-threequbit-pauli-objectwise-bridge.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "source_alignment": {
            "external_2026_Schur64": (
                "Nurowski arXiv:2609.10751 identifies the normal order-128 group as the real three-qubit Pauli group generated by -I and Xi,Zi for i=1,2,3."
            ),
            "repo_E7": (
                "Pass8489-8496 identifies all 63 antipodal E7 root pairs with all 63 nonzero vectors of a six-dimensional symplectic quotient."
            ),
        },
        "standard_coordinate_order": ["x1", "z1", "x2", "z2", "x3", "z3"],
        "E7_symplectic_matrix": J.astype(int).tolist(),
        "standard_symplectic_matrix": JSTD.astype(int).tolist(),
        "standard_to_E7_basis_matrix_columns": P.astype(int).tolist(),
        "chosen_E7_hyperbolic_basis_columns": [list(v) for v in symp_basis],
        "census": {
            "projective_threequbit_Pauli_directions": 63,
            "pair_relations_checked": pair_checks,
            "commuting_pairs": commuting,
            "anticommuting_pairs": anticommuting,
            "closed_anticommuting_XOR_triangles": len(e7_triangles),
        },
        "dictionary": dictionary,
        "theorem": (
            "In the standard Xi,Zi gauge used by the Schur64 real three-qubit Pauli normal subgroup, the 63 noncentral projective phase directions admit an explicit symplectic objectwise dictionary to the 63 antipodal E7 root pairs; the dictionary preserves every commutation relation and every one of the 336 closed anticommuting XOR triangles."
        ),
        "claim_boundary": (
            "This identifies the Schur64 normal phase quotient E3/Z(E3) with the repo's E7/three-qubit Pauli carrier. It does not yet identify Schur's 64 lines or 64 ordinary triple points objectwise with E7 roots, Pauli classes, or affine F2^6 states."
        ),
        "checks": checks,
    }


def main():
    r = build_result()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(r, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": r["status"],
        "directions": r["census"]["projective_threequbit_Pauli_directions"],
        "anticommuting_pairs": r["census"]["anticommuting_pairs"],
        "triangles": r["census"]["closed_anticommuting_XOR_triangles"],
    }, sort_keys=True))
    return 0 if r["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
