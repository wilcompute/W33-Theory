"""Resolve the mixed Z4^R anomaly on the E6 orbifold's common Cartan lattice."""

import json
from collections import defaultdict
from itertools import product

import sympy as sp
from sympy.matrices.normalforms import smith_normal_decomp
from sympy.polys.matrices import DomainMatrix

from toe_20261116_E6_full_cubic_SM_stabilizer import (
    cubic_derivation_rows, cubic_monomials, hypercharge_integer_weights,
)
from toe_20261117_E6_two_corner_vacuum import corner_system


def cartan_lattice(cubic):
    incidence = sp.zeros(len(cubic), 27)
    for row, triple in enumerate(cubic):
        for i in triple:
            incidence[row, i] = 1
    diagonal, u, v = smith_normal_decomp(incidence, domain=sp.ZZ)
    assert u*incidence*v == diagonal and abs(v.det()) == 1
    rank = diagonal.rank()
    basis = v[:, rank:]
    assert rank == 21 and incidence*basis == sp.zeros(len(cubic), 6)
    return basis


def adjoint_roots(cubic, charges, corners):
    rows = cubic_derivation_rows(cubic)
    indices = defaultdict(list)
    for i, j in product(range(charges.rows), repeat=2):
        if i != j:
            root = tuple(charges[i, :]-charges[j, :])
            assert any(root)
            indices[root].append((i, j))
    roots = {}
    for root, pairs in indices.items():
        index = {charges.rows*i+j: n for n, (i, j) in enumerate(pairs)}
        restrictions = []
        for row in rows:
            if reduced := {index[k]: sp.QQ(v) for k, v in row.items() if k in index}:
                restrictions.append(reduced)
        matrix = DomainMatrix(dict(enumerate(restrictions)),
                              (len(restrictions), len(pairs)), sp.QQ)
        if len(pairs)-matrix.rank():
            assert len(pairs)-matrix.rank() == 1
            signs = {tuple(p[i]*p[j] for p in corners) for i, j in pairs}
            assert len(signs) == 1
            roots[root] = signs.pop()
    assert len(roots) == 72
    return roots


def anomaly_matrices(cubic, corners):
    charges = cartan_lattice(cubic)
    roots = adjoint_roots(cubic, charges, corners)
    # A, B and the two copies K,L each come with a dual hypermultiplet.
    intrinsic_sums = (0, -4, 4, 0)
    source_signs = [(1, 1, -1, -1), (1, -1, 1, -1),
                    (-1, -1, 1, 1), (-1, -1, 1, 1)]
    assert tuple(2*sum(s) for s in zip(*source_signs, strict=True)) == intrinsic_sums
    norm = charges.T*charges/6
    assert all(v.is_Integer for v in norm)
    local = []
    for f, reflection in enumerate(corners):
        adjoint = sum((signs[f]*sp.Matrix(root)*sp.Matrix(root).T
                       for root, signs in roots.items()), sp.zeros(6))
        hyper = charges.T*sp.diag(*reflection)*charges
        local.append((adjoint-intrinsic_sums[f]*hyper)/4)
    total = sum(local, sp.zeros(6))
    # Independently use only the projected zero modes.
    zero_mode_total = sp.zeros(6)
    for root, signs in roots.items():
        if len(set(signs)) == 1:
            zero_mode_total += signs[0]*sp.Matrix(root)*sp.Matrix(root).T
    for signs in source_signs:
        for i in range(charges.rows):
            combined = {p[i]*eta for p, eta in zip(corners, signs, strict=True)}
            if len(combined) == 1:
                zero_mode_total -= 2*combined.pop()*charges[i, :].T*charges[i, :]
    assert total == zero_mode_total
    residual = (total-2*norm).applyfunc(lambda n: n % 4)
    return charges, norm, local, total, residual


def trinification_root_fluxes():
    for factor, (i, j) in product(range(3), product(range(3), repeat=2)):
        if i == j:
            continue
        levels = [[0]*3 for _ in range(3)]
        levels[factor][i], levels[factor][j] = 1, -1
        left, right, color = levels
        charge = ([l-r for l, r in product(left, right)]
                  + [r-c for r, c in product(right, color)]
                  + [c-l for c, l in product(color, left)])
        yield factor, i, j, sp.Matrix(charge)


