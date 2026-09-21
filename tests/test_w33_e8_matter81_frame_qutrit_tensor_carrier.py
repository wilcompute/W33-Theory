from __future__ import annotations
import importlib.util
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def load():
    p=ROOT/"analysis/w33_e8_matter81_frame_qutrit_tensor_carrier.py"
    s=importlib.util.spec_from_file_location("m81tensor",p)
    assert s and s.loader
    m=importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m

def test_e8_matter81_frame_qutrit_tensor_carrier():
    o=load().main(False)
    assert o["status"]=="PASS_E8_MATTER81_EQUALS_27_COMPLETE_FRAMES_X_3_EXTERNAL_QUTRIT_PHASES"
    assert o["chart"]["root_count"]==81
    assert o["tensor_factorization"]["root_to_frame_phase_bijective"] is True
    assert o["cubic_lift"]["zero_sum_E8_triples"]==270
    assert o["cubic_lift"]["zero_sum_lifts_per_base_tritangent"]==6
    assert o["cubic_lift"]["allowed_phase_multiset"]==[0,1,2]
    assert o["cubic_lift"]["triples_per_root"]==10
    assert o["checks"]["transported_45_tritangents_exact"] is True
