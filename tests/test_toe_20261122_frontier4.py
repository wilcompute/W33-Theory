"""Regression certificates for 2026-11-22 fourth-stage Hessian + five independent physics fronts."""
from pathlib import Path
from functools import lru_cache
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'analysis'))
import toe_20261122_fourth_hessian_census as fourth
import toe_20261122_e6_132_constructive_embedding as bridge
import toe_20261122_e6_higgs_cubic_mass_lift as Higgs
import toe_20261122_photonic_sparse_isometry_loss as optical
import toe_20261122_causal_aldous_null_control as causal
import toe_20261122_20effect_Witting_context_POVM as povm20

@lru_cache(None)
def c():return fourth.verify()
@lru_cache(None)
def b():return bridge.verify()
@lru_cache(None)
def h():return Higgs.verify()
@lru_cache(None)
def o():return optical.verify()
@lru_cache(None)
def a():return causal.verify()
@lru_cache(None)
def p():return povm20.verify()

def test_fourth_exact_153million_gates():
    d=c();assert d['fourth_stage_exact_matrices']==153160632
    assert d['fourth_stage_inequivalent_left_H_cosets']==236359
    assert d['fourth_stage_candidate_representatives']==324729

def test_fourth_exact_bra_equivalence_not_float_hash():
    d=c();m=d['complete_exact_bra_and_matrix_membership']
    assert m['exact_matrix_membership_comparisons']==1010231
    assert m['signature_bucket_count']==176230
    assert len(d['exact_unitarity_spot_checks'])==6

def test_132_E6_H27_witness_isometry():
    d=b();assert d['target_dimension']==132 and d['source_dimension']==81
    assert d['explicit_isometric_intertwiner_shape']==[132,81]
    assert max(d['intertwiner_max_abs_residual'].values())<2e-12

def test_132_adj_quotient_characters_and_leakage_warning():
    d=b();assert d['adjoint_78_Z3_squared_char_multiplicity']=={'trivial':14,'each_nontrivial':8}
    assert 'NOT E6-invariant' in d['caveats']

def test_E6_family_H27_cubic_charge_and_singlet_F():
    d=h();assert d['original_singlet_F_constraints_remain_satisfied']
    assert d['Hessian_family_spectrum_MdagM']=={'7/4':2,'1':1}

def test_E6_ten_mass_lift_leaves_spinor_obstruction():
    d=h();assert d['ten_chiral_Higgs_components_massive']==60
    assert d['spinor_chiral_Higgs_components_not_lifted_after_gauge']==64

def test_actual_adjacent_Givens_30_39_isometry():
    rows=o()['rows'];assert rows[0]['base']['gate_count']==138
    assert all(r['base']['gate_count']==110 for r in rows[1:])
    assert all(r['base']['reconstruction_error']<2e-10 for r in rows)

def test_loss_model_state_dependence_and_row_order():
    rows=o()['rows']
    assert rows[0]['base']['maximally_mixed_input_detection_probability']>0.90
    assert all(r['best_of_21_row_orders']['gates']<=109 for r in rows[1:])
    assert all(r['best_of_21_row_orders']['detection_probability']>0.919 for r in rows[1:])

def test_Aldous_exact_free_interchange_gap():
    rows=a()['samples'];assert [r['n'] for r in rows]==[4,5,6,7]
    assert all(.9<r['ratio_W33_over_free']<.97 for r in rows)

def test_causal_gap_scaling_is_not_gravity_evidence():
    d=a();assert 'not evidence' in d['inference']
    assert d['samples'][-1]['zero_action_adjacent_swap_gap']<d['samples'][0]['zero_action_adjacent_swap_gap']

def test_five_Witting_orthonormal_tetrads_make_20_IC():
    d=p();assert d['number_of_outcomes']==20
    assert len(d['five_disjoint_orthonormal_contexts'])==5
    assert all(rank==16 for _,rank in d['six_finite_field_IC_ranks'])
    assert 87.4<d['frame_condition_number']<87.5

def test_20_effect_Givens_and_risk_tradeoff():
    d=p();assert d['optical_constructive_Givens']['gate_count']==70
    assert d['optical_constructive_Givens']['maximally_mixed_input_detection_probability']>0.94
    assert d['seeded_pure_state_HS_risk_coefficient']>50
