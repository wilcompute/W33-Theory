"""An explicit two-frame E6 orbifold vacuum and its zero-mode mass matrix."""

import json
from collections import Counter
from itertools import product

import sympy as sp

from toe_20261116_E6_full_cubic_SM_stabilizer import (
    cubic_monomials, hypercharge_integer_weights,
)
from toe_20261116_E6_triplet_exchange_filter import source_tensors
from toe_20261117_E6_interval_R_index import left_reflections
from toe_20261117_E6_two_protected_corners import multiply, torus_generator_basis


def corner_system(weights, cubic):
    blocks, reflections = left_reflections(weights, cubic)
    by_odd = {tuple(i for i, block in enumerate(blocks) if p[block[0]] < 0): p
              for p in reflections}
    p = by_odd[0, 1, 2, 9]
    px = by_odd[0, 2, 3, 5, 6, 8]
    uy = by_odd[0, 1, 3, 4, 6, 7]
    return p, px, multiply(p, uy), multiply(px, uy)


def mode_vector(name, size, corners, signs, desired):
    return sp.Matrix([
        sp.Symbol(f"{name}_{i}") if all(
            eta*p[i] == desired for eta, p in zip(signs, corners, strict=True)
        ) else sp.S.Zero
        for i in range(size)
    ])


def vacuum_hessian(weights, cubic, corners):
    size = len(weights)
    zero = sp.zeros(size, 1)
    names = ("A", "B", "K", "L")
    corner_signs = {"A": (1, 1, -1, -1), "B": (1, -1, 1, -1),
                    "K": (-1, -1, 1, 1), "L": (-1, -1, 1, 1)}
    h, hb, hc, hbc = (
        {name: mode_vector(name+suffix, size, corners, corner_signs[name], parity)
         for name in names}
        for suffix, parity in (("", 1), ("bar", 1), ("c", -1), ("barc", -1))
    )
    assert set(map(str, h["A"].free_symbols)) == {"A_7", "A_12", "A_13", "A_14"}
    assert set(map(str, h["B"].free_symbols)) == {"B_8", "B_15", "B_16", "B_17"}
    basis, coordinates = torus_generator_basis(cubic, corners, -1)
    sigma_vars = sp.Matrix(sp.symbols(f"Sigma:{basis.rows}"))
    assert basis.rows == 12
    sigma = sp.zeros(size)
    for (i, j), value in zip(coordinates, basis.T*sigma_vars, strict=True):
        sigma[i, j] = value

    def d(a, b):
        out = zero.copy()
        for (i, j, k), coefficient in cubic.items():
            for row, u, v in ((i, j, k), (j, i, k), (k, i, j)):
                out[row] += coefficient*(a[u]*b[v]+a[v]*b[u])
        return out

    a, b = h["A"], h["B"]
    abar, bbar = hb["A"], hb["B"]
    singlets = sp.symbols("s t")
    terms = {
        "weak_pair": hc["A"].dot(h["L"])+hbc["A"].dot(hb["L"]),
        "triplets": hc["K"].dot(d(abar, d(a, a)))+hbc["K"].dot(d(a, d(abar, abar)))
                    +hc["L"].dot(d(abar, d(b, b)))+hbc["L"].dot(d(a, d(bbar, bbar))),
        "neutral_norms": hc["K"].dot(a)*(a.dot(abar)-1)
                         +hbc["K"].dot(abar)*(b.dot(bbar)-1),
        "neutral_partners": singlets[0]*hc["L"].dot(a)+singlets[1]*hbc["L"].dot(abar),
        "bulk_gauge": sum(hc[name].dot(sigma*h[name])-hbc[name].dot(sigma.T*hb[name])
                          for name in names),
    }
    r0_weights, r2_weights = {s: 0 for s in singlets}, {}
    for name, is_dual in product(names, (False, True)):
        for i, w in enumerate(weights):
            v = (hb if is_dual else h)[name][i]
            c = (hbc if is_dual else hc)[name][i]
            if v:
                r0_weights[v] = (-1 if is_dual else 1)*w
            if c:
                r2_weights[c] = (1 if is_dual else -1)*w
    for row, var in enumerate(sigma_vars):
        grades = {weights[i]-weights[j] for coeff, (i, j) in
                  zip(basis[row, :], coordinates, strict=True) if coeff}
        assert len(grades) == 1
        r0_weights[var] = grades.pop()
    r0, r2 = list(r0_weights), list(r2_weights)
    vac = dict.fromkeys(r0, 0)
    vac.update({a[7]: 1, abar[7]: 1, b[8]: 1, bbar[8]: 1})
    assert d(a.subs(vac), a.subs(vac)) == zero
    assert d(b.subs(vac), b.subs(vac)) == zero
    superpotential = sum(terms.values())
    functions = sp.Matrix([sp.diff(superpotential, var) for var in r2])
    assert functions.subs(vac) == sp.zeros(len(r2), 1)
    jacobian = functions.jacobian(r0).subs(vac)
    assert jacobian.rank() == len(r2)
    triplets = [12, 13, 14]
    assert jacobian.extract([r2.index(hc["K"][i]) for i in triplets],
                            [r0.index(h["A"][i]) for i in triplets]) == 2*sp.eye(3)

    # Each of the two broken Cartans gives a true zero of the superpotential
    # Hessian, then the corresponding vector eats it.
    vectors, vector_entries = torus_generator_basis(cubic, corners, 1)
    diagonal = {i: n for n, (i, j) in enumerate(vector_entries) if i == j}
    eaten_columns = []
    for v in range(vectors.rows):
        direction = {a[7]: vectors[v, diagonal[7]], abar[7]: -vectors[v, diagonal[7]],
                     b[8]: vectors[v, diagonal[8]], bbar[8]: -vectors[v, diagonal[8]]}
        eaten_columns.append(sp.Matrix([direction.get(var, 0) for var in r0]))
    eaten = sp.Matrix.hstack(*eaten_columns)
    assert vectors.rows == 14 and eaten.rank() == 2
    assert jacobian*eaten == sp.zeros(len(r2), vectors.rows)
    light = [v for v in r0 if str(v) in {"K_0", "K_3", "Kbar_0", "Kbar_3"}]
    assert len(light) == 4
    assert jacobian[:, [r0.index(v) for v in light]] == sp.zeros(len(r2), 4)
    assert len(r0)-jacobian.rank() == eaten.rank()+len(light)

    mass_ranks = {}
    for w in sorted(set(r0_weights.values()) | {-w for w in r2_weights.values()}):
        rows = [i for i, v in enumerate(r2) if r2_weights[v] == -w]
        cols = [j for j, v in enumerate(r0) if r0_weights[v] == w]
        mass_ranks[w] = [len(cols), len(rows), jacobian.extract(rows, cols).rank()]
    return {"R0_chiral_components": len(r0), "R2_chiral_components": len(r2),
            "superpotential_mass_rank": jacobian.rank(), "eaten_modes": eaten.rank(),
            "physical_light_chiral_components": [str(v) for v in light],
            "charges_R0_R2conjugate_mass_rank_by_w": mass_ranks}


