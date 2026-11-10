"""Exact Cartan selection rules for the primitive W33 monopole's lowest waves."""

from itertools import product
import json

import numpy as np
import sympy as sp
from sympy.matrices.normalforms import hermite_normal_form

import toe_20261110_monopole_core_channels as core

OUT = 'data/toe_20261110_monopole_boundary_lattice.json'


def angular_weights():
    flat = core.flat
    gauge, internal, cartan, color, weak, y = flat.compact_chart()
    five = core.topology.representation_check(internal, cartan, weak, y)['fundamental5_chart']
    _, coroot = core.monopole_root(internal, five)
    records = flat.vacuum.native.build_records()
    _, _, _, fundamental, spaces, _ = core.vectors.flavor.projected_space(
        gauge, internal, color, weak, y, records)
    m = sp.Matrix(fundamental).gauss_jordan_solve(sp.Matrix(coroot))[0]
    alpha = tuple(map(int, fundamental[five[0]] - fundamental[five[3]]))
    gluino_wino = np.stack([flat.adjoint_charges(np.stack([*color, weak, weak.T]), h)
                           for h in fundamental.T], axis=1)
    gauginos = {tuple(map(int, w)): 1 for w in gluino_wino}
    charged = {sign: {} for sign in (-1, 1)}
    for weight, multiplicity in [(tuple(map(int, w)), len(v)) for w, v in spaces.items()] + list(gauginos.items()):
        flux = sp.Matrix(weight).dot(m)
        if flux:
            assert flux in (-1, 1) and weight not in charged[flux]
            charged[flux][weight] = multiplicity
    assert [sum(counts.values()) for counts in charged.values()] == [16, 16]
    return charged, alpha, m, sp.Matrix(fundamental).T


def add(left, right):
    return tuple(a + b for a, b in zip(left, right))


def negative(weight):
    return tuple(-a for a in weight)


def columns(weights):
    return sp.Matrix(list(weights)).T


def signed_pairs(incoming, outgoing, alpha):
    """Order the ordinary chiral pairs by a common family label, then the four holes."""
    holes = sorted(weight for weight in incoming if negative(weight) in outgoing)
    direct = sorted(set(incoming) - set(holes))
    assert len(holes) == 4 and all(incoming[w] == 1 for w in holes)
    assert len(direct) == 4 and all(incoming[w] == 3 for w in direct)
    # The outgoing down doublet contains three leptons plus one Higgsino.
    # Assign the Higgsino to the hole and the three leptons to direct pairs.
    paired = [add(w, alpha) for w in direct]
    expected = {}
    for w in paired * 3 + [negative(w) for w in holes]:
        expected[w] = expected.get(w, 0) + 1
    assert expected == outgoing
    return direct, holes, paired


def fock_witnesses(direct, holes, paired):
    # Include formal (3B,L) to distinguish the lepton and Higgsino with equal gauge charge.
    in_bl = {1: (1, 0), 2: (-1, 0), 6: (0, -1)}
    out_bl = {-4: (-1, 0), -3: (0, 1), 1: (1, 0)}
    incoming = [w + in_bl[w[-1]] for w in direct] + [w + (0, 0) for w in holes]
    particles = [w + out_bl[w[-1]] for w in paired] + [negative(w) + (0, 0) for w in holes]
    options = sorted(set(particles) | {negative(w) for w in particles})
    conserving, violating = {}, {}
    layer = {(0,) * 6: ()}
    for count in range(1, 8):
        # One witness per weight suffices. Repeated species may occupy distinct momenta.
        following = {}
        for weight, witness in layer.items():
            for option in options:
                following.setdefault(add(weight, option), witness + (option,))
        layer = following
        if count % 2 == 0:
            continue
        for initial in incoming:
            if initial in layer:
                conserving.setdefault(initial, layer[initial])
            if initial in violating:
                continue
            for delta_l in range(-count - 1, count + 2):
                target = add(initial, (0, 0, 0, 0, 3 * delta_l, delta_l))
                if delta_l and target in layer:
                    violating.setdefault(initial, {})[delta_l] = layer[target]
    assert [len(conserving[w]) for w in incoming] == [3] * 4 + [1] * 4
    assert all(len(witness) == (5 if w in incoming[:4] else 7)
               for w in incoming for witness in violating[w].values())
    assert [sorted(violating[w]) for w in incoming] == [[-1], [1], [1], [-1], [-1], [1], [-1], [-1]]
    return [dict(incoming=w, minimum_outgoing_fermions=len(conserving[w]),
                 conserving_witness=conserving[w],
                 minimum_b_minus_l_preserving_violation=len(next(iter(violating[w].values()))),
                 violating_witnesses_by_delta_l=violating[w]) for w in incoming]


def reflection(indices):
    normal = sp.zeros(16, 1)
    for index in indices:
        normal[index] = 1
    return sp.eye(16) - 2 * normal * normal.T / normal.dot(normal)


