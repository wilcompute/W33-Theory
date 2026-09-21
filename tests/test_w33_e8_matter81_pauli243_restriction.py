from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load():
    p=ROOT/"analysis/w33_e8_matter81_pauli243_restriction.py"
    s=importlib.util.spec_from_file_location("m81p243",p); assert s and s.loader
    m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
def test_matter81_pauli243_restriction():
    o=load().main(False)
    assert o["status"]=="PASS_MATTER81_RESTRICTS_TO_NINE_TWO_QUTRIT_SCHRODINGER_MODULES_NOT_REGULAR_F3_4_SET"
    assert o["matter_representation"]["dimension"]==81
    assert o["matter_representation"]["irreducible_dimension"]==9
    assert o["matter_representation"]["multiplicity"]==9
    assert o["projective_weight_rays"]["orbit_count"]==9
    assert o["projective_weight_rays"]["orbit_size"]==9
    assert o["operator_quotient"]["count"]==81
    assert o["equivariance_verdict"]["matter_rays_equivariantly_bijective_to_operator_quotient"] is False
    assert all(o["checks"].values())
