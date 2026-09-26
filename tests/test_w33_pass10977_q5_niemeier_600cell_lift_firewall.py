import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "p10977",
    ROOT / "analysis" / "w33_pass10977_q5_niemeier_600cell_lift_firewall.py",
)
P = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(P)

CERT_PATH = ROOT / "data" / "w33_pass10977_q5_niemeier_600cell_lift_firewall.json"
CERT = json.loads(CERT_PATH.read_text(encoding="utf-8"))

def test_certificate_replays_exactly():
    assert P.payload() == CERT

def test_common_six_carrier_survives():
    b = CERT["coarse_six_object_bridge"]
    assert b["status"] == "EXACT"
    assert b["niemeier_objects"] == "six A4 components"

def test_niemeier_and_600cell_full_actions_differ():
    r = CERT["niemeier_root_packet"]
    c = CERT["cell600_packet"]
    assert r["root_count"] == 120
    assert r["diagonal_S5_action"]["regular"] is True
    assert r["A5_restriction"]["root_orbit_sizes"] == [60, 60]
    assert c["binary_group"]["order"] == 120
    assert c["binary_group"]["involutions"] == 1

def test_projective_orbit_firewall():
    r = CERT["niemeier_root_packet"]["projective_roots"]
    c = CERT["cell600_packet"]["antipodal_quotient"]
    assert r["count"] == 60
    assert r["A5_orbit_sizes"] == [30, 30]
    assert r["A5_stabilizer_order"] == 2
    assert c["vertices"] == 60
    assert c["regular"] is True

def test_full_cover_involution_firewall():
    f = CERT["lift_firewall"]
    assert f["root_cover_involutions"] == 25
    assert f["cell600_cover_involutions"] == 1
    assert f["full_120_equivariant_identification"] is False
    assert f["projective_60_equivariant_identification"] is False