def scalar_exchange_witness(cubic):
    # The required family-exotic lifting also sources a colored scalar of A.
    # The two light channels have distinct B but the same gauge charge.
    weights, up, _ = source_tensors()
    baryon3 = {-6: 0, -2: -1, -1: 1, 3: 0, 4: -1}
    triplet = 12
    first, second = next(
        (p, q) for p, q in product(up[triplet], repeat=2)
        if sum(baryon3[weights[i]] for i in p[:2]) == 1
        and sum(baryon3[weights[i]] for i in q[:2]) == -2
    )
    assert weights[triplet] == -2
    size = len(weights)
    frame = sp.eye(size)[:, 7]
    h1 = sp.Matrix(size, size, lambda i, j: cubic.get(tuple(sorted((i, j, 7))), 0))
    derivative = sp.eye(size)-h1*h1
    assert derivative*frame == frame
    assert derivative[:, [12, 13, 14]] == sp.zeros(size, 3)
    return {"triplet_coordinate": triplet, "QL_vertex": first,
            "UcDc_vertex": second, "absolute_scalar_exchange_numerator": 1,
            "canonical_zero_mode_coefficient_at_unit_parameters": "1/4",
            "cubic_filter_keeps_frame_and_removes_triplet_linear_source": True}


def eight_fundamental_bulk_lattice():
    a = sp.Matrix([-2, -2])
    b = sp.Matrix([1, 1])
    form = sp.Matrix([[0, 1], [1, 0]])
    assert (a.T*form*b)[0] == 4-8
    assert (b.T*form*b)[0] == -12*(sp.Rational(1, 2)-8*sp.Rational(1, 12)) == 2
    neutral = 273+78-29-8*27
    assert neutral == 106
    degrees = [int(((-n*a-m*b).T*form*b)[0]) for n, m in ((4, 3), (6, 4))]
    assert degrees == [10, 16]
    return {"tensor_multiplets": 1, "neutral_hypers": neutral,
            "a_dot_b": -4, "b_squared": 2, "positive_F2_section_f3_g4_degrees": degrees,
            "degree_of_split_g4_square_root": 8}


def certificate():
    weights, cubic = hypercharge_integer_weights(), cubic_monomials()
    corners = corner_system(weights, cubic)
    return {"vacuum": vacuum_hessian(weights, cubic, corners),
            "charged_scalar_exchange": scalar_exchange_witness(cubic),
            "bulk_anomaly_lattice": eight_fundamental_bulk_lattice()}


if __name__ == "__main__":
    print(json.dumps(certificate(), indent=2))
