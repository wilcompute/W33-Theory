#!/usr/bin/env python3
"""Pass 1345: exact modular basic algebras and associated-graded relations."""
from __future__ import annotations
from pathlib import Path
import json
import numpy as np
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"data"
BASIC_OUT=DATA/"w33_pass1345_modular_basic_algebras.json"
import w33_pass1330_1334_modular_triality_cycle_atlas as old
import w33_pass1345_1349_support as support

class RowBasis:
    """Incremental exact row basis over F_p; p=2 uses integer bitsets."""
    def __init__(self, p: int, n: int):
        self.p, self.n, self.rows = p, n, {}

    def add(self, vector) -> bool:
        if self.p == 2:
            if isinstance(vector, int):
                bits = vector
            else:
                bits = 0
                for i, x in enumerate(vector):
                    if int(x) & 1:
                        bits |= 1 << i
            while bits:
                pivot = (bits & -bits).bit_length() - 1
                if pivot in self.rows:
                    bits ^= self.rows[pivot]
                else:
                    self.rows[pivot] = bits
                    return True
            return False
        a = np.array(vector, dtype=np.int64) % self.p
        for pivot in sorted(self.rows):
            if a[pivot]:
                a = (a - int(a[pivot]) * self.rows[pivot]) % self.p
        nz = np.flatnonzero(a)
        if len(nz) == 0:
            return False
        pivot = int(nz[0])
        a = (a * pow(int(a[pivot]), -1, self.p)) % self.p
        for old_pivot, row in list(self.rows.items()):
            if row[pivot]:
                self.rows[old_pivot] = (row - int(row[pivot]) * a) % self.p
        self.rows[pivot] = a
        return True

    @property
    def rank(self) -> int:
        return len(self.rows)


def rref_rows(rows, p):
    if not rows:
        return [], []
    matrix = [[int(x) % p for x in row] for row in rows]
    m, n, r, pivots = len(matrix), len(matrix[0]), 0, []
    for col in range(n):
        pivot = next((i for i in range(r, m) if matrix[i][col]), None)
        if pivot is None:
            continue
        matrix[r], matrix[pivot] = matrix[pivot], matrix[r]
        inv = pow(matrix[r][col], -1, p)
        matrix[r] = [(inv * x) % p for x in matrix[r]]
        for i in range(m):
            if i != r and matrix[i][col]:
                z = matrix[i][col]
                matrix[i] = [(matrix[i][j] - z * matrix[r][j]) % p for j in range(n)]
        pivots.append(col)
        r += 1
        if r == m:
            break
    return matrix[:r], pivots


def nullspace_iter(rows, p, ncols):
    reduced, pivots = rref_rows(rows, p)
    pivot_set = set(pivots)
    for free in range(ncols):
        if free in pivot_set:
            continue
        vector = [0] * ncols
        vector[free] = 1
        for i, pivot in enumerate(pivots):
            vector[pivot] = (-reduced[i][free]) % p
        yield vector


def quotient_complement(super_basis, sub_basis, p):
    basis = RowBasis(p, 26)
    for vector in sub_basis:
        basis.add(vector)
    answer = []
    for vector in super_basis:
        if basis.add(vector):
            answer.append([int(x) % p for x in vector])
    return answer


def corner_basis(vectors, left, right, p):
    return old.span([support.mul(support.mul(left, x, p), right, p) for x in vectors], p)


def solve_coords_mod(vector, basis, p):
    if not basis:
        assert not any(int(x) % p for x in vector)
        return []
    return support.solve_field([list(x) for x in zip(*basis)], [int(x) % p for x in vector], p)


