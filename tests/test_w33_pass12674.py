"""Pass 12674: effective code-space SOS (validated), degree-8 certificate to 9 digits, stabiliser types of global minimisers."""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load = lambda f: json.load(open(os.path.join(ROOT, "data", f)))
C8 = 2.4985086466880784


def test_effective_sos_validated():
    t6 = load("w33_f8_codespace_effective_sos_T_deg6.json")
    assert abs(t6["bound"] - 2.4966772779) < 1e-7 and abs(t6["effective_min"] - C8) < 1e-8
    s6 = load("w33_f8_codespace_effective_sos_S_deg6.json")
    assert abs(s6["bound"] - 2.081828) < 1e-5          # other track's PPT dual on the common code
    b6 = load("w33_f8_codespace_effective_sos_B_deg6.json")
    assert 2.47 < b6["bound"] < C8
    t8 = load("w33_f8_codespace_effective_sos_T_deg8.json")
    assert abs(t8["bound"] - C8) < 1e-7


def test_deg8_certificates():
    for C in ("4997_2000", "624627_250000", "12492543_5000000", "15615679_6250000", "1249254323_500000000"):
        d = load(f"w33_f8_codespace_deg8_certificate_{C}.json")
        assert d["certified"] and 0 < d["gap"] < 1e-5
    assert load("w33_f8_codespace_deg8_certificate_1249254323_500000000.json")["gap"] < 1e-9


def test_global_minimiser_stabiliser_types():
    d = load("w33_f8_global_minimiser_stabilisers.json")
    assert d["n_at_c8"] >= 10 and d["stabiliser_orders"] == {"4": d["n_at_c8"]} and not d["any_covered"]
    assert set(d["weight_hist_types"]) == {"[(0, 156), (1, 63), (2, 36)]", "[(0, 138), (1, 99), (2, 18)]"}
