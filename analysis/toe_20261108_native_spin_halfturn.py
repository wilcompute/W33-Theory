"""Transport the exact Pass10956 Spin(9) half-turn to the native signed cubic."""

from collections import Counter
from itertools import product
import hashlib
import json
from pathlib import Path

import sympy as sp

import toe_20261108_exact_signed_cubic_stabilizer as cubic
import w33_pass10950_clock_albert_lorentz_spinor as albert

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data/toe_20261108_native_spin_halfturn.json'


def pullback(terms, transformation):
    rows = [list(transformation.row(i).todok().items()) for i in range(27)]
    coefficients = Counter()
    for (a, b, c), sign in terms.items():
        for ((_, i), x), ((_, j), y), ((_, k), z) in product(rows[a], rows[b], rows[c]):
            coefficients[tuple(sorted((i, j, k)))] += sign * x * y * z
    return {key: sp.expand(value) for key, value in coefficients.items() if sp.expand(value) != 0}


def halfturn():
    model = albert.build_clock_albert()
    frame = [model['idx'][root] for root in model['G']]
    eye = sp.eye(27)
    unit = sum((eye[:, i] for i in frame), sp.zeros(27, 1))
    c, e2, e3 = (eye[:, i] for i in frame)
    s = e2 - e3
    u = unit - c
    operators = [
        sp.Matrix([[sp.Rational(value) for value in row] for row in op]).T
        for op in model['prod']
    ]

    def left(vector):
        return sum((value * op for value, op in zip(vector, operators) if value), sp.zeros(27))

    trace = sp.Matrix([[sp.trace(op) for op in operators]])

    def pairing(x, y):
        return (trace * left(x) * y)[0]

    Lc = left(c)
    # Use the same canonical nullspace and first spatial axis as Pass10956.
    basis = [sp.Matrix(v) for v in albert.nullspace(Lc.tolist())]
    for axis in basis:
        spatial = axis - pairing(axis, u) / pairing(u, u) * u
        z = spatial - pairing(spatial, s) / pairing(s, s) * s
        if pairing(z, z) != 0:
            z *= sp.ilcm(*(value.q for value in z))
            break
    else:
        raise AssertionError('No nonzero second spatial axis')

    # Pass10956 works with the integer Jordan multiplication.
    denominator = sp.ilcm(*(value.denominator for value in model['prod'].flat))
    Ls, Lz = left(s), left(z)
    D = denominator**2 * (Ls * Lz - Lz * Ls)
    spin = 4 * Lc * (eye - Lc)
    vector = eye - spin
    assert spin**2 == spin and spin.trace() == 16
    assert D * spin == spin * D and D**2 * spin == -4 * spin
    assert D**3 * vector == -16 * D * vector and D.rank() == 18
    # At angle pi in the vector plane, the spinor has angle pi/2.
    rotation = D * spin / 2 + (eye + D**2 / 8) * vector
    chirality = 2 * Ls * spin
    assert chirality**2 == spin and chirality.trace() == 0
    assert rotation * chirality == -chirality * rotation
    assert rotation**2 == eye - 2 * spin and rotation**4 == eye
    assert rotation * c == c and rotation * s == -s and rotation * z == -z
    assert rotation.eigenvals() == {1: 9, -1: 2, sp.I: 8, -sp.I: 8}
    transport = sp.zeros(27)
    for j, column in enumerate(model['complex_basis']):
        for root, value in column.items():
            transport[model['root_to_i27'][root], j] = sp.Rational(value.a) + sp.I * sp.Rational(value.b)
    inverse = transport.inv()

    def native(matrix):
        return sp.SparseMatrix((transport * matrix * inverse).applyfunc(sp.expand))

    return native(rotation), native(spin), native(chirality), native(D)


def matrix_entries(matrix):
    return [[i, j, str(value)] for (i, j), value in sorted(matrix.todok().items())]


