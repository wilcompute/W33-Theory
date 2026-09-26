"""Regression for Pass 10972: tetrahedral cubic clock selector."""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "p10972", ROOT / "analysis" / "w33_pass10972_tetrahedral_cubic_clock_selector.py"
)
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)
CERT = json.loads(
    (ROOT / "data" / "w33_pass10972_tetrahedral_cubic_clock_selector.json").read_text()
)


def test_certificate_passes():
    p = M.payload()
    assert p["status"] == "PASS"
    assert all(p["checks"].values())


def test_exact_tetrahedral_cubic_bound():
    c = CERT["invariants"]
    assert c["cubic_bound_on_p2_1"] == "|p3| <= 1/sqrt(3)"
    cases = {r["multiplicity_a"]: r for r in c["stationary_classification"]}
    assert cases[1]["p3_squared"] == "1/3"
    assert cases[2]["p3_squared"] == "0"
    assert cases[3]["p3_squared"] == "1/3"


def test_four_vacua_have_S3_stabilizer():
    rows = CERT["representation"]["clock_vectors"]
    assert len(rows) == 4
    assert {r["stabilizer_order"] for r in rows} == {6}
    assert {r["orbit_size"] for r in rows} == {4}
    assert {r["normalized_cubic_squared"] for r in rows} == {"1/3"}


def test_landau_selector_breaks_S4_to_S3():
    s = CERT["landau_selector"]
    assert s["symmetry"] == "full S4"
    assert s["breaking"] == "S4 -> S3"
    assert s["vacuum_stabilizer"] == "S3"
    assert "four positive tetrahedral" in s["angular_vacua"]
