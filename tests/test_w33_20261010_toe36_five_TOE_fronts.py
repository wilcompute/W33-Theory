"""Round36 focused regression tests; exact identities and frozen certificates."""
from pathlib import Path
import json,sys,math
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_20261010_toe36_chiral_domain_wall as chiral
import w33_20261010_toe36_spinorial_triality_translation_gate as group
import w33_20261010_toe36_deck_rank_vacuum_selector as vacuum
import w33_20261010_toe36_incidence_relativistic_walk as wave
import w33_20261010_toe36_qed_running_alpha_gate as qed
def frozen(filename):
 x=json.loads((ROOT/'data'/f'w33_20261010_toe36_{filename}.json').read_text(encoding='utf-8'))
 assert x['status']=='PASS'
 return x
def test_domain_wall_interface_index_anomalies_and_mirror_firewall():
 x=chiral.run()
 y=frozen('chiral_domain_wall')
 assert x['one_wall_Q_index']==y['one_wall_Q_index']==1
 assert x['finite_square_closed_system_index']==0
 assert x['SU2_Witten_doublets']==4
 assert x['SM_U1_cubic_anomaly']=='0' and x['su5_anomaly_cubic_integer']==0
 assert x['localized_profile_residual']<1e-12
def test_spinorial_triality_spin11_twist_centralizer_19():
 x=group.run();y=frozen('spinorial_triality_translation_gate')
 assert x['wedge2_adjoint_eigenmultiplicities']==y['wedge2_adjoint_eigenmultiplicities']=={'1':19,'omega':18,'omega2':18}
 assert x['exact_commutant_dimension']==19 and x['R11_order3_error']<1e-12
 assert 'not an F3' in x['translation_obstruction']
def test_free_boson_vacuum_cannot_spontaneously_select_deck_rank():
 x=vacuum.run();y=frozen('deck_rank_vacuum_selector')
 assert [s['vertices'] for s in x['rank_scenarios']]==[240,720,2160]
 assert [s['Perron_adjacency_eigenvalue'] for s in x['rank_scenarios']]==[4]*3
 assert len({s['ground_one_free_boson'] for s in x['rank_scenarios']})==1
 assert x['artificial_rank_chemical_potential'][1]['minimizing_deck_ranks']==[1,2,3]
 assert all(abs(a['full_laplacian_gap']-b['full_laplacian_gap'])<1e-8 for a,b in zip(x['rank_scenarios'],y['rank_scenarios']))
def test_local_wave_incidence_BdagB_identity_and_flatbands():
 x=wave.run();y=frozen('incidence_relativistic_walk')
 assert x['generic_flat_zero_modes']==y['generic_flat_zero_modes']==80
 assert x['zero_modes_at_k0']==82
 assert max(z['adjoint_matrix_identity_residual'] for z in x['directional_verified_dispersion'])<1e-12
 assert all(abs(z['measured_over_acoustic_prediction']-1)<.02 for z in x['directional_verified_dispersion'])
 assert min(x['acoustic_velocity_eigenvalues'])>0
def test_QED_running_not_posthoc_fit_at_Thomson_Q0():
 x=qed.run();y=frozen('qed_running_alpha_gate')
 assert x['naive_discrepancy_in_sigma']>200
 assert 7.<x['inferred_arbitrary_Q_keV']<8
 assert .014<x['inferred_arbitrary_Q_over_me_to_match_CODATA_if_W33_is_Thomson_baseline']<.015
 assert abs(x['inferred_arbitrary_Q_keV']-y['inferred_arbitrary_Q_keV'])<1e-5
 assert qed.vacuum_shift(.1)>0 and qed.vacuum_shift(.2)>qed.vacuum_shift(.1)
