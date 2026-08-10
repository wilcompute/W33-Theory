import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(name):return json.loads((ROOT/'data'/name).read_text(encoding="utf-8"))

def test_release_lock():
 p=load('w33_pass578_582_residual_colored_johnson_completion_continuous_release.json')
 assert p['status']=='PASS' and p['owner_check_total']==66 and all(p['release_checks'].values())

def test_residual_symmetry_classification():
 p=load('w33_pass578_residual_collision_symmetry.json')
 assert p['natural_global_search']['global_projective_maps']==3
 assert p['fixed_locus_S3']['projective_group_order']==6
 assert p['fixed_locus_S3']['size3_S3_orbits']==22
 assert p['combined_partial_quotient']['residual_collision_excess']==44191

def test_colored_600cell_module():
 p=load('w33_pass579_colored_600cell_module.json')
 assert p['snub_octahedral_colorings']['count']==5
 assert p['module_bridge']['F3_Jordan_type']=={'J1':3,'J2':0,'J3':3}
 assert p['module_bridge']['with_apex']=={'J1':4,'J2':0,'J3':3}

def test_singer_johnson_fusion():
 p=load('w33_pass580_singer_johnson_fusion.json')
 assert len(p['fusions'])==4
 assert p['imprimitivity']['identification']=='Johnson association scheme J(8,3)'
 assert p['representation_restriction']['block_constant_dimensions']==[1,7,20,28]
 assert p['terwilliger_J83_basepoint']['dimension']==38

def test_cyclotomic_completion_source():
 p=load('w33_pass581_cyclotomic_completion_formal.json')
 assert p['algebra']['residue_quotient']=='O_5/(lambda) ~= F_5'
 assert p['algebra']['completion']=='AdicCompletion (lambda) O_5'
 assert all(p['checks'].values())

def test_continuous_blackwell_regions():
 p=load('w33_pass582_continuous_bellman_enclosure.json')
 assert all(x['one_step_gain']>0 for x in p['profiles'].values())
 assert all(x['strict_L1_neighborhood_radius']>0 for x in p['profiles'].values())
 assert all(all(m['quartic_marginal_error']<1e-14 for m in x['blackwell_marginals']) for x in p['profiles'].values())
