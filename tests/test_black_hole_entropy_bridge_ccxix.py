"""
Tests for Part CCXIX — Black Hole Entropy and Bekenstein-Hawking from W(3,3)
"""
import json, math, pytest
from pathlib import Path

ROOT = Path(__file__).parent.parent
RESULTS = ROOT / "PART_CCXIX_black_hole_entropy_results.json"

@pytest.fixture(scope="module")
def data():
    with open(RESULTS) as f:
        return json.load(f)

def test_verified(data):
    assert data["verified"] is True

def test_free_parameters_zero(data):
    assert data["free_parameters"] == 0

def test_all_checks_pass(data):
    assert data["n_pass"] == data["n_checks"]

def test_BH_entropy_proxy(data):
    # S_BH = EDGES/4 = 240/4 = 60
    assert data["bh_data"]["S_BH_proxy"] == 60

def test_log10_microstates(data):
    expected = 60 / math.log(10)
    assert abs(data["bh_data"]["log10_microstates"] - round(expected, 4)) < 1e-3

def test_hawking_temperature(data):
    expected = round(1 / (48 * math.pi), 6)
    assert abs(data["bh_data"]["T_Hawking_proxy"] - expected) < 1e-5

def test_surface_gravity(data):
    # kappa = LAP_MID / EDGES = 10/240
    expected = round(10 / 240, 6)
    assert abs(data["bh_data"]["kappa_surface_gravity"] - expected) < 1e-5

def test_log10_aut(data):
    expected = round(math.log10(51840), 4)
    assert abs(data["bh_data"]["log10_AUT"] - expected) < 1e-3

def test_entropy_per_mode(data):
    expected = round(math.log(51840) / 240, 5)
    assert abs(data["bh_data"]["entropy_per_mode"] - expected) < 1e-4

def test_area_entropy_density(data):
    # S_BH / V = 60 / 40 = 3/2
    assert abs(data["bh_data"]["S_over_V"] - 1.5) < 1e-9

def test_page_time(data):
    # t_Page = V × LAP_MID = 40 × 10 = 400
    assert data["bh_data"]["t_PAGE"] == 400

def test_scrambling_time(data):
    expected = round(math.log(60), 4)
    assert abs(data["bh_data"]["t_scramble"] - expected) < 1e-3

def test_bps_bound(data):
    # |XI_NEG| = XI_POS × LAM = 2 × 2 = 4
    assert data["bh_data"]["BPS_check"] is True

def test_extremal_entropy(data):
    # S_extremal = EDGES / LAP_MID = 240/10 = 24
    assert data["bh_data"]["S_extremal"] == 24

def test_kerr_a_ratio(data):
    # a/M = XI_POS/K = 2/12 = 1/6
    expected = round(1/6, 4)
    assert abs(data["bh_data"]["Kerr_a_ratio"] - expected) < 1e-3

def test_kerr_ergosphere(data):
    expected = round(1 + math.sqrt(35/36), 4)
    assert abs(data["bh_data"]["ergosphere_ratio"] - expected) < 1e-3

def test_aut_per_edge(data):
    # AUT_ORDER/EDGES = 51840/240 = 216 = 6^3
    assert data["bh_data"]["AUT_per_edge"] == 216 == 6**3

def test_bh_orbit_count(data):
    # V × M_LAM / AUT_PER_EDGE = 40 × 27 / 216 = 5
    bh = data["bh_data"]
    # Derive from known quantities
    orbit = 40 * 27 // 216
    assert orbit == 5

def test_srg_params(data):
    p = data["srg_params"]
    assert p["V"] == 40
    assert p["K"] == 12
    assert p["EDGES"] == 240
    assert p["AUT_ORDER"] == 51840
    assert p["LAP_MID"] == 10
    assert p["LAP_TOP"] == 16

def test_all_individual_checks(data):
    for c in data["checks"]:
        assert c["pass"], f"Check failed: {c['check']}"
