"""Compute the SM-resolved chiral R-index of 27 hypermultiplets on an interval."""

import json
from collections import Counter, defaultdict
from itertools import permutations, product

import sympy as sp
from sympy.polys.matrices import DomainMatrix

from toe_20261116_E6_full_cubic_SM_stabilizer import (
    cubic_derivation_rows, cubic_monomials, hypercharge_integer_weights, vev_constraints,
)


def sm_components(weights, cubic):
    size = len(weights)
    rows = cubic_derivation_rows(cubic) + vev_constraints()
    rows += [{size*i+j: 1} for i, j in product(range(size), repeat=2)
             if weights[i] != weights[j]]
    matrix = DomainMatrix(
        {i: {j: sp.QQ(v) for j, v in row.items()} for i, row in enumerate(rows)},
        (len(rows), size**2), sp.QQ,
    )
    sm = matrix.nullspace().to_Matrix()
    assert sm.rows == 12
    neighbors = [{i} for i in range(size)]
    for i, j in product(range(size), repeat=2):
        if any(sm[:, size*i+j]):
            neighbors[i].add(j)
            neighbors[j].add(i)
    components = []
    pending = set(range(size))
    while pending:
        block = {min(pending)}
        while (expanded := set.union(*(neighbors[i] for i in block))) != block:
            block = expanded
        assert len({weights[i] for i in block}) == 1
        components.append(sorted(block))
        pending -= block
    return components


def left_reflections(weights, cubic):
    components = sm_components(weights, cubic)
    orbit = {i: n for n, block in enumerate(components) for i in block}
    signs = []
    for parity in product((-1, 1), repeat=len(components)):
        if all(sp.prod(parity[orbit[i]] for i in term) == 1 for term in cubic):
            signs.append(tuple(parity[orbit[i]] for i in range(len(weights))))
    return components, sorted(signs)


def adjoint_index(weights, cubic, left, right, basis):
    size = len(weights)
    blocks = defaultdict(list)
    for i, j in product(range(size), repeat=2):
        signs = (left[i]*left[j], right[i]*right[j])
        if signs[0] == signs[1]:
            blocks[(weights[i]-weights[j], signs[0])].append(size*i+j)
    result = Counter()
    rows = cubic_derivation_rows(cubic)
    for (grade, sign), columns in blocks.items():
        positions = {column: i for i, column in enumerate(columns)}
        restricted = []
        for row in rows:
            subset = {positions[k]: sp.QQ(v) for k, v in row.items() if k in positions}
            if subset:
                restricted.append(subset)
        matrix = DomainMatrix(dict(enumerate(restricted)),
                              (len(restricted), len(columns)), sp.QQ)
        if (dim := len(columns)-matrix.rank()):
            result[grade] -= sign*dim
    assert set(result) <= set(basis)
    return result


def obstruction(matrix, target):
    for v in matrix.T.nullspace():
        if v.dot(target):
            v *= sp.ilcm(*(x.q for x in v))
            return list(map(int, v))
    return None


def representation_traces(weights, cubic, parity, basis, include_650=False):
    exterior, symmetric = Counter(), Counter()
    for i in range(len(weights)):
        symmetric[2*weights[i]] += 1
        for j in range(i+1, len(weights)):
            weight, sign = weights[i]+weights[j], parity[i]*parity[j]
            exterior[weight] += sign
            symmetric[weight] += sign
        # The cubic identifies the dual 27 summand of the symmetric square.
        symmetric[-weights[i]] -= parity[i]
    adjoint = adjoint_index(weights, cubic, parity, parity, basis)
    traces = {
        "adjoint_78": {w: -adjoint[w] for w in basis},
        "exterior_square_351": exterior,
        "symmetric_square_minus_dual_351prime": symmetric,
    }
    if include_650:
        product_trace = Counter()
        for i, j in product(range(len(weights)), repeat=2):
            product_trace[weights[i]-weights[j]] += parity[i]*parity[j]
        product_trace[0] -= 1
        product_trace.subtract(traces["adjoint_78"])
        traces["tensor_product_minus_1_and_78_650"] = product_trace
    return traces


