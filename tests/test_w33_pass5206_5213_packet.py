from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
def load(name):return json.loads((ROOT/'data'/name).read_text())

def test_5206():
 d=load('PART_W33_PASS5206_Q5_LEADER36_FULLCUT_DEGREECLASS_DIAGNOSTIC.json')
 assert d['status']=='EXACT_Q5_LEADER36_FULLCUT_DEGREECLASS_REDUNDANCY'
 assert d['derived_N2_caps']['64']==381

def test_5207():
 d=load('PART_W33_PASS5207_Q5_PHEAVY_EQUALITY_FOOTPRINT_REDUCTION.json')
 assert d['status']=='THEOREM_Q5_PHEAVY_EQUALITY_IMPLIES_FOOTPRINT_WEIGHT_AT_MOST_24'
 assert d['Pheavy_component_minimum_cost']==26

def test_5208():
 d=load('PART_W33_PASS5208_ODDQ_DUALGRID_SPANNING_RANK_REDUCTION.json')
 assert d['target_rank']=='q(q^2+1)/2'
 assert d['anchors']['11']==671

def test_5209():
 d=load('PART_W33_PASS5209_Q5_FOOTPRINT_CODE_HULL_MOD4.json')
 assert d['hull_dimension']==64
 assert d['pair_sums']=={'collinear_weight':40,'noncollinear_weight':48}

def test_5210():
 d=load('PART_W33_PASS5210_ROOT_CONTROLLER_DUALGRID_EQUIVARIANCE.json')
 assert d['root_system']=='C2'
 assert d['intertwiner']=='P_pts(g) F = F P_grid(g)'

def test_5211():
 d=load('PART_W33_PASS5211_ODDQ_PBLOCK_NO5PLUS.json')
 assert d['graph']=='NO_5^+(q)'
 assert d['q5']['vertices']==325 and d['q5']['degree']==144

def test_5212():
 d=load('PART_W33_PASS5212_Q5_DUALGRID_HOFFMAN_13_COVER.json')
 assert d['selected_blocks']==13 and d['partition_points']==156
 assert d['Hoffman_bound']==13

def test_5213():
 d=load('PART_W33_PASS5213_Q5_FOOTPRINT_DUAL_325_260_8.json')
 assert d['code_parameters']=='[325,260,8]_2'
 assert d['weight7_exclusion']['backtrack_nodes']==265
 assert len(d['weight8_support'])==8

def test_manifest():
 s=(ROOT/'analysis/W33_CURRENT_FRONTIER_MANIFEST.tex').read_text()
 assert r'\input{analysis/PASS5206_5213_leader36_footprint_NO5_insert}' in s
