"""Round33 seven reproducibility gates across five independent fronts."""
from pathlib import Path
import sys,json,math
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_20261010_toe33_joint_spacetime_decoder as decoder
import w33_20261010_toe33_p13_cpsat_cover as p13
import w33_20261010_toe33_girth_moore_bound as moore
import w33_20261010_toe33_a6_torus_translation_obstruction as a6
import w33_20261010_toe33_bloch_spectral_spacetime as dimension
import w33_20261010_toe33_C8_measured_comparator as hardware
def frozen(name,r):
 x=json.loads((ROOT/'data'/f'w33_20261010_toe33_{name}.json').read_text(encoding='utf-8'))
 assert r==x

def test_joint_5round_decoder_reduces_logical_failure_same_trials():
 r=decoder.run(trials=180);frozen('joint_spacetime_decoder',r)
 assert [z['logical_failures']['joint'] for z in r['outcomes']]==[13,14,36]
 assert [z['logical_failures']['individual'] for z in r['outcomes']]==[40,35,53]
 assert all(z['mismatched_check_values_total']['joint']<z['mismatched_check_values_total']['individual'] for z in r['outcomes'])

def test_CP_SAT_unknown_is_NOT_a_no_go():
 r=json.loads((ROOT/'data/w33_20261010_toe33_p13_cpsat_cover.json').read_text())
 assert r['prime']==13 and r['chord_variables']==81 and r['constraints']==1620
 assert len(r['tree_gauge_fixed_edges'])==79 and len(r['free_chords'])==81
 assert len(set(r['tree_gauge_fixed_edges'])&set(r['free_chords']))==0
 assert r['solver_status'] in ('OPTIMAL','FEASIBLE','INFEASIBLE','UNKNOWN')
 if r['solver_status']=='UNKNOWN':assert not r['found']
 if r['found']:
  from w33_20261009_toe26_css_matching_family import wilson
  import numpy as np
  edges,D,C=wilson()
  assert np.all((C.astype(np.int16)@np.asarray(r['voltages'],dtype=np.int16))%13!=0)

def test_exact_bipartite_Moore_cover_bounds():
 r=moore.run();frozen('girth_moore_bound',r)
 assert [b['minimum_W33_cover_degree'] for b in r['target_bounds']]==[1,4,10,28,82]

def test_A6_F3_root_torus_fails_4D_invariant_translation_subspace():
 r=a6.run();frozen('a6_torus_translation_obstruction',r)
 assert r['generator_order']==360
 assert r['orbit_generated_submodule_dim_counts']=={'1':2,'5':240}
 assert r['invariant_functional_dim']==0

def test_1360_vertex_voltage_Bloch_spectrum_lacks_decade_dim_plateau():
 r=dimension.run();frozen('bloch_spectral_spacetime',r)
 assert r['vertices']==1360
 assert 0.6<r['Laplacian_nonzero_gap']<0.8
 assert not r['one_decade_three_dim_plateau']
 assert not r['one_decade_four_dim_plateau']
 assert r['spectral_dimension_near3_band_2p75_to3p25']['span_ratio']<2

def test_2018_measured_transmon_lifetime_does_not_meet_60us_pair_condition():
 r=hardware.run();frozen('C8_measured_comparator',r)
 x=r['measured_reference_T1_pair_survival_if_reused_under_independent_markov_model']
 assert abs(x[-1]['no_loss_two_excitations']-math.exp(-3))<1e-12
 assert r['half_pair_survival_required_T1_us']['60.0']>173
 assert len(r['relevant_published_devices'])==3

def test_both_T_and_hypercharge_reduce_commutant_exactly_to_SU3_SU2():
 import w33_20261010_toe33_hypercharge_translation_incompatibility as both
 r=both.run();frozen('hypercharge_translation_incompatibility',r)
 assert r['parent_faithful_A6_commutant_dim']==24
 assert r['with_hypercharge_rotation_A6_Z7_commutant_dim']==12
 assert r['with_central_3_extension_translations_commutant_dim']==11
 assert r['with_both_T_and_Z7_hypercharge_commutant_dim_proved']==11
 assert r['centre_dim']==0
