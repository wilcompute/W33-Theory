from __future__ import annotations
import hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def load(name):
 p=json.loads((ROOT/'data'/name).read_text()); assert p['status']=='PASS'; assert all(p['checks'].values()); return p

def test_pass871_atlas_standard_conjugacy():
 p=load('w33_pass871_atlas_standard_conjugacy.json'); assert p['generator_conversion']['generated_outer_group_order']==51840; assert set(p['exact_matches'])=={'6','14','40'}; assert all(z['conjugator_rank']==z['dimension'] for z in p['exact_matches'].values()); assert p['exact_matches']['40']['extended_algebra_dimension']==1600; assert p['exact_matches']['40']['extended_endomorphism_dimension']==1

def test_pass872_heisenberg_loewy_basis():
 p=load('w33_pass872_heisenberg_loewy_basis.json'); assert p['module']['Loewy_layers']==[1,2,4,2,1]; assert p['module']['radical_dimensions']==[10,9,7,3,1,0]; assert p['middle_layer']['basis_words']==['xx','xy','yx','yy']; assert len(p['canonical_monomial_basis']['basis_columns_in_original_cut_quotient_coordinates'])==10

def test_pass873_scalar_schur_factor_set():
 p=load('w33_pass873_scalar_schur_factor_set.json'); assert p['central_extension']['base_order']==25920; assert p['central_extension']['cover_order']==51840; assert p['factor_set']['cocycle_identity_checks']==414720; assert p['presentation_representative']['nonzero_relator_count']>=1

def test_pass874_adaptive_audit_regret_game():
 p=load('w33_pass874_adaptive_audit_regret_game.json'); v=p['policy_challenge']['validated_policy']; assert v=={'exploration':0.3,'temperature':1.0}; assert not p['policy_challenge']['incumbent_survived']; assert p['third_holdout']['validated_regret_over_oracle_lower_bound']<p['third_holdout']['incumbent_regret_over_oracle_lower_bound']; assert p['third_holdout']['null_alarms']==0

def test_pass875_hardware_phase_dispatcher():
 p=load('w33_pass875_hardware_phase_dispatcher.json'); assert p['correction']['off_wall_integer_counterexamples']==1089; assert p['integer_hardware']['entries']==7776; assert p['integer_hardware']['phase_count']==22
 for name,key in [('w33_phase_dispatcher.h','c'),('w33_phase_dispatcher.sv','sv'),('w33_phase_rom.mem','mem')]: assert hashlib.sha256((ROOT/'hardware'/name).read_bytes()).hexdigest()==p['integer_hardware']['hashes'][key]
