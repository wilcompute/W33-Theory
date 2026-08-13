import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(n):return json.loads((ROOT/'data'/n).read_text())
def test_5016_closure():
 x=load('PART_W33_PASS5016_RADIUS_RP2_SYMMETRY_CLOSURE.json');assert (x['all_relations'],x['triangle_internal_relations'],x['missing_after_local'])==(1566,756,1296);assert x['factorization']==[755,1,270,540] and x['covering_radius']==[134,173]
def test_5017_opposite_extensions():
 x=load('PART_W33_PASS5017_REAL60_K60_OPPOSITE_EXTENSIONS.json');assert x['equation_kernel_nullities']=={'F2':174,'F3':130,'F5':60};assert x['PGSp_Hom']['L60_to_K60']['rank']==14 and x['PGSp_Hom']['K60_to_L60']['rank']==46;assert x['S14_matches_Pass5010_V20_image'] and not x['isomorphic']
def test_5018_coherent_config():
 x=load('PART_W33_PASS5018_200_COVER_COHERENT_CONFIGURATION.json');assert x['cover_orbits']=={'points':40,'flags':160};assert x['ordered_orbitals']==19 and x['orbital_split']=={'PP':3,'PF':4,'FP':4,'FF':8};assert x['cover_tritangent_incidence']['rank']==25
def test_5019_code():
 x=load('PART_W33_PASS5019_STEINER_K33_V24_CODE.json');assert x['ranks']=={'Q':24,'F2':24,'F3':24};assert x['binary_code']=={'n':45,'k':24,'d':6,'minimum_words':120};assert x['ternary_code']=={'n':45,'k':24,'d':6,'minimum_words':240}
def test_5020_cubes():
 x=load('PART_W33_PASS5020_GLUED_EIGHT_COVER_CUBES.json');assert x['global_graph']['vertices']==200 and x['global_graph']['edges']==480;assert x['global_graph']['degrees']=={'point_cover':12,'flag_cover':3};assert x['line_cover_incidence']['ranks']=={'Q':40,'F2':40,'F3':40}
def test_5021_homology():
 x=load('PART_W33_PASS5021_CUBE_COMPLEX_HOMOLOGY_81.json');assert x['cell_counts']=={'C0':200,'C1':480,'C2':240};assert x['homology']=={'H0':1,'H1':81,'H2':40}
def test_5022_frames():
 x=load('PART_W33_PASS5022_COVER_CIRCUIT_V24_FRAME_DUALITY.json');assert x['cover_centered_rank']==x['circuit_rank']==24;assert x['identity']=='Uc^T Uc = 2 S^T S'
def test_5023_bridge():
 x=load('PART_W33_PASS5023_CUBE81_TO_W33_HODGE81_CHAIN_ISOMORPHISM.json');assert x['source_H1']==x['target_H1']==81 and x['induced_rank_F2']==x['induced_rank_F3']==81 and x['isomorphism']
