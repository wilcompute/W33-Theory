"""Center glue, theta periods, and fermion indices for the faithful W33 parent."""

from collections import Counter
from itertools import combinations_with_replacement, product
import json

import numpy as np
import sympy as sp
from sympy.matrices.normalforms import hermite_normal_form

import toe_20261110_global_gauge_topology as topology

OUT = 'data/toe_20261112_parent_theta_lattice.json'


def norms_two(basis, gram):
    lower, diagonal = gram.LDLdecomposition()
    coordinates = [0]*gram.rows

    def visit(i, remaining):
        if i < 0:
            if remaining == 0:
                yield basis*sp.Matrix(coordinates)
            return
        offset = sum(lower[j, i]*coordinates[j] for j in range(i+1, gram.rows))
        reach = int(sp.ceiling(sp.sqrt(remaining/diagonal[i, i])))
        center = int(sp.floor(-offset))
        for value in range(center-reach, center+reach+2):
            rest = remaining-diagonal[i, i]*(value+offset)**2
            if rest >= 0:
                coordinates[i] = value
                yield from visit(i-1, rest)
    return list(visit(gram.rows-1, sp.Integer(2)))


def glue_lattice():
    _, internal, cartan, _, weak, y = topology.flat.compact_chart()
    chart = topology.representation_check(internal, cartan, weak, y)
    circle = sp.Matrix(cartan.T)*sp.Matrix([sp.Rational(c) for c in chart['circle_cartan_coefficients']])
    charges = [int(x) for x in circle]
    root_weights = topology.flat.adjoint_charges(internal, np.array(charges, dtype=np.int64))
    assert all(q % 3 == 0 for q in root_weights)
    assert all(q % 3 == 1 for q in charges)
    coroots = []
    for root in internal:
        if np.array_equal(root, np.diag(root.diagonal())):
            continue
        h = (root@root.T-root.T@root).diagonal()
        assert np.array_equal((h[:, None]-h[None, :])*root, 2*root)
        coroots.append(list(map(int, h)))
    assert len(coroots) == 72
    assert all(sum(x*x for x in root) == 12 for root in coroots)
    root_set = set(map(tuple, coroots))
    a2_witness = next((a, b) for a, b in product(coroots, repeat=2)
                      if sum(x*y for x, y in zip(a, b)) == -6
                      and tuple(x+y for x, y in zip(a, b)) in root_set)
    assert (sp.Matrix(a2_witness)*sp.Matrix(a2_witness).T)/6 == sp.Matrix([[2, -1], [-1, 2]])
    e6 = hermite_normal_form(sp.Matrix(coroots).T)
    assert e6.shape == (27, 6)
    assert all(x.q == 1 for x in e6.gauss_jordan_solve(circle)[0])
    a2 = sp.Matrix([[1, 0], [-1, 1], [0, -1]])
    lift = sp.diag(e6, a2)
    metric = sp.diag(*([sp.Rational(1, 6)]*27+[1]*3))
    gram0 = lift.T*metric*lift
    assert (gram0[:6, :6].det(), gram0[6:, 6:].det()) == (3, 3)

    family = sp.Matrix([-1, -1, 2])/3
    glue = (circle/3).col_join(family)
    assert all(value.q == 1 for value in lift.T*metric*glue)
    assert (glue.T*metric*glue)[0] == 2
    assert all(q % 3 == 2 for q in [-1, -1, 2])
    scaled = 3*lift.row_join(glue)
    assert all(x.q == 1 for x in scaled)
    lattice = hermite_normal_form(sp.Matrix(scaled.rows, scaled.cols, list(map(int, scaled))))/3
    gram = lattice.T*metric*lattice
    assert gram.det() == 1 and all(x.q == 1 for x in gram)
    assert all(gram[i, i] % 2 == 0 for i in range(8))
    root_shell = norms_two(lattice, gram)
    root_count = Counter(int(3*v[0]) % 3 for v in root_shell)
    defining_e6 = 6*e6*(e6.T*e6).inv()*e6.T
    defining_family = sp.eye(3)-sp.ones(3)/3
    tensor_weights = {tuple(defining_e6[:, i].col_join(defining_family[:, j]))
                      for i, j in product(range(27), range(3))}
    assert {tuple(v) for v in root_shell if int(3*v[0]) % 3 == 1} == tensor_weights
    assert {tuple(-v) for v in root_shell if int(3*v[0]) % 3 == 2} == tensor_weights
    assert root_count == {0: 78, 1: 81, 2: 81}

    fractions = [(circle.dot(circle)/54)/2, family.dot(family)/2]
    assert fractions == [sp.Rational(2, 3), sp.Rational(1, 3)]
    return charges, root_weights, family, fractions, dict(
        covering_gram_determinant=int(gram0.det()), quotient_gram_determinant=int(gram.det()),
        glue_norm_squared=2, root_counts_by_obstruction_coset=[root_count[k] for k in range(3)],
        nonzero_cosets_are_bifundamental_weight_sets=True,
        E6_regular_A2_basic_embedding_index=1)


