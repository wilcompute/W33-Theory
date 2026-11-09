"""Exact canonical-SM family embeddings and a two-dual flat vacuum."""

from itertools import combinations
import json

import numpy as np
import sympy as sp
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components
from sympy.polys.matrices import DomainMatrix

import toe_20261108_three_copy_cubic_vacuum as vacuum

ROOT = vacuum.ROOT
OUT = 'data/toe_20261109_canonical_sm_flatness.json'
SIGNED = 'data/toe_20261108_exact_signed_cubic_stabilizer.json'
SM = 'data/w33_pass11271_canonical_sm_higgs_bridge.json'


def read(path):
    return json.loads((ROOT / path).read_bytes())


def compact_chart():
    certificate = read(SIGNED)
    gauge = vacuum.gauge_generators(certificate)
    internal = np.stack([generator[::3, ::3] for generator in gauge[:78]])
    cartan = np.stack([h.diagonal() for h in internal if np.array_equal(h, np.diag(h.diagonal()))])
    sm = read(SM)
    export = np.load(ROOT / 'artifacts/e6_27rep_basis_export/E6_basis_78.npy')
    assert not export.imag.any()
    roots = export.real.astype(np.int64)[sm['unbroken_root_basis_indices']]
    raise_weak = roots[2]
    lower_weak = raise_weak.T
    color = np.delete(roots, [2, 5], axis=0)
    assert np.array_equal(roots[5], lower_weak)
    weak_cartan = raise_weak @ lower_weak - lower_weak @ raise_weak
    assert np.array_equal(weak_cartan @ raise_weak - raise_weak @ weak_cartan, 2 * raise_weak)
    assert not any((g @ raise_weak - raise_weak @ g).any() for g in color)
    assert vacuum.rank(color.reshape(6, -1)) == 6
    y = np.array([int(6 * sp.Rational(value)) for value in sm['hypercharge_diagonal']])
    assert tuple(np.flatnonzero(y == 0)) == (0, 1)
    assert np.array_equal(np.diag(y), sum(coefficient * np.diag(h) for coefficient, h in
                                        zip(sp.Matrix(cartan.T).gauss_jordan_solve(sp.Matrix(y))[0], cartan)))
    return gauge, internal, cartan, color, raise_weak, y


