"""Relative QCD theta matching from exact canonical W33 color blocks."""

import json

import numpy as np
import sympy as sp

import toe_20261110_light_yukawa_completion as flavor


OUT = 'data/toe_20261113_canonical_strong_cp.json'


def weight_block(matrix, weights, weight):
    cols = np.flatnonzero((weights == weight).all(axis=1))
    rows = np.flatnonzero((weights == -np.array(weight)).all(axis=1))
    return sp.Matrix(matrix[np.ix_(rows, cols)]), rows, cols


def color_triplets(hessian, split, weights, orbit):
    """One color weight counts each triplet-antitriplet pair once."""
    color = (0, 1)
    ranks = {}
    for weight in sorted(set(map(tuple, weights.tolist()))):
        if weight[:2] != color:
            continue
        full, rows, cols = weight_block(hessian, weights, weight)
        change, _, _ = weight_block(split, weights, weight)
        pivot_cols = full.rref()[1]
        rank = len(pivot_cols)
        ranks[weight[2:]] = rank
        if not any(change):
            assert weight[-1] != -2
            continue
        assert weight[2:] == (0, -2) and change.rank() == 3
        # This makes the same quotient and reference determinant usable
        # at every nonzero coefficient, with light and gauge kernels fixed.
        assert all(change*v == sp.zeros(change.rows, 1) for v in full.nullspace())
        assert all(change.T*v == sp.zeros(change.cols, 1) for v in full.T.nullspace())
        pivot_rows = full[:, pivot_cols].T.rref()[1]
        mass = full.extract(pivot_rows, pivot_cols)
        pencil = mass.inv()*change.extract(pivot_rows, pivot_cols)
        assert pencil*pencil == pencil
        assert pencil.trace() == 3 and rank == 21
        assert len(cols)-rank-sp.Matrix(orbit[:, cols]).rank() == 0
        assert len(rows)-rank-sp.Matrix(orbit[:, rows]).rank() == 3
    assert sum(ranks.values()) == 39
    assert sp.Matrix(orbit[:, np.flatnonzero((weights[:, :2] == color).all(axis=1))]).rank() == 9
    return [dict(weak_and_six_Y=list(key), rank=rank) for key, rank in ranks.items()]


def calculate():
    flat = flavor.flat
    gauge, adjoint, _, color, weak, y = flat.compact_chart()
    records = flat.vacuum.native.build_records()
    x, dual, mesons, fundamental, spaces, (hessian, orbit, weights) = flavor.projected_space(
        gauge, adjoint, color, weak, y, records
    )
    flavor.check_old_cubic(spaces)
    color_coroot = color[0] @ color[0].T - color[0].T @ color[0]
    trace_27 = int(np.trace(color_coroot @ color_coroot))
    assert trace_27 == 12
    # The basic E6 form is Tr_27/6, and the basic SU(3) coroot norm is two.
    embedding_index = sp.Rational(trace_27, 6*2)
    assert embedding_index == 1
    adjoint_piece = np.zeros_like(hessian)
    adjoint_piece[405:, 405:] = flat.sextic_adjoint_hessian(adjoint, y)
    # With meson 1 switched off, only the triplet splitting term remains.
    triplet_mesons = list(mesons)
    triplet_mesons[1] = np.zeros_like(mesons[1])
    split = flat.split_exotic_hessian(x, y, triplet_mesons, records, orbit)
    color_fundamental = {(0, 1), (1, -1), (-1, 0)}
    assert color_fundamental <= set(map(tuple, fundamental[:, :2].tolist()))
    color_nontrivial = {(i, j) for i, j in weights[:, :2] if i or j}
    color_roots = color_nontrivial-color_fundamental-{(-i, -j) for i, j in color_fundamental}
    assert color_roots == {(2, -1), (-2, 1), (1, 1), (-1, -1), (1, -2), (-1, 2)}
    colored_adjoint_rows = set(np.flatnonzero(
        (weights[:, :2] != 0).any(axis=1) & np.any(adjoint_piece, axis=1)
    ))
    octet_rows = set()
    for root in sorted(color_roots):
        weight = (*root, 0, 0)
        full, rows, cols = weight_block(hessian, weights, weight)
        piece, _, _ = weight_block(adjoint_piece, weights, weight)
        assert len(cols) == len(rows) == 1 and cols[0] >= 405 and rows[0] >= 405
        assert full == piece == sp.Matrix([[480]])
        assert not split[np.ix_(rows, cols)].any()
        assert not orbit[:, cols].any()
        gram = int(np.trace(adjoint[rows[0]-405] @ adjoint[cols[0]-405]))
        assert gram == 6
        octet_rows.update(cols)
    assert colored_adjoint_rows == octet_rows
    # Check all the colored weights touched by the triplet coefficient.
    touched = set(map(tuple, weights[np.any(split, axis=1)].tolist()))
    assert touched == {(*w, 0, -2) for w in color_fundamental} | {
        (-i, -j, 0, 2) for i, j in color_fundamental
    }
    blocks = color_triplets(hessian, split, weights, orbit)
    light = flat.read(flavor.OUT)['completion']
    yukawa = [sp.Matrix(light[label]).det() for label in ('up_matrix', 'down_matrix')]
    assert yukawa == [-27, -108]
    # Independent R-redefinition check with the earlier parent anomaly:
    # theta_E shifts by +90 r, W by -2 r, and the gluino mass by +2 r.
    heavy_weight = sum(row['rank'] for row in blocks) + 3
    uniform_weight = heavy_weight + 6
    assert 90-2*uniform_weight+2*3 == 0
    parent = flat.read('data/toe_20261112_theta_rephasing.json')
    labels = parent['angle_coefficient_labels']
    e6_phases = dict(zip(labels, parent['invariant_phase_coefficients'][0]))
    assert e6_phases['A5'] + e6_phases['A6'] == 3
    return dict(status='PASS', color_embedding_index=int(embedding_index),
                triplet_weight_blocks=blocks, triplet_split_determinant_ratio='z_T**3',
                octet_root_mass_numerator=480, octet_root_metric=6,
                octet_relative_majorana_mass='z_A', octet_anomaly_weight=3,
                broken_color_vector_triplet_pairs=18,
                heavy_chiral_uniform_superpotential_phase_weight=heavy_weight,
                uniform_superpotential_phase_weight_including_light_yukawas=uniform_weight,
                reference_light_yukawa_determinants=list(map(int, yukawa)),
                light_gluino_mass_phase_weight=3)


if __name__ == '__main__':
    result = json.dumps(calculate(), indent=2) + '\n'
    (flavor.flat.ROOT / OUT).write_text(result, encoding='utf-8')
    print(result)
