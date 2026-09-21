from __future__ import annotations
import importlib.util
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"analysis/w33_qpsi_matter_parity_e8_d8_bridge.py"

def load():
    spec=importlib.util.spec_from_file_location("qpsi_parity",SRC)
    assert spec and spec.loader
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def test_qpsi_matter_parity_e8_d8_bridge():
    out=load().main(False)
    assert out["status"]=="PASS_QPSI_MATTER_PARITY_EXTENDS_TO_E8_D8_INVOLUTION"
    assert out["E6_27"]["odd_dimension"]==16
    assert out["E6_cubic"]["all_cubics_matter_parity_even"] is True
    assert out["E8_Qpsi_mod2"]["even_roots"]==112
    assert out["E8_Qpsi_mod2"]["odd_roots"]==128
    assert out["E8_Qpsi_mod2"]["fixed_lie_dimension"]==120
    assert out["standard_E8_crosscheck"]["even_root_system"]=="D8"