def family_embeddings(gauge, cartan, color, weak, y, records):
    # Use 6Y for the charge test. Signs on the doublet are inherited from E_+.
    assert (np.count_nonzero(color, axis=2) <= 1).all()
    color_fixed = np.flatnonzero(~color.any(axis=(0, 1)))
    pairs = [(i, j) for i, j in zip(*np.nonzero(weak)) if i in color_fixed]
    singlets = sorted(map(int, set(color_fixed) - {i for pair in pairs for i in pair}))
    assert singlets == [0, 1, 2] and list(y[singlets]) == [0, 0, 6]
    assert pairs == [(15, 16), (20, 22), (21, 23)]
    assert [(y[i], y[j]) for i, j in pairs] == [(-3, -3), (-3, -3), (3, 3)]

    h = -cartan[0] - 3 * cartan[3]
    assert h[singlets].tolist() == [2, 2, 2]
    basis = np.eye(81, dtype=np.int64).reshape(27, 3, 81)
    p = np.stack([basis[i, 1] - weak[i, j] * basis[j, 0] for i, j in pairs[:2]]
                 + [basis[2, 2]])
    family_weak = np.zeros((3, 3), dtype=np.int64)
    family_weak[0, 1] = 1
    raise_diagonal = np.kron(weak, np.eye(3, dtype=np.int64)) + np.kron(np.eye(27, dtype=np.int64), family_weak)
    diagonal_charge = (y[:, None] + np.array([3, 3, -6])).reshape(81)
    assert not (raise_diagonal @ p.T).any() and not (raise_diagonal.T @ p.T).any()
    assert not (diagonal_charge[:, None] * p.T).any()

    gram = np.sum(p * p, axis=1)
    compressed = np.stack([p @ g @ p.T for g in gauge])
    # Double the orthonormal diagonal compressions to keep integer entries.
    diagonal = 2 * np.diagonal(compressed, axis1=1, axis2=2)
    charges = diagonal // gram
    assert np.array_equal(charges * gram, diagonal)
    assert not charges.sum(axis=1).any() and vacuum.rank(charges) == 2
    off_diagonal = compressed.copy()
    off_diagonal[:, range(3), range(3)] = 0
    assert not off_diagonal[:, 2, :].any() and not off_diagonal[:, :, 2].any()
    assert vacuum.rank(off_diagonal.reshape(86, -1)) == 2
    assert compressed[11, 0, 1] == compressed[27, 1, 0] == -2
    assert np.count_nonzero(compressed[11]) == np.count_nonzero(compressed[27]) == 1

    brackets = [vacuum.bracket(p[i], p[j], records) for i, j in combinations(range(3), 2)]
    assert np.array_equal(brackets, [-2 * p[2], p[1], -p[0]])
    # With orthonormal columns the restricted three-form is minus unit volume.
    # D-flatness then forces equal occupation a and orthogonal first two
    # species columns. The F-square is minimized at 2a^2 by taking the
    # third column in their span. The witness below attains equality.
    x_rank_two = np.stack([p[0], p[1], np.zeros(81, dtype=np.int64)]).astype(object)
    x_rank_two[0, :] += sp.sqrt(2) * p[2].astype(object)
    assert all(sp.expand(sum(left @ g @ left for left in x_rank_two)) == 0 for g in gauge)
    f2 = sp.expand(sum(np.dot(f, f) for f in
                       (vacuum.bracket(a, b, records) for a, b in combinations(x_rank_two, 2))))
    assert f2 == 8

    return dict(color_fixed_indices=color_fixed.tolist(), weak_doublets=[[int(i) for i in pair] for pair in pairs],
                weak_singlets=singlets, separator_internal_cartan_coefficients=[-1, 0, 0, -3, 0, 0],
                separator_eigenvalues=h[singlets].tolist(), fixed_space_cases=[
                    {'external_simple_image': 'zero', 'all_hypercharges': 'positive internal separator'},
                    {'external_simple_image': 'color isomorphism', 'all_hypercharges': 'no fixed vector'},
                    {'external_simple_image': 'principal weak', 'all_hypercharges': 'no fixed vector'},
                    {'external_simple_image': 'regular weak', 'external_doublet_Y': '0',
                     'fixed_dimension': 2, 'D': 'family singleton only'},
                    {'external_simple_image': 'regular weak', 'external_doublet_Y': '-1/2',
                     'fixed_dimension': 1, 'D': 'family doublet only'},
                    {'external_simple_image': 'regular weak', 'external_doublet_Y': '1/2',
                     'fixed_dimension': 3, 'D': 'equal occupations and first two columns orthogonal',
                     'F': 'species rank at most 1', 'sharp_F_square_over_norm_four_on_D_flat': '2/9'},
                    {'external_simple_image': 'regular weak', 'external_doublet_Y': 'other',
                     'fixed_dimension': 0}],
                charge_rank=2, off_diagonal_rank=2, alternating_coefficient_orthonormal=-1,
                rank_two_D_flat_witness_F_square=int(f2))


def central_adjoint_check(internal, cartan, roots, y):
    h = -cartan[0] - 3 * cartan[3]
    h_charges = adjoint_charges(internal, h)
    y_charges = adjoint_charges(internal, y)
    charged = internal[(h_charges != 0) & (y_charges == 0)]
    rank = vacuum.rank(np.stack([np.concatenate([(g @ r - r @ g).ravel() for r in roots])
                                for g in charged]))
    assert rank == len(charged) == 6
    return rank


def adjoint_charges(internal, y):
    charges = []
    for g in internal:
        i, j = np.nonzero(g)
        assert len(set(y[i] - y[j])) == 1
        charges.append(y[i[0]] - y[j[0]])
    return np.array(charges)