def neutral_nonabelian_traces(weights, cubic, parity, include_650=False):
    """Extract the color octet and weak triplet via the Weyl denominator."""
    h1, h2, weak = (1, -1, 0), (0, 1, -1), (1, -1, 0)
    cartan = []
    for i, j in product(range(3), repeat=2):
        cartan.append((0, 0, weak[i]))
    for i, j in product(range(3), repeat=2):
        cartan.append((-h1[j], -h2[j], 0))
    for i, j in product(range(3), repeat=2):
        cartan.append((h1[i], h2[i], -weak[j]))
    assert all(sum(cartan[i][a] for i in term) == 0
               for term in cubic for a in range(3))
    exterior, symmetric = Counter(), Counter()
    for i, weight in enumerate(weights):
        if not weight:
            symmetric[tuple(2*v for v in cartan[i])] += 1
            symmetric[tuple(-v for v in cartan[i])] -= parity[i]
        for j in range(i+1, len(weights)):
            if weight+weights[j] == 0:
                key = tuple(a+b for a, b in zip(cartan[i], cartan[j], strict=True))
                exterior[key] += parity[i]*parity[j]
                symmetric[key] += parity[i]*parity[j]

    def extract(character, highest):
        total = 0
        for perm in permutations((1, 0, -1)):
            sign = (-1)**sum(perm[i] < perm[j] for i in range(3) for j in range(i+1, 3))
            a, b = perm[0]-perm[1], perm[1]-perm[2]
            for shift, weak_sign in ((0, 1), (2, -1)):
                key = (highest[0]+1-a, highest[1]+1-b, highest[2]+shift)
                total += sign*weak_sign*character[key]
        return total

    def pair(character):
        return [extract(character, highest) for highest in ((1, 1, 0), (0, 0, 2))]

    traces = {
        "adjoint_78": [1, 1],
        "exterior_square_351": pair(exterior),
        "symmetric_square_minus_dual_351prime": pair(symmetric),
    }
    if include_650:
        product_trace = Counter()
        for i, j in product(range(len(weights)), repeat=2):
            if weights[i] == weights[j]:
                key = tuple(a-b for a, b in zip(cartan[i], cartan[j], strict=True))
                product_trace[key] += parity[i]*parity[j]
        traces["tensor_product_minus_1_and_78_650"] = [v-1 for v in pair(product_trace)]
    return traces


