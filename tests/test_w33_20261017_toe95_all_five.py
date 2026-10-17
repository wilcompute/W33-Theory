"""TOE95 five-front reproducibility tests; no physical security claim."""
from __future__ import annotations
from functools import lru_cache
import math
import pytest
from analysis import w33_20261017_toe95_allpairs as F
from analysis import w33_20261017_toe95_group32 as G
from analysis import w33_20261017_toe95_finite_population as Q
from analysis import w33_20261017_toe95_calibration as C
from analysis import w33_20261017_toe95_polar_instrument as P

@lru_cache(None)
def result(tag):
    return {'f1':F.certificate,'unit':G.certificate,
            'sampling':Q.certificate,'cal':C.certificate,
            'polar':P.certificate}[tag]()

def test_every_admissible_F1_target_pair_is_inconsistent():
    x=result('f1')
    assert x['tested_pair_count']==468
    assert x['solvable_pair_count']==0
    assert x['rank83_pair_count']==36
    assert x['rank95_pair_count']==432
    assert x['coefficient_rank_by_target_face_rank']=={'83':180,'95':143}
    assert len(x['all_pairs_reduced_systems'])==468
    assert all(not z['extension_exists'] and z['contradiction_rows']>0
               for z in x['all_pairs_reduced_systems'])

def test_f1_rank83_and_rank95_independent_samples():
    x=result('f1')['all_pairs_reduced_systems']
    a=next(z for z in x if z['pair']==[0,10])
    b=next(z for z in x if z['pair']==[1,2])
    assert (a['target_face_rank'],a['equation_count'],a['coefficient_rank'])==(83,940,180)
    assert (b['target_face_rank'],b['equation_count'],b['coefficient_rank'])==(95,748,143)

def test_full_projective_U4_action_and_all_mu6_phases():
    x=result('unit')
    assert x['projective_group_size']==25920
    assert x['number_of_projective_Cayley_edges_tested']==129600
    assert x['scalar_kernel_candidates_numerically_observed']==6
    assert x['numerical_full_unitary_group_order_if_mu6_is_exact_kernel']==155520
    assert x['max_projective_unitary_closure_error']==0
    assert x['scalar_mu6_powers_histogram']=={'0':46642,'1':10292,'2':12743,
                                               '3':10920,'4':12250,'5':10834}

def test_exact_cyclotomic_omega_braid_and_determinants():
    x=result('unit')['exact_cyclotomic_braid']
    assert x['identity']=='U4 U1 U4 = omega U1 U4 U1'
    assert x['verified_field']=='Q(sqrt(3),i)'
    assert x['exact_generator_determinants']==['omega^2']*4+['1']

def test_hypergeometric_sampling_exact_coverage_boundary():
    x=result('sampling')
    assert x['population_rounds']==4292
    assert x['test_positions']==4096
    assert x['key_positions']==196
    assert [r['remaining_key_errors_upper'] for r in x['rows']]==[2,3,4,5,6,8,11]
    for r in x['rows']:
        bound,total=Q.upper_remaining(r['observed_test_errors'])
        assert bound==r['remaining_key_errors_upper']
        assert total==r['worst_total_errors_at_confidence']

def test_fixed_pattern_sampling_does_not_prove_coherent_Eve_security():
    x=result('sampling')['fully_leaked_test_schedule_counterexample']
    assert x['observed_test_errors']==0 and x['actual_key_errors']==196
    assert x['fraction_key_wrong']==1

def test_calibration_budget_fully_specified():
    x=result('cal')
    assert x['number_of_tetrad_settings']==40
    assert sorted(x['simulated_setting_schedule'])==list(range(40))
    assert x['total_shots_for_that_conservative_target']==76689920
    assert x['shots_per_probe_to_certify_separable_ceiling_at_most_0_44']==479312
    assert len(x['zero_wrong_output_budget'])==4
    assert x['full_40_analyzer_model_drift_census'][-1]['trusted_no_background_separable_upper']==pytest.approx(.406217696786,abs=1e-10)

def test_polar_CPTP_instrument_and_H27_sector_orbits():
    x=result('polar')
    assert x['polar_ray_count']==13
    assert x['tetrad_count']==40
    assert x['H27_orbit_sizes']==[1,3,3,3,3]
    assert x['polar_tetrad_membership_histogram']=={'1':36,'4':4}
    assert x['flag_effect_eigenvalues']==[.1,.4,.4,.4]
    assert x['polar_frame_law_max_residual']==0
    assert x['Kraus_completeness_max_residual_40_settings']==0
    assert x['measured_outcome_flag_density_max_offdiagonal']==0
    assert x['flag_probability_on_hub_state']==.1
    assert x['flag_probability_on_uniform_hub_orthogonal_mixture']==.4
    assert x['flag_probability_on_maximally_mixed_ququart']==.325
