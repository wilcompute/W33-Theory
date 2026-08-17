#!/usr/bin/env python3
"""Passes 5736--5743: characteristic-3 quadratic evaluation code on the W33 point set.

Prior-art boundary:
  * the [40,10,18]_3 self-orthogonal design code, dual [40,30,4]_3 and its
    260 weight-4 dual words were already reported by B. G. Rodrigues (2008);
  * the degree-2 projective Reed--Muller / quadratic Veronese code on PG(3,3)
    is classical and its ternary higher-weight spectrum was treated by
    K. Kaipa and P. Pradhan (2024).

What this verifier contributes to the repository is the exact coordinate bridge:
  W33 non-collinearity = square of the symplectic form = one symmetric generator
  matrix for that ambient quadratic code, plus a sparse 40->10->40 factorization,
  the CSS/logical-line interpretation, and a 234-member census of distinct W33
  symplectic overlays that all preserve the same ambient code.

No measured-physics, Standard-Model, spacetime, coupling, or uniqueness claim follows.
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
J = np.array([[0,1,0,0],[-1,0,0,0],[0,0,0,1],[0,0,-1,0]], dtype=np.int64) % Q

# Monomial order: x0^2,x0x1,x0x2,x0x3,x1^2,x1x2,x1x3,x2^2,x2x3,x3^2.
B_CORE = np.array([
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
], dtype=np.int64)


def rank_mod(A, p=Q):
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


def build_points():
    pts = sorted({canonical_projective(v) for v in itertools.product(range(Q), repeat=4)
                  if any(v)})
    assert len(pts) == 40
    return pts


def build_veronese(pts):
    return np.array([[(p[i] * p[j]) % Q for i, j in MONOMIALS] for p in pts],
                    dtype=np.int64)


def bilinear(a, form, b):
    return int(np.asarray(a, dtype=np.int64) @ form @ np.asarray(b, dtype=np.int64)) % Q


def build_noncollinearity(pts, form=J):
    return np.array([[pow(bilinear(a, form, b), 2, Q) for b in pts] for a in pts],
                    dtype=np.int64)


def build_lines(pts):
    pidx = {p: i for i, p in enumerate(pts)}
    lines = set()
    for i, j in itertools.combinations(range(40), 2):
        a, b = np.asarray(pts[i]), np.asarray(pts[j])
        support = set()
        for x, y in itertools.product(range(Q), repeat=2):
            if x == y == 0:
                continue
            support.add(pidx[canonical_projective((x * a + y * b) % Q)])
        assert len(support) == 4
        lines.add(tuple(sorted(support)))
    lines = sorted(lines)
    assert len(lines) == 130
    return lines


def is_isotropic(line, pts, form=J):
    return bilinear(pts[line[0]], form, pts[line[1]]) == 0


def alternating_matrix(coeff):
    # Projective coordinates are entries 01,02,03,12,13,23.
    a,b,c,d,e,f = coeff
    M = np.zeros((4,4), dtype=np.int64)
    for (i,j), x in {
        (0,1):a, (0,2):b, (0,3):c, (1,2):d, (1,3):e, (2,3):f
    }.items():
        M[i,j] = x % Q
        M[j,i] = (-x) % Q
    return M


def nondegenerate_alternating_classes():
    classes = set()
    for coeff in itertools.product(range(Q), repeat=6):
        if not any(coeff):
            continue
        M = alternating_matrix(coeff)
        if rank_mod(M) == 4:
            classes.add(canonical_projective(coeff))
    classes = sorted(classes)
    assert len(classes) == 234
    return classes


def weight_enumerator(G):
    out = Counter()
    for coeff in itertools.product(range(Q), repeat=10):
        w = (np.asarray(coeff, dtype=np.int64) @ G) % Q
        out[int(np.count_nonzero(w))] += 1
    return dict(sorted(out.items()))


def srg_parameters(A):
    A = np.asarray(A, dtype=np.int64)
    degrees = A.sum(axis=1)
    assert len(set(map(int, degrees))) == 1
    lam, mu = set(), set()
    for i in range(len(A)):
        for j in range(i + 1, len(A)):
            common = int(A[i] @ A[j])
            (lam if A[i, j] else mu).add(common)
    assert len(lam) == len(mu) == 1
    return [len(A), int(degrees[0]), next(iter(lam)), next(iter(mu))]


def compute_certificate():
    pts = build_points()
    V = build_veronese(pts)       # 40 x 10
    G = V.T % Q                   # 10 x 40
    C = build_noncollinearity(pts)

    # 5736: exact coordinate bridge to the known quadratic Veronese / PRM code.
    assert rank_mod(G) == rank_mod(C) == rank_mod(np.vstack([G, C])) == 10
    weights = weight_enumerator(G)
    expected = {0:1, 18:1560, 24:21060, 27:18800, 30:16848, 36:780}
    assert weights == expected and sum(weights.values()) == Q ** 10

    # 5737: sparse symmetric-square compiler for this W33 polarity.
    assert np.array_equal((V @ B_CORE @ V.T) % Q, C)
    assert np.array_equal(B_CORE, B_CORE.T)
    assert np.array_equal((B_CORE @ B_CORE) % Q, np.eye(10, dtype=np.int64))
    assert np.count_nonzero(V) == 216
    assert np.count_nonzero(B_CORE) == 10
    assert np.count_nonzero(C) == 1080

    # 5738: square-zero and self-orthogonal standard CSS consequence.
    assert np.max((C @ C) % Q) == 0
    assert np.max((G @ G.T) % Q) == 0

    lines = build_lines(pts)
    H = np.zeros((130, 40), dtype=np.int64)
    for r, L in enumerate(lines):
        H[r, list(L)] = 1
    assert np.max((H @ V) % Q) == 0
    assert rank_mod(H) == 30
    assert rank_mod(np.vstack([G, H])) == 30  # C is contained in C^perp.
    assert set(map(int, H.sum(axis=1))) == {4}
    assert set(map(int, H.sum(axis=0))) == {13}

    # 5739: exact dual distance and support classification.
    for r in [1, 2, 3]:
        for support in itertools.combinations(range(40), r):
            assert rank_mod(G[:, support]) == r
    dependent4 = {tuple(s) for s in itertools.combinations(range(40), 4)
                  if rank_mod(G[:, s]) < 4}
    assert dependent4 == set(lines)

    # 5740: local-repair split for the selected W33 symplectic overlay.
    isotropic = [is_isotropic(L, pts) for L in lines]
    assert Counter(isotropic) == Counter({True: 40, False: 90})
    repair_profile = []
    for p in range(40):
        through = [r for r, L in enumerate(lines) if p in L]
        n_iso = sum(isotropic[r] for r in through)
        repair_profile.append((len(through), n_iso, len(through) - n_iso))
    assert set(repair_profile) == {(13, 4, 9)}
    assert np.max((H @ G.T) % Q) == 0

    # 5741: line incidence rows span the entire classical dual.
    assert 40 - rank_mod(H) == 10

    # 5742: minimum logical rays inherit the projective line-intersection graph.
    Aline = np.zeros((130, 130), dtype=np.int64)
    for i, Li in enumerate(lines):
        Si = set(Li)
        for j in range(i + 1, 130):
            if Si.intersection(lines[j]):
                Aline[i, j] = Aline[j, i] = 1
    assert srg_parameters(Aline) == [130, 48, 20, 16]
    I = [i for i, x in enumerate(isotropic) if x]
    O = [i for i, x in enumerate(isotropic) if not x]
    Aiso = Aline[np.ix_(I, I)]
    Aord = Aline[np.ix_(O, O)]
    Across = Aline[np.ix_(I, O)]
    assert srg_parameters(Aiso) == [40, 12, 2, 4]
    assert set(map(int, Across.sum(axis=1))) == {36}
    assert set(map(int, Across.sum(axis=0))) == {16}
    assert set(map(int, Aord.sum(axis=1))) == {32}
    assert np.array_equal((H @ H.T) % Q, (np.eye(130, dtype=np.int64) + Aline) % Q)

    # 5743: all projective symplectic polarities give different W33 overlays but the SAME code.
    forms = nondegenerate_alternating_classes()
    overlay_bytes = set()
    line_overlay_multiplicity = np.zeros(130, dtype=np.int64)
    for coeff in forms:
        form = alternating_matrix(coeff)
        Cj = build_noncollinearity(pts, form)
        assert rank_mod(Cj) == 10
        assert rank_mod(np.vstack([G, Cj])) == 10
        assert np.max((Cj @ Cj) % Q) == 0
        overlay_bytes.add(Cj.tobytes())
        iso_j = [is_isotropic(L, pts, form) for L in lines]
        assert sum(iso_j) == 40
        line_overlay_multiplicity += np.asarray(iso_j, dtype=np.int64)
    assert len(overlay_bytes) == 234
    assert set(map(int, line_overlay_multiplicity)) == {72}

    # Order calculation: PGL(4,3) / PGSp(4,3) = 234.
    gl4_order = (81-1)*(81-3)*(81-9)*(81-27)
    pgl4_order = gl4_order // 2
    sp4_order = (3**4) * (3**2 - 1) * (3**4 - 1)
    pgsp4_order = sp4_order  # |GSp|/(q-1) = |Sp| for q=3.
    assert pgl4_order == 12130560
    assert pgsp4_order == 51840
    assert pgl4_order // pgsp4_order == 234

    factor_terms = 2 * np.count_nonzero(V) + np.count_nonzero(B_CORE)
    return {
        "schema": "w33.pass5736_5743.quadratic_evaluation_code.v2",
        "prior_art": {
            "Rodrigues_2008": "[40,10,18]_3 self-orthogonal code; dual [40,30,4]_3 with 260 weight-4 words; full design/code automorphism group L4(3):2_1",
            "Kaipa_Pradhan_2024": "ternary quadratic Veronese 3-fold / second-order projective Reed-Muller code on PG(3,3), including higher weight spectra",
            "claim_tier": "parameters and Veronese family are prior art; coordinate bridge and machine-layer synthesis are new-to-repo unless separately sourced",
        },
        "pass_5736": {
            "identification": "rowspace_F3(W33_noncollinearity)=quadratic_Veronesecode_C3_on_PG(3,3)",
            "parameters": [40,10,18],
            "weight_enumerator": {str(k): int(v) for k, v in weights.items()},
            "codewords": 59049,
        },
        "pass_5737": {
            "factorization": "C=V B V^T mod 3",
            "V_shape": [40,10], "V_nnz": 216,
            "B_shape": [10,10], "B_nnz": 10,
            "B_squared_is_identity": True,
            "direct_C_nnz": 1080,
            "factorized_nonzero_term_count": int(factor_terms),
            "direct_over_factorized_term_ratio": float(1080 / factor_terms),
            "B": B_CORE.tolist(),
        },
        "pass_5738": {
            "C_squared_zero_mod3": True,
            "self_orthogonal": True,
            "standard_css_consequence": "[[40,20,4]]_3",
            "warning": "CSS parameters are a standard consequence of the known classical code and dual distance, not claimed as coding-theory novelty",
        },
        "pass_5739": {
            "dual_distance": 4,
            "minimum_projective_supports": 130,
            "minimum_vector_words": 260,
            "support_classification": "all projective lines of PG(3,3)",
        },
        "pass_5740": {
            "repair_groups_per_coordinate": 13,
            "queries_per_repair": 3,
            "w33_native_isotropic_groups": 4,
            "ambient_nonisotropic_groups": 9,
            "repair_law": "x_p=-sum_{q in L\\{p}} x_q mod 3",
        },
        "pass_5741": {
            "line_check_matrix_shape": [130,40],
            "line_check_rank_F3": 30,
            "row_weight": 4,
            "column_weight": 13,
            "kernel_dimension": 10,
            "rowspace_is_full_classical_dual": True,
            "containment": "C subset C^perp",
        },
        "pass_5742": {
            "minimum_logical_commutation_graph": "Grassmann line-intersection graph J_3(4,2)",
            "srg_parameters": [130,48,20,16],
            "w33_isotropic_induced_srg": [40,12,2,4],
            "isotropic_lines": 40,
            "nonisotropic_lines": 90,
            "isotropic_to_nonisotropic_degree": 36,
            "nonisotropic_to_isotropic_degree": 16,
            "nonisotropic_induced_degree": 32,
        },
        "pass_5743": {
            "ambient_code_automorphism_order": pgl4_order,
            "w33_polarity_stabilizer_order": pgsp4_order,
            "symplectic_overlay_count": 234,
            "distinct_overlay_matrices": 234,
            "all_overlays_generate_same_code": True,
            "native_w33_lines_per_overlay": 40,
            "ambient_lines": 130,
            "overlays_in_which_each_line_is_native": 72,
            "architecture_reading": "one 40-coordinate quadratic code supports 234 selectable W33 symplectic routing overlays without changing the code space",
            "boundary": "finite reconfiguration statement only; not a physical gauge-field or spacetime claim",
        },
    }


def main():
    result = compute_certificate()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("PASS_QUADRATIC_EVALUATION_CODE", json.dumps({
        "code": result["pass_5736"]["parameters"],
        "css": result["pass_5738"]["standard_css_consequence"],
        "dual_distance": result["pass_5739"]["dual_distance"],
        "line_supports": result["pass_5739"]["minimum_projective_supports"],
        "repair_profile": [13,4,9],
        "logical_graph": result["pass_5742"]["srg_parameters"],
        "symplectic_overlays": result["pass_5743"]["symplectic_overlay_count"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