def certificate(right_reflection=None, include_650=False):
    weights = hypercharge_integer_weights()
    cubic = cubic_monomials()
    components, gauge_signs = left_reflections(weights, cubic)
    default_right = tuple((-1 if w % 2 else 1) for w in weights)
    right = default_right if right_reflection is None else tuple(right_reflection)
    assert right in gauge_signs
    trace_counts = Counter(map(sum, gauge_signs))
    assert trace_counts == {27: 1, 3: 4, -5: 3}
    traces = sorted({eta*sum(signs) for signs in gauge_signs for eta in (-1, 1)})
    assert traces == [-27, -5, -3, 3, 5, 27]
    basis = list(range(-12, 13))
    if right_reflection is None:
        assert sum(adjoint_index(weights, cubic, (1,)*len(weights), right, basis).values()) == -38
    kinds_by_left = defaultdict(set)
    for conjugate, right_eta, left_eta, left in product(
        (False, True), (-1, 1), (-1, 1), gauge_signs,
    ):
        index = Counter()
        for w, r, l in zip(weights, right, left, strict=True):
            index[-w if conjugate else w] += (right_eta*r+left_eta*l)//2
        kinds_by_left[left].add(tuple(index[w] for w in basis))
    target = sp.Matrix([2 if abs(w) == 3 else 0 for w in basis])
    right_traces = representation_traces(weights, cubic, right, basis, include_650)
    identity_traces = representation_traces(weights, cubic, (1,)*len(weights), basis, include_650)
    expected_dimensions = [78, 351, 351] + ([650] if include_650 else [])
    assert [sum(trace.values()) for trace in identity_traces.values()] == expected_dimensions
    right_neutral = neutral_nonabelian_traces(weights, cubic, right, include_650)
    identity_neutral = neutral_nonabelian_traces(weights, cubic, (1,)*len(weights), include_650)
    cases = []
    all_label = "all_four" if include_650 else "all_three"
    combined_label = f"{all_label}_together"
    for left, kinds in kinds_by_left.items():
        neutral_singlet = sp.Matrix([int(w == 0) for w in basis])
        matrix = sp.Matrix.hstack(*(sp.Matrix(v) for v in sorted(kinds)), neutral_singlet)
        odd = tuple(n for n, c in enumerate(components) if left[c[0]] == -1)
        gauge = adjoint_index(weights, cubic, left, right, basis)
        # The target includes the SM gauginos (R = +1) at grade zero.
        gauge_residual = target - sp.Matrix([gauge[w]+12*(w == 0) for w in basis])
        matter_witness = obstruction(matrix, target)
        gauge_witness = obstruction(matrix, gauge_residual)
        if right_reflection is None:
            assert matter_witness is not None and gauge_witness is not None

        # Overestimate allowed brane content by admitting every parity block
        # of the endpoint 27 and its conjugate separately, with either sign.
        boundary_columns = []
        for reflection, parity, conjugate in product((left, right), (-1, 1), (-1, 1)):
            contents = Counter(conjugate*w for w, s in zip(weights, reflection, strict=True)
                               if s == parity)
            boundary_columns.append(sp.Matrix([contents[w] for w in basis]))
        extended = matrix.row_join(sp.Matrix.hstack(*boundary_columns))
        boundary_witness = obstruction(extended, gauge_residual)
        boundary_deficit = (int(sp.Matrix(boundary_witness).dot(gauge_residual))
                            if boundary_witness is not None else 0)
        left_traces = representation_traces(weights, cubic, left, basis, include_650)
        left_neutral = neutral_nonabelian_traces(weights, cubic, left, include_650)
        larger_columns = {}
        refined_columns = {}
        for name, left_trace in left_traces.items():
            right_trace = right_traces[name]
            columns = []
            refined = []
            for conjugate, l, r in product((-1, 1), repeat=3):
                doubled = [l*left_trace.get(conjugate*w, 0) +
                           r*right_trace.get(conjugate*w, 0) for w in basis]
                assert all(value % 2 == 0 for value in doubled)
                column = sp.Matrix([value//2 for value in doubled])
                columns.append(column)
                neutral = [l*a+r*b for a, b in
                           zip(left_neutral[name], right_neutral[name], strict=True)]
                assert all(value % 2 == 0 for value in neutral)
                refined.append(column.col_join(sp.Matrix([v//2 for v in neutral])))
            larger_columns[name] = columns
            refined_columns[name] = refined
        larger_results = {
            name: obstruction(extended.row_join(sp.Matrix.hstack(*columns)),
                              gauge_residual) is not None
            for name, columns in larger_columns.items()
        }
        larger_results[combined_label] = obstruction(
            extended.row_join(sp.Matrix.hstack(*(column for cols in larger_columns.values()
                                                 for column in cols))), gauge_residual
        ) is not None
        # The desired gauge octet and weak triplet are already included in
        # the gauge contribution; the 27 blocks contribute neither.
        refined_base = extended.col_join(sp.zeros(2, extended.cols))
        refined_target = gauge_residual.col_join(sp.zeros(2, 1))
        for name, columns in {
            "adjoint_78": refined_columns["adjoint_78"],
            combined_label: [col for cols in refined_columns.values() for col in cols],
        }.items():
            larger_results[name+"_resolving_SM_octet_and_triplet"] = (
                obstruction(refined_base.row_join(sp.Matrix.hstack(*columns)),
                            refined_target) is not None
            )
        all_refined = refined_base.row_join(sp.Matrix.hstack(
            *(col for cols in refined_columns.values() for col in cols)
        ))
        strong_witness = obstruction(all_refined, refined_target)
        if not include_650 and right_reflection is None:
            assert strong_witness is not None
        strong_deficit = 0
        if strong_witness is not None:
            assert all_refined.T*sp.Matrix(strong_witness) == sp.zeros(all_refined.cols, 1)
            strong_deficit = int(sp.Matrix(strong_witness).dot(refined_target))
            assert strong_deficit
        cases.append({
            "left_odd_SM_blocks": odd,
            "hypermultiplet_span_rank_with_neutral_column": matrix.rank(),
            "adjoint_index": dict(sorted(gauge.items())),
            "matter_only_obstruction": {w: v for w, v in zip(
                basis, matter_witness or [0]*len(basis), strict=True) if v},
            "obstruction_with_gauge_and_boundary_27_blocks": {
                w: value for w, value in zip(
                    basis, boundary_witness or [0]*len(basis), strict=True) if value
            },
            "target_deficit_in_that_functional": boundary_deficit,
            "index_obstruction_with_additional_bulk_representations": larger_results,
            "left_neutral_octet_and_triplet_traces": left_neutral,
            f"obstruction_with_{all_label}_larger_bulk_representations": {
                label: value for label, value in zip(
                    [f"w={w}" for w in basis]+["color_octet", "weak_triplet"],
                    strong_witness or [0]*(len(basis)+2), strict=True,
                ) if value
            },
            f"target_deficit_with_{all_label}_larger_bulk_representations": strong_deficit,
        })
    return {
        "SM_blocks": [{"w": weights[c[0]], "indices": c} for c in components],
        "left_gauge_reflection_trace_counts": dict(sorted(trace_counts.items())),
        "traces_with_intrinsic_phase": traces,
        "right_neutral_octet_and_triplet_traces": right_neutral,
        "neutral_octet_and_triplet_multiplicities": identity_neutral,
        "independent_reflection_cases": cases,
    }


if __name__ == "__main__":
    print(json.dumps(certificate(), indent=2))
