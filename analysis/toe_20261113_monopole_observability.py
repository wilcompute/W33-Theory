"""Exact matching controls at the W33 monopole channel dimensions."""

import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
STEM = 'toe_20261113_monopole_'


def cycle_control(heavy, light, winding, isolated):
    """Feed a cycle through one light port and isolate chosen winding states."""
    size = heavy + light
    linked = list(range(isolated, heavy + 1))
    successor = list(range(size))
    for source, target in zip(linked, linked[1:] + linked[:1]):
        successor[source] = target

    # Each column of B is a partial permutation with a unit-modulus phase.
    # The phase drops out of the observation norm, so integer matrices suffice.
    unitary = sp.zeros(size)
    for source, target in enumerate(successor):
        unitary[target, source] = 1
    assert unitary.T * unitary == sp.eye(size)
    heavy_map = unitary[:heavy, :heavy]
    observation = unitary[heavy:, :heavy]
    propagated = observation
    gramian = sp.zeros(heavy)
    for _ in range(heavy):
        gramian += propagated.T * propagated
        propagated = propagated * heavy_map
    assert gramian == sp.diag(*([0] * isolated + [1] * (heavy - isolated)))

    # In the outgoing-to-incoming relation, every visit to a winding
    # heavy output contributes z^(-1) when solving the heavy constraint.
    z = sp.Symbol('z')
    exterior = [z] * winding + [sp.S.One] * (heavy - winding)
    reflection = sp.zeros(light)
    for port in range(heavy, size):
        amplitude = sp.S.One
        target = successor[port]
        while target < heavy:
            amplitude /= exterior[target]
            target = successor[target]
        reflection[target - heavy, port - heavy] = amplitude
    inverse_determinant = sp.cancel(1 / reflection.det())
    assert inverse_determinant == z**(winding - isolated)
    assert all(successor[i] == i and exterior[i] == z for i in range(isolated))
    return dict(
        heavy=heavy,
        light=light,
        winding_mass_channels=winding,
        heavy_compression_norm=1,
        heavy_unit_singular_values=heavy - 1,
        observation_gramian_rank=heavy - isolated,
        exact_zero_mode_multiplicity_at_z_1=isolated,
        physical_reflection_determinant=str(inverse_determinant),
        reflection_winding=winding - isolated,
    )


def calculate():
    ledger = json.loads((ROOT / 'data' / f'{STEM}grand_spin.json').read_text())
    controls = {}
    for name, entries in ledger['winding_charge_blocks'].items():
        dimensions = {
            (row['heavy_each_direction'], row['light_each_direction'], row['winding_multiplicity'])
            for row in entries
        }
        assert len(dimensions) == 1
        heavy, light, winding = dimensions.pop()
        controls[name] = [
            cycle_control(heavy, light, winding, isolated)
            for isolated in range(winding + 1)
        ]
    return dict(status='PASS', scope='exact exterior controls with fixed unitary boundaries',
                controls=controls)


if __name__ == '__main__':
    result = json.dumps(calculate(), indent=2) + '\n'
    (ROOT / 'data' / f'{STEM}observability.json').write_text(result, encoding='utf-8')
    print(result)