def gluing(direct, holes, paired, alpha, m):
    # Work in outgoing coordinates with a sign change on the four hole slots.
    q_in = columns(direct * 3 + holes)
    q_out = columns(paired * 3 + holes)
    particle_out = columns(paired * 3 + [negative(w) for w in holes])
    signs = sp.diag(*([1] * 12 + [-1] * 4))
    assert q_out == particle_out * signs
    assert q_in * q_in.T == particle_out * particle_out.T
    assert sum(map(sp.Matrix, direct), sp.zeros(4, 1)) == -2 * sp.Matrix(alpha)
    assert (m.T * q_in) == -sp.ones(1, 16)

    # Formal B-L on the massless free fields. It is not a UV symmetry assumption.
    b_in = sp.Matrix([[{1: 1, 2: -1, 6: 3}[w[-1]] for w in direct] * 3 + [0] * 4])
    b_out = sp.Matrix([[{-4: -1, -3: -3, 1: 1}[w[-1]] for w in paired] * 3 + [0] * 4])

    results = {}
    for name, blocks in [('collective', [range(12)]),
                         ('family', [range(4 * a, 4 * a + 4) for a in range(3)])]:
        r = sp.eye(16)
        for block in blocks:
            r *= reflection(block)
        r = signs * r
        assert r.T * r == sp.eye(16)
        assert particle_out * r == q_in
        assert b_out * r == b_in
        periods = [len(block) // 2 for block in blocks]
        denom = sp.ilcm(1, *(value.q for value in r))
        assert denom == max(periods)
        # Integrality iff the independent block sums vanish modulo the periods.
        for residues in product(*(range(period) for period in periods)):
            representative = sp.zeros(16, 1)
            for block, residue in zip(blocks, residues):
                representative[block.start] = residue
            assert all(value.q == 1 for value in r * representative) == (not any(residues))
        results[name] = dict(denominator=denom, integral_sector_quotient=periods,
                             block_indices_zero_based=[list(block) for block in blocks])
    # An integral orthogonal matrix is a signed permutation. Charge multiplicity
    # rules out such a matrix, so the denominator-two example is optimal.
    assert any(w not in set(paired + holes) | set(map(negative, paired + holes)) for w in direct)
    return results


def wino_gate(lattice, direct, paired, holes, m):
    # Index-two missing charge of the ordinary outgoing lowest-wave Fock space.
    wino, = [negative(w) for w in holes if w[-1] == w[0] == w[1] == 0]
    without_wino = paired + [negative(w) for w in holes if negative(w) != wino]
    sublattice = hermite_normal_form(columns(without_wino))
    assert sublattice.det() == 2 * lattice.det()
    character = sp.Matrix([[0, 0, sp.Rational(1, 2), -sp.Rational(3, 2)]])
    assert all(value.q == 1 for value in character * lattice)
    assert all(value % 2 == 0 for value in character * columns(without_wino))
    assert all(value % 2 == 1 for value in character * columns(direct + [wino]))
    assert hermite_normal_form(columns(paired + [wino])) == lattice
    neutral_higgs = sp.Matrix([0, 0, -1, 3])
    electric = sp.Matrix([0, 0, sp.Rational(1, 2), sp.Rational(1, 6)])
    assert neutral_higgs.dot(m) == neutral_higgs.dot(electric) == 0
    assert character.dot(neutral_higgs) % 2 == 1
    assert hermite_normal_form(columns(without_wino).row_join(neutral_higgs)) == lattice
    return dict(neutral_up_higgs_weight=list(neutral_higgs),
                neutral_higgs_vev_removes_index_two_obstruction=True,
                index_without_charged_wino=2, missing_character_mod_2=['0', '0', '1/2', '-3/2'],
                charged_wino_outgoing_weight=wino,
                no_wino_obstructs_all_12_ordinary_incoming_channels=True)



def calculate():
    charged, alpha, m, fundamental = angular_weights()
    incoming, outgoing = charged[-1], charged[1]
    direct, holes, paired = signed_pairs(incoming, outgoing, alpha)
    # The SU(5) five restricts to all five diagonal characters of S(U(3)xU(2)).
    lattice = hermite_normal_form(fundamental)
    assert lattice == hermite_normal_form(columns(incoming)) == hermite_normal_form(columns(outgoing))
    assert lattice.det() == 6
    assert all(value.q == 1 for value in m.T * lattice)
    return dict(status='PASS', cartan=['color1', 'color2', '2T3', '6Y'],
                root_step=alpha, character_lattice_hnf=lattice.tolist(),
                incoming_signed_pair_order=direct * 3 + holes,
                outgoing_particle_order=paired * 3 + [negative(w) for w in holes],
                signed_hole_indices_zero_based=list(range(12, 16)),
                fixed_dyon_single_outgoing_capacity=4,
                charged_wino_gate=wino_gate(lattice, direct, paired, holes, m),
                root_shift_single_outgoing_capacity=12,
                fixed_dyon_fock_witnesses=fock_witnesses(direct, holes, paired),
                exact_abelian_gluing=gluing(direct, holes, paired, alpha, m))


if __name__ == '__main__':
    result = json.dumps(calculate(), indent=2, default=int) + '\n'
    (core.flat.ROOT / OUT).write_text(result, encoding='utf-8')
    print(result)
