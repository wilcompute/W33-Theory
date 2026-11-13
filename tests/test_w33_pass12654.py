"""Pass 12654: five-qubit size-8 exhaustive verdict, Shannon sqrt58, E6(6) real form, trinification frames = W(3,3) lines."""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load = lambda f: json.load(open(os.path.join(ROOT, "data", f)))


def test_five_qubit_size8_none_all_orbits_complete():
    d = load("w33_five_qubit_size8_dlx_full.json")
    assert d["control_n3_size5"]["status"] == "exists" and d["control_n3_size7"]["status"] == "none"
    n = d["n5_size8"]
    assert n["status"] == "none" and n["example"] is None and len(n["per_rep"]) == 8
    assert not any(r["timeout"] for r in n["per_rep"]) and all(r["found"] is None for r in n["per_rep"])
    assert sum(r["nodes"] for r in n["per_rep"]) == n["nodes"] == 433517130
    assert load("w33_five_qubit_size7_dlx.json")["control_n5_size7"]["status"] == "none"
    assert load("w33_five_qubit_size9_verify.json")["maximal"] is True


def test_shannon_sqrt58_independently_verified():
    d = load("w33_shannon_square_long.json"); v = load("w33_shannon_square_long_verify.json")
    assert d["alpha_G2_best"] == 58 and d["verified_independent"]
    assert v["size"] == 58 and v["conflicts"] == 0 and v["GQ_axiom"] and v["Theta_lower"] > 7.6


def test_e6_split_real_form():
    d = load("w33_e6_cubic_real_form.json")
    assert d["source_files_same_polynomial"] and d["transpose_closure_residual"] < 1e-10
    assert (d["dim_k_skew"], d["dim_p_sym"]) == (36, 42) and (d["killing_positive"], d["killing_negative"]) == (42, 36)
    assert d["real_form"] == "E6(6) split"
    p = load("w33_e6_cubic_skew_stabilizer_projection.json")
    assert p["dim_g_N_signed"] == 78 and p["dim_k_N"] == 36 and 0.2 < p["projection_norm_ratio"] < 0.3


def test_trinification_frames_are_w33_lines():
    d = load("w33_trinification_frames.json")
    assert d["n_frames"] == 40 and d["n_A2"] == 120 and d["control_point_vs_line_noniso"]
    rel = [r for r in d["relations"] if r["relation"] == "(0, 0)"][0]
    assert rel["degrees"] == [12] and rel["iso_W33_lines"] and not rel["iso_W33_points"]
