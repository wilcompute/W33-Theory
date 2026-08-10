import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def load(name):return json.loads((ROOT/'data'/name).read_text(encoding='utf-8'))

def test_4713_invariant_cohomology():
    z=load('PART_W33_PASS4713_INVARIANT_FLAG_COHOMOLOGY.json')
    assert z['base']=={'vertices':810,'valency':16,'edges':6480,'diameter':5,'connected':True,'betti_1':5671,'construction':'smallest connected self-paired PSp orbital'}
    assert z['lift']['vertices']==1620 and z['lift']['edges_per_base_edge']==2
    assert z['nonzero_cycle']['projected_flag_cycle']==[0,482,367,0]
    assert z['cohomology']['deck_class_nonzero'] and z['cohomology']['PGSp_invariant']
    assert z['cohomology']['generated_submodule_dimension']==1

def test_4714_intrinsic_gq42():
    z=load('PART_W33_PASS4714_DUALSHELL_GQ42_DESIGN.json')
    assert z['pair_graph']['parameters']==[45,12,3,3]
    assert z['pair_graph']['maximal_K5']==27
    assert z['GQ']['order']==[4,2] and z['GQ']['dual_point_graph']==[27,10,1,5]
    assert z['triangle_incidence']['SNF_nonzero']=={'1':44,'3':1}
    assert z['point_line_incidence']['SNF_nonzero']=={'1':21}
    assert z['automorphism_group_order']==51840

def test_4715_character_kernels():
    z=load('PART_W33_PASS4715_EDGE_KERNEL_CHARACTER_DECOMPOSITION.json')
    h=z['hot_405'];c=z['cold_1620']
    assert h['rank']==24 and c['rank']==146
    assert sum({'15_L':15,'20':20,'24':24,'30_C-':30,'30_C+':30,'60':60,'64':64}[k]*v for k,v in h['kernel_378'].items())==378
    dims={'15_L':15,'20':20,'24':24,'30_R':30,'30_C-':30,'30_C+':30,'40_C+':40,'40_C-':40,'45_C+':45,'45_C-':45,'60':60,'64':64,'81':81}
    assert sum(dims[k]*v for k,v in c['kernel_1485'].items())==1485
    assert c['local_12_image_order']==96 and c['local_complex_dimensions']==[1,1,1,3,6]

def test_4716_s3_bundle():
    z=load('PART_W33_PASS4716_SELECTED270_BUNDLE_CONNECTION.json')
    assert z['selected135_cover']['connection_group']=='S3'
    assert z['triangle_holonomy']['base_triangles']==270 and z['triangle_holonomy']['all_order']==2
    assert sum(z['triangle_holonomy']['transposition_census'].values())==270
    assert z['selected270_reconstruction']=={'vertices':270,'intersection_graph_recovered_exactly':True,'Petersen_fibers':27,'vertices_per_fiber':10,'hot_edges':405,'cold_edges':1620}
    assert z['interfiber_connection']['law'].startswith('3 disjoint K2,2')

def test_4717_capacity():
    z=load('PART_W33_PASS4717_CAPACITY_QUEUE_ERASURE_ROUTER.json')
    assert z['capacity']['breakpoints']==['63/155','111/137','239/105']
    assert z['equal_capacity']['optimal_mix']=={'P0':'13/80','P1':'67/80'}
    assert z['equal_capacity']['per_edge_load']=='659/15' and z['equal_capacity']['lambda_max']=='15/659'
    assert z['erasure_retransmission_example']['lambda_effective']=='372/16475'

def test_4718_design_contains_petersen():
    z=load('PART_W33_PASS4718_DUALSHELL_PETERSEN_DESIGN_SPECTRUM.json')
    assert z['triangle_incidence_spectrum']=={'54':1,'27':20,'9':24}
    assert z['fiber_relations']['intersection_1']['graph']=='Petersen'
    assert z['fiber_relations']['intersection_1']['edges_total']==405
    assert z['shortcut_identification']['intersection_1_relation_equals_selected270_shortcut_edges']

def test_4719_regular_closure_nonidentification():
    z=load('PART_W33_PASS4719_S3_REGULAR_CLOSURE.json')
    r=z['regular_closure'];k=z['selected270_base_nonidentification']
    assert r['vertices']==k['vertices']==270 and r['edges']==k['edges']==1620
    assert r['bipartite'] is True and k['bipartite'] is False
    assert r['deck_group']=='S3' and r['identification'].startswith('Kronecker')

def test_4720_petersen_code():
    z=load('PART_W33_PASS4720_PETERSEN_NETWORK_CODE.json')
    assert z['local_cycle_code']['parameters']=='[15,6,5]_2'
    assert z['local_cycle_code']['weight_enumerator']=={'0':1,'5':12,'6':10,'8':15,'9':20,'10':6}
    assert z['guaranteed_erasure_correction']==4
    assert z['symmetry']['Petersen_automorphism_order']==120
    assert z['global_27_fiber_direct_sum']['cycle_parameters']=='[405,162,5]_2'
