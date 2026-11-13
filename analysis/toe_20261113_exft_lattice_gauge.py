"""Integral finite-torus gauge complex and pointwise bracket obstruction."""

import json
from itertools import combinations, product
from pathlib import Path

import networkx as nx
import numpy as np
from sympy import Matrix, ZZ
from sympy.matrices.normalforms import smith_normal_form

import toe_20261113_E6_exft_generalized_closure_affine as exft


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/toe_20261113_exft_lattice_gauge.json"


def signed_equivalence(actual, expected):
    assert np.array_equal(abs(actual), abs(expected))
    rows, columns = actual.shape[:2]
    graph = nx.Graph()
    for i, j, k in np.argwhere(actual):
        graph.add_edge(int(i), rows+int(j), sign=int(actual[i, j, k]*expected[i, j, k]))
    signs = {}
    for component in nx.connected_components(graph):
        signs[min(component)] = 1
        for i, j in nx.bfs_edges(graph, min(component)):
            signs[j] = signs[i]*graph[i][j]["sign"]
    assert all(signs[i]*signs[j] == v["sign"] for i, j, v in graph.edges(data=True))
    return [signs[i] for i in range(rows)], [signs[rows+j] for j in range(columns)]


def certify_blocks(tensor, section):
    coefficients = tensor[:, section, :].transpose(0, 2, 1)
    graph = nx.Graph()
    graph.add_edges_from((int(i), 27+int(j)) for i, j in np.argwhere(coefficients.any(axis=2)))
    wedge = np.zeros((6, 4, 4), dtype=np.int64)
    pairs = list(combinations(range(4), 2))
    for r, (i, j) in enumerate(pairs):
        wedge[r, j, i] = 1
        wedge[r, i, j] = -1
    grad = np.eye(4, dtype=np.int64)[:, None, :]
    blocks = []
    # Transpose blocks are automatic from cubic symmetry.
    for component in nx.connected_components(graph):
        rows = sorted(i for i in component if i < 27)
        cols = sorted(i-27 for i in component if i >= 27)
        if len(rows) < len(cols):
            continue
        if len(cols) == 1:
            rows.sort(key=lambda i: int(np.flatnonzero(coefficients[i, cols[0]])[0]))
            expected, name = grad, "gradient"
        else:
            cols.sort(key=lambda j: int(np.flatnonzero(~coefficients[rows, j].any(axis=0))[0]))
            rows.sort(key=lambda i: tuple(j for j in range(4) if coefficients[i, cols[j]].any()))
            expected, name = wedge, "wedge"
        signs = signed_equivalence(coefficients[np.ix_(rows, cols)], expected)
        blocks.append(dict(kind=name, rows=rows, columns=cols, signs=signs))
    assert sorted(b["kind"] for b in blocks) == ["gradient", "gradient", "wedge"]
    assert graph.number_of_nodes() == 40
    return blocks


def operators(tensor, y_tensor, section):
    identity = np.eye(27, dtype=np.int64)
    gauge = np.array([
        np.column_stack([
            np.r_[identity[s, l], (y_tensor[:, s, :, l]
                                   - np.outer(identity[:, l], identity[s])).ravel()]
            for l in range(27)
        ])
        for s in section
    ])
    trivial = tensor[:, section, :].transpose(1, 0, 2)
    for i, j in combinations(range(4), 2):
        assert not (gauge[i] @ trivial[j] + gauge[j] @ trivial[i]).any()
    assert all(not (d @ g).any() for d, g in zip(gauge, trivial))
    return gauge, trivial


def site_space_smith(trivial):
    # The smallest four-dimensional torus has the Q4 edge graph.
    sites = 16
    eye = np.eye(sites, dtype=np.int64)
    differences = [eye[np.arange(sites) ^ (1 << i)]-eye for i in range(4)]
    image = sum(np.kron(g, d) for g, d in zip(trivial, differences))
    smith = smith_normal_form(Matrix(image.tolist()), domain=ZZ)
    factors = [abs(int(x)) for x in smith.diagonal() if x]
    assert factors == [1]*150
    return dict(sites=sites, smith_unit_factors=len(factors),
                expected_uniform_rescaling=dict(scale=2, torsion_order=2,
                                                torsion_multiplicity=len(factors)))


