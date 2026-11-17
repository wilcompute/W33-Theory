"""Exact lattice lifts, Hodge modes and nonlinear sampling of the native torus."""

import json
from collections import Counter
from itertools import combinations, product

import sympy as sp

from w33_dual_szilassi_from_cyclic_csaszar import cyclic_csaszar_faces
from w33_heawood_szilassi_spectrum import fano_incidence_matrix


PERIODS = sp.Matrix([[-3, -1], [1, -2]])
Q = sp.Matrix([[1, sp.Rational(1, 2)], [sp.Rational(1, 2), 1]])
STEPS = ((1, 0), (0, 1), (1, -1), (-1, 0), (0, -1), (-1, 1))
WAVES = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1))


def face_and_hodge():
    faces = cyclic_csaszar_faces()
    lattice_faces = sorted({tuple(sorted((r % 7, (r+1) % 7, (r+3) % 7))) for r in range(7)}
                           | {tuple(sorted((r+1) % 7 for r in (j, j+2, j+3))) for j in range(7)})
    assert faces == lattice_faces
    assert PERIODS.det() == 7 and PERIODS.T*Q*PERIODS == 7*Q
    rotation = sp.Matrix([[0, -1], [1, 1]])
    assert rotation.T*Q*rotation == Q
    assert PERIODS.inv()*rotation*PERIODS == rotation
    assert all((sp.Matrix([[1, 3]])*rotation[:, j])[0] % 7 == (3*sp.Matrix([[1, 3]])[j]) % 7
               for j in range(2))
    edge_steps = {(x+3*y) % 7: sp.Matrix([x, y]) for x, y in STEPS}
    assert set(edge_steps) == set(range(1, 7))
    edges = list(combinations(range(7), 2))
    d1, d2 = sp.zeros(7, 21), sp.zeros(21, 14)
    edge_index = {edge: i for i, edge in enumerate(edges)}
    for i, (a, b) in enumerate(edges):
        d1[a, i], d1[b, i] = -1, 1
    for i, (a, b, c) in enumerate(faces):
        for u, v, sign in ((a, b, 1), (b, c, 1), (a, c, -1)):
            d2[edge_index[u, v], i] = sign
    # Fix a global surface orientation without changing the input face list.
    oriented = d2.nullspace()
    assert len(oriented) == 1 and all(abs(x) == 1 for x in oriented[0])
    d2 *= sp.diag(*oriented[0])
    assert d1*d2 == sp.zeros(7, 14)
    l0, l1, l2 = d1*d1.T, d1.T*d1+d2*d2.T, d2.T*d2
    assert l0 == 7*sp.eye(7)-sp.ones(7)
    hodge = sp.Matrix.hstack(*(edge_steps[(b-a) % 7] for a, b in edges)).T
    assert hodge.rank() == 2 and d1*hodge == sp.zeros(7, 2) and d2.T*hodge == sp.zeros(14, 2)
    cycles = ((0, 1, 2, 0), (0, 1, 4, 0))
    periods = sp.Matrix.hstack(*(sum((edge_steps[(b-a) % 7] for a, b in zip(cycle, cycle[1:])),
                                   sp.zeros(2, 1)) for cycle in cycles))
    assert periods == -PERIODS
    normalized = hodge*PERIODS.inv().T
    assert normalized.T*(d1.T*d1+d2*d2.T)*normalized == sp.zeros(2)
    z = sp.Symbol("z")
    expected = z**2*(z-7)**6*(z-6)*(z*z-6*z+7)**6
    assert sp.factor(l1.charpoly(z).as_expr()-expected) == 0
    dual = 3*sp.eye(14)-l2
    assert all(dual[i, j] in (0, 1) for i, j in product(range(14), repeat=2))
    fano = fano_incidence_matrix()
    assert fano*fano.T == 2*sp.eye(7)+sp.ones(7)
    assert sp.factor(l2.charpoly(z).as_expr()) == z*(z-6)*(z*z-6*z+7)**6
    # Native face labels give honeycomb shifts {0,1,-2}; their signed
    # pair differences fill all six nonzero residues exactly once.
    shifts = {j for j in range(7) if len({0, 1, 3} & {j, (j+2) % 7, (j+3) % 7}) == 2}
    assert shifts == {0, 1, 5}
    differences = Counter((a-b) % 7 for a, b in product(shifts, repeat=2))
    assert differences == Counter({0: 3, **{k: 1 for k in range(1, 7)}})
    integer_rows = lambda matrix: [[int(x) for x in row] for row in matrix.tolist()]
    return {"period_basis": integer_rows(PERIODS), "metric_Gram": [[str(x) for x in row] for row in Q.tolist()],
            "primal_f_vector": [7, 21, 14], "dual_f_vector": [14, 21, 7],
            "edge_harmonic_lifts_dx_dy": integer_rows(hodge),
            "two_cycle_lift_periods": integer_rows(periods),
            "edge_Hodge_characteristic_polynomial": str(expected),
            "edge_Hodge_eigenvalues": {"0": 2, "7": 6, "6": 1,
                                         "3-sqrt(2)": 6, "3+sqrt(2)": 6},
            "honeycomb_shifts_in_native_labels": sorted(shifts)}


def shell_moment(power, refinement):
    coefficients = Counter({(0, 0): sp.S.One})
    for _ in range(power):
        updated = Counter()
        for (x, y), value in coefficients.items():
            for dx, dy in WAVES:
                updated[x+dx, y+dy] += value/2
        coefficients = updated
    if refinement is None:
        return coefficients[0, 0]
    inverse = PERIODS.T.inv()/refinement
    return sum(value for mode, value in coefficients.items()
               if all(x.is_Integer for x in inverse*sp.Matrix(mode)))


def certificate():
    geometry = face_and_hodge()
    moments = {str(n): [str(shell_moment(p, n)) for p in (2, 3, 4, 5, 6)]
               for n in (1, 2, 3)}
    continuum = [str(shell_moment(p, None)) for p in (2, 3, 4, 5, 6)]
    assert moments["1"][:3] == ["3/2", "15/4", "93/8"]
    assert moments["2"][:4] == continuum[:4]
    assert moments["3"] == continuum
    return {"geometry_and_harmonics": geometry,
            "triad_powers": [2, 3, 4, 5, 6], "continuum_moments": continuum,
            "finite_moments_by_refinement": moments,
            "site_count_by_refinement": {str(n): 7*n*n for n in (1, 2, 3)},
            "vertex_heat_trace": "1+6 exp(-7 beta)",
            "edge_heat_trace": "2+6 exp(-7 beta)+exp(-6 beta)+6 exp(-(3-sqrt(2))beta)+6 exp(-(3+sqrt(2))beta)",
            "Szilassi_vertex_heat_trace": "1+exp(-6 beta)+6 exp(-(3-sqrt(2))beta)+6 exp(-(3+sqrt(2))beta)",
            "W33_graph_heat_trace_from_existing_oscillator": "1+24 exp(-10 beta)+15 exp(-16 beta)"}


if __name__ == "__main__":
    print(json.dumps(certificate(), indent=2))
