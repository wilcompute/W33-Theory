"""Pass 12727."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "data", "explore_pass12727_round.json")))
Fl = json.load(open(os.path.join(ROOT, "data", "explore_pass12727_firstlayer.json")))


def test_isocurvature():
    r = D["isocurvature"]["rows"][0]
    assert 5e4 < r["H_I_max"] < 5e5


def test_fifth_force():
    assert all(x["below_0p1"] for x in D["fifth_force"])


def test_radiative_brane():
    assert all(r["shift"] < -1 and 0.3 < r["magnitude"] < 2 for r in D["radiative_brane"]["rows"])


def test_first_layer():
    for c in ("prose", "code"):
        r = Fl[c]
        gap_all, gap_l0 = r["all_ternary"] - r["fp32"], r["ternary_fp_layer0"] - r["fp32"]
        assert gap_l0 < 0.35 * gap_all
