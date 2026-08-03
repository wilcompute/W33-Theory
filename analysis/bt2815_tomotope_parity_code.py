#!/usr/bin/env python3
from __future__ import annotations

from itertools import combinations, permutations
from collections import Counter
import hashlib
import json
from bt2810_signed_support_tomotope import build_poset, canon_sign, signed_faces, is_incident


def phase_bits(v):
    v = canon_sign(v)
    assert v[0] == 1 and all(x in (-1, 1) for x in v)
    return tuple(1 if v[i] == -1 else 0 for i in (1, 2, 3))


def parity(bits):
    return sum(bits) % 2


def minority_coordinate(v):
    v = canon_sign(v)
    counts = Counter(v)
    assert sorted(counts.values()) == [1, 3]
    minority = min(counts, key=counts.get)
    return v.index(minority)


def permute_sign(v, p):
    out = [0] * 4
    for i, x in enumerate(v):
        out[p[i]] = x
    return canon_sign(out)


def cell_from_full_sign(v):
    v = canon_sign(v)
    if parity(phase_bits(v)) == 0:
        return ('T', v)
    j = minority_coordinate(v)
    return ('H', tuple(i for i in range(4) if i != j))


def hamming(a, b):
    return sum(x != y for x, y in zip(a, b))


def main():
    ranks, incidence = build_poset()
    full = signed_faces(4)
    even = [v for v in full if parity(phase_bits(v)) == 0]
    odd = [v for v in full if parity(phase_bits(v)) == 1]
    C = [phase_bits(v) for v in even]
    O = [phase_bits(v) for v in odd]
    mapped = [cell_from_full_sign(v) for v in full]

    equiv = True
    for p in permutations(range(4)):
        for v in full:
            lhs = cell_from_full_sign(permute_sign(v, p))
            rhs = cell_from_full_sign(v)
            if rhs[0] == 'T':
                rhs = ('T', permute_sign(rhs[1], p))
            else:
                rhs = ('H', tuple(sorted(p[i] for i in rhs[1])))
            equiv &= lhs == rhs

    pairs = []
    for face in ranks[2]:
        cells = [c for c in ranks[3] if is_incident((2, face), (3, c), incidence)]
        assert len(cells) == 2 and {c[0] for c in cells} == {'H', 'T'}
        H = next(c for c in cells if c[0] == 'H')
        T = next(c for c in cells if c[0] == 'T')
        pairs.append((H, T, face))
    ht_pairs = {(h, t) for h, t, _ in pairs}

    odd_minority = {''.join(map(str, phase_bits(v))): minority_coordinate(v) for v in odd}
    checks = {
        'eight_full_projective_sign_classes': len(full) == 8,
        'even_code_four': len(C) == 4,
        'odd_coset_four': len(O) == 4,
        'even_code_linear_dimension_two': set(C) == {(0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 0)},
        'even_code_min_distance_two': min(hamming(a, b) for a, b in combinations(C, 2)) == 2,
        'odd_coset_min_distance_two': min(hamming(a, b) for a, b in combinations(O, 2)) == 2,
        'parity_map_bijects_onto_eight_cells': set(mapped) == set(ranks[3]) and len(set(mapped)) == 8,
        'odd_words_unique_minority_coordinate': len(set(odd_minority.values())) == 4,
        'S4_equivariant_cell_map': equiv,
        'sixteen_rank2_faces': len(pairs) == 16,
        'top_incidence_is_complete_K44': len(ht_pairs) == 16 and len({h for h, _, _ in pairs}) == 4 and len({t for _, t, _ in pairs}) == 4,
        'one_face_per_H_T_pair': all(sum(1 for h, t, _ in pairs if h == H and t == T) == 1 for H, T in ht_pairs),
    }
    assert all(checks.values()), [k for k, v in checks.items() if not v]

    top_payload = sorted((repr(h), repr(t), repr(f)) for h, t, f in pairs)
    out = {
        'schema': 'w33.bt2815.tomotope_parity_code.v1',
        'status': 'COMPLETE_EXACT',
        'theorem': 'The eight full-support projective sign classes split by the [3,2,2] parity code. Even words label the four tetrahedral cells. Odd words have a unique minority coordinate; deleting it labels the four hemioctahedral cells. The 16 triangular faces are the 16 edges of K4,4 between these two cell classes.',
        'even_codewords': [''.join(map(str, b)) for b in sorted(C)],
        'odd_coset': [''.join(map(str, b)) for b in sorted(O)],
        'odd_minority_coordinate': odd_minority,
        'syndrome_cell_type': {''.join(map(str, phase_bits(v))): cell_from_full_sign(v)[0] for v in full},
        'code_parameters': '[3,2,2] binary single-parity-check code',
        'top_incidence': 'K4,4 with rank-2 faces as its 16 edges',
        'top_incidence_sha256': hashlib.sha256(json.dumps(top_payload, separators=(',', ':')).encode()).hexdigest(),
        'checks': checks,
        'check_count': len(checks),
        'hardware_reading': 'One XOR computes the cell-type syndrome. Even phase parity selects a tetrahedral packet. Odd parity selects a hemioctahedral packet, with a four-way minority-coordinate decoder.',
        'boundary': 'The parity code exactly controls the finite tomotope cell incidence. Physical chirality, spin or topology-change interpretations require additional structure.',
    }
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
