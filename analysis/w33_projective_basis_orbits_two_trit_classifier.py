#!/usr/bin/env python3
"""Six PSp(4,3) orbits of projective bases and a minimal two-trit classifier.

This continues the quartic determinant/matroid bridge.  Four independent Pauli
projective directions in PG(3,3) always give determinant one in the Cauchy--Binet
quartic, so det alone cannot distinguish the geometry of a four-direction basis.
The missing information is the zero pattern of the native symplectic Gram matrix.

For a projective basis B={v0,v1,v2,v3}, define

    z_ij = 1 - <vi,vj>^2 in F3.

Because every nonzero scalar in F3 has square one, z_ij is exactly the projective
orthogonality indicator: one for a W33 edge and zero otherwise.  Two symmetric
projective invariants then suffice:

    E = sum_{i<j} z_ij                         (edge count mod 3)
    W = sum_i sum_{j<k, j,k != i} z_ij z_ik  (adjacent-edge-pair count mod 3).

Exhaustion of all C(40,4)=91390 four-point subsets gives 63180 projective bases.
Under PSp(4,3) these bases split into exactly six orbits, classified completely
by the induced orthogonality graph, and the pair (E,W) is distinct on all six:

  C4          :  1620, (E,W)=(1,1), stabilizer 16
  P4          : 12960, (0,2), stabilizer 2
  P3 + K1     : 25920, (2,1), stabilizer 1
  2 K2        :  3240, (2,0), stabilizer 8
  K2 + 2 K1   : 12960, (1,0), stabilizer 2
  4 K1        :  6480, (0,0), stabilizer 4

The C4 orbit is exactly the 1620 generalized-quadrangle apartments.  For an
ordered apartment a-b-c-d-a the symplectic Gram Pfaffian is

    Pf(G) = -<a,c><b,d>,

because the four cycle-edge pairings vanish.  Hence Pf(G)^2=1 and the quartic
determinant is forced to one from incidence alone.  This is the point-shadow of
the 1620 minimum-weight Levi 8-cycle apartments already certified in the repo.

Boundary: this is finite geometry/representation theory.  The two trits are
canonical discrete observables of a projective basis; no physical controller,
Hamiltonian addressability, or non-Clifford gate is inferred.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter, deque
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_projective_basis_orbits_two_trit_classifier.json"
q = 3
J = np.array(
    [[0, 1, 0, 0], [-1, 0, 0, 0], [0, 0, 0, 1], [0, 0, -1, 0]],
    dtype=np.int64,
) % q


def canon(v):
    v = np.asarray(v, dtype=np.int64) % q
    i = next(i for i, x in enumerate(v) if x)
    return tuple((v * pow(int(v[i]), -1, q)) % q)


P = sorted({canon(v) for v in itertools.product(range(q), repeat=4) if any(v)})
PI = {x: i for i, x in enumerate(P)}
assert len(P) == 40


def omega(a, b):
    return int(np.asarray(a, dtype=np.int64) @ J @ np.asarray(b, dtype=np.int64) % q)


def rank_mod3(cols):
    A = np.asarray(cols, dtype=np.int64).T.copy() % q
    r = 0
    for c in range(A.shape[1]):
        p = next((i for i in range(r, A.shape[0]) if A[i, c]), None)
        if p is None:
            continue
        A[[r, p]] = A[[p, r]]
        A[r] = A[r] * pow(int(A[r, c]), -1, q) % q
        for i in range(A.shape[0]):
            if i != r and A[i, c]:
                A[i] = (A[i] - A[i, c] * A[r]) % q
        r += 1
    return r


def det_mod3(cols):
    A = np.asarray(cols, dtype=np.int64).T.copy() % q
    d = 1
    for c in range(4):
        p = next((i for i in range(c, 4) if A[i, c]), None)
        if p is None:
            return 0
        if p != c:
            A[[c, p]] = A[[p, c]]
            d = -d
        x = int(A[c, c])
        d = d * x % q
        inv = pow(x, -1, q)
        for i in range(c + 1, 4):
            if A[i, c]:
                A[i] = (A[i] - A[i, c] * inv * A[c]) % q
    return d % q


def graph_signature(S):
    deg = [0, 0, 0, 0]
    edges = 0
    for i, j in itertools.combinations(range(4), 2):
        if omega(P[S[i]], P[S[j]]) == 0:
            edges += 1
            deg[i] += 1
            deg[j] += 1
    sig = (edges, tuple(sorted(deg)))
    names = {
        (4, (2, 2, 2, 2)): "C4",
        (3, (1, 1, 2, 2)): "P4",
        (2, (0, 1, 1, 2)): "P3+K1",
        (2, (1, 1, 1, 1)): "2K2",
        (1, (0, 0, 1, 1)): "K2+2K1",
        (0, (0, 0, 0, 0)): "4K1",
    }
    assert sig in names
    return names[sig], edges, deg


def classifier(S):
    z = {}
    for i, j in itertools.combinations(range(4), 2):
        s = omega(P[S[i]], P[S[j]])
        z[i, j] = (1 - s * s) % q
    E = sum(z.values()) % q
    W = 0
    for i in range(4):
        js = [j for j in range(4) if j != i]
        for j, k in itertools.combinations(js, 2):
            a = z[tuple(sorted((i, j)))]
            b = z[tuple(sorted((i, k)))]
            W = (W + a * b) % q
    return E, W


def trans(v):
    v = np.asarray(v, dtype=np.int64).reshape(1, 4) % q
    c = J @ v.T
    g = (np.eye(4, dtype=np.int64) + c @ v) % q
    assert np.array_equal(g @ J @ g.T % q, J)
    return g


def point_perm(g):
    return tuple(PI[canon(np.asarray(x, dtype=np.int64) @ g)] for x in P)


def pf4(G):
    return int((G[0, 1] * G[2, 3] - G[0, 2] * G[1, 3] + G[0, 3] * G[1, 2]) % q)


def main(write=True):
    bases = set()
    by_type = Counter()
    classifier_by_type = {}
    determinant_values = set()
    apartment_pf_sq = set()

    for S in itertools.combinations(range(40), 4):
        if rank_mod3([P[i] for i in S]) != 4:
            continue
        bases.add(S)
        name, _, _ = graph_signature(S)
        by_type[name] += 1
        ew = classifier(S)
        if name in classifier_by_type:
            assert classifier_by_type[name] == ew
        else:
            classifier_by_type[name] = ew
        d = det_mod3([P[i] for i in S])
        determinant_values.add((d * d) % q)
        if name == "C4":
            V = np.asarray([P[i] for i in S], dtype=np.int64).T % q
            G = V.T @ J @ V % q
            apartment_pf_sq.add((pf4(G) ** 2) % q)

    expected_counts = {
        "C4": 1620,
        "P4": 12960,
        "P3+K1": 25920,
        "2K2": 3240,
        "K2+2K1": 12960,
        "4K1": 6480,
    }
    expected_classifier = {
        "C4": (1, 1),
        "P4": (0, 2),
        "P3+K1": (2, 1),
        "2K2": (2, 0),
        "K2+2K1": (1, 0),
        "4K1": (0, 0),
    }
    assert len(bases) == 63180
    assert dict(by_type) == expected_counts
    assert classifier_by_type == expected_classifier
    assert len(set(classifier_by_type.values())) == 6
    assert determinant_values == {1}
    assert apartment_pf_sq == {1}

    seed_vectors = [np.eye(4, dtype=np.int64)[i] for i in range(4)] + [
        np.array(v, dtype=np.int64)
        for v in ((1, 1, 0, 0), (0, 0, 1, 1), (1, 0, 1, 0), (0, 1, 0, 1))
    ]
    gens = [point_perm(trans(v)) for v in seed_vectors]

    unseen = set(bases)
    orbits = []
    while unseen:
        seed = next(iter(unseen))
        orb = {seed}
        Q = deque([seed])
        while Q:
            S = Q.popleft()
            for p in gens:
                T = tuple(sorted(p[i] for i in S))
                assert T in bases
                if T not in orb:
                    orb.add(T)
                    Q.append(T)
        unseen.difference_update(orb)
        orbits.append(orb)

    assert len(orbits) == 6
    orbit_rows = []
    for orb in orbits:
        names = {graph_signature(S)[0] for S in orb}
        assert len(names) == 1
        name = next(iter(names))
        assert len(orb) == expected_counts[name]
        orbit_rows.append(
            {
                "graph": name,
                "orbit_size": len(orb),
                "PSp_stabilizer_order": 25920 // len(orb),
                "classifier_EW": list(classifier_by_type[name]),
            }
        )
    orbit_rows.sort(key=lambda r: (r["orbit_size"], r["graph"]))

    out = {
        "schema": "w33.projective_basis_orbits_two_trit_classifier.v1",
        "status": "PASS",
        "headline": "The 63180 projective bases of PG(3,3) split into exactly six PSp(4,3) orbits, classified by the induced W33 orthogonality graph. The symmetric projective pair (E,W) over F3 is distinct on all six and therefore gives a minimal two-trit orbit classifier. The C4 orbit has size 1620 and is exactly the apartment shell.",
        "totals": {
            "PG33_points": 40,
            "four_point_subsets": 91390,
            "projective_bases": 63180,
            "dependent_four_sets": 28210,
            "PSp_order": 25920,
            "basis_orbits": 6,
        },
        "orbits": orbit_rows,
        "classifier": {
            "orthogonality_bit": "z_ij = 1 - <v_i,v_j>^2 in F3",
            "E": "sum_{i<j} z_ij mod 3",
            "W": "sum_i sum_{j<k, j,k != i} z_ij z_ik mod 3",
            "distinct_pairs": {k: list(v) for k, v in expected_classifier.items()},
            "minimality": "One trit has only three values and cannot classify six orbits; the displayed two trits do classify all six.",
        },
        "determinant_boundary": {
            "quartic_det_on_every_projective_basis": 1,
            "consequence": "The four-direction determinant phase is universal across all six basis orbits and cannot by itself distinguish an apartment from another projective basis.",
        },
        "apartment": {
            "graph": "C4",
            "count": 1620,
            "basis_fraction": "1/39",
            "PSp_stabilizer_order": 16,
            "pfaffian_formula": "For ordered a-b-c-d-a, Pf(G)=-<a,c><b,d>; hence Pf(G)^2=1.",
            "levi_bridge": "These are the point shadows of the 1620 minimum-weight Levi 8-cycle apartments already certified in Pass 5042 / the apartment code arc.",
        },
        "boundary": "Exact finite geometry only. The classifier is a canonical pair of discrete projective observables; no hardware addressability, Hamiltonian coupling, or physical non-Clifford action is claimed.",
        "checks": {
            "63180_bases": True,
            "six_PSp_orbits": True,
            "graph_type_classifies_orbit": True,
            "two_trit_pairs_distinct": True,
            "determinant_blind_across_bases": True,
            "1620_C4_apartments": True,
            "apartment_pfaffian_square_one": True,
        },
    }
    if write:
        OUT.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    main(True)