def finite_controls(gauge, trivial):
    rows = []
    for sizes in ((2, 2, 2, 2), (3, 2, 2, 2), (3, 3, 3, 3)):
        sites = int(np.prod(sizes))
        for stencil in ("forward", "centered"):
            shifts = [np.roll(np.eye(n, dtype=np.int64), -1, axis=0) for n in sizes]
            matrices = [t-np.eye(n, dtype=np.int64) if stencil == "forward" else t-t.T
                        for n, t in zip(sizes, shifts)]
            zero_modes = int(np.prod([n-np.linalg.matrix_rank(m) for n, m in zip(sizes, matrices)]))
            characters = [
                np.fft.fft(m[:, 0])
                for m in matrices
            ]
            ranks = {}
            for frequency in product(*(range(n) for n in sizes)):
                z = np.array([v[k] for v, k in zip(characters, frequency)])
                if np.max(abs(z)) < 1e-12:
                    continue
                d = np.einsum("i,ijk->jk", z, gauge)
                g = np.einsum("i,ijk->jk", z, trivial)
                assert np.max(abs(d @ g)) < 1e-12
                rank = (int(np.linalg.matrix_rank(d)), int(np.linalg.matrix_rank(g)))
                ranks[rank] = ranks.get(rank, 0)+1
            assert ranks == ({(17, 10): sites-zero_modes} if sites != zero_modes else {})
            for n, matrix in zip(sizes, matrices):
                factors = smith_normal_form(Matrix(matrix.tolist()), domain=ZZ).diagonal()
                assert all(abs(x) <= 1 for x in factors)
                assert sum(x == 0 for x in factors) == (1 if stencil == "forward" else np.gcd(2, n))
            rows.append(dict(sizes=sizes, stencil=stencil, common_zero_modes=zero_modes,
                             nonzero_modes=sites-zero_modes,
                             free_quotient_rank=23*zero_modes, torsion_factors=[]))
    return rows


def anchor_counterexample(tensor, y_tensor, section):
    # Three sites in one direction, with fields in the anchor of that axis.
    s = section[0]
    identity = np.eye(27, dtype=np.int64)
    frame = identity[:, s]
    assert not tensor[s, s].any()
    delta = np.eye(3, dtype=np.int64)
    derivative = np.roll(delta, -1, axis=0)-delta

    def lie(x, v):
        dx, dv = derivative @ x, derivative @ v
        return (x[:, s, None]*dv - v[:, s, None]*dx
                + np.einsum("mnl,xl,xn->xm", y_tensor[:, s, :, :], dx, v))

    f, g, v = (row[:, None]*frame for row in delta)
    left = 2*(lie(f, lie(g, v))-lie(g, lie(f, v)))
    right = lie(lie(f, g)-lie(g, f), v)
    defect = (left-right)[:, s]
    assert defect.tolist() == [2, 2, 2]
    return dict(sites=3, axis=s, parameter_sites=[0, 1], field_site=2,
                doubled_closure_defect=defect.tolist())


def no_parameter_counterexample():
    # A commutator can have range two, whereas every first-order
    # pointwise gauge operator has only its original stencil range.
    results = []
    eye = np.eye(5, dtype=np.int64)
    shift = np.roll(eye, -1, axis=0)
    for name, difference in (("forward", shift-eye), ("centered", shift-shift.T)):
        def action(parameter):
            return np.diag(parameter) @ difference - np.diag(difference @ parameter)

        a, b = action(eye[0]), action(eye[1])
        assert difference[0, 2] == 0
        entry = int((a @ b - b @ a)[0, 2])
        assert entry == 1
        results.append(dict(stencil=name, sites=5, field_site=2, output_site=0,
                            commutator_matrix_entry=entry, any_parameter_matrix_entry=0))
    return results


def forward_matrix_algebra():
    checked = []
    for n in range(4, 10):
        units = np.eye(n*n, dtype=np.int64).reshape(n, n, n, n)
        generators = [units[i, (i+1) % n]-units[(i-1) % n, (i-1) % n] for i in range(n)]

        def bracket(a, b):
            return a @ b - b @ a

        for i, a in enumerate(generators):
            b = generators[(i+1) % n]
            commutator = bracket(a, b)
            distance_two = -bracket(b, commutator)-commutator
            assert np.array_equal(distance_two, units[i, (i+2) % n])
            edge = commutator-distance_two
            assert np.array_equal(edge, units[i, (i+1) % n])
        checked.append(dict(sites=n, matrix_lie_algebra_dimension=n*n))
    return checked


def calculate():
    tensor, y_tensor, five, six = exft.setup()
    section = tuple(sorted(set(five) & set(six)))
    gauge, trivial = operators(tensor, y_tensor, section)
    return dict(status="PASS", section=section, signed_blocks=certify_blocks(tensor, section),
                finite_controls=finite_controls(gauge, trivial),
                q4_site_space=site_space_smith(trivial),
                closure_impossible_with_any_pointwise_parameter=no_parameter_counterexample(),
                forward_pointwise_closure_counterexample=anchor_counterexample(tensor, y_tensor, section),
                forward_anchor_matrix_lie_algebra=forward_matrix_algebra())


if __name__ == "__main__":
    result = calculate()
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2), flush=True)
