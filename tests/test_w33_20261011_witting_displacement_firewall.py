import importlib.util, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"analysis"/"w33_20261011_witting_displacement_firewall.py"
SPEC=importlib.util.spec_from_file_location("wd_firewall",SCRIPT)
M=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(M)

def test_certificate_replays():
    got=M.payload()
    frozen=json.loads((ROOT/"data/w33_20261011_witting_displacement_firewall.json").read_text())
    assert got==frozen

def test_exact_witting_tangent_firewall():
    p=M.payload();g=p["exact_group_data"]
    assert (g["G25_order"],g["G32_order"])==(648,155520)
    assert g["G25_tangent_fixed_dimension"]==0
    assert g["G25_cotangent_fixed_dimension"]==0
    assert all(p["checks"].values())

def test_pass11891_boundary_and_flavour_target():
    p=M.payload()
    assert "epsilon is linear" in p["pass11891_correction"]["stands"]
    assert "degree-12" in p["pass11891_correction"]["withdraw"]
    assert p["flavour_weld"]["pass11921_up_Higgs_top_space_dimension"]==3
    assert "not a derived physical coupling" in p["flavour_weld"]["firewall"].lower()
