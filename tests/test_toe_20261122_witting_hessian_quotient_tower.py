"""Exact quotient-tower tests for Witting 27/9/4 phase geometry."""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'analysis'))
import toe_20261122_witting_hessian_quotient_tower as model

def test_nine_center_fibers_and_affine_action():
    d=model.verify()
    assert (d['G25_order'],d['H27_order'],d['central_Z3_order'])==(648,27,3)
    assert d['induced_9_cell_group_order']==216
    assert d['induced_H27_translation_order']==9
    assert d['induced_H27_translation_is_regular_and_abelian']
    assert len(d['nine_center_fibers'])==9
    assert all(len(x)==3 for x in d['nine_center_fibers'])

def test_polar_pencil_A4():
    d=model.verify()
    assert d['induced_pencil_4_line_group_order']==12
    assert d['induced_pencil_4_line_group_is_A4']
    assert d['central_Z3_fixes_13_polar_neighborhood_points']
