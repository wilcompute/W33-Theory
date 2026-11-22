"""Pass 12692: five checks."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "data", "toe_pass12692_five_checks.json")))


def test_alpha_ew_and_km3net():
    assert D["alpha_vs_EW"]["ratio"] > 1e4
    assert 2.0 < D["km3net_flux"]["sigma"] < 2.4


def test_axiflavon_bound():
    assert 0.08 < D["axiflavon"]["C_sd_max_at_fa_1e11"] < 0.1
    assert D["axiflavon"]["C_sd=0.22"]["ma_max_ueV"] < 45


def test_vlq_rates_validated_on_ttbar():
    v = D["vlq_production_decay"]
    assert 450 < v["sigma_ttbar_LO_pb"] < 530 and 1.5 < v["K_from_ttbar"] < 1.9
    assert 5000 < v["HL_LHC_events_3ab_triplet"] < 30000 and 5e-5 < v["theta_crossover"] < 3e-4


def test_helium_neff_coincidence():
    h = D["neutron_bbn"]["helium_Neff"]["rows"]
    assert abs(h["all four"]["Neff_at_bottle_tau"] - 2.86) < 0.1
    assert h["without EMPRESS"]["Neff_at_bottle_tau"] > 2.9
