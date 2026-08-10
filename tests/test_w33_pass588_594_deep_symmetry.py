import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(n):return json.loads((ROOT/'data'/n).read_text(encoding="utf-8"))
def test_release():
 p=load('w33_pass588_594_deep_symmetry_release.json');assert p['status']=='PASS' and p['owner_check_total']==86 and all(p['release_checks'].values())
def test_degree_optimality():
 p=load('w33_pass588_minimal_degree_groupoid.json');assert p['transpositions']['exact_degree']==13 and p['point_indicator']['distinct_degree13_leading_forms']==1093
def test_full_linear_group():
 p=load('w33_pass589_full_linear_symmetry_centralizer.json');assert len(p['colored_projective_search']['automorphism_matrices'])==3 and p['checks']['universal_linear_A4_no_go']
def test_oriented_cover():
 p=load('w33_pass590_oriented_singer_cover.json');assert p['oriented_Johnson']['double_cover_objects']==112 and p['Singer_refinement']['oriented_flags']==672
def test_dvr_arithmetic():
 p=load('w33_pass591_cyclotomic_dedekind_dvr.json');assert p['global_order']['index_squared']==1 and p['local_prime']['ramification_index']==4 and p['local_prime']['residue_degree']==1
def test_affinity_correction():
 p=load('w33_pass592_aspirational_affinity_correction.json');assert p['strictness']['certified_uniform_gap_lower_bound']>.9995 and p['checks']['old_grid_value_violates_orientation_lower_bound']
def test_icosahedral_holonomy():
 p=load('w33_pass593_icosahedral_singer_fibre.json');q=load('w33_pass594_johnson_pentagon_holonomy.json');assert p['augmentation']['global_bundle_dimension']==280 and q['holonomy']['order']==120 and q['holonomy']['triangles_generate_full_holonomy']