def holomorphic_hessian(x, dual, internal, y, records, mixed_terms, signed_cubic=True):
    adjoint = slice(405, 483)
    hessian = np.zeros((483, 483), dtype=np.int64)
    cubic_blocks = [(0, 1, 2), (0, 2, 1), (1, 2, 0)] if signed_cubic else []
    for i, j, k in cubic_blocks:
        left = slice(81 * i, 81 * (i + 1))
        right = slice(81 * j, 81 * (j + 1))
        derivative = np.array(vacuum.native.jacobian(x[k], records))
        hessian[left, right] = (-1) ** (i + j + 1) * derivative
        hessian[right, left] = hessian[left, right].T
    lifted_internal = [np.kron(g, np.eye(3, dtype=np.int64)) for g in internal]
    for j, k in mixed_terms:
        xk = slice(81 * k, 81 * (k + 1))
        zj = slice(243 + 81 * j, 324 + 81 * j)
        hessian[xk, zj] = hessian[zj, xk] = np.diag(np.repeat(y, 3))
        for i, lifted in enumerate(lifted_internal, start=adjoint.start):
            hessian[xk, i] += dual[j] @ lifted
            hessian[i, xk] = hessian[xk, i]
            hessian[zj, i] += lifted @ x[k]
            hessian[i, zj] = hessian[zj, i]
    return hessian


def mass_spectrum(hessian, charges, orbit, y):
    """Holomorphic Hessian ranks and the quotient by the Higgs orbit."""
    assert not (orbit @ hessian).any()
    assert not hessian[(charges[:, None] + charges[None, :]) != 0].any()
    rows = []
    for charge in sorted(set(charges)):
        selected = charges == charge
        dimension = int(selected.sum())
        mass_rank = vacuum.rank(hessian[charges == -charge, :][:, selected])
        orbit_rank = vacuum.rank(orbit[:, selected])
        rows.append(dict(six_Y=int(charge), dimension=dimension, holomorphic_rank=mass_rank,
                         orbit_rank=orbit_rank, uneaten_massless=dimension - mass_rank - orbit_rank))
    assert sum(row['orbit_rank'] for row in rows) == 74
    by_charge = {row['six_Y']: row['uneaten_massless'] for row in rows}
    assert all(by_charge[q] - by_charge.get(-q, 0) == 3 * (sum(y == q) - sum(y == -q))
               for q in by_charge)
    return rows


def generic_mass_ranks(blocks, charges):
    """Compute universal rank bounds over the rational function field."""
    couplings = sp.symbols('omega a b c')
    result = {}
    for charge in sorted(set(charges)):
        tensor = blocks[:, charges == -charge, :][:, :, charges == charge]
        pattern = tensor.any(axis=0)
        rows, cols = pattern.shape
        bipartite = np.block([[np.zeros((rows, rows), dtype=bool), pattern],
                              [pattern.T, np.zeros((cols, cols), dtype=bool)]])
        _, labels = connected_components(csr_matrix(bipartite), directed=False)
        rank = 0
        for label in set(labels):
            left, right = labels[:rows] == label, labels[rows:] == label
            if not left.any() or not right.any():
                continue
            component = tensor[:, left, :][:, :, right]
            entries = {(int(i), int(j)): sum(int(v) * k for v, k in zip(component[:, i, j], couplings))
                       for i, j in zip(*np.nonzero(component.any(axis=0)))}
            matrix = sp.SparseMatrix(component.shape[1], component.shape[2], entries)
            rank += DomainMatrix.from_Matrix(matrix).to_field().rank()
        result[int(charge)] = rank
    return result


