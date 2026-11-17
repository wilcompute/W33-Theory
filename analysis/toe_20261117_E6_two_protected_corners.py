"""Compute the R-index on a flat E6 T^2/Z2 with two protected corners."""

import json
from collections import Counter
from itertools import combinations, product

import sympy as sp
from sympy.matrices.normalforms import smith_normal_decomp
from sympy.polys.matrices import DomainMatrix

from toe_20261116_E6_full_cubic_SM_stabilizer import (
    cubic_derivation_rows, cubic_monomials, hypercharge_integer_weights,
)
from toe_20261117_E6_interval_R_index import (
    left_reflections, obstruction, sm_cartan, weyl_multiplicity,
)


def multiply(left, right):
    return tuple(a*b for a, b in zip(left, right, strict=True))


def conjugate(label):
    w, a, b, c = label
    return (-w, b, a, c)


def irrep_dimension(label):
    _, a, b, c = label
    return (a+1)*(b+1)*(a+b+2)*(c+1)//2


def adjoint_character(weights, cubic, parity):
    size = len(weights)
    entries = {}
    for i, j in product(range(size), repeat=2):
        weight = tuple(a-b for a, b in zip(weights[i], weights[j], strict=True))
        entries.setdefault((weight, parity[i]*parity[j]), []).append(size*i+j)
    rows = cubic_derivation_rows(cubic)
    trace = Counter()
    for (weight, sign), columns in entries.items():
        index = {c: i for i, c in enumerate(columns)}
        restricted = []
        for row in rows:
            if term := {index[k]: sp.QQ(v) for k, v in row.items() if k in index}:
                restricted.append(term)
        matrix = DomainMatrix(dict(enumerate(restricted)),
                              (len(restricted), len(columns)), sp.QQ)
        trace[weight] += sign*(len(columns)-matrix.rank())
    return trace


def representation_characters(weights, cubic, parity):
    fundamental, exterior, symmetric, mixed = (Counter() for _ in range(4))
    for i, j in product(range(len(weights)), repeat=2):
        mixed[tuple(a-b for a, b in zip(weights[i], weights[j], strict=True))] += parity[i]*parity[j]
    for i, j in combinations(range(len(weights)), 2):
        label = tuple(a+b for a, b in zip(weights[i], weights[j], strict=True))
        exterior[label] += parity[i]*parity[j]
        symmetric[label] += parity[i]*parity[j]
    for i, label in enumerate(weights):
        fundamental[label] += parity[i]
        symmetric[tuple(2*a for a in label)] += 1
        symmetric[tuple(-a for a in label)] -= parity[i]
    adjoint = adjoint_character(weights, cubic, parity)
    mixed[(0, 0, 0, 0)] -= 1
    mixed.subtract(adjoint)
    return {"27": fundamental, "78": adjoint, "351": exterior, "351prime": symmetric, "650": mixed}


def highest_weight_traces(character):
    sectors = {}
    for (w, *weight), multiplicity in character.items():
        sectors.setdefault(w, Counter())[tuple(weight)] = multiplicity
    return {(w, *weight): trace for w, sector in sectors.items() for weight in sector
            if all(x >= 0 for x in weight) and (trace := weyl_multiplicity(sector, weight))}


def trace_tables(weights, cubic, reflections):
    full_weights = [(w, *cartan) for w, cartan in zip(weights, sm_cartan(cubic), strict=True)]
    out = {}
    for parity in reflections:
        chars = representation_characters(full_weights, cubic, parity)
        out[parity] = {name: highest_weight_traces(char) for name, char in chars.items()}
        for name, table in out[parity].items():
            assert sum(irrep_dimension(label)*v for label, v in table.items()) == sum(chars[name].values())
    return out


