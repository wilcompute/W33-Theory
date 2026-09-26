"""Regression for Pass 10969: heavy-superpartner RPV rescue vs the measured Higgs quartic."""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("p10969", ROOT / "analysis" / "w33_pass10969_rpv_heavy_superpartners_vs_higgs_quartic.py")
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)
CERT = json.loads((ROOT / "data" / "w33_pass10969_rpv_heavy_superpartners_vs_higgs_quartic.json").read_text())


def test_control_reproduces_buttazzo_fit():
    ref = M.run(173.34, 125.15, 0.1184, 80.384)
    assert abs(M.lam(ref, 1.22e19) - (-0.0143)) < 0.002
    assert 1e9 < M.zero(ref, 173.34) < 1e11


def test_pdg_instability_scale():
    s = M.run(172.57)
    z = M.zero(s, 172.57)
    assert 1e10 < z < 1e11
    assert M.lam(s, 1e15) < -0.008


def test_rpv_needs_superheavy_squarks():
    assert min(CERT["m_squark_needed"].values()) > 5e14


def test_required_top_mass_is_several_sigma_low():
    assert CERT["mt_needed"]["1e+15"] < 171.1
    assert CERT["sigma_below_PDG"]["1e+15"] > 5


def test_monotone_in_top_mass():
    zs = [CERT["zero_crossing_scan"][k] for k in sorted(CERT["zero_crossing_scan"], key=float)]
    assert all(a > b for a, b in zip(zs, zs[1:]))


def test_bt475_claim_refuted():
    a = CERT["bt475_audit"]
    assert a["measured_lambda_1e16"] < 0 < a["claim"]
    assert a["mt_needed_for_claim"] < 168
