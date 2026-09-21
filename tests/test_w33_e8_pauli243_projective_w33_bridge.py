from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load():
    p=ROOT/"analysis/w33_e8_pauli243_projective_w33_bridge.py"
    s=importlib.util.spec_from_file_location("e8w33",p); assert s and s.loader
    m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
def test_e8_pauli243_projects_to_canonical_w33():
    o=load().main(False)
    assert o["status"]=="PASS_EXPLICIT_E8_PAULI243_PROJECTIVE_QUOTIENT_IS_CANONICAL_W33"
    assert o["projective_quotient"]["projective_rays"]==40
    assert o["commutator_form"]["all_81x81_pairs_checked"] is True
    assert o["W33"]["degree"]==12 and o["W33"]["lambda"]==2 and o["W33"]["mu"]==4
    assert o["W33"]["isotropic_lines"]==40
    assert o["W33"]["literal_point_table_equals_repo_canonical_two_qutrit_W33"] is True
