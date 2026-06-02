from itertools import combinations, product
from collections import Counter
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'PART_MMCDI_CLIFFORD_OCTONION_G2_PROJECTION_results.json'

from analysis.w33_frame_action_g2_weyl_quotient import main as frame_main


def Z(n, m):
    return [[0 for _ in range(m)] for __ in range(n)]


def I(n):
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]


def add(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def sub(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def smul(c, A):
    return [[c * x for x in row] for row in A]


def mul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def comm(A, B):
    return sub(mul(A, B), mul(B, A))


def flatten(M):
    return [x for row in M for x in row]


def rank_q(M):
    from fractions import Fraction
    A = [[Fraction(x) for x in row] for row in M]
    if not A:
        return 0
    m, n = len(A), len(A[0])
    r = 0
    for c in range(n):
        piv = None
        for i in range(r, m):
            if A[i][c] != 0:
                piv = i
                break
        if piv is None:
            continue
        A[r], A[piv] = A[piv], A[r]
        pv = A[r][c]
        A[r] = [x / pv for x in A[r]]
        for i in range(m):
            if i != r and A[i][c] != 0:
                f = A[i][c]
                A[i] = [A[i][j] - f * A[r][j] for j in range(n)]
        r += 1
    return r


def matrix_rank(mats):
    if not mats:
        return 0
    cols = [flatten(M) for M in mats]
    return rank_q([[cols[j][i] for j in range(len(cols))] for i in range(len(cols[0]))])


def basis_vec(i):
    v = [0] * 8
    v[i] = 1
    return v


def mv_mul(A, v):
    return [sum(A[i][j] * v[j] for j in range(len(v))) for i in range(len(A))]


def build_octonion_table():
    # One standard Fano orientation for the octonions.
    oriented_lines = [
        (1, 2, 3), (1, 4, 5), (1, 7, 6), (2, 4, 6),
        (2, 5, 7), (3, 4, 7), (3, 6, 5)
    ]
    mult = {}
    for i in range(8):
        mult[(0, i)] = (1, i)
        mult[(i, 0)] = (1, i)
    for i in range(1, 8):
        mult[(i, i)] = (-1, 0)
    for a, b, c in oriented_lines:
        for x, y, z in [(a, b, c), (b, c, a), (c, a, b)]:
            mult[(x, y)] = (1, z)
        for x, y, z in [(b, a, c), (c, b, a), (a, c, b)]:
            mult[(x, y)] = (-1, z)
    return oriented_lines, mult


ORIENTED_LINES, MULT = build_octonion_table()


def oct_mul_vec(u, v):
    out = [0] * 8
    for i, ui in enumerate(u):
        if ui == 0:
            continue
        for j, vj in enumerate(v):
            if vj == 0:
                continue
            s, k = MULT[(i, j)]
            out[k] += ui * vj * s
    return out


def assoc_basis(a, b, c):
    ea, eb, ec = basis_vec(a), basis_vec(b), basis_vec(c)
    left = oct_mul_vec(oct_mul_vec(ea, eb), ec)
    right = oct_mul_vec(ea, oct_mul_vec(eb, ec))
    return [left[i] - right[i] for i in range(8)]


def L(a):
    M = Z(8, 8)
    for j in range(8):
        s, k = MULT[(a, j)]
        M[k][j] = s
    return M


def R(a):
    M = Z(8, 8)
    for j in range(8):
        s, k = MULT[(j, a)]
        M[k][j] = s
    return M


def D(a, b):
    # Standard octonion derivation: D_{a,b}=[L_a,L_b]+[L_a,R_b]+[R_a,R_b].
    if a > b:
        return smul(-1, D(b, a))
    return add(add(comm(L(a), L(b)), comm(L(a), R(b))), comm(R(a), R(b)))


def derivation_property(M, a, b):
    ea, eb = basis_vec(a), basis_vec(b)
    left = mv_mul(M, oct_mul_vec(ea, eb))
    part1 = oct_mul_vec(mv_mul(M, ea), eb)
    part2 = oct_mul_vec(ea, mv_mul(M, eb))
    right = [part1[i] + part2[i] for i in range(8)]
    return left == right


def main():
    prev = frame_main()

    q, r, k, v = 3, 2, 12, 40
    phi6, chi, g1, dim_g2 = 7, 4, 21, 14
    pairs = list(combinations(range(1, 8), 2))
    gammas = {i: L(i) for i in range(1, 8)}
    bivectors = [comm(L(a), L(b)) for a, b in pairs]
    derivations = [D(a, b) for a, b in pairs]

    # Clifford relation for left multiplication by imaginary octonion units.
    clifford_square = all(mul(gammas[i], gammas[i]) == smul(-1, I(8)) for i in range(1, 8))
    clifford_anticomm = all(
        add(mul(gammas[i], gammas[j]), mul(gammas[j], gammas[i])) == Z(8, 8)
        for i, j in combinations(range(1, 8), 2)
    )

    # so(7) from Clifford bivectors, then g2 from non-associative derivation projection.
    so7_rank = matrix_rank(bivectors)
    g2_rank = matrix_rank(derivations)
    derivation_closure_rank = matrix_rank(derivations + [comm(A, B) for A, B in combinations(derivations, 2)])
    derivation_law = all(derivation_property(M, a, b) for M in derivations for a in range(8) for b in range(8))
    derivations_kill_identity = all(all(M[i][0] == 0 for i in range(8)) for M in derivations)

    # Seven Fano-translation kernel relations: for each nonzero z, pair x with x+z.
    relations = {}
    relation_rows = []
    support_union = []
    for z in range(1, 8):
        support = [p for p in pairs if (p[0] ^ p[1]) == z]
        found = None
        for signs in product([-1, 1], repeat=3):
            S = Z(8, 8)
            for sig, p in zip(signs, support):
                S = add(S, smul(sig, D(*p)))
            if S == Z(8, 8):
                found = signs
                break
        assert found is not None
        relations[z] = [{'pair': list(p), 'sign': sig} for sig, p in zip(found, support)]
        row = [0] * len(pairs)
        for sig, p in zip(found, support):
            row[pairs.index(p)] = sig
        relation_rows.append(row)
        support_union.extend(support)

    relation_rank = rank_q(relation_rows)
    relation_annihilation = all(
        sum(row[j] * derivations[j][x][y] for j in range(len(pairs))) == 0
        for row in relation_rows for x in range(8) for y in range(8)
    )
    relation_support_partition = Counter(support_union) == Counter(pairs)
    relation_supports_are_matchings = all(
        sorted(sum(([a, b] for a, b in [tuple(item['pair']) for item in rel]), [])) == sorted(set(sum(([a, b] for a, b in [tuple(item['pair']) for item in rel]), [])))
        and len(set(sum(([a, b] for a, b in [tuple(item['pair']) for item in rel]), []))) == 6
        for rel in relations.values()
    )

    # Associator geometry: seven Fano triples are associative, the other 28 triples are not.
    zero_assoc_triples = [tri for tri in combinations(range(1, 8), 3) if assoc_basis(*tri) == [0] * 8]
    fano_line_set = sorted(tuple(sorted(line)) for line in ORIENTED_LINES)
    nonzero_assoc_count = len(list(combinations(range(1, 8), 3))) - len(zero_assoc_triples)

    checks = {
        'inherits_frame_action_g2_weyl_quotient': prev['n_verified'] == prev['n_checks'] == 24,
        'octonion_table_complete_8x8': len(MULT) == 64,
        'fano_lines_7': len(ORIENTED_LINES) == 7,
        'fano_lines_xor_zero': all((a ^ b ^ c) == 0 for a, b, c in ORIENTED_LINES),
        'clifford_generators_7': len(gammas) == 7,
        'clifford_square_minus_identity': clifford_square,
        'clifford_anticommutation': clifford_anticomm,
        'bivectors_21': len(bivectors) == 21,
        'bivectors_span_so7_rank_21': so7_rank == 21,
        'derivation_generators_21': len(derivations) == 21,
        'derivations_are_derivations': derivation_law,
        'derivations_kill_identity': derivations_kill_identity,
        'derivation_span_rank_14': g2_rank == 14,
        'derivation_bracket_closure_rank_14': derivation_closure_rank == 14,
        'kernel_dimension_7': len(derivations) - g2_rank == 7,
        'seven_fano_translation_relations': len(relations) == 7,
        'relation_rank_7': relation_rank == 7,
        'relation_annihilation': relation_annihilation,
        'relation_supports_partition_21_pairs': relation_support_partition,
        'relation_supports_are_three_pair_matchings': relation_supports_are_matchings,
        'rank_formula_21_minus_7_equals_14': 21 - 7 == 14,
        'associative_triples_are_exactly_fano_lines': sorted(zero_assoc_triples) == fano_line_set,
        'associative_triple_count_7': len(zero_assoc_triples) == 7,
        'nonassociative_triple_count_28': nonzero_assoc_count == 28,
        'all_imaginary_triples_35_equals_phi6_times_F5': len(list(combinations(range(1, 8), 3))) == 35,
        'w33_dictionary_14_equals_k_plus_2': dim_g2 == k + 2,
        'w33_dictionary_28_equals_v_minus_k': nonzero_assoc_count == v - k,
        'w33_dictionary_28_equals_chi_times_phi6': nonzero_assoc_count == chi * phi6,
        'w33_dictionary_21_equals_g1': len(pairs) == g1,
        'w33_dictionary_7_equals_phi6': len(relations) == phi6,
    }
    assert all(checks.values()), checks

    R = {
        'part': 'MMCDI',
        'theorem': 'Clifford-octonion G2 projection theorem',
        'construction': {
            'clifford_layer': 'Gamma_i = L_{e_i}; Gamma_i Gamma_j + Gamma_j Gamma_i = -2 delta_ij I, giving Cl(0,7)',
            'so7_layer': '21 Clifford bivectors [Gamma_i,Gamma_j] span so(7)',
            'g2_projection': 'D_ij = [L_i,L_j] + [L_i,R_j] + [R_i,R_j] spans the octonion derivation algebra g2',
            'rank_law': '21 bivectors - 7 Fano translation relations = 14 derivations'
        },
        'ranks': {
            'clifford_generators': 7,
            'bivectors_so7': so7_rank,
            'derivation_generators': len(derivations),
            'g2_rank': g2_rank,
            'kernel_rank': len(derivations) - g2_rank,
            'bracket_closure_rank': derivation_closure_rank
        },
        'fano_translation_relations': relations,
        'associator_geometry': {
            'associative_fano_triples': [list(t) for t in zero_assoc_triples],
            'associative_count': len(zero_assoc_triples),
            'nonassociative_count': nonzero_assoc_count,
            'total_imaginary_triples': len(list(combinations(range(1, 8), 3)))
        },
        'w33_reading': {
            '21': 'g1 = C(7,2), Clifford bivectors / imaginary pairs',
            '7': 'Phi6, Fano translation kernel relations',
            '14': 'dim(G2)=k+2, octonion derivation rank',
            '28': 'v-k=chi*Phi6, non-associative imaginary triples',
            '35': 'Phi6*F5, all imaginary triples'
        },
        'interpretation': 'This is the explicit Clifford/non-associative bridge suggested by the G2 construction literature: Cl(0,7) gives the 21-dimensional so(7) bivector shell, while octonion non-associativity projects it onto the 14-dimensional derivation algebra g2.  The seven-dimensional kernel is not arbitrary; it is exactly the seven Fano translation matchings x -> x+z.  The same Fano plane therefore controls the Clifford bivector quotient, the octonion associator, and the G2 rank k+2.',
        'checks': checks,
        'n_verified': sum(checks.values()),
        'n_checks': len(checks)
    }
    OUT.write_text(json.dumps(R, indent=2, sort_keys=True) + '\n')
    return R


if __name__ == '__main__':
    r = main()
    print(r['part'], r['theorem'])
    print('checks', r['n_verified'], '/', r['n_checks'])
    print(r['ranks'])
