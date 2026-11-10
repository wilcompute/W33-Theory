"""Pass 12644 checks (read committed JSON; regenerate with the analysis scripts)."""
import json, os
import mpmath as mp
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def load(n):
    return json.load(open(os.path.join(ROOT, "data", n)))
def test_four_qubit_certificate():
    r = load("w33_four_qubit_theta_full_dual.json")
    assert abs(r["t"] - 14) < 1e-5 and not any(a["exact_psd"] for a in r["attempts"])
    best = [x for x in r["relaxed"] if x["exact_psd"]]
    assert best and best[-1]["F_lower"] == "1999/32000"
    m = load("w33_four_qubit_mstar.json")
    assert m["disjoint"] and m["maximal"] and m["m_star"] == 1
    e = load("w33_four_qubit_theta_exact.json")
    assert e["size"] == 9 and e["n_uncovered"] == 120 and e["degree"] == 56
def test_cover_controls():
    c = load("w33_anticommuting_clique_cover.json")
    assert c["n2_size3_k2"]["verified"] and not c["n3_size5_k6"]["found"] and c["n3_size5_k7"]["verified"]
def test_shor_vacuous():
    s = load("w33_shor_pure_state_relaxation.json")
    assert abs(s["n3_size5_strong"]["shor_bound"] - 7) < 1e-6 and abs(s["n2_size3_plain"]["shor_bound"] - 3) < 1e-6
def test_nonstabiliser_values():
    r = load("w33_nonstabiliser_optimisers.json")
    mp.mp.dps = 30
    assert abs(r["pentad"]["min_F"] - float((207 - 19 * mp.sqrt(57)) / 432)) < 1e-14
    assert abs(r["d25_single_cover"]["min_F"] - 13 / 75) < 1e-14
    assert r["pentad"]["n_profiles"] == 1 and r["d25_single_cover"]["n_profiles"] == 1