def relation_presentation(p):
    quotient = support.quotient_record(p)
    radical = old.span(quotient["radical_basis"], p)
    powers = [radical]
    while powers[-1]:
        powers.append(old.product_ideal(powers[-1], radical, p))

    lifts = support.orthogonal_primitive_lifts(p)
    representatives, seen = [], set()
    for label, idempotent, component, steps in lifts:
        if component not in seen:
            seen.add(component)
            representatives.append((label, idempotent, component, steps))

    arrows = []
    for target, (_, e_t, _, _) in enumerate(representatives):
        for source, (_, e_s, _, _) in enumerate(representatives):
            top = corner_basis(powers[0], e_t, e_s, p)
            lower = corner_basis(powers[1], e_t, e_s, p)
            for vector in quotient_complement(top, lower, p):
                arrows.append({
                    "name": f"a{len(arrows)}",
                    "source": source,
                    "target": target,
                    "vector": vector,
                })

    paths = {0: [()], 1: [(i,) for i in range(len(arrows))]}
    for degree in range(2, len(powers) + 1):
        current = []
        for path in paths[degree - 1]:
            terminal = arrows[path[-1]]["target"]
            for i, arrow in enumerate(arrows):
                if arrow["source"] == terminal:
                    current.append(path + (i,))
        paths[degree] = current

    def path_product(path):
        value = arrows[path[0]]["vector"]
        for arrow_index in path[1:]:
            value = support.mul(arrows[arrow_index]["vector"], value, p)
        return value

    quotient_bases = {}
    for degree in range(1, len(powers)):
        layer = []
        for _, e_t, _, _ in representatives:
            for _, e_s, _, _ in representatives:
                top = corner_basis(powers[degree - 1], e_t, e_s, p)
                lower = corner_basis(powers[degree], e_t, e_s, p)
                layer += quotient_complement(top, lower, p)
        quotient_bases[degree] = layer

    path_maps, kernel_dimensions = {}, {}
    for degree, path_list in paths.items():
        if degree == 0:
            continue
        quotient_basis = quotient_bases.get(degree, [])
        lower = powers[degree] if degree < len(powers) else []
        full_basis = lower + quotient_basis
        columns = []
        for path in path_list:
            coordinates = solve_coords_mod(path_product(path), full_basis, p) if full_basis else []
            columns.append(coordinates[len(lower):])
        rows = [list(row) for row in zip(*columns)] if quotient_basis else []
        _, pivots = rref_rows(rows, p)
        path_maps[degree] = rows
        kernel_dimensions[degree] = len(path_list) - len(pivots)

    minimal_relations = {}
    degree_summary = {}
    for degree in sorted(kernel_dimensions):
        path_index = {path: i for i, path in enumerate(paths[degree])}
        consequences = RowBasis(p, len(paths[degree]))
        for old_degree, relations in minimal_relations.items():
            if old_degree >= degree:
                continue
            for relation in relations:
                support_terms = [(paths[old_degree][i], c % p) for i, c in enumerate(relation) if c % p]
                for left_length in range(degree - old_degree + 1):
                    right_length = degree - old_degree - left_length
                    for left_path in paths[left_length]:
                        for right_path in paths[right_length]:
                            vector = [0] * len(paths[degree])
                            nonzero = False
                            for middle_path, coefficient in support_terms:
                                full_path = left_path + middle_path + right_path
                                index = path_index.get(full_path)
                                if index is not None:
                                    vector[index] = (vector[index] + coefficient) % p
                                    nonzero = True
                            if nonzero:
                                consequences.add(vector)
        consequence_dimension = consequences.rank
        need = kernel_dimensions[degree] - consequence_dimension
        assert need >= 0
        new_relations = []
        if need:
            for vector in nullspace_iter(path_maps[degree], p, len(paths[degree])):
                if consequences.add(vector):
                    new_relations.append(vector)
                if len(new_relations) == need:
                    break
        assert consequences.rank == kernel_dimensions[degree]
        minimal_relations[degree] = new_relations
        degree_summary[str(degree)] = {
            "path_dimension": len(paths[degree]),
            "radical_layer_dimension": len(quotient_bases.get(degree, [])),
            "relation_kernel_dimension": kernel_dimensions[degree],
            "consequences_of_lower_relations_dimension": consequence_dimension,
            "minimal_relation_count": len(new_relations),
        }

    def sparse_relation(relation, degree):
        return [
            {
                "coefficient": int(coefficient) % p,
                "path": [arrows[i]["name"] for i in paths[degree][index]],
            }
            for index, coefficient in enumerate(relation)
            if coefficient % p
        ]

    return {
        "vertices": [x[0] for x in representatives],
        "arrows": [
            {
                "name": arrow["name"],
                "source": representatives[arrow["source"]][0],
                "target": representatives[arrow["target"]][0],
            }
            for arrow in arrows
        ],
        "ext1_adjacency": [
            [sum(1 for arrow in arrows if arrow["target"] == i and arrow["source"] == j) for j in range(len(representatives))]
            for i in range(len(representatives))
        ],
        "degree_summary": degree_summary,
        "minimal_relations": {
            str(degree): [sparse_relation(relation, degree) for relation in relations]
            for degree, relations in minimal_relations.items()
            if relations
        },
        "loewy_power_dimensions_full_algebra": [len(power) for power in powers],
    }


