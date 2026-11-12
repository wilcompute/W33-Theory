"""Grand-spin-zero channel closure for the canonical W33 hedgehog core."""

from collections import Counter
import json

import numpy as np
import sympy as sp

import toe_20261110_monopole_core_channels as core
import toe_20261113_monopole_heavy_phase_flow as flow


OUT = 'data/toe_20261113_monopole_grand_spin.json'


def angular_tensors():
    sigma1 = sp.Matrix([[0, 1], [1, 0]])
    sigma2 = sp.Matrix([[0, -sp.I], [sp.I, 0]])
    sigma3 = sp.diag(1, -1)
    singlet = sp.Matrix([0, 1, -1, 0])
    vector = sp.kronecker_product(sigma3, sp.eye(2))*singlet
    for sigma in (sigma1, sigma2, sigma3):
        assert (sp.kronecker_product(sigma, sp.eye(2))
                +sp.kronecker_product(sp.eye(2), sigma))*singlet == sp.zeros(4, 1)
    angular_gauge = (sp.kronecker_product(sigma2, sigma1)
                     -sp.kronecker_product(sigma1, sigma2))/2
    assert angular_gauge*singlet == sp.I*vector
    assert angular_gauge*vector == -sp.I*singlet
    isospin = sp.kronecker_product(sp.eye(2), sigma3)
    assert isospin*singlet == -vector and isospin*vector == -singlet
    return dict(radial_basis=['S', 'sigma_dot_rhat S'],
                kinetic_offdiagonal=['-i (d/dr + K/r)', '-i (d/dr - K/r)'],
                mass_angle_map='M0 tensor I - M1 tensor sigma1',
                regular_origin_radial_orders=[1, 2], singular_radial_order=-1)


def calculate():
    flat = core.flat
    gauge, adjoint, cartan, color, weak, y = flat.compact_chart()
    five = core.topology.representation_check(adjoint, cartan, weak, y)['fundamental5_chart']
    root, magnetic = core.monopole_root(adjoint, five)
    assert not root[:2, :].any() and not root[:, :2].any()
    fixed = flat.read(core.OUT)['fixed_torus_sector']['fixed_internal_adjoint_slots']
    selected = adjoint[fixed]
    constraints = np.concatenate(
        [(selected @ g-g @ selected).reshape(len(fixed), -1)
         for g in (root, root.T, color[0], color[0].T)], axis=1
    )
    assert len(fixed)-flat.vacuum.rank(constraints) == 6
    assert Counter(map(int, magnetic)) == {-1: 6, 0: 15, 1: 6}
    assert Counter(map(int, flat.adjoint_charges(adjoint, magnetic))) == {
        -2: 1, -1: 20, 0: 36, 1: 20, 2: 1,
    }
    generators = np.stack(
        [(g @ g.T-g.T @ g).diagonal() for g in (color[0], color[1], weak)]+[y], axis=1
    )
    step = generators[five[0]]-generators[five[3]]
    magnetic_coefficients = sp.Matrix(generators).gauss_jordan_solve(sp.Matrix(magnetic))[0]

    def magnetic_charge(weight):
        value = sp.Matrix(list(weight)).dot(magnetic_coefficients)
        assert value.is_integer
        return int(value)

    def perpendicular(weight, charge):
        return tuple(map(int, 2*np.array(weight)-charge*step))

    def magnetic_weights(weights, sign):
        return Counter(perpendicular(w, sign) for w in weights if magnetic_charge(w) == sign)

    chiral = np.stack([flat.field_charges(adjoint, h) for h in generators.T], axis=1)
    gaugino = np.stack([flat.adjoint_charges(adjoint, h) for h in generators.T], axis=1)
    ultraviolet = np.concatenate([chiral, gaugino])
    blocks = magnetic_weights(ultraviolet, 1)
    assert blocks == magnetic_weights(ultraviolet, -1)
    assert sum(blocks.values()) == 130 and len(blocks) == 14
    assert sum(magnetic_weights(chiral[:405], 1).values()) == 90
    assert sum(magnetic_weights(chiral[405:], 1).values()) == 20
    assert sum(magnetic_weights(gaugino, 1).values()) == 20

    light = core.vectors.flavor.projected_space(
        gauge, adjoint, color, weak, y, flat.vacuum.native.build_records()
    )[4]
    # Nonzero unbroken gaugino weights are exactly the color and weak roots.
    light_gaugino = gaugino[(gaugino[:, -1] == 0) & np.any(gaugino[:, :3], axis=1)]
    assert len(light_gaugino) == 8
    light_weights = [weight for weight, lifts in light.items() for _ in lifts]
    light_weights.extend(map(tuple, light_gaugino.tolist()))
    plus, minus = (magnetic_weights(light_weights, sign) for sign in (1, -1))
    assert sum(plus.values()) == sum(minus.values()) == 16
    assert all(blocks[weight] for weight in plus.keys() | minus.keys())

    winding = {}
    for row in flat.read(flow.OUT)['monopole_channel_count']:
        weights = Counter(perpendicular(np.array(lam) @ generators[five], 1)
                          for lam in row['unit_flux_weights'])
        entries = []
        for weight, multiplicity in weights.items():
            opposite = tuple(-value for value in weight)
            positive = plus[weight]+plus[opposite]
            negative = minus[weight]+minus[opposite]
            assert positive == negative
            total = blocks[weight]+blocks[opposite]
            entries.append(dict(doubled_perpendicular_weight=list(weight),
                                winding_multiplicity=multiplicity,
                                Weyl_doublets_in_paired_block=total,
                                light_each_direction=positive,
                                heavy_each_direction=total-positive,
                                minimum_unit_singular_values_in_full_heavy_compression=total-2*positive))
        winding[row['phase']] = entries
    assert all(row['Weyl_doublets_in_paired_block'] == 4 and row['light_each_direction'] == 1
               for row in winding['adjoint'])
    assert winding['triplet'][0]['Weyl_doublets_in_paired_block'] == 49
    assert winding['triplet'][0]['light_each_direction'] == 4
    return dict(status='PASS', Weyl_doublets=130, radial_coefficients_before_Nambu_doubling=260,
                angular_tensors=angular_tensors(),
                Cartan_step_weight=list(map(int, step)),
                charge_blocks=[dict(doubled_perpendicular_weight=list(key), Weyl_doublets=blocks[key],
                                    light_positive_flux=plus[key], light_negative_flux=minus[key])
                               for key in sorted(blocks)],
                winding_charge_blocks=winding)


if __name__ == '__main__':
    result = json.dumps(calculate(), indent=2) + '\n'
    (core.flat.ROOT / OUT).write_text(result, encoding='utf-8')
    print(result)
