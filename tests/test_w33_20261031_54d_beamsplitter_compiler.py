"""Regression of canonical and all-81-mode signed-Givens optical pulse compiler."""
import json
import numpy as np
from analysis import w33_20261031_54d_beamsplitter_compiler as C

def test_canonical_rotation_and_givens_angles():
    U,p=C.canonical()
    assert U.shape==(3,3)
    assert np.linalg.det(U)>0.999999999
    assert np.max(abs(U@U-np.eye(3)))<1e-13
    assert p["chronological_layers"][2]=="phase_pi_on_canonical_2_and_3"

def test_all_54_physical_triangle_blocks():
    p=C.payload()
    assert p["status"]=="PASS"
    for side,chosen in (("plus",7),("minus",6)):
        b=p[side]
        assert b["factor"]==chosen and b["mode_triangles"]==27
        assert b["max_abs_matrix_error"]<2e-14
        all_modes=[m for rec in b["schedule"] for m in rec["modes"]]
        assert sorted(all_modes)==list(range(81))
        assert all(sorted(abs(x) for x in rec["axis_integer"])==[1,2,3] for rec in b["schedule"])

def test_frozen_certificate_and_resource_upper_bound():
    p=json.loads(C.OUT.read_text())
    assert p["status"]=="PASS"
    assert p["resource_upper_bound_per_triangle"]["real_two_mode_rotations"]==4
    assert p["resource_upper_bound_per_triangle"]["pi_phase_shifters"]==2
    assert p["resource_upper_bound_per_triangle"]["parallel_triangles"]==27
