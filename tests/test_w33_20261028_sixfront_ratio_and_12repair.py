"""Six-front W33 source-boundary regression tests for exact 12-loop repair."""
from analysis.w33_20261028_sixfront_ratio_and_12repair import verify

def test_unimodular_twelve_harmonic_repair_and_exact_witness():
    c=verify()['Bloch_repair']
    assert c['unimodular_stack_det']==-1
    assert c['correction_harmonics']==12 and c['previous_harmonics']==24
    assert c['kernel_equals_six_loop_all_unitary_momenta']
    assert c['frozen_witness_flux_norms']==[4112913]*5+[0]
    assert c['epsilon_001_witness_repair_cost']=='49/13000'
    assert c['old_witness_repair_cost']=='49/7800'

def test_reflection_odd_flux_parameter_and_dimensional_scope():
    c=verify()
    assert c['action_selection']['reflection_even_affine_H_theta_requires_theta']==0
    assert c['parity_dimensionality']['even_spatial_rank']==3
    assert not c['parity_dimensionality']['clock_and_physical_helicities_derived']

def test_E6_exact_charge_trace_and_basis_falsification():
    c=verify()['E6_charge_traces']
    assert c['quadratic_trace']==[[120,0],[0,72]]
    assert c['rebased_quadratic_trace']==[[120,120],[120,192]]
    assert c['rebased_diagonal_ratio']=='5/8'
    assert not c['basis_independent_physical_5_over_3']

def test_H4_dual_schlafli_and_W33_spectral_ratio():
    c=verify()['H4_600_120_sixth']
    assert c['600_cell_Schlafli']==[3,3,5]
    assert c['120_cell_Schlafli']==[5,3,3]
    assert c['edge_cell_incidence_both']==3600
    assert c['H4_root_count']==120 and c['E6_root_count']==72
    assert c['W33_prime_power_equals_5over3_only_q3']
    assert not c['causal_physical_link_established']

def test_strict_electric_gram_bound_and_limited_rotor_scope():
    c=verify()['quantum_rotor']
    assert c['electric_gram_gt_7I']
    assert c['sum_positive_cosine_weights']=='7009/28125'
    assert .2356<c['schur_lower_bound_using_previous_numerical_eigenvalue']<.2357
