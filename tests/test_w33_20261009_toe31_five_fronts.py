"""Round31 six focused reproducibility tests for five independent fronts."""
import sys,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_20261009_toe31_compact_voltage_cover as search
import w33_20261009_toe31_compact_cover_certificate as cert
import w33_20261009_toe31_cat_detector_budget as cat
import w33_20261009_toe31_E8_spin16_even_split_obstruction as e8
import w33_20261009_toe31_observer_lightcone_lift as geo
import w33_20261009_toe31_C8_two_boson_loss_hardware_gate as lab
def frozen(name,rec):
 p=ROOT/'data'/f'w33_20261009_toe31_{name}.json'
 assert json.loads(p.read_text())==rec

def test_binary_voltages_obstruction_and_17_cover_search():
 r=search.run()
 frozen('compact_voltage_cover',r)
 assert r['binary_infeasible']
 assert len(r['binary_unsat_even_column_odd_row_subset'])%2==1
 assert r['smallest_connected_cover_found_in_this_search']['p']==17

def test_construct_connected_compact_girth10_witness():
 r=cert.build()
 frozen('compact_cover_certificate',r)
 assert r['exact_girth']==10
 assert len(r['length10_cycle'])==10
 assert r['HGP_parameters']=='[[9245281,1852321,10]]_3'

def test_cat_verifier_probability_budget_and_majority_failure():
 r=cat.run()
 frozen('cat_detector_budget',r)
 assert r['verification_measurements_per_extraction_attempt']==797
 assert r['sample_probabilities'][2]['mean_global_rounds_until_all_clean']>50
 assert r['sample_probabilities'][2]['mean_per_check_prep_attempts_for_159_accepted_checks']<170
 assert r['sample_probabilities'][1]['three_round_majority_one_check_wrong_probability']<.00001

def test_spin16_all_even_nondegenerate_splits_have_no_St81():
 r=e8.run()
 frozen('E8_spin16_even_split_obstruction',r)
 assert len(r['cases'])==5
 assert all(q['St81_multiplicity']==0 for q in r['cases'])
 assert max(q['largest_invariant_block'] for q in r['cases'])==66

def test_finite_null_20_and_external_spatial_lift():
 r=geo.run()
 frozen('observer_lightcone_lift',r)
 assert r['exact_null_by_residue_time']=={'0':8,'1':6,'2':6}
 assert r['future_ball_samples'][1]['size']==7
 assert r['future_ball_samples'][2]['size']==25
 assert r['future_ball_samples'][10]['size']==1561

def test_C8_pair_loss_60us_requirements_are_conditional():
 r=lab.run()
 frozen('C8_two_boson_loss_hardware_gate',r)
 assert r['required_attractive_pair_binding_U_over_h_MHz']==160
 assert r['pair_survival_50_percent_at_60us_requires_T1_us_greater_than']>170
 assert abs([q for q in r['hypothetical_lifetime_coherence_grid'] if q['T1_us']==100][0]['pair_survival_last_60us']-math.exp(-1.2))<1e-12
