from __future__ import annotations
import json, time
from pathlib import Path
import numpy as np
from w33_pass1060_1064_core import *
from w33_pass1060_minimal_signed_cover import lift_signs, signed_perm

GENERATOR_POINT_INDICES = [0, 1, 4, 5, 13]


def matmul(A: tuple[int, ...], B: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(sum(A[4*i+k]*B[4*k+j] for k in range(4)) % 3
                 for i in range(4) for j in range(4))


def matneg(A: tuple[int, ...]) -> tuple[int, ...]:
    return tuple((-x) % 3 for x in A)


def matpow(A: tuple[int, ...], n: int) -> tuple[int, ...]:
    I = tuple(int(x) for x in np.eye(4, dtype=int).flat)
    out, base = I, A
    while n:
        if n & 1:
            out = matmul(out, base)
        base = matmul(base, base)
        n >>= 1
    return out


def canonical_projective(A: tuple[int, ...]) -> tuple[int, ...]:
    return min(A, matneg(A))


def transvection_matrix(v: tuple[int, ...]) -> tuple[int, ...]:
    vv = np.array(v, dtype=int) % 3
    M = (np.eye(4, dtype=int) + np.outer(vv, J @ vv)) % 3
    return tuple(int(x) for x in M.flat)


def compose_bytes(a: bytes, b: bytes) -> bytes:
    return bytes(a[b[i]] for i in range(len(a)))


def inverse_bytes(a: bytes) -> bytes:
    out = bytearray(len(a))
    for i, x in enumerate(a):
        out[x] = i
    return bytes(out)


def main():
    w = build_w33(); q = build_quot(w); axes = build_axes(w, q)
    e8 = build_e8(); iso = isometry(q, e8)
    reps = [e8.positive[iso[c]] for c in axes.coords]

    matrix_gens = [transvection_matrix(w.points[i]) for i in GENERATOR_POINT_INDICES]
    axis_gens = [axes.axis_gens[i] for i in GENERATOR_POINT_INDICES]
    signed_gens_perm = [signed_perm(p, lift_signs(p, reps)) for p in axis_gens]
    signed_gens = [bytes(pimages(g, 240)) for g in signed_gens_perm]

    I4 = tuple(int(x) for x in np.eye(4, dtype=int).flat)
    minusI4 = matneg(I4)
    id240 = bytes(range(240))
    neg240 = bytes(2*i + (b ^ 1) for i in range(120) for b in (0, 1))

    # Enumerate Sp(4,3) and the signed E8 action in lockstep.  This gives an
    # explicit extension isomorphism, not merely an equality of group orders.
    signed_image = {I4: id240}
    parent = {I4: (None, 0)}
    frontier = [I4]
    while frontier:
        nxt = []
        for M in frontier:
            sM = signed_image[M]
            for gi, (G, sG) in enumerate(zip(matrix_gens, signed_gens)):
                N = matmul(G, M)
                sN = compose_bytes(sG, sM)
                if N not in signed_image:
                    signed_image[N] = sN
                    parent[N] = (M, gi + 1)
                    nxt.append(N)
                elif signed_image[N] != sN:
                    raise AssertionError("generator map is not a well-defined homomorphism")
        frontier = nxt

    repsP = sorted({canonical_projective(M) for M in signed_image})
    section_signed = {M: signed_image[M] for M in repsP}

    def cocycle(M, N):
        P = matmul(M, N)
        return 0 if P == canonical_projective(P) else 1

    # The section construction proves the cocycle identity algebraically.  We
    # additionally check it on every group element and every ordered pair of
    # the five generating projective classes (648,000 exact instances).
    cocycle_failures = 0
    for g in repsP:
        for h in matrix_gens:
            gh = canonical_projective(matmul(g, h))
            for k in matrix_gens:
                hk = canonical_projective(matmul(h, k))
                lhs = cocycle(g, h) ^ cocycle(gh, k)
                rhs = cocycle(h, k) ^ cocycle(g, hk)
                cocycle_failures += lhs != rhs

    # The exhaustive Cayley-graph lockstep above proves that the matrix and
    # signed-root extensions are isomorphic.  Extract a shortest positive-word
    # witness for the central element -I from the same breadth-first tree.
    word = []
    cur = minusI4
    while cur != I4:
        prev, label = parent[cur]
        word.append(label)
        cur = prev
    word.reverse()
    Mword, Sword = I4, id240
    for label in word:
        idx = label - 1
        Mword = matmul(matrix_gens[idx], Mword)
        Sword = compose_bytes(signed_gens[idx], Sword)

    table = [[cocycle(canonical_projective(a), canonical_projective(b))
              for b in matrix_gens] for a in matrix_gens]

    checks = {
        'Sp43_matrix_group_order_51840': len(signed_image) == 51840,
        'PSp43_projective_quotient_order_25920': len(repsP) == 25920,
        'kernel_minusI_maps_to_global_root_negation': signed_image[minusI4] == neg240,
        'normalized_on_identity': all(cocycle(I4, g) == 0 and cocycle(g, I4) == 0 for g in repsP),
        'cocycle_identity_generator_complete_check': cocycle_failures == 0,
        'matrix_and_signed_root_extensions_match_on_full_Cayley_graph': len(signed_image) == 51840,
        'short_relator_projects_to_identity': canonical_projective(Mword) == I4,
        'short_relator_lifts_to_minusI': Mword == minusI4,
        'same_relator_lifts_to_global_root_negation': Sword == neg240,
        'base_group_is_perfect': w.G.derived_subgroup().order() == 25920,
    }
    assert all(checks.values()), checks

    return {
        'schema': 'w33.pass1065.schur_cocycle.v1',
        'status': 'PASS',
        'headline': 'A normalized C2-valued cocycle for PSp(4,3) is extracted from the canonical projective-matrix section.  It is nontrivial, matches the signed E8-root extension generator-by-generator, and therefore represents the unique nonzero Schur-multiplier class.',
        'section_rule': 'Represent a projective class by the lexicographically smaller of M and -M in Sp(4,3).  Set c(g,h)=0 when s(g)s(h)=s(gh), and 1 when s(g)s(h)=-s(gh).',
        'orders': {'PSp43': 25920, 'Sp43': 51840, 'kernel': 2},
        'generator_point_indices': GENERATOR_POINT_INDICES,
        'generator_cocycle_table': table,
        'shortest_detected_nontrivial_relator': {
            'word_left_multiplication_labels': word,
            'length': len(word),
            'matrix_lift': '-I4',
            'root_lift': 'global antipodal permutation on 240 roots'
        },
        'cohomology_decision': {
            'class_nonzero': True,
            'schur_multiplier_order': 2,
            'conclusion': 'The class generates H^2(PSp(4,3),C2).',
            'primary_external_anchor': 'ATLAS U4(2): order 25920, multiplier 2, outer automorphism order 2.'
        },
        'maslov_metaplectic_comparison': 'The matrix cocycle is the central sign cocycle of Sp(4,3)->PSp(4,3).  The lockstep E8-root action gives an explicit isomorphism of extensions.  Since the Schur multiplier is C2, this is the same cohomology class as every nontrivial finite metaplectic/Maslov realization, although normalized cocycle representatives may differ by a coboundary.',
        'cocycle_identity_checks': 25920 * 5 * 5,
        'cayley_transition_checks': 51840 * 5,
        'check_count': len(checks),
        'checks': checks,
        'scope': 'Exact finite arithmetic over F3 plus exact signed permutations on 240 roots.  The comparison is at cohomology-class/extension level; it does not claim literal equality with a convention-dependent analytic Maslov formula.'
    }


if __name__ == '__main__':
    started = time.time(); result = main()
    output = Path(__file__).resolve().parents[1] / 'data' / 'w33_pass1065_schur_cocycle.json'
    output.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'status': result['status'], 'check_count': result['check_count'], 'relator_length': result['shortest_detected_nontrivial_relator']['length'], 'seconds': round(time.time()-started, 3)}, indent=2))
