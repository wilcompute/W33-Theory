"""Inter-bus Walsh qutrit transport overlap rank and explicit multi-rail proof."""
import sys
from pathlib import Path
import numpy as np
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_walsh_qutrit_interbus_rank_20261023 import (
    code_for_line,interbus_isometry,census,run)
from w33_fractal_linebus_switch_matrix_20261023 import LINES
def test_complete_intersection_and_code_overlap_census():
    a=census()
    assert a['distinct_line_pairs']==780
    assert a['line_intersection_distribution']=={0:540,1:240}
    assert a['direct_qutrit_overlap_rank_distribution']=={0:540,1:240}
    assert a['intersecting_direct_overlap_singular_values']==[.75,0,0]
def test_every_line_isometry_and_all_pairs_rank_upper_bound():
    for i in range(40):
        V=code_for_line(i)
        assert np.linalg.norm(V.T@V-np.eye(3))<1e-12
        for j in range(i+1,40):
            W=code_for_line(j)
            overlap=V.T@W
            assert int(np.linalg.matrix_rank(overlap,tol=1e-10))<=1
def test_actual_multirail_permutation_all_780_pairs():
    for i in range(40):
        for j in range(i+1,40):
            a=interbus_isometry(i,j)
            share=len(set(LINES[i])&set(LINES[j]))
            assert a['moved_rail_count']==4-share
            assert a['logical_qutrit_transfer_error']<1e-12
            if share:assert a['shared_point'] in LINES[i]
def test_rank_obstruction_does_not_assert_no_physical_transfer():
    c=census()
    assert c['explicit_full_qutrit_permutation_transfer']['intersecting']['moved_rail_count']==3
    assert c['explicit_full_qutrit_permutation_transfer']['skew']['moved_rail_count']==4
    assert any('not a physical circuit' in s for s in c['scope'])
def test_reproducible_and_invalid_boundary():
    assert run()['sha256']==run()['sha256']
    with pytest.raises(ValueError):interbus_isometry(0,0)
    with pytest.raises(ValueError):code_for_line(0,[0,0,0,0])