def components_from_cartan(cartan):
    n, seen, components = len(cartan), set(), []
    for seed in range(n):
        if seed in seen:
            continue
        queue, component = [seed], []
        seen.add(seed)
        while queue:
            i = queue.pop()
            component.append(i)
            for j in range(n):
                if i != j and (cartan[i][j] or cartan[j][i]) and j not in seen:
                    seen.add(j)
                    queue.append(j)
        components.append(sorted(component))
    return components


def modular_basic_algebras():
    records = {}
    for p in (2, 3, 5):
        spec = support.DECOMP[p]
        D, simple_dims = spec["D"], spec["dims"]
        assert all(sum(a * b for a, b in zip(row, simple_dims)) == dimension for row, dimension in zip(D, support.ORDINARY_MULTIPLICITY_DIMS))
        ordinary, modular = support.ordinary_and_modular_traces(p)
        for ordinary_dimension, trace_row, decomposition_row in zip(support.ORDINARY_MULTIPLICITY_DIMS, ordinary, D):
            expected = [sum(decomposition_row[j] * modular[j][i] for j in range(len(modular))) % p for i in range(26)]
            assert [x % p for x in trace_row] == expected
            candidates = []
            def search(position, remaining, current):
                if position == len(simple_dims):
                    if remaining == 0:
                        candidate_trace = [sum(current[j] * modular[j][i] for j in range(len(modular))) % p for i in range(26)]
                        if candidate_trace == [x % p for x in trace_row]:
                            candidates.append(current.copy())
                    return
                for coefficient in range(remaining // simple_dims[position] + 1):
                    current.append(coefficient)
                    search(position + 1, remaining - coefficient * simple_dims[position], current)
                    current.pop()
            search(0, ordinary_dimension, [])
            assert candidates == [decomposition_row]

        lifts = support.orthogonal_primitive_lifts(p)
        representatives, seen = [], set()
        for label, e, component, steps in lifts:
            if component not in seen:
                seen.add(component)
                representatives.append((label, e, component))
        cartan = [[support.corner_dim(e, f, p) for _, f, _ in representatives] for _, e, _ in representatives]
        dt_d = (np.array(D, dtype=int).T @ np.array(D, dtype=int)).tolist()
        assert cartan == dt_d
        projective_dims = [support.left_ideal_dim(e, p) for _, e, _ in representatives]
        assert sum(d * s for d, s in zip(projective_dims, simple_dims)) == 26
        components = components_from_cartan(cartan)
        presentation = relation_presentation(p)
        relation_hash = support.sha_json(presentation["minimal_relations"])
        records[str(p)] = {
            "ordinary_simples": support.ORDINARY,
            "modular_simples": spec["simples"],
            "modular_simple_dimensions": simple_dims,
            "decomposition_matrix": D,
            "decomposition_rows_unique_from_trace_congruences": True,
            "cartan_matrix": cartan,
            "cartan_equals_D_transpose_D": True,
            "projective_indecomposable_dimensions": projective_dims,
            "block_components": components,
            "basic_algebra_dimension": sum(sum(row) for row in cartan),
            "quiver_and_associated_graded_relations": presentation,
            "minimal_relation_sha256": relation_hash,
        }
    result = {
        "schema": "w33.pass1345.modular_basic_algebras.v1",
        "status": "PASS",
        "records": records,
        "boundary": "These are basic algebras of the literal 26-dimensional Hecke reductions, not Brauer trees of the ambient group algebra.",
    }
    BASIC_OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result