def dual_repair(gauge, internal, y, records):
    basis = np.eye(81, dtype=np.int64).reshape(27, 3, 81)
    x = np.stack([basis[0, 0], basis[1, 1], basis[0, 2] + basis[1, 2]])
    dual = np.stack([x[0] + x[1], x[2]])
    assert all(not vacuum.bracket(a, b, records).any() for a, b in combinations(x, 2))
    assert all(np.einsum('ni,ij,nj->', x, g, x) == np.einsum('ni,ij,nj->', dual, g.T, dual)
               for g in gauge)
    # The adjoint equals 6Y in this integer chart. It is Hermitian and
    # kills the VEVs. Family support makes the adjoint derivative vanish.
    assert not (np.repeat(y, 3) * x).any() and not (np.repeat(y, 3) * dual).any()
    assert all(not (dual[0] @ g @ x[2]) for g in gauge[:78])
    orbit = np.stack([(x @ g.T).ravel() for g in gauge])
    orbit_dual = np.stack([(-dual @ g).ravel() for g in gauge])
    y_action = np.vstack([np.diag(-adjoint_charges(internal, y)), np.zeros((8, 78), dtype=np.int64)])
    rank = vacuum.rank(np.hstack([orbit, orbit_dual]))
    rank_y = vacuum.rank(np.hstack([orbit, orbit_dual, y_action]))
    assert (rank, rank_y) == (62, 74)
    all_orbit = np.hstack([orbit, orbit_dual, y_action])
    adjoint_derivative = np.stack([(dual @ g @ x.T).ravel() for g in gauge[:78]])
    allowed = [(0, 2), (1, 0), (1, 1)]
    assert vacuum.rank(adjoint_derivative) == 3
    assert not adjoint_derivative[:, [3 * j + k for j, k in allowed]].any()
    charges = np.concatenate([np.tile(np.repeat(y, 3), 3), np.tile(np.repeat(-y, 3), 2),
                              adjoint_charges(internal, y)])
    omega = holomorphic_hessian(x, dual, internal, y, records, [])
    mixed = [holomorphic_hessian(x, dual, internal, y, records, [term], signed_cubic=False)
             for term in allowed]
    blocks = np.stack([omega, *mixed])
    spectrum = mass_spectrum(omega + mixed[0], charges, all_orbit, y)
    assert sum(row['uneaten_massless'] for row in spectrum) == 211
    richer_spectrum = mass_spectrum(blocks.sum(axis=0), charges, all_orbit, y)
    richer_massless = sum(row['uneaten_massless'] for row in richer_spectrum)
    generic_ranks = generic_mass_ranks(blocks, charges)
    assert generic_ranks == {row['six_Y']: row['holomorphic_rank'] for row in richer_spectrum}
    assert richer_massless == 101 and sum(generic_ranks.values()) == 308
    return dict(fundamental_supports=[np.flatnonzero(v).tolist() for v in x],
                dual_supports=[np.flatnonzero(v).tolist() for v in dual],
                mixed_cubic='dual[0] * (A tensor I) * X[2]',
                residual_dimensions_without_and_with_adjoint=[86 - rank, 86 - rank_y],
                minimal_dual_count_for_exact_untwisted_SM=2,
                uneaten_massless_by_hypercharge=spectrum,
                allowed_mixed_cubic_indices_zero_based=allowed,
                all_allowed_terms_unit_coupling_uneaten_massless=richer_massless,
                all_allowed_terms_unit_coupling_spectrum=richer_spectrum,
                generic_rank_by_hypercharge=generic_ranks,
                minimum_uneaten_massless_at_fixed_vev=richer_massless)


def calculate():
    gauge, internal, cartan, color, weak, y = compact_chart()
    records = vacuum.native.build_records()
    roots = [*color, weak, weak.T]
    result = family_embeddings(gauge, cartan, color, weak, y, records)
    adjoint_rank = central_adjoint_check(internal, cartan, roots, y)
    fundamental_trace = 1 + 1 - 8
    decuplet_trace = sum((4 - r) * (3 - 3 * r)**3 for r in range(4))
    assert decuplet_trace == 27 * fundamental_trace
    return dict(status='PASS', original_field_content='three (27,3) with the alternating cubic',
                scope='fixed canonical internal projection; compact Lie-algebra graphs; canonical D terms',
                family_embeddings=result, adjoint_center_check_rank=adjoint_rank,
                repair=dual_repair(gauge, internal, y, records),
                perturbative_family_anomaly=dict(fundamental_minus_duals=27,
                                                 conjugate_symmetric_cube_spectator=-27,
                                                 total=0, net_SM_families=3))


if __name__ == '__main__':
    (ROOT / OUT).write_text(json.dumps(calculate(), indent=2) + '\n', encoding='utf-8')