def covering_nonabelian_levels():
    out = []
    for f, intrinsic_sum in enumerate((0, -4, 4, 0)):
        if f == 2:
            out.append({"Spin10": (8+2*intrinsic_sum)//4,
                        "U1psi_charge_squared_trace": (-288-40*intrinsic_sum)//4})
        else:
            out.append({"SU6": -intrinsic_sum//2,
                        "SU2": -4+3*intrinsic_sum//2})
    assert [row.get("SU6", row.get("Spin10")) % 4 for row in out] == [0, 2, 0, 0]
    return out


def local_quotient_witnesses(corners, charges, norm, local, total):
    result = []
    for f in (0, 1, 3):
        parity = corners[f]
        flux = next((tag, i, j, h) for tag, i, j, h in trinification_root_fluxes()
                    if sum(h[n]**2 for n, sign in enumerate(parity) if sign == 1) == 6
                    and h.dot(h) == 12)
        factor, i, j, h = flux
        v = charges.gauss_jordan_solve(h)[0]
        assert all(value.is_Integer for value in v)
        inherited_number = (v.T*norm*v)[0]
        phases = [int((v.T*matrix*v)[0]) for matrix in local]
        assert inherited_number == 2 and phases[f] % 4 == 2
        total_phase = (v.T*total*v)[0] % 4
        assert total_phase == sum(phases) % 4
        result.append({"corner": f, "trinification_factor_L_R_C": factor,
                       "root_flux_diagonal_indices": [i, j], "E6_instanton_number": 2,
                       "local_phase_exponents_mod4": [value % 4 for value in phases],
                       "global_phase_exponent_mod4": int(total_phase)})
    return result


def global_witness(charges, norm, local, total):
    root_fluxes = list(trinification_root_fluxes())
    for (r, i, j, h), (s, k, ell, g) in product(root_fluxes, repeat=2):
        if r == s or h.dot(g):
            continue
        v, w = (charges.gauss_jordan_solve(t)[0] for t in (h, g))
        assert all(value.is_Integer for value in list(v)+list(w))
        if (v.T*total*w)[0] % 4 == 2:
            assert (v.T*norm*w)[0] == 0
            return {
                "first_trinification_factor_and_indices": [r, i, j],
                "second_trinification_factor_and_indices": [s, k, ell],
                "first_flux_charges_on_27": list(map(int, h)),
                "second_flux_charges_on_27": list(map(int, g)),
                "E6_instanton_number": 0,
                "local_exponents_mod4": [int((v.T*m*w)[0] % 4) for m in local],
                "global_exponent_mod4": 2,
            }
    raise AssertionError("No orthogonal trinification flux witness")


def local_invariant_decomposition(corners, charges, norm, local, levels):
    out = []
    classes = []
    for f, parity in enumerate(corners):
        if f == 2:
            # The 1_4 in the Spin(10) corner supplies a genuine quotient
            # character. In bilinear flux conventions its square is I_{Q=4}.
            charge = charges[8, :]
            assert parity[8] == 1
            character_square = charge.T*charge
            assert local[f] == 4*norm-10*character_square
            classes.append(character_square)
            out.append({"inherited_E6_coefficient": 4,
                        "quotient_character_square_coefficient": -10,
                        "quotient_character_coordinate": 8})
        else:
            plus = charges.T*sp.diag(*[int(s == 1) for s in parity])*charges
            minus = charges.T*sp.diag(*[int(s == -1) for s in parity])*charges
            four_i2 = (2*minus-plus)/3
            assert all(value.is_Integer for value in four_i2)
            a6, a2 = levels[f]["SU6"], levels[f]["SU2"]
            assert (a2-a6) % 4 == 0
            assert local[f] == a6*norm+((a2-a6)//4)*four_i2
            classes.append(four_i2)
            out.append({"inherited_E6_coefficient": a6,
                        "four_times_SU2_instanton_coefficient": (a2-a6)//4})
    return out, classes


def global_inflow_span(total, norm, classes):
    generators = [list(map(int, x)) for x in [norm, *classes]]
    target = [int(n % 4) for n in total]
    matches = []
    for coeffs in product(range(4), repeat=len(generators)):
        if all(sum(c*v for c, v in zip(coeffs, row, strict=True)) % 4 == expected
               for row, expected in zip(zip(*generators, strict=True), target, strict=True)):
            matches.append(coeffs)
    assert matches and not any(not any(c[1:]) for c in matches)
    minimum = min(sum(bool(c) for c in solution[1:]) for solution in matches)
    return {"minimum_nonuniversal_classes": minimum,
            "smallest_coefficient_vectors_mod4": [
                c for c in matches if sum(bool(a) for a in c[1:]) == minimum
            ]}


def as_integers(matrix):
    assert all(value.is_Integer for value in matrix)
    return [list(map(int, row)) for row in matrix.tolist()]


def certificate():
    cubic = cubic_monomials()
    corners = corner_system(hypercharge_integer_weights(), cubic)
    charges, norm, local, total, residual = anomaly_matrices(cubic, corners)
    witnesses = local_quotient_witnesses(corners, charges, norm, local, total)
    levels = covering_nonabelian_levels()
    decomposition, classes = local_invariant_decomposition(corners, charges, norm, local, levels)
    return {
        "corner_order_00_10_01_11": levels,
        "cartan_cocharacter_basis_on_the_27": as_integers(charges),
        "E6_normalized_instanton_bilinear": as_integers(norm),
        "local_anomaly_bilinear_by_corner": [as_integers(m) for m in local],
        "integrated_anomaly_bilinear": as_integers(total),
        "integrated_residual_after_universal_coefficient_2_mod4": as_integers(residual),
        "diagonal_center_quotient_backgrounds": witnesses,
        "global_orthogonal_flux_obstruction": global_witness(charges, norm, local, total),
        "local_index_as_quotient_characteristic_classes": decomposition,
        "global_inflow_in_order_E6_00_10_01_11": global_inflow_span(total, norm, classes),
    }


if __name__ == "__main__":
    print(json.dumps(certificate(), indent=2))
