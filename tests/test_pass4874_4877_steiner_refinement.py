from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'

def load(name):return json.loads((DATA/name).read_text())

def test_pass4874_association_scheme():
    d=load('PART_W33_PASS4874_STEINER_W33_ASSOCIATION_SCHEME.json')
    s=d['scheme']
    assert s['classes']==4 and s['commutative'] and s['imprimitive']
    assert s['valencies']==[1,2,27,36,54]
    assert s['multiplicities']==[1,24,15,20,60]
    assert s['first_eigenmatrix']==[[1,2,27,36,54],[1,2,-3,6,-6],[1,2,3,-12,6],[1,-1,9,0,-9],[1,-1,-3,0,3]]
    q=d['Q43_line_quotient']
    assert q['parameters']==[40,12,2,4]
    assert q['identification']=='Q(4,3) point graph = W(3,3) line-intersection graph'
    assert q['dividing_by_fiber_size_recovers_common_SRG_eigenvalues']==[12,2,-4]
    assert d['correction']['original_W33_point_quotient_label'] is False
    assert d['correction']['scheme_arithmetic_changed'] is False
    assert d['nonedge_refinement']['R2_is_perfect_matching_for_all_540_Q43_nonedges']
    assert d['transverse_sector']['primitive_multiplicities']==[20,60]

def test_pass4875_outer_selection_rule():
    d=load('PART_W33_PASS4875_PGSP_QUADRATIC_CHIRALITY.json')
    assert d['PSp_quadratic_Hom_dimension']==2
    assert d['PGSp_quadratic_Hom_dimension']==0
    assert d['PSp_pair_orbits'][2]==[2160,12,2]
    assert d['PGSp_pair_orbits'][2]==[2160,24,0]
    assert d['outer_action']=={'plus_dimension':0,'minus_dimension':2,'matrix_up_to_basis':'-I_2'}
    assert not d['preferred_projective_channel_selected']

def test_pass4877_equal_120s_are_not_same_gset():
    d=load('PART_W33_PASS4877_MAXCUT_STEINER_NONBIJECTION.json')
    assert d['maximum_cuts']['count']==d['Steiner_triangles']['count']==120
    assert d['maximum_cuts']['stabilizer_order']==d['Steiner_triangles']['stabilizer_order']==432
    assert d['maximum_cuts']['stabilizer_fixed_Steiner_triangles']==0
    assert d['Steiner_triangles']['stabilizer_fixed_Steiner_triangles']==1
    assert d['maximum_cuts']['stabilizer_order_census']['8']==108
    assert '8' not in d['Steiner_triangles']['stabilizer_order_census']
    assert not d['nonbijection']['PGSp_equivariant_bijection_exists']

def test_shared_frontier_contains_new_refinement_once():
    live=(ROOT/'analysis/W33_CURRENT_FRONTIER_MANIFEST.tex').read_text()
    for token in ('PASS4874_steiner_w33_association_scheme_insert','PASS4875_pgsp_quadratic_selection_insert','PASS4877_maxcut_steiner_nonbijection_insert'):
        assert live.count(token)==1
    insert=(ROOT/'analysis/PASS4874_steiner_w33_association_scheme_insert.tex').read_text()
    assert 'Q(4,3)' in insert and 'line action' in insert
