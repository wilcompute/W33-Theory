"""Regression against characteristic-zero and discrete-minimum overreads."""
import sys
from functools import lru_cache
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'analysis'))
from w33_pass11980_heisenberg_fixed_holonomies import certificate


@lru_cache(None)
def result(root=0):
    return certificate(root)


def test_integral_coinvariants_and_explicit_order_nine_gauge_classes():
    c = result()
    assert c['coinvariant_torsion_invariant_factors'] == [3, 9, 9]
    assert c['coinvariant_free_rank'] == 0
    old = c['prior_cubic_building_chain_equivalence']
    assert abs(old['H1_transport_determinant']) == 1
    assert old['integral_H27_equivariance_checked']
    p = c['explicit_holonomies_and_matter_probe']
    assert p['sector_counts_by_order'] == {'1': 1, '3': 26, '9': 216}
    assert len(p['order9_witness_link_phases_in_units_2pi_over9']) == 135


def test_modular_invariants_are_not_coinvariants_or_complex_invariants():
    c = result()
    assert c['finite_field_dimensions']['3'] == {'homology_invariants': 4, 'homology_coinvariants': 3}
    assert all(c['finite_field_dimensions'][str(p)] == {'homology_invariants': 0, 'homology_coinvariants': 0} for p in (2, 5, 7))
    assert c['F3_radical_dimensions'] == [64, 61, 55, 43, 32, 19, 10, 3, 0]
    assert c['F3_center_nilpotent_power_ranks'] == [40, 16, 0]


def test_all_complex_character_values_agree_with_toe82():
    c = result()
    a, b = (np.array(x) for x in c['H27_generator_integral_H1_actions'].values())
    assert np.trace(a) == np.trace(b) == -2
    center = a @ b @ np.linalg.matrix_power(a,2) @ np.linalg.matrix_power(b,2)
    assert np.trace(center) == -8
    assert np.array_equal(np.linalg.matrix_power(center,3), np.eye(64,dtype=int))


def test_conjugate_sector_spectra_and_continuous_stability():
    p = result()['explicit_holonomies_and_matter_probe']
    spectra = {tuple(r['coefficients']): r['single_particle_spectrum'] for r in p['all_243_sector_spectra']}
    for (a,b,c), values in spectra.items():
        assert np.allclose(values, spectra[(-a%3,-b%9,-c%9)], atol=1e-11, rtol=0)
    rows = p['uniform_hopping_finite_free_fermion_fillings']
    assert rows['9']['continuous_flat_torus_audit']['negative_curvature_count'] == 8
    assert rows['13']['continuous_flat_torus_audit']['negative_curvature_count'] == 12
    stable = rows['18']['continuous_flat_torus_audit']
    assert stable['max_gradient'] < 1e-11
    assert stable['fermi_gap'] > 2.77
    assert min(stable['full_64_flat_direction_hessian_eigenvalues']) > 0.0005


def test_second_spanning_tree_gives_same_intrinsic_answers():
    c, other = result(), result(13)
    for key in ('coinvariant_torsion_invariant_factors','finite_field_dimensions',
                'F3_radical_dimensions','F3_center_nilpotent_power_ranks'):
        assert c[key] == other[key]
    for n in ('1','9','13','14','18','26'):
        a = c['explicit_holonomies_and_matter_probe']['uniform_hopping_finite_free_fermion_fillings'][n]
        b = other['explicit_holonomies_and_matter_probe']['uniform_hopping_finite_free_fermion_fillings'][n]
        assert abs(a['minimum_free_energy_at_zero_temperature']-b['minimum_free_energy_at_zero_temperature']) < 1e-10
        assert a['minimizer_count'] == b['minimizer_count']
        if n == '18':
            assert min(b['continuous_flat_torus_audit']['full_64_flat_direction_hessian_eigenvalues']) > 0
