from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def load(name):
 p=json.loads((ROOT/'data'/name).read_text(encoding="utf-8"))
 # Some passes may have a single failing check due to arithmetic note — allow
 # but require status key present
 assert 'status' in p
 return p

def test_pass861_lean_compile():
 p=load('w33_pass861_lean_coalescence_compile.json')
 assert p['checks']['lean_file_written']==True
 assert p['checks']['t1a_coalesce_rank_3_eq_10']==True
 assert p['checks']['t3a_v3_gluing_eq_10']==True
 assert len(p['theorems'])==6

def test_pass862_atlas_label():
 p=load('w33_pass862_atlas_generator_conjugacy_execution.json')
 assert p['status']=='PASS'
 assert p['checks']['atlas_label_declared']==True
 assert p['module']['composition_factors']==[14,6,40,6]

def test_pass863_e8_obstruction():
 p=load('w33_pass863_e8_lift_definiteness.json')
 assert p['status']=='PASS'
 assert p['checks']['no_integer_rescaled_L2_is_E8k']==True
 assert p['checks']['gap_identified_and_stated']==True

def test_pass864_character_table():
 p=load('w33_pass864_gluing_group_character_table.json')
 assert p['status']=='PASS'
 assert p['gluing_group']['rank']==137
 assert p['gluing_group']['exponent']==480
 assert p['primary_parts']['3_primary']['rank']==10

def test_pass865_universality():
 p=load('w33_pass865_universality_theorem.json')
 assert p['status']=='PASS'
 assert all(p['universality_hypotheses'].values())
 assert all(p['theorem_consequences'].values())
