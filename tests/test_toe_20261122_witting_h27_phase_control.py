"""Checks for the exact H27 regular 27-orbit and optical controller."""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'analysis'))
import toe_20261122_witting_h27_phase_control as model

def test_extraspecial_normal_H27():
    d=model.verify()
    assert d['normal_subgroup_order']==27
    assert d['normal_subgroup_center_order']==d['normal_subgroup_derived_order']==3
    assert d['subgroup_element_order_profile']=={'1':1,'3':26}
    assert d['quotient_order']==24

def test_regular_27_address_and_full_control():
    d=model.verify()
    assert d['regular_orbit_size']==27
    assert d['stabilizer_of_tunable_ray_in_H27']==1
    assert d['controller_lie_dimension']==16
