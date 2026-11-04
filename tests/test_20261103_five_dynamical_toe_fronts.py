"""Focused regression suite for six independent TOE dynamics falsifiers.

Reruns every producer and independently checks the saved certificate.
"""
from __future__ import annotations
import sys,subprocess,json,math
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
NAMES=[
"2026_11_03_csg_action_heldout",
"2026_11_03_two_slot_quantum_memory_choi",
"2026_11_03_incidence_dimension_phase_competition",
"2026_11_03_local_spin2_hamiltonian_closure",
"2026_11_03_transmutation_identifiability_firewall",
"2026_11_03_spin2_soft_ward_universality",
]
@pytest.fixture(scope='module')
def certs():
    for name in NAMES:
        p=subprocess.run([sys.executable,str(ROOT/'analysis'/(name+'.py'))],
             cwd=ROOT,capture_output=True,text=True,timeout=160)
        assert p.returncode==0,(name,p.stdout[-1400:],p.stderr[-1400:])
    data_names=NAMES.copy()
    data_names[0]='2026_11_03_causal_growth_action_competition'
    return [json.loads((ROOT/'data'/(s+'.json')).read_text(encoding='utf8'))
            for s in data_names]
def test_six_producers_replay(certs):
    assert len(certs)==6
    assert all(d['status'].startswith('PASS_') for d in certs)
def test_csg_has_exactly_normalized_predecessor_probabilities(certs):
    d=certs[0]
    assert d['normalized_exact_predecessor_posets'].startswith('4-element')
    assert len(d['scan_p_only_by_training_density'])>=10
    assert d['frozen_p']>0
    assert d['sprinkling_dimension_4_supplied']
def test_causal_density_matching_does_not_match_height(certs):
    d=certs[0]
    control=d['frozen_growth_model_holdout']
    hold=d['target_holdout']
    assert abs(control['mean_density']-hold['mean_density'])<.02
    assert abs(control['mean_height']-hold['mean_height'])>1.0
    assert all(x['effective_sample_size']<=128 for x in d['tilted_D4_BDG_like_action'])
def test_positive_two_slot_choi_causal_trace_rules(certs):
    d=certs[1]
    assert len(d['two_slot_break_responses'])==4
    for o in d['models'].values():
        assert o['min_Choi_eigenvalue']>-1e-12
        assert abs(o['Choi_trace']-4)<1e-10
        assert o['max_later_output_no_signalling_defect']<1e-11
        assert o['initial_state_trace_rule_defect']<1e-11
def test_causal_break_bypassed_only_through_memory(certs):
    for row in certs[1]['two_slot_break_responses']:
        a=row['first_reprepared_bit_a'];b=row['causal_break_reprepared_bit_b']
        assert row['Markov_final_distribution'][b]==1.
        assert row['SWAP_memory_final_distribution'][a]==1.
def test_dimension_action_parameter_bands(certs):
    d=certs[2]
    assert [v['expected_mode'] for v in d['phase_scan']]==[3,4,3,1,3,4]
    assert all(x['max_absolute_frequency_error']<.04 for x in d['phase_scan'])
    assert '-4b < a < -3b' in d['dimension_4_unique_ground_state_iff']
def test_local_spin2_constraints_close_only_in_flat_control(certs):
    d=certs[3]
    good=d['commuting_cartesian_control']
    bad=d['inhomogeneous_local_skew_derivative_defect']
    assert good['max_scalar_momentum_Poisson_bracket']<1e-11
    assert good['max_scalar_evolution_minus_momentum_divergence']<1e-11
    assert good['max_momentum_evolution_residual']<1e-11
    assert bad['max_scalar_momentum_Poisson_bracket']>.01
    assert bad['max_momentum_evolution_residual']>.01
    assert [v['remaining_configuration_modes'] for v in d['nonzero_and_zero_momentum_sector_tests']]==[6,2,2,2]
def test_transmutation_does_not_identify_cutoff(certs):
    d=certs[4]
    assert len(d['distinct_cutoff_identical_spectra'])==5
    assert len(d['RG_invariance_tests'])==6
    for row in d['distinct_cutoff_identical_spectra']:
        assert abs(row['reproduced_mass_pair'][0]-.001)<1e-10
        assert abs(row['reproduced_mass_pair'][1]-1)<1e-10
    for row in d['RG_invariance_tests']:
        assert abs(row['RG_invariant_gap']-1e-4)<1e-14
def test_soft_graviton_gauge_ward_universality(certs):
    d=certs[5]
    assert d['status']=='PASS_SOFT_SPIN2_TWO_SPECIES_GAUGE_UNIVERSALITY'
    assert len(d['nonuniversal_numeric_controls'])==4
    rows=d['nonuniversal_numeric_controls']
    assert abs(rows[0]['soft_polarization_gauge_variation'])<1e-15
    assert all(abs(x['soft_polarization_gauge_variation'])>1e-6 for x in rows[1:])
    assert 'kA' in d['symbolic_deltaS'] and 'kB' in d['symbolic_deltaS']
