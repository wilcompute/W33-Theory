import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'data'
def load(n):return json.loads((DATA/n).read_text(encoding="utf-8"))

def test_total_checks_74():
 files=[f'w33_pass108{i}_'+s for i,s in [(1,'frame_module_lattice.json'),(2,'frame_coherent_configuration.json'),(3,'levi_frame_steinberg_intertwiner.json'),(4,'g32_g25_parabolic_normalizer.json'),(5,'hardware_in_loop_rehearsal.json'),(6,'contextuality_claim_firewall.json')]]
 ds=[load(f) for f in files];assert all(d['status']=='PASS' for d in ds);assert sum(d['check_count'] for d in ds)==74;assert all(all(d['checks'].values()) for d in ds)
def test_module_lattice():
 d=load('w33_pass1081_frame_module_lattice.json');assert d['block_systems']['4']['block_count']==135;assert d['block_systems']['12']['block_count']==45;assert d['block_systems']['15']['block_count']==36;assert d['row_space_intersections']=={'4&12':45,'4&15':1,'12&15':1};assert d['spread_block_module_intersection_dim']==1
def test_orbital_pairing_correction():
 d=load('w33_pass1082_frame_coherent_configuration.json');assert d['inner_rank']==32 and d['outer_rank']==22;assert d['inner_self_paired_count']==12;assert d['inner_nonself_paired_count']==20;assert d['outer_self_paired_count']==14;assert d['outer_nonself_paired_count']==8;assert d['outer_fusion_equals_transpose_closure'] is False;assert d['frame_graph_relation_valencies']==[3,6,12,12,12,24,48]
def test_steinberg_intertwiner():
 d=load('w33_pass1083_levi_frame_steinberg_intertwiner.json');assert d['selected_rank']==81;assert d['map_span_rank_mod_1000003']==2;assert set(d['cross_orbit_sizes'])=={27,81};assert any(v==162 for v in d['pair_image_ranks'].values());assert any(v==81 for v in d['pair_image_ranks'].values())
def test_parabolic_normalizer():
 d=load('w33_pass1084_g32_g25_parabolic_normalizer.json');assert d['normalizer']['setwise_slice_stabilizer_order']==3888;assert d['normalizer']['pointwise_G25_order']==648;assert d['normalizer']['invariant_action_mod43']=={'u6':1,'v9':42,'w12':1};assert d['exact_arrangement']['multiplicity_profile']=={'1':12,'3':9}
def test_hardware_rehearsal_and_claim_firewall():
 h=load('w33_pass1085_hardware_in_loop_rehearsal.json');assert h['telemetry_event_count']==240;assert h['analysis']['decision']=='contextual_positive';assert h['analysis']['contextual_fraction_claim'] is None;f=load('w33_pass1086_contextuality_claim_firewall.json');assert f['correct_CF']=={'W33':1.0,'doily':0.0};assert 'not a contextual fraction' in f['one_tenth_status']
def test_legacy_estimator_renamed():
 text=(ROOT/'analysis/bt1901_contextual_fraction_estimator.py').read_text(encoding="utf-8");assert 'TARGET_CLICK_RATE' in text;assert 'corrected_signal_click_rate' in text;assert 'corrected_contextual_fraction' not in text;assert 'does NOT estimate the' in text