def calculate():
    rotation, spin, chirality, D = halfturn()
    terms = cubic.signed_terms(cubic.CUBIC)
    assert rotation.H * rotation == sp.eye(27)
    assert len(rotation.todok()) == 27
    assert pullback(terms, rotation) == terms
    assert D.H == -D
    rows = cubic.coefficient_rows(terms, 27)
    coefficients = {27 * i + j: value for (i, j), value in D.todok().items()}
    cubic.verify_basis(rows, [coefficients])
    lifted = sp.kronecker_product(rotation, sp.eye(3))
    vacuum_path = ROOT / 'data/toe_20261108_three_copy_cubic_vacuum.json'
    vacuum = json.loads(vacuum_path.read_text(encoding='utf-8'))
    X = sp.zeros(81, 3)
    for j, support in enumerate(vacuum['chosen_supports']):
        for i in support:
            X[i, j] = 1
    overlap = X.H * lifted * X / 3
    defect = lifted * X - X * overlap
    assert sp.trace(defect.H * defect) == 8
    # The internal reduction removes both family and species unitaries.
    flatten = sp.Matrix(27, 9, lambda i, j: X[3*i + j//3, j%3])
    density = flatten * flatten.H
    moved_density = rotation * density * rotation.H
    density_difference = moved_density - density
    norm_squared = sp.trace(density_difference.H * density_difference)
    assert norm_squared == 0 and flatten.H * flatten == sp.eye(9)
    # If compensation exists, this forced operator must factor on family/species.
    forced = flatten.H * rotation * flatten
    assert rotation * flatten == flatten * forced
    def schmidt_rank(operator):
        return sp.Matrix(9, 9, lambda i, j: operator[3*(i//3) + j//3, 3*(i%3) + j%3]).rank()

    power_ranks = [schmidt_rank(forced**power) for power in range(4)]
    assert power_ranks == [1, 2, 2, 2]
    local_state = sp.Matrix([1, 1, 0])
    output = (forced * sp.kronecker_product(local_state, local_state)).reshape(3, 3)
    assert (output * output.H / 4).eigenvals() == {sp.Rational(1, 2): 2, 0: 1}
    inputs = [ROOT / cubic.CUBIC, albert.P.CANON, albert.P.META, vacuum_path,
              Path(albert.__file__), Path(albert.P.__file__)]
    return dict(
        status='EXACT_NATIVE_ALBERT_HALF_TURN_AND_VACUUM_COMPATIBILITY_TEST',
        coordinate_order='native i27, with family fastest in the 81-coordinate lift',
        frame=sorted(terms)[0],
        rotation=matrix_entries(rotation),
        infinitesimal_generator=matrix_entries(D),
        peirce_spinor_projector=matrix_entries(spin),
        chirality_on_spinor_and_zero_elsewhere=matrix_entries(chirality),
        eigenvalue_multiplicities={'+1': 9, '-1': 2, '+i': 8, '-i': 8},
        signed_cubic_coefficients_preserved=len(terms),
        rotation_order=4,
        chirality_exchanged=True,
        species_projection_overlap=matrix_entries(overlap),
        species_projection_defect_squared=8,
        internal_density_defect_squared=int(norm_squared),
        forced_family_species_operator=matrix_entries(forced),
        forced_operator_schmidt_ranks_for_powers_0_to_3=power_ranks,
        example_product_input='(e0+e1) tensor (e0+e1), normalized by 2',
        example_output_reduced_density_eigenvalues=['1/2', '1/2', '0'],
        scope='The half-turn preserves the action but moves the selected vacuum. The internal density is preserved, but each nonidentity power induces an operator of Schmidt rank two on the family/species grid. Independent family and species unitaries cannot compensate it.',
        input_sha256={path.relative_to(ROOT).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
                      for path in inputs},
    )


if __name__ == '__main__':
    result = calculate()
    OUT.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(result['status'], result['internal_density_defect_squared'])
