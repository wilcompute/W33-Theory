"""Pass 12684: Higgs quartic zero vs dark-dimension species scale and natural intermediate scales."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "data", "toe_pass12684_higgs_criticality_dark_dimension.json")))


def test_two_loop_running_matches_buttazzo_three_loop_fit():
    diffs = [v["diff"] for v in D["validation"]]
    assert all(abs(d) < 0.0015 for d in diffs) and max(diffs) - min(diffs) < 0.0002   # uniform offset only


def test_dark_dimension_identification_needs_heavy_top():
    lo, hi = D["Mt_window_R_1_to_30um"]["0.118"]
    assert 174.0 <= lo <= hi <= 175.0                       # vs measured 172.57 +- 0.29


def test_natural_scales():
    n = D["natural_scales"]
    assert abs(n["sqrt(v M_Pl), M_Pl = 1.2209e19"]["Mt_required"] - 172.57) < 0.1
    assert 170.7 < n["M_Pl (lambda(M_Pl) = 0)"]["Mt_required"] < 171.3
    assert 171.2 < n["M_GUT^2 / M_Pl (string SUSY-breaking, Ibanez-Valenzuela)"]["Mt_required"] < 171.7


def test_look_elsewhere_is_not_significant():
    assert 0.05 < D["look_elsewhere"]["probability_within_1sigma"] < 0.25
