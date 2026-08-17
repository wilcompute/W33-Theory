from __future__ import annotations
import importlib.util, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/'analysis/w33_pass5856_5862_doily_quadratic_orbits.py'
CERT=ROOT/'data/PART_W33_PASS5856_5862_DOILY_QUADRATIC_ORBITS.json'

def load_module():
    spec=importlib.util.spec_from_file_location('p5856',SCRIPT); assert spec and spec.loader
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def test_byte_exact_replay():
    before=CERT.read_bytes(); load_module().main(); assert CERT.read_bytes()==before

def test_radon_radicals():
    d=json.loads(CERT.read_text())['pass_5856_mod2_radon_radical_map']
    assert d['R_transpose_mod2_rank']==d['D_mod2_rank']==5
    assert d['H_transpose_mod2_rank']==2
    assert d['line_radical_dim']==5 and d['point_heavy_radical_dim']==3
    assert d['R_transpose_image']=='exactly the 5D line radical'

def test_bent_orbits():
    d=json.loads(CERT.read_text())['pass_5857_quadratic_refinement_bent_orbits']
    assert d['quadratic_refinements']==16
    assert (d['hyperbolic_grid_forms'],d['elliptic_ovoid_forms'])==(10,6)
    assert (d['Walsh_eigenvalue_hyperbolic'],d['Walsh_eigenvalue_elliptic'])==(4,-4)

def test_grid_partition_model():
    d=json.loads(CERT.read_text())['pass_5858_ovoid_grid_partition_model']
    assert d['ovoids']==6 and d['grids']==10
    assert d['induced_graph']=='K3,3'
    assert d['pair_intersection_points']==15

def test_s6_action():
    d=json.loads(CERT.read_text())['pass_5859_explicit_S6_action']
    assert d['Sp4_2_order']==720
    assert d['distinct_permutations_on_six_ovoids']==720
    assert d['distinct_permutations_on_ten_grids']==720

def test_grid_angles():
    d=json.loads(CERT.read_text())['pass_5860_grid_pair_angle_bijection']
    assert d['grid_pairs']==d['distinct_five_point_intersections']==45
    assert d['intersection_size']==5

def test_nested_rook():
    d=json.loads(CERT.read_text())['pass_5861_nested_rook_subconstituent']
    assert d['rank_one_induced_graph']=='L2(3)=SRG(9,4,1,2)'
    assert d['determinant_grid_stabilizer_order']==72

def test_simplex_puncture_boundary():
    d=json.loads(CERT.read_text())['pass_5862_simplex_puncture_unit_line']
    assert d['projective_lines_wholly_in_units']==2
    assert d['deleted_line_maps_to_one_unit_line']
    assert d['unit_lines_are_nonisotropic']
