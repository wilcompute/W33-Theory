import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(name):return json.loads((ROOT/'data'/name).read_text(encoding="utf-8"))

def test_release_lock():
 p=load('w33_pass583_587_groupoid_intertwiner_johnson_local_blackwell_release.json')
 assert p['status']=='PASS' and p['owner_check_total']==61 and all(p['release_checks'].values())

def test_exceptional_groupoid():
 p=load('w33_pass583_collision_groupoid_polynomial.json')
 assert p['spectral_partition']['equivalence_groupoid_arrows']==3199632
 assert p['checks']['two_transpositions_generate_S3']
 assert p['low_degree_no_go']['tested']==784 and not p['low_degree_no_go']['survivors']

def test_colored_intertwiner_boundary():
 p=load('w33_pass584_colored_intertwiner_a4.json')
 assert p['C3_intertwiner']['det_nonzero']
 assert p['C3_intertwiner']['equation']=='U_packet T = T P_colored'
 assert len(p['A4_transport']['spectral_symmetry_indices'])==3

def test_singer_pentagon_flags():
 p=load('w33_pass585_singer_pentagon_triples.json')
 assert p['Johnson_quotient']['blocks']==56 and p['Johnson_quotient']['block_size']==6
 assert p['six_fibre']['image_order']==120 and p['six_fibre']['kernel_order']==3
 assert p['checks']['Singer_stabilizer_equals_15colon4']

def test_localized_cyclotomic_arithmetic():
 p=load('w33_pass586_cyclotomic_local_dvr.json')
 assert p['algebra']['ramification_index']==4 and p['algebra']['residue_degree']==1
 assert p['algebra']['unit_factor_residue_mod_lambda']==4
 assert all(p['checks'].values())

def test_infinite_horizon_policy_lift():
 p=load('w33_pass587_infinite_horizon_blackwell_lift.json')
 assert all(all(x['same_cost'] and x['garbling_error']<1e-14 for x in r['policy_lifts']) for r in p['profiles'].values())
 assert p['checks']['continuous_action_set_global_nonworsening']
 assert p['checks']['aspirational_M24_tie_preserved']
