from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def test_qpsi_matter_parity_anomaly_firewall():
    p=ROOT/"analysis/w33_matter_parity_dai_freed_firewall.py"
    s=importlib.util.spec_from_file_location("mpdf",p);assert s and s.loader
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
    o=m.main(False)
    assert o["status"]=="PASS_QPSI_MATTER_PARITY_ANOMALY_FIREWALL_WITH_MIXED_SYMMETRY_BOUNDARY"
    assert o["computed"]["A_gravity_U1psi"]==0
    assert o["computed"]["A_U1psi_cubed"]==0
    assert o["computed"]["A_SO10sq_U1psi"]==0
    assert o["literature_imports"]["pure_Z2"]["result"]=="Omega_5^Spin(BZ2)=0"
    assert "Z4_X" in o["firewalls"]["not_Z4X"]
