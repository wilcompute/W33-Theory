#!/usr/bin/env python3
"""Passes 5736--5743: characteristic-3 quadratic evaluation code on the W33 point set.

This verifier deliberately separates the classical/background layer from the repo-specific
identification.

Classical/background:
  * homogeneous quadrics on PG(3,3) form the degree-2 projective evaluation code;
  * the quadratic Veronese feature space has dimension C(4+2-1,2)=10.

Exact finite result checked here:
  * the W(3,3) NON-COLLINEARITY adjacency matrix C over F3 has rowspace equal to that
    degree-2 evaluation code;
  * it is a [40,10,18]_3 self-orthogonal code with full weight enumerator
      1 + 1560 z^18 + 21060 z^24 + 18800 z^27 + 16848 z^30 + 780 z^36;
  * C = V B V^T over F3 for a sparse involutory 10x10 core B;
  * C^2=0 over F3;
  * the dual has distance 4, and its 130 minimum projective supports are exactly the
    130 projective lines of PG(3,3), each represented by the all-one incidence word;
  * the standard q-ary CSS construction with the same self-orthogonal C on X and Z
    therefore has exact parameters [[40,20,4]]_3;
  * every classical coordinate has 13 three-query repair groups, split as 4 W33-isotropic
    lines and 9 non-isotropic ambient projective lines;
  * the 130 line checks have rank 30 and span C^perp;
  * the commutation graph of minimum logical rays is the line-intersection Grassmann graph
    J_3(4,2)=SRG(130,48,20,16).  The 40 W33-isotropic lines induce SRG(40,12,2,4).

Boundary:
  The PRM/Veronese family and symmetric-power dimension are classical.  What is promoted
  here is the exact identification of the W33 characteristic-3 complement-adjacency
  rowspace with that code, plus the exact finite consequences above.  The 130-line dual
  geometry belongs to ambient PG(3,3); W33 singles out 40 isotropic lines among those 130.
  No physical mass, coupling, spacetime, Standard-Model, or uniqueness claim is inferred.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

import numpy as np

Q = 3
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PART_W33_PASS5736_5743_QUADRATIC_EVALUATION_CODE.json"
MONOMIALS = [(i, j) for i in range(4) for j in range(i, 4)]

# In the monomial order x0^2,x0x1,x0x2,x0x3,x1^2,x1x2,x1x3,x2^2,x2x3,x3^2.
B_CORE = np.array(
    [
        [0,0,0,0,1,0,0,0,0,0],
        [0,1,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,2,0,0,0],
        [0,0,0,0,0,1,0,0,0,0],
        [1,0,0,0,0,0,0,0,0,0],
        [0,0,0,1,0,0,0,0,0,0],
        [0,0,2,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,1],
        [0,0,0,0,0,0,0,0,1,0],
        [0,0,0,0,0,0,0,1,0,0],
    ],
    dtype=np.int64,
)

J = np.array(
    [[0,1,0,0],[-1,0,0,0],[0,0,0,1],[0,0,-1,0]], dtype=np.int64
) % Q


def rank_mod(A: np.ndarray, p: int = Q) -> int:
    A = np.asarray(A, dtype=np.int64).copy() % p
    m, n = A.shape
    r = 0
    for c in range(n):
        pivot = next((i for i in range(r, m) if A[i, c] % p), None)
        if pivot is None:
            continue
        A[[r, pivot]] = A[[pivot, r]]
        A[r] = (A[r] * pow(int(A[r, c]), -1, p)) % p
        for i in range(m):
            if i != r and A[i, c] % p:
                A[i] = (A[i] - A[i, c] * A[r]) % p
        r += 1
        if r == m:
            break
    return r


def canonical_projective(v):
    v = tuple(int(x) % Q for x in v)
    if not any(v):
        return None
    i = next(i for i, x in enumerate(v) if x)
    inv = pow(v[i], -1, Q)
    return tuple((x * inv) % Q for x in v)


def projective_points():
    seen = set()
    pts = []
    for raw in itertools.product(range(Q), repeat=4):
        if raw == (0,0,0,0):
            continue
        p = canonical_projective(raw)
        if p not in seen:
            seen.add(p)
            pts.append(p)
    pts.sort()
    assert len(pts) == 40
    return pts


def veronese_matrix(pts):
    # Rows are projective points; columns are homogeneous quadratic monomials.
    return np.array(
        [[(p[i] * p[j]) % Q for i, j in MONOMIALS] for p in pts],
        dtype=np.int64,
    )


def symplectic_value(a, b):
    return int(np.asarray(a, dtype=np.int64) @ J @ np.asarray(b, dtype=np.int64)) % Q


def noncollinearity_matrix(pts):
    n = len(pts)
    C = np.zeros((n, n), dtype=np.int64)
    for i, a in enumerate(pts):
        for j, b in enumerate(pts):
            C[i, j] = pow(symplectic_value(a, b), 2, Q)
    return C % Q


def projective_lines(pts):
    pidx = {p: i for i, p in enumerate(pts)}
    lines = set()
    for i, j in itertools.combinations(range(len(pts)), 2):
        a = np.asarray(pts[i], dtype=np.int64)
        b = np.asarray(pts[j], dtype=np.int64)
        support = set()
        for x, y in itertools.product(range(Q), repeat=2):
            if x == 0 and y == 0:
                continue
            p = canonical_projective((x * a + y * b) % Q)
            support.add(pidx[p])
        assert len(support) == 4
        lines.add(tuple(sorted(support)))
    lines = sorted(lines)
    assert len(lines) == 130
    return lines


def is_isotropic_line(line, pts):
    return symplectic_value(pts[line[0]], pts[line[1]]) == 0


def all_codewords(G):
    # G is 10x40. Exhaust all 3^10 coefficient vectors exactly.
    weights = Counter()
    for coeff in itertools.product(range(Q), repeat=G.shape[0]):
        c = np.asarray(coeff, dtype=np.int64)
        word = (c @ G) % Q
        weights[int(np.count_nonzero(word))] += 1
    return dict(sorted(weights.items()))


def srg_parameters(A):
    A = np.asarray(A, dtype=np.int64)
    n = A.shape[0]
    degrees = A.sum(axis=1)
    assert len(set(map(int, degrees))) == 1
    k = int(degrees[0])
    lam = set()
    mu = set()
    for i in range(n):
        for j in range(i + 1, n):
            common = int(A[i] @ A[j])
            (lam if A[i, j] else mu).add(common)
    assert len(lam) == 1 and len(mu) == 1
    return [n, k, next(iter(lam)), next(iter(mu))]


def compute_certificate():
    pts = projective_points()
    V = veronese_matrix(pts)          # 40x10
    G = V.T % Q                       # 10x40 generator
    C = noncollinearity_matrix(pts)   # 40x40

    assert rank_mod(G) == 10
    assert rank_mod(C) == 10
    assert rank_mod(np.vstack([G, C])) == 10
    assert np.array_equal((V @ B_CORE @ V.T) % Q, C)
    assert np.array_equal((B_CORE @ B_CORE) % Q, np.eye(10, dtype=np.int64))
    assert np.array_equal(B_CORE, B_CORE.T)
    assert np.count_nonzero(B_CORE) == 10
    assert np.count_nonzero(V) == 216
    assert np.count_nonzero(C) == 1080

    # SRG complement identity in characteristic 3: C^2=0.
    assert np.max((C @ C) % Q) == 0
    assert np.max((G @ G.T) % Q) == 0

    weights = all_codewords(G)
    expected_weights = {0:1, 18:1560, 24:21060, 27:18800, 30:16848, 36:780}
    assert weights == expected_weights
    assert sum(weights.values()) == Q ** 10

    lines = projective_lines(pts)
    H = np.zeros((len(lines), len(pts)), dtype=np.int64)
    for r, L in enumerate(lines):
        H[r, list(L)] = 1
    assert np.max((H @ V) % Q) == 0
    assert rank_mod(H) == 30
    assert len(pts) - rank_mod(H) == 10
    assert rank_mod(np.vstack([G, H])) == 40  # C direct-sums a complementary 30-space.
    assert set(map(int, H.sum(axis=1))) == {4}
    assert set(map(int, H.sum(axis=0))) == {13}

    # Dual distance: no 1-, 2-, or 3-column dependence in G; line incidence gives d^perp<=4.
    for r in [1, 2, 3]:
        for support in itertools.combinations(range(40), r):
            assert rank_mod(G[:, support]) == r
    dual_distance = 4

    # Classify every dependent 4-subset: exactly the 130 projective lines.
    dependent4 = set()
    for support in itertools.combinations(range(40), 4):
        if rank_mod(G[:, support]) < 4:
            dependent4.add(tuple(support))
    assert dependent4 == set(lines)

    iso = [is_isotropic_line(L, pts) for L in lines]
    assert sum(iso) == 40 and len(iso) - sum(iso) == 90

    # Every point has 13 repair lines, split 4 isotropic + 9 non-isotropic.
    repair_profile = []
    for p in range(40):
        through = [r for r, L in enumerate(lines) if p in L]
        n_iso = sum(1 for r in through if iso[r])
        repair_profile.append((len(through), n_iso, len(through) - n_iso))
    assert set(repair_profile) == {(13, 4, 9)}

    # For every codeword and every line, the four symbols sum to zero; hence any symbol
    # is reconstructed from the other three by x_p = -sum_{q in L\{p}} x_q.
    assert np.max((H @ G.T) % Q) == 0

    # Line-intersection / minimum-logical commutation graph.
    Aline = np.zeros((130, 130), dtype=np.int64)
    for i, Li in enumerate(lines):
        Si = set(Li)
        for j in range(i + 1, 130):
            if Si.intersection(lines[j]):
                Aline[i, j] = Aline[j, i] = 1
    assert srg_parameters(Aline) == [130, 48, 20, 16]

    I = [i for i, b in enumerate(iso) if b]
    O = [i for i, b in enumerate(iso) if not b]
    Aiso = Aline[np.ix_(I, I)]
    Aord = Aline[np.ix_(O, O)]
    Across_IO = Aline[np.ix_(I, O)]
    assert srg_parameters(Aiso) == [40, 12, 2, 4]
    assert set(map(int, Across_IO.sum(axis=1))) == {36}
    assert set(map(int, Across_IO.sum(axis=0))) == {16}
    assert set(map(int, Aord.sum(axis=1))) == {32}

    # The line incidence rows are minimum dual rays. Their dot product is intersection
    # number mod 3, hence two distinct minimum logical rays anticommute exactly when the
    # corresponding projective lines intersect.
    gram_lines = (H @ H.T) % Q
    assert np.array_equal((gram_lines - np.eye(130, dtype=np.int64) - Aline) % Q,
                          np.zeros((130,130), dtype=np.int64))

    result = {
        "schema": "w33.pass5736_5743.quadratic_evaluation_code.v1",
        "boundary": (
            "PRM/Veronese evaluation codes are classical. The exact promoted result is the "
            "W33 characteristic-3 non-collinearity-rowspace identification and its finite "
            "code/CSS/line-geometry consequences. The 130 dual lines are ambient PG(3,3), "
            "with W33 selecting the 40 isotropic lines. No measured-physics claim is made."
        ),
        "projective_space": {
            "field": 3,
            "points": 40,
            "lines": 130,
            "w33_isotropic_lines": 40,
            "ambient_nonisotropic_lines": 90,
        },
        "pass_5736": {
            "identification": "rowspace_F3(W33_noncollinearity) = degree_2_projective_quadratic_evaluation_code_on_PG(3,3)",
            "classical_parameters": [40, 10, 18],
            "weight_enumerator": {str(k): v for k, v in weights.items()},
            "codewords": int(Q ** 10),
        },
        "pass_5737": {
            "factorization": "C = V B V^T mod 3",
            "V_shape": [40, 10],
            "V_nnz": int(np.count_nonzero(V)),
            "B_shape": [10, 10],
            "B_nnz": int(np.count_nonzero(B_CORE)),
            "B_squared_is_identity": True,
            "direct_C_nnz": int(np.count_nonzero(C)),
            "factorized_nonzero_term_count": int(2 * np.count_nonzero(V) + np.count_nonzero(B_CORE)),
            "direct_over_factorized_term_ratio": float(np.count_nonzero(C) / (2*np.count_nonzero(V)+np.count_nonzero(B_CORE))),
            "B": B_CORE.tolist(),
        },
        "pass_5738": {
            "C_squared_zero_mod3": True,
            "self_orthogonal": True,
            "css_parameters": [[40, 20, 4]],
            "css_notation": "[[40,20,4]]_3",
        },
        "pass_5739": {
            "dual_distance": dual_distance,
            "minimum_projective_supports": 130,
            "minimum_vector_words": 260,
            "support_classification": "all projective lines of PG(3,3)",
            "line_word": "all-one incidence vector on the four points of the line, up to scalar 1 or 2",
        },
        "pass_5740": {
            "repair_groups_per_coordinate": 13,
            "queries_per_repair": 3,
            "w33_native_isotropic_groups": 4,
            "ambient_nonisotropic_groups": 9,
            "repair_law": "x_p = -sum_{q in L\\{p}} x_q mod 3",
        },
        "pass_5741": {
            "line_check_matrix_shape": [130, 40],
            "line_check_rank_F3": 30,
            "row_weight": 4,
            "column_weight": 13,
            "kernel_dimension": 10,
            "rowspace_equals_full_classical_dual": True,
        },
        "pass_5742": {
            "minimum_logical_commutation_graph": "Grassmann line-intersection graph J_3(4,2)",
            "srg_parameters": [130, 48, 20, 16],
            "w33_isotropic_induced_srg": [40, 12, 2, 4],
            "isotropic_to_nonisotropic_degree": 36,
            "nonisotropic_to_isotropic_degree": 16,
            "nonisotropic_induced_degree": 32,
        },
        "pass_5743": {
            "prior_art_guard": [
                "projective Reed-Muller / projective quadratic evaluation family is classical",
                "Veronese quadratic embedding is classical",
                "symmetric-power dimension bound is classical",
            ],
            "repo_specific_claim": (
                "the W33 non-collinearity adjacency over F3 is a square-zero symmetric "
                "rank-10 generator of this classical code, exposing a sparse 40->10->40 "
                "compiler and a W33 40+90 split of its minimum-dual line geometry"
            ),
        },
    }
    return result


def main():
    result = compute_certificate()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("PASS_QUADRATIC_EVALUATION_CODE", json.dumps({
        "code": result["pass_5736"]["classical_parameters"],
        "css": result["pass_5738"]["css_notation"],
        "dual_distance": result["pass_5739"]["dual_distance"],
        "line_supports": result["pass_5739"]["minimum_projective_supports"],
        "repair_profile": [result["pass_5740"]["repair_groups_per_coordinate"],
                           result["pass_5740"]["w33_native_isotropic_groups"],
                           result["pass_5740"]["ambient_nonisotropic_groups"]],
        "logical_graph": result["pass_5742"]["srg_parameters"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
