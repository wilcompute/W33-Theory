"""Pass 12658: line-Fourier identity, F_8 regulus min F, five-qubit quotient sets, degree-6 SOS for type B."""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load = lambda f: json.load(open(os.path.join(ROOT, "data", f)))
KAPPA = 2.498508646688


def test_line_fourier_identity_and_quotients_maximal():
    d = load("w33_regulus_f8_and_quotient.json")
    assert all(v < 1e-12 for v in d["line_fourier_identity_residual"].values())
    assert len(d["quotients"]) == 6
    for r in d["quotients"]:
        assert r["Q0_p"] == 1 and r["covered"] == 279 and r["maximal"] and r["extendible_T"] == 0 and r["n_simple_eigs"] == 1
    assert {r["top_multiplicities"][2][1] for r in d["quotients"]} == {17, 27}
    assert d["pass12650_set_invariants"]["n_simple_eigs"] > 200
    assert d["control_singular_point_quotients"] == [False, False]


def test_regulus_min_f_constants():
    d = load("w33_regulus_minF_gradient.json")
    assert d["gradient_check"] < 1e-6
    assert abs(d["q2"]["min_F_times_d"] - 1) < 1e-9 and abs(d["q4"]["min_F_times_d"] - 1) < 1e-9
    assert abs(d["q8"]["min_F_times_d"] - KAPPA) < 1e-8
    low = d["q8"]["lowest"]
    assert max(low) - min(low) < 1e-12  # six starts agree


def test_quotient_sets_share_the_constant():
    d = load("w33_five_qubit_quotient_sets_minF.json")
    assert abs(d["pass12650"]["times_32"] - 1) < 1e-8
    for k in ("quotient_type27", "quotient_type17"):
        assert abs(d[k]["times_32"] - KAPPA) < 1e-8


def test_degree6_sos_typeB():
    d = load("w33_typeB_degree6_sos.json")
    assert (d["sector0_K"], d["sector0_G"]) == (51, 136)
    assert abs(d["control_two_bases"]["delta"]) < 1e-5
    assert 0.044 < d["typeB"]["delta"] < 0.0625 and d["typeB"]["status"] == "optimal"


def test_group_codes_do_not_beat_60():
    d = load("w33_shannon_group_codes.json")
    assert d["best_size"] <= 60