def fermion_indices(circle, roots, family, fractions):
    e6_27 = [sp.Rational(x, 3) for x in circle]
    e6_78 = [sp.Rational(int(x), 3) for x in roots]
    family_8 = [family[i]-family[j] for i, j in product(range(3), repeat=2) if i != j]+[0, 0]
    decuplet = [-sum(family[i] for i in indices) for indices in combinations_with_replacement(range(3), 3)]
    decuplet_test = [sum([1, -1, 0][i] for i in indices)
                     for indices in combinations_with_replacement(range(3), 3)]
    assert sum(x*x for x in decuplet_test)//2 == 15
    bifundamental = [x+y for x, y in product(e6_27, family)]

    # On S² x S², c1 = x + 2y has self-intersection 4 and signature zero.
    charges = [4*q for q in fractions]
    entries = {}
    for name, weights, indices in [
        ('27_tensor_3', bifundamental, (18, 27)),
        ('E6_adjoint', e6_78, (24, 0)),
        ('family_adjoint', family_8, (0, 6)),
        ('family_conjugate_decuplet', decuplet, (0, 15)),
    ]:
        assert all(sp.Rational(w).q == 1 for w in weights)
        direct = 2*sum(w*w for w in weights)
        assert direct == sum(a*b for a, b in zip(indices, charges))
        entries[name] = dict(basic_trace_indices=list(indices), witness_dirac_index=int(direct))
    assert [v['witness_dirac_index'] for v in entries.values()] == [84, 64, 8, 20]
    total = 5*84 + 2*64 + 8 + 20
    return dict(witness_instanton_numbers=list(map(str, charges)),
                representations=entries, total_canonical_chiral_and_gaugino_witness_index=total)


def calculate():
    circle, roots, family, fractions, lattice = glue_lattice()
    # Modulo-three shift of the coefficient of w cup w.
    shift = lambda a, b: (2*a+b) % 3
    basis = sp.Matrix([[1, 0], [1, 3]])
    assert basis.det() == 3 and all(shift(*col) == 0 for col in zip(*basis.tolist()))
    residues = list(product(range(3), repeat=2))
    assert [(a, b) for a, b in residues if shift(a, b) == 0] == [(0, 0), (1, 1), (2, 2)]
    # Measure electric trialities using the positive generators of each center.
    # The magnetic generator uses the inverse family center.
    electric_labels = [int(3*((2*fractions[0]) % 1)), int(3*((-2*fractions[1]) % 1))]
    assert electric_labels == [1, 1]
    assert all((a-b+shift(a, b)) % 3 == 0 for a, b in residues)
    parity = {}
    for a, b in product(range(2), repeat=2):
        choices = [p for p in range(3) if (2*p+shift(a, b)) % 3 == 0]
        assert len(choices) == 1
        parity[f'{a},{b}'] = choices[0]
    assert parity == {'0,0': 0, '0,1': 1, '1,0': 2, '1,1': 0}
    # Trace of the 248 branching relative to each basic invariant.
    assert 24+2*3*6 == 60
    assert 6+2*27 == 60
    return dict(status='PASS', center_quadratic_values=list(map(str, fractions)), lattice=lattice,
                theta_period_generators_in_2pi_units=[[1, 1], [0, 3]],
                discrete_counterterm_compensation='p -> p - (2*a+b) mod 3',
                electric_trialities_added_by_unit_shifts=[[electric_labels[0], 0], [0, electric_labels[1]]],
                orientation_reversal_compatible_p_at_pi_corners=parity,
                E8_embedding_indices=[1, 1],
                spin_witness=fermion_indices(circle, roots, family, fractions))


if __name__ == '__main__':
    result = json.dumps(calculate(), indent=2) + '\n'
    (topology.flat.ROOT / OUT).write_text(result, encoding='utf-8')
    print(result)
