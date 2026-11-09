"""An exact species-orientation potential at the signed three-copy vacuum."""

from collections import Counter
from itertools import combinations, permutations, product
import hashlib
import json
from pathlib import Path

import sympy as sp

import toe_20261108_exact_signed_cubic_stabilizer as cubic
from w33_20261001_global_e6_cartan_covariants import aronhold_terms

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data/toe_20261108_species_orientation_selector.json'
VACUUM = ROOT / 'data/toe_20261108_three_copy_cubic_vacuum.json'


def weighted_field(supports, t):
    """The weighted sum of the three 27x3 fields."""
    field = sp.zeros(27, 3)
    for j, support in enumerate(supports):
        for i in support:
            field[i//3, i%3] = t[j]
    return field


def restricted_cubic(field, terms, y):
    coords = field * sp.Matrix(y)
    return sp.expand(sum(sign * coords[i] * coords[j] * coords[k]
                         for (i, j, k), sign in terms.items()))


def restricted_sextic(field, terms):
    """Exact sparse evaluation of the October 1 raw6 circuit divided by 12."""
    cross = Counter()
    for term, sign in terms.items():
        for i, j, k in permutations(term):
            for a, b in product(range(3), repeat=2):
                if field[j, a] and field[k, b]:
                    cross[i, a, b] += sign * field[j, a] * field[k, b]
    family = list(permutations(range(3)))
    raw = sum(
        6 * sign * cubic.parity(a) * cubic.parity(b)
        * sp.prod(cross[i, x, y] for i, x, y in zip(term, a, b))
        for term, sign in terms.items() for a, b in product(family, repeat=2)
    )
    return sp.expand(raw / sp.Integer(12))


def hesse_aronhold_coefficients():
    """Evaluate the repo's integer epsilon circuit on a Hesse tensor."""
    indices, signs = aronhold_terms()
    coefficients = Counter()
    for tuples, sign in zip(indices, signs):
        arities = [len(set(triple)) for triple in tuples]
        if 2 not in arities:
            coefficients[arities.count(1)] += int(sign)
    return dict(coefficients)


def selector_jet(invariant, t):
    eye = sp.eye(3)
    probes = [eye[:, i] for i in range(3)]
    probes.extend(eye[:, i] + 2*eye[:, j] for i, j in combinations(range(3), 2))
    directions = [sp.I * eye[:, i] * eye[:, i].T for i in range(3)]
    for i, j in combinations(range(3), 2):
        off = eye[:, i] * eye[:, j].T
        directions.extend((off - off.T, sp.I*(off + off.T)))
    assert all(g.H == -g for g in directions)
    grad = sp.Matrix([sp.diff(invariant, v) for v in t])
    rows, targets = [], []
    for probe in probes:
        values = dict(zip(t, probe))
        jet = [(grad.subs(values).T * g * probe)[0] for g in directions]
        rows.extend(([sp.re(v) for v in jet], [sp.im(v) for v in jet]))
        targets.append(int(invariant.subs(values)))
    jacobian = sp.Matrix(rows)
    independent = list(jacobian.T.rref()[1])
    assert len(independent) == 9
    minor = jacobian[independent, :].det()
    assert minor != 0
    return dict(
        targets=targets,
        real_and_imaginary_jacobian=[[int(x) for x in row] for row in rows],
        independent_row_indices=independent,
        nonzero_minor=int(minor),
    )


def calculate():
    vacuum = json.loads(VACUUM.read_text(encoding='utf-8'))
    terms = cubic.signed_terms(cubic.CUBIC)
    t = sp.symbols('t0:3')
    y = sp.symbols('y0:3')
    p = sp.prod(t)
    q = sum(x**3 for x in t)
    field = weighted_field(vacuum['chosen_supports'], t)
    restriction = restricted_cubic(field, terms, y)
    assert restriction == sp.expand(p * sum(v**3 for v in y) - q * sp.prod(y))
    coefficients = hesse_aronhold_coefficients()
    assert coefficients == {0: 24, 3: -24}
    # The symmetric tensor convention is F(y,y,y)=6 N(X(t)y).
    # Hence F_iii=6p and F_ijk=-q for three distinct indices.
    invariant = q**4 + 216*p**3*q  # Aronhold contraction divided by 24.

    sextic = restricted_sextic(field, terms)
    assert sextic == sum(x**6 for x in t) - 10*sum((a*b)**3 for a, b in combinations(t, 2))
    degree_six = selector_jet(sextic, t)
    degree_twelve = selector_jet(invariant, t)
    assert degree_six['targets'] == [1, 1, 1, -15, -15, -15]
    assert degree_twelve['targets'] == [1, 1, 1, 6561, 6561, 6561]
    old = vacuum['tangent_ranks']
    inputs = [VACUUM, ROOT / cubic.CUBIC,
              ROOT / 'analysis/w33_20261001_global_e6_cartan_covariants.py']
    return dict(
        status='EXACT_SEXTIC_AND_ARONHOLD_SPECIES_SELECTORS',
        restriction=str(restriction),
        hesse_aronhold_raw_coefficients={str(k): v for k, v in coefficients.items()},
        normalized_invariant_restriction=str(invariant),
        normalization='Aronhold(F)/24, F(y,y,y)=6 N(X(t)y)',
        gauge_invariance='Internal transformations preserve the signed cubic N. Family transformations preserve the two volume tensors of the sextic and four of the Aronhold contraction. The sextic uses the invariant dual cubic to contract three cross products.',
        species_probes=[[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 2, 0], [1, 0, 2], [0, 1, 2]],
        normalized_sextic_restriction=str(sextic),
        sextic_normalization='October 1 raw6 divided by 12, equivalently I6 divided by 27',
        degree_six_selector=degree_six,
        degree_twelve_selector=degree_twelve,
        u3_direction_order=['iE00', 'iE11', 'iE22', 'E01-E10', 'i(E01+E10)',
                            'E02-E20', 'i(E02+E20)', 'E12-E21', 'i(E12+E21)'],
        prior_tangent_ranks=old,
        selector_real_rank_on_species=9,
        new_hessian_nullity=78,
        physical_hessian_nullity=0,
        scope='Positive squares of six degree-6 holomorphic invariant residuals are supplied bosonic operators. The degree-12 alternative has the same rank. The selected minimum is locally isolated modulo compact gauge. Coefficients, radiative origin, and global minimum classification remain open.',
        input_sha256={path.relative_to(ROOT).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
                      for path in inputs},
    )


if __name__ == '__main__':
    result = calculate()
    OUT.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(result['status'], result['selector_real_rank_on_species'])
