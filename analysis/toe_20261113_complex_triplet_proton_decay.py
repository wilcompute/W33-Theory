"""Exact dimension-five triplet exchange along the complex strong-CP deformation."""

import json

import numpy as np
import sympy as sp

import toe_20261110_light_yukawa_completion as flavor


OUT = 'data/toe_20261113_complex_triplet_proton_decay.json'


def remove_light_source(source, kernel, metric):
    if not kernel:
        return source, 0
    null = sp.Matrix.hstack(*kernel)
    overlap = (null.T*source).applyfunc(sp.expand)
    projected = source - metric*null*(null.T*metric*null).inv()*overlap
    return projected.applyfunc(sp.expand), overlap.rank()


def exchange_pencil(mass, change, left, right, phase, *, metrics=None):
    for source in (left, right):
        assert all(sp.Poly(entry, phase).degree() <= 1 for entry in source)
    left_null, right_null = mass.T.nullspace(), mass.nullspace()
    light_ranks = [0, 0]
    if metrics is not None:
        left, light_ranks[0] = remove_light_source(left, left_null, metrics[0])
        right, light_ranks[1] = remove_light_source(right, right_null, metrics[1])
    for null in right_null:
        assert change*null == sp.zeros(change.rows, 1)
        assert (null.T*right).applyfunc(sp.expand) == sp.zeros(1, right.cols)
    for null in left_null:
        assert change.T*null == sp.zeros(change.cols, 1)
        assert (null.T*left).applyfunc(sp.expand) == sp.zeros(1, left.cols)
    cols = mass.rref()[1]
    rows = mass[:, cols].T.rref()[1]
    assert len(rows) == len(cols) == 21
    reference = mass.extract(rows, cols)
    inverse = reference.inv()
    projector = inverse*change.extract(rows, cols)
    assert projector*projector == projector and projector.trace() == 3
    selected_left = left[list(rows), :]
    selected_right = right[list(cols), :]
    fixed = sp.eye(len(cols))-projector
    numerator = (
        selected_right.T*(phase*fixed+projector)*inverse*selected_left
    ).applyfunc(sp.expand)
    # Resolve both source legs and both propagator blocks independently.
    left_pieces = (selected_left.subs(phase, 0), selected_left.diff(phase))
    right_pieces = (selected_right.subs(phase, 0), selected_right.diff(phase))
    separate_ranks = [
        [[(right_piece.T*block*inverse*left_piece).rank() for left_piece in left_pieces]
         for right_piece in right_pieces]
        for block in (fixed, projector)
    ]
    powers = {power: numerator.applyfunc(lambda entry: entry.coeff(phase, power))
              for power in range(4)}
    assert sum((phase**power*matrix for power, matrix in powers.items()),
               sp.zeros(numerator.rows, numerator.cols)) == numerator
    record = dict(shape=list(numerator.shape), mass_rank=len(cols), projector_rank=3,
                removed_kernel_source_ranks=light_ranks,
                source_variation_ranks=[left.diff(phase).rank(), right.diff(phase).rank()],
                separate_contraction_ranks_fixed_then_scaled=separate_ranks,
                numerator_coefficient_ranks=[matrix.rank() for matrix in powers.values()],
                reference_exchange_rank=numerator.subs(phase, 1).rank(),
                nonzero_exchange_entries=[
                    [i, j, str(sp.factor(numerator[i, j]/phase))]
                    for i, j in np.ndindex(numerator.shape) if numerator[i, j]
                ])
    return record, numerator/phase


def calculate():
    flat = flavor.flat
    gauge, adjoint, _, color, weak, y = flat.compact_chart()
    records = flat.vacuum.native.build_records()
    x, dual, mesons, fundamental, spaces, (hessian, orbit, weights) = flavor.projected_space(
        gauge, adjoint, color, weak, y, records
    )
    flavor.check_old_cubic(spaces)
    phase = sp.Symbol('z_T', nonzero=True)
    sources = flavor.colored_sources(
        x, mesons, fundamental, spaces, orbit, weights, adjoint, weak, y,
        flavor.internal_maps(x, dual, y), records, flat.read(flavor.OUT)['completion'],
        triplet_coefficient=phase, include_higgs=True,
    )
    triplet_mesons = list(mesons)
    triplet_mesons[1] = np.zeros_like(mesons[1])
    variation = flat.split_exotic_hessian(x, y, triplet_mesons, records, orbit)
    flattened = adjoint.reshape(78, -1)
    metric = sp.diag(sp.eye(405), sp.Matrix(flattened @ flattened.T))
    channels = {}
    exchange = {}
    for name, (rows, cols, left, right) in sources.items():
        metrics = (metric.extract(rows.tolist(), rows.tolist()),
                   metric.extract(cols.tolist(), cols.tolist())) if name.startswith('QQQHd') else None
        channels[name], exchange[name] = exchange_pencil(
            sp.Matrix(hessian[np.ix_(rows, cols)]), sp.Matrix(variation[np.ix_(rows, cols)]),
            left, right, phase, metrics=metrics,
        )
    for name in ('QQQL', 'UcUcDcEc'):
        assert not channels[name]['nonzero_exchange_entries']
        assert channels[name]['separate_contraction_ranks_fixed_then_scaled'] == [
            [[0, 0], [0, 0]], [[0, 0], [0, 0]],
        ]
    first, second = (exchange[name] for name in ('QQQHd_Q1Q2', 'QQQHd_Q2Q3'))
    coefficients = {
        (i, j, k): sp.factor(first[k, 3*i+j]+second[i, 3*j+k])
        for i, j, k in np.ndindex(3, 3, 3)
    }
    witness = coefficients[(0, 2, 2)]
    assert witness == sp.Rational(4112, 813)*phase
    nonzero_count = sum(value != 0 for value in coefficients.values())
    assert nonzero_count == 14
    down_yukawa = sp.Matrix(flat.read(flavor.OUT)['completion']['down_matrix'])
    assert down_yukawa.det() == -108
    return dict(status='PASS', channels=channels,
                QQQHd_summed_ordered_flavor_witness=dict(indices=[0, 2, 2], coefficient=str(witness)),
                QQQHd_summed_nonzero_count=nonzero_count,
                down_yukawa_invertible_for_holomorphic_field_redefinition=True)


if __name__ == '__main__':
    result = json.dumps(calculate(), indent=2) + '\n'
    (flavor.flat.ROOT / OUT).write_text(result, encoding='utf-8')
    print(result)