def index_column(traces, corners, name, signs, labels, reverse=False):
    four_times = [
        sum(sign*traces[parity][name].get(label, 0)
            for parity, sign in zip(corners, signs, strict=True))
        for label in (map(conjugate, labels) if reverse else labels)
    ]
    assert all(n % 4 == 0 for n in four_times)
    return sp.Matrix([n//4 for n in four_times])


def integer_solution(matrix, residual):
    diagonal, left, right = smith_normal_decomp(matrix, domain=sp.ZZ)
    assert left*matrix*right == diagonal
    transformed = left*residual
    values = sp.zeros(matrix.cols, 1)
    for row, value in enumerate(transformed):
        divisor = diagonal[row, row] if row < diagonal.cols else 0
        if not divisor:
            assert not value
            continue
        quotient, remainder = divmod(value, divisor)
        if remainder:
            return None, {"remainder": int(remainder), "divisor": int(divisor)}
        values[row] = quotient
    solution = right*values
    assert matrix*solution == residual
    return solution, None


def bulk_anomaly_check(identity):
    # E6 has no independent quartic Casimir, so this nonzero Cartan
    # direction fixes C_R in tr_R F^4 = C_R (tr_27 F^2)^2.
    traces = {
        name: [sum(irrep_dimension(k)*n*k[0]**power for k, n in identity[name].items())
               for power in (2, 4)]
        for name in ("27", "78")
    }
    q27, fourth27 = traces["27"]
    q78, fourth78 = traces["78"]
    assert (q27, fourth27, q78, fourth78) == (180, 2700, 720, 16200)
    lambda_e6 = 6
    a_dot_b = sp.Rational(lambda_e6, 6)*(sp.Rational(q78, q27)-4)
    b_squared = -sp.Rational(lambda_e6**2, 3)*sp.Rational(fourth78-4*fourth27, q27**2)
    lattice = sp.Matrix([[0, 1], [1, 0]])
    a, b = sp.Matrix([-2, -2]), sp.Matrix([1, -1])
    assert (a.T*lattice*b)[0] == a_dot_b == 0
    assert (b.T*lattice*b)[0] == b_squared == -2
    assert (a.T*lattice*a)[0] == 8
    neutral_hypers = 273+78-29-4*27
    assert neutral_hypers == 214
    # On F2 the basis (section+fiber, fiber) has intersection form U.
    # The section is b and the canonical divisor is a.
    f3_degree = ((-4*a-3*b).T*lattice*b)[0]
    g4_degree = ((-6*a-4*b).T*lattice*b)[0]
    assert (f3_degree, g4_degree) == (6, 8)
    s, t = sp.symbols("s t")
    f, g = s**3, s**4*(t**2+s)
    enhancement = [min(sum(m) for m in sp.Poly(term, s, t).monoms())
                   for term in (f, g, 4*f**3+27*g**2)]
    assert enhancement == [3, 5, 9]
    return {"fundamental_and_adjoint_traces_Y2_Y4": traces,
            "tensor_multiplets": 1, "neutral_bulk_hypermultiplets_for_273": neutral_hypers,
            "a_in_even_unimodular_U": list(map(int, a)),
            "b_in_even_unimodular_U": list(map(int, b)),
            "a_dot_b": int(a_dot_b), "b_squared": int(b_squared),
            "F2_E6_section_leading_degrees_f3_g4": [int(f3_degree), int(g4_degree)],
            "F2_split_square_root_degree": int(g4_degree//2),
            "simple_enhancement_orders_f_g_discriminant": enhancement}


def fundamental_zero_modes(weights, corners):
    out = []
    for eta_y in (-1, 1):
        # The sourced doublet has P=-1, and the protected corners agree on
        # its gauge sign, so its intrinsic inversion and x signs are fixed.
        signs = (-1, -1, -eta_y, -eta_y)
        modes = [
            [i for i in range(len(weights))
             if all(eta*p[i] == charge for p, eta in zip(corners, signs, strict=True))]
            for charge in (1, -1)
        ]
        if 0 in modes[0]:
            assert 3 in modes[0]
            out.append({
                "translation_y_intrinsic_sign": eta_y,
                "R0_indices": modes[0],
                "R2_dual_indices": modes[1],
            })
    return out


def torus_generator_basis(cubic, corners, parity):
    size = len(corners[0])
    positions = [(i, j) for i, j in product(range(size), repeat=2)
                 if all(p[i]*p[j] == parity for p in corners)]
    index = {size*i+j: n for n, (i, j) in enumerate(positions)}
    rows = []
    for row in cubic_derivation_rows(cubic):
        if restricted := {index[k]: sp.QQ(v) for k, v in row.items() if k in index}:
            rows.append(restricted)
    matrix = DomainMatrix(dict(enumerate(rows)), (len(rows), len(positions)), sp.QQ)
    return matrix.nullspace().to_Matrix(), positions


def rank_checks(weights, cubic, corners):
    sourced = fundamental_zero_modes(weights, corners)[0]
    assert sourced["R0_indices"] == [0, 3]
    assert sourced["R2_dual_indices"] == [7, 12, 13, 14]
    # The successful Smith solution uses auxiliary 27 and dual hypers
    # with intrinsic inversion, x, y signs (+,-,+).
    signs = (1, -1, 1, -1)
    auxiliary = {
        key: [i for i in range(len(weights))
              if all(eta*p[i] == charge for p, eta in zip(corners, signs, strict=True))]
        for key, charge in (("R0_indices", 1), ("R2_dual_indices", -1))
    }
    assert auxiliary == {"R0_indices": [8, 15, 16, 17],
                         "R2_dual_indices": [18, 19, 21, 22, 24, 25]}
    sigma, positions = torus_generator_basis(cubic, corners, -1)
    generator_columns = {pair: column for column, pair in enumerate(positions)}
    auxiliaries_r2 = auxiliary["R2_dual_indices"]
    forward = sigma[:, [generator_columns[i, 8] for i in auxiliaries_r2]]
    backward = sigma[:, [generator_columns[8, i] for i in auxiliaries_r2]]
    sigma_mass_rank = forward.row_join(backward).rank()
    assert sigma.rows == sigma_mass_rank == 12

    # d*(bar H2, d(H1, .)) or its transpose mixes the two antitriplet
    # blocks. Compute in both directions to fix the orientation.
    def polarization(frame):
        length = len(weights)
        return sp.Matrix(length, length, lambda i, j: cubic.get(tuple(sorted((i, j, frame))), 0))

    h1, h2 = polarization(7), polarization(8)
    triplet = (h1*h2).extract([12, 13, 14], [15, 16, 17])
    reverse = (h2*h1).extract([15, 16, 17], [12, 13, 14])
    assert triplet.rank() == reverse.rank() == 3 and triplet == reverse.T

    vector, vector_positions = torus_generator_basis(cubic, corners, 1)
    vector_columns = {pair: column for column, pair in enumerate(vector_positions)}
    neutral_rank = vector[:, [vector_columns[7, 7], vector_columns[8, 8]]].rank()
    assert vector.rows == 14 and neutral_rank == 2
    return {
        "auxiliary_27_parities_and_zero_modes": auxiliary,
        "adjoint_chiral_zero_modes": sigma.rows,
        "adjoint_chiral_bulk_mass_rank_with_H2_and_dual": sigma_mass_rank,
        "triplet_map_with_H1_and_H2_insertions": [list(map(int, row)) for row in triplet.tolist()],
        "two_extra_U1_vev_charge_rank": neutral_rank,
    }


def scan():
    weights, cubic = hypercharge_integer_weights(), cubic_monomials()
    components, reflections = left_reflections(weights, cubic)
    by_odd_blocks = {
        tuple(n for n, c in enumerate(components) if reflection[c[0]] < 0): reflection
        for reflection in reflections
    }
    start = by_odd_blocks[0, 1, 2, 9]
    next_x = by_odd_blocks[0, 2, 3, 5, 6, 8]
    holonomy_x = multiply(start, next_x)
    traces = trace_tables(weights, cubic, reflections)
    identity = traces[by_odd_blocks[()]]
    assert {name: sum(irrep_dimension(k)*n for k, n in table.items())
            for name, table in identity.items()} == {"27": 27, "78": 78, "351": 351,
                                                     "351prime": 351, "650": 650}
    all_positive = (1,)*4
    labels = sorted({*{k for table in identity.values() for k in table},
                     *{conjugate(k) for table in identity.values() for k in table}})
    target_table = {(-3, 0, 0, 1): 1, (3, 0, 0, 1): 1, (0, 1, 1, 0): -1,
                    (0, 0, 0, 2): -1, (0, 0, 0, 0): -1}
    target = sp.Matrix([target_table.get(label, 0) for label in labels])

    def adjoint_trace(parity):
        return sum(irrep_dimension(key)*n for key, n in traces[parity]["78"].items())

    cases = []
    for odd_y, holonomy_y in by_odd_blocks.items():
        corners = (start, next_x, multiply(start, holonomy_y), multiply(next_x, holonomy_y))
        gauge = -index_column(traces, corners, "78", all_positive, labels)
        # For the vector zero-mode dimension both translations must be +1
        # and inversion must be +1, so include the untwisted trace as well.
        vector_traces = (by_odd_blocks[()], holonomy_x, holonomy_y,
                         multiply(holonomy_x, holonomy_y), *corners)
        vector_dim = sum(map(adjoint_trace, vector_traces))//8
        columns = [sp.Matrix([int(label == (0, 0, 0, 0)) for label in labels])]
        descriptions = [{"type": "boundary singlet"}]
        for name, eta, eta_x, eta_y, dual in product(
            traces[start], (-1, 1), (-1, 1), (-1, 1), (False, True),
        ):
            signs = (eta, eta*eta_x, eta*eta_y, eta*eta_x*eta_y)
            columns.append(index_column(traces, corners, name, signs, labels, dual))
            descriptions.append({"type": "bulk", "representation": name, "dual": dual,
                                 "intrinsic_signs_inversion_x_y": [eta, eta_x, eta_y]})
        for corner, sign, dual in product(dict.fromkeys(corners), (-1, 1), (False, True)):
            reps = map(conjugate, labels) if dual else labels
            columns.append(sp.Matrix([(identity["27"].get(k, 0)+sign*traces[corner]["27"].get(k, 0))//2
                                      for k in reps]))
            descriptions.append({"type": "boundary", "corner": corners.index(corner),
                                 "parity_block": sign, "dual": dual})
        matrix = sp.Matrix.hstack(*columns)
        sourced = fundamental_zero_modes(weights, corners)
        assert len(sourced) == 1
        eta_y = sourced[0]["translation_y_intrinsic_sign"]
        signs = (-1, -1, -eta_y, -eta_y)
        fixed_sources = sum((index_column(traces, corners, "27", signs, labels, dual)
                             for dual in (False, True)), sp.zeros(len(labels), 1))
        residual = target-gauge-fixed_sources
        witness = obstruction(matrix, residual)
        solution, integrality = (integer_solution(matrix, residual) if witness is None
                                 else (None, None))
        cases.append({
            "translation_y_gauge_odd_SM_blocks": odd_y,
            "corner_fixed_lie_dimensions": [(78+adjoint_trace(p))//2 for p in corners],
            "vector_zero_mode_dimension_before_Higgsing": vector_dim,
            "sourced_27_parities_and_zero_modes": sourced,
            "index_span_rank": matrix.rank(),
            "obstruction": [{"SM_irrep": label, "coefficient": n}
                            for label, n in zip(labels, witness or [0]*len(labels), strict=True) if n],
            "index_deficit": int(sp.Matrix(witness).dot(residual)) if witness else 0,
            "integrality_obstruction": integrality,
            "integer_solution": [{"copies_signed": int(n), **desc} for n, desc in
                                 zip(solution, descriptions, strict=True) if n]
                                if solution is not None else None,
        })
        if odd_y == (0, 1, 3, 4, 6, 7):
            cases[-1]["four_hypermultiplet_candidate_rank_checks"] = rank_checks(weights, cubic, corners)
    assert sum(case["integer_solution"] is not None for case in cases) == 4
    return {"SM_irrep_label": ["w", "SU3_Dynkin_a", "SU3_Dynkin_b", "SU2_Dynkin_c"],
            "cases": cases, "four_bulk_fundamentals_anomaly_check": bulk_anomaly_check(identity)}


if __name__ == "__main__":
    print(json.dumps(scan(), indent=2))
