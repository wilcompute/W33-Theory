import json
import importlib.util
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"analysis"/"w33_20261011_g32_spectral_moment_rigidity.py"
SPEC=importlib.util.spec_from_file_location("g32_moment",SCRIPT)
M=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(M)

def test_frozen_certificate():
    got=M.payload()
    frozen=json.loads((ROOT/"data/w33_20261011_g32_spectral_moment_rigidity.json").read_text())
    assert got==frozen

def test_commutants_and_moments():
    p=M.payload()
    assert [p["commutants"][str(k)]["commutant_dimension"] for k in range(1,5)]==[1,1,1,2]
    assert p["moment_replay"]["max_rigid_residual"]<1e-10
    assert p["moment_replay"]["p4_range"][1]-p["moment_replay"]["p4_range"][0]>.1
    assert all(p["checks"].values())
