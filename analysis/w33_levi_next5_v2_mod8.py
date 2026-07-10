"""Track module extracted from w33_levi_next5_v2."""
from __future__ import annotations
from w33_levi_next5_v2_common import *

def p_valuation(value: int, prime: int, cap: int = 64) -> int:
    value = int(value)
    if value == 0:
        return cap
    count = 0
    while value % prime == 0:
        value //= prime
        count += 1
    return count


def p_adic_snf_generators(gram: Matrix, prime: int = 2):
    rank = gram.rows
    determinant = abs(int(gram.det()))
    valuation = p_valuation(determinant, prime)
    B = valuation + 1
    modulus = prime**B
    work = [[int(gram[r, c]) % modulus for c in range(rank)] for r in range(rank)]
    right = [[int(r == c) for c in range(rank)] for r in range(rank)]

    def row_op(dst, src, mult):
        for c in range(rank):
            work[dst][c] = (work[dst][c] - mult * work[src][c]) % modulus

    def col_op(dst, src, mult):
        for r in range(rank):
            work[r][dst] = (work[r][dst] - mult * work[r][src]) % modulus
            right[r][dst] = (right[r][dst] - mult * right[r][src]) % modulus

    def swap_rows(a, b):
        work[a], work[b] = work[b], work[a]

    def swap_cols(a, b):
        for r in range(rank):
            work[r][a], work[r][b] = work[r][b], work[r][a]
            right[r][a], right[r][b] = right[r][b], right[r][a]

    valuations = []
    for t in range(rank):
        best = None
        best_value = B
        for r in range(t, rank):
            for c in range(t, rank):
                current = p_valuation(work[r][c], prime, B)
                if current < best_value:
                    best_value = current
                    best = (r, c)
        if best is None or best_value >= B:
            valuations.extend([B] * (rank - t))
            break
        pr, pc = best
        swap_rows(t, pr)
        swap_cols(t, pc)
        unit = work[t][t] // prime**best_value
        unit_inverse = pow(unit, -1, modulus)
        for r in range(t + 1, rank):
            row_op(r, t, (work[r][t] // prime**best_value) * unit_inverse % modulus)
        for c in range(t + 1, rank):
            col_op(c, t, (work[t][c] // prime**best_value) * unit_inverse % modulus)
        valuations.append(best_value)

    generators = [
        (prime**valuations[i], np.array([right[r][i] for r in range(rank)], dtype=object))
        for i in range(rank)
        if 0 < valuations[i] < B
    ]
    return valuations, generators


def compose_linear_columns(columns: tuple[int, ...], vector: int) -> int:
    out = 0
    while vector:
        bit = vector & -vector
        out ^= columns[bit.bit_length() - 1]
        vector ^= bit
    return out


def fixed_subspace(generators: list[tuple[int, ...]], dimension: int) -> list[int]:
    identity = tuple(1 << i for i in range(dimension))
    equations = []
    for generator in generators:
        difference = tuple(generator[i] ^ identity[i] for i in range(dimension))
        equations.extend(bit_columns_to_rows(difference, dimension))
    return base.gf2_nullspace(equations, dimension)


def projective_transvections(geometry: base.Geometry) -> list[tuple[int, ...]]:
    field = base.FiniteField(3)
    index = {point: i for i, point in enumerate(geometry.points)}
    seeds = [
        (1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1),
        (1, 1, 0, 0), (1, 0, 1, 0), (0, 1, 0, 1), (1, 1, 1, 1),
    ]
    permutations = []
    for seed in seeds:
        perm = []
        for point in geometry.points:
            coefficient = field.symplectic_form(point, seed)
            image = field.add_vectors(point, field.scale(coefficient, seed))
            perm.append(index[field.normalize_projective(image)])
        permutations.append(tuple(perm))
    return permutations


def permute_mask(mask: int, permutation: tuple[int, ...]) -> int:
    out = 0
    while mask:
        bit = mask & -mask
        index = bit.bit_length() - 1
        out |= 1 << permutation[index]
        mask ^= bit
    return out


def trade_basis_and_action(geometry: base.Geometry):
    incidence = Matrix([
        [(geometry.incidence_columns[line] >> point) & 1 for point in range(40)]
        for line in range(40)
    ])
    D, _, T = smith_normal_decomp(incidence, domain=ZZ)
    zero_columns = [column for column in range(40) if D[column, column] == 0]
    trade_basis = T[:, zero_columns]

    masks = []
    for column in range(15):
        mask = 0
        for row in range(40):
            if int(trade_basis[row, column]) & 1:
                mask |= 1 << row
        masks.append(mask)
    tagged = base.tagged_basis(masks)

    actions = []
    for permutation in projective_transvections(geometry):
        columns = []
        for mask in masks:
            remainder, coordinate = base.coordinates(permute_mask(mask, permutation), tagged)
            if remainder:
                raise AssertionError("trade action escaped the mod-two lattice span")
            columns.append(coordinate)
        actions.append(tuple(columns))
    return incidence, trade_basis, actions


def mod8_lift_track(geometry: base.Geometry) -> dict:
    incidence, trade_basis, actions = trade_basis_and_action(geometry)
    gram = trade_basis.T * trade_basis
    fixed = fixed_subspace(actions, 15)
    valuations, generators = p_adic_snf_generators(gram, 2)
    orders = [order for order, _ in generators]
    scaled = [column * (8 // order) for order, column in generators]
    h = scaled[-1]
    gram_object = np.array(gram.tolist(), dtype=object)
    q_h_numerator = int(h @ gram_object @ h) % 128

    two_torsion_basis = scaled[:14] + [4 * h]
    fixed_coordinate = fixed[0] if len(fixed) == 1 else 0
    fixed_target = np.array([4 if (fixed_coordinate >> i) & 1 else 0 for i in range(15)], dtype=object)

    fixed_shadow_mask = None
    complement_q = []
    for mask in range(1 << 15):
        vector = np.zeros(15, dtype=object)
        for index, basis_vector in enumerate(two_torsion_basis):
            if (mask >> index) & 1:
                vector += basis_vector
        if fixed_shadow_mask is None and all(int(vector[i] - fixed_target[i]) % 8 == 0 for i in range(15)):
            fixed_shadow_mask = mask
        if int(vector @ gram_object @ h) % 64 == 0:
            complement_q.append(int(vector @ gram_object @ vector) % 128)

    q_counts = Counter(complement_q)
    c8_sum = sum(cmath.exp(1j * math.pi * q_h_numerator * k * k / 64) for k in range(8)) / math.sqrt(8)
    c8_brown = round(cmath.phase(c8_sum) / (2 * math.pi) * 8) % 8
    complement_gauss = (q_counts[0] - q_counts[64]) / math.sqrt(len(complement_q))
    complement_brown = 0 if abs(complement_gauss - 1) < 1e-9 else 4 if abs(complement_gauss + 1) < 1e-9 else None

    checks = {
        "trade_rank_15": trade_basis.shape == (40, 15),
        "trade_is_incidence_kernel": incidence * trade_basis == Matrix.zeros(40, 15),
        "gram_entrywise_even": all(int(gram[i, j]) % 2 == 0 for i in range(15) for j in range(15)),
        "two_part_is_C2_14_plus_C8": Counter(orders) == Counter({2: 14, 8: 1}),
        "fixed_space_dimension_one": len(fixed) == 1,
        "fixed_line_maps_to_4h": fixed_shadow_mask == 1 << 14,
        "q_h_is_11_over_8": q_h_numerator == 88,
        "q_4h_is_zero_mod_2": (16 * q_h_numerator) % 128 == 0,
        "orthogonal_complement_dimension_14": len(complement_q) == 1 << 14,
        "orthogonal_complement_is_O14_minus": q_counts == Counter({0: 8128, 64: 8256}),
        "brown_split_7_plus_4_equals_3": c8_brown == 7 and complement_brown == 4 and (c8_brown + complement_brown) % 8 == 3,
    }
    return {
        "status": "PROVED" if all(checks.values()) else "FAIL",
        "all_pass": all(checks.values()),
        "checks": checks,
        "two_part": "A_2(L_-4) = (Z/2)^14 + Z/8",
        "canonical_filtration": {
            "depth_generator": "h of order 8",
            "q_h": "11/8 mod 2Z",
            "fixed_line": "<4h>, isotropic",
            "U14_minus": "h^perp inside A_2[2]",
            "U14_isotropic_nonzero": 8127,
            "U14_anisotropic": 8256,
        },
        "brown_invariants": {"Z8_depth_block": c8_brown, "U14_minus": complement_brown, "full_2_part": 3},
        "theorem": (
            "The natural isomorphism L_-4/2L_-4 -> A_2(L_-4)[2], x -> x/2, sends the unique trivial "
            "PSp(4,3)-line to <4h>; its orthogonal complement is exactly U14- and the order-eight lift has q(h)=11/8."
        ),
    }
