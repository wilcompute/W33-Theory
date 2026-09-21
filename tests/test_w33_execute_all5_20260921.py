from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def run(rel,name):
    p=ROOT/rel; s=importlib.util.spec_from_file_location(name,p); assert s and s.loader
    m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m.main(False)

def test_objectwise_matter_parity_cubic():
    o=run("analysis/w33_objectwise_matter_parity_cubic_incidence.py","mpcubic")
    assert o["status"]=="PASS_W33_ONLY_OBJECTWISE_MATTER_PARITY_CUBIC"
    assert o["tritangent_census"]["SO10"]=={"1+10+10":5,"10+16+16":40}

def test_fi_family_a2_weyl_intertwiner():
    o=run("analysis/w33_fi_family_a2_weyl_intertwiner.py","fia2")
    assert o["status"]=="PASS_EXPLICIT_FI_TO_CE2_FAMILY_A2_WEYL_INTERTWINER"
    assert o["word_length"]==23 and o["grade_intertwining"]=={"0->0":78,"1->1":81,"2->2":81}

def test_z6_objectwise_carriers():
    o=run("analysis/w33_z6_objectwise_33_48_32_carrier.py","z6obj")
    assert o["status"]=="PASS_OBJECTWISE_Z6_33_48_32_CARRIER"
    assert o["nonzero_Z3_sector"]["even_33"]["objects"]==33
    assert o["nonzero_Z3_sector"]["odd_48"]["objects"]==48
    assert o["grade_zero_odd_32"]["objects"]==32

def test_d8_weyl_conjugator():
    o=run("analysis/w33_physical_theta3_qpsi_d8_weyl_conjugator.py","d8conj")
    assert o["status"]=="PASS_EXPLICIT_D8_INVOLUTION_WEYL_CONJUGATOR"
    assert o["word_length"]==10
    assert o["root_parity_census"]=={"physical_even_to_qpsi_even":112,"physical_odd_to_qpsi_odd":128}
