import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCER = ROOT / "analysis/w33_pass10949_freudenthal_quasiconformal_clock_cone.py"
CERT = ROOT / "data/w33_pass10949_freudenthal_quasiconformal_clock_cone.json"


def load():
    return json.loads(CERT.read_text(encoding="utf-8"))


def test_producer_replays_and_matches_certificate():
    subprocess.run([sys.executable, str(PRODUCER)], cwd=ROOT, check=True,
                   capture_output=True, text=True, timeout=600)
    assert load()["status"] == (
        "PASS_FREUDENTHAL_QUARTIC_QUASICONFORMAL_57_CONE_AND_LORENTZIAN_CLOCK_REAL_FORM")


def test_contact56_straddles_the_clock_grading():
    b = load()["bigrading"]
    assert b["contact_minus1_56_by_clock_degree"] == {"-3": 1, "-2": 27, "-1": 27, "0": 1}
    assert b["overlap_of_contact56_and_clock54"] == 27
    assert b["verdict_on_54_plus_2"].startswith("REFUTED")


def test_heisenberg_form_is_unimodular_matching():
    h = load()["heisenberg"]
    assert abs(h["det_omega"]) == 1
    assert h["omega_is_signed_perfect_matching"] is True
    assert h["g_minus3_is_zero_so_center_is_f"] is True


def test_e7_quartic_and_freudenthal_normal_form():
    q = load()["quartic"]
    assert q["monomials"] == 1036
    assert q["content_of_ad4_polynomial"] == 6
    assert q["e7_invariance_failures"] == 0 and q["e7_root_generators_checked"] == 126
    assert q["monomial_types"] == {"XXXb": 45, "XXYY": 918, "XYab": 27, "YYYa": 45, "aabb": 1}
    fn = load()["freudenthal_normal_form"]
    assert fn["residual_monomials"] == 0 and fn["sign_repairs_needed"] == 0


def test_albert_identities_and_frames():
    a = load()["albert"]
    assert a["adjoint_identity_(X#)#=N(X)X_polynomial_failures"] == 0
    assert a["euler_identity_X.X#=3N"] is True
    assert all(v["equal_to_canonical_triads"] for v in
               a["triads_are_strongly_orthogonal_root_triples_in_layers"].values())
    assert a["split_peirce_for_each_coordinate_idempotent"]["J0_quadratic_inertia"] == [5, 5]


def test_quasiconformal_light_cone():
    c = load()["light_cone_57"]
    assert c["heisenberg_law_checks"] == 3 and c["distance_checks"] == 3
    assert c["inverted_points_in_big_cell"] == c["inversion_points"] == 6
    assert c["quasiconformal_pairs_checked"] == 15


def test_real_forms_and_tick_line_klein_group():
    r = load()["real_forms"]
    assert r["compact_automorphism_failures"] == 0
    inv = r["involutions"]
    assert inv["tick line L0 (-1)^a7"]["E8"]["name"] == "E8(-24)"
    assert inv["tick line L0 (-1)^a7"]["contact_levi_E7"]["name"] == "E7(-25)"
    height = inv["height (-1)^ht = exp(i pi rho_vee) [repo split Theta twist]"]
    assert height["E8"]["name"] == "E8(8)" and height["contact_levi_E7"]["name"] == "E7(7)"
    assert sorted(r["tick_lines"]["klein_dims"].values()) == [56, 56, 56, 80]


def test_lorentzian_peirce_slice_only_in_clock_real_form():
    j = load()["euclidean_albert_from_clock"]
    assert j["real_dimension"] == 27
    assert j["trace_form_inertia"] == [27, 0, 0]
    assert j["peirce_of_primitive_idempotent"] == {"0": 10, "1/2": 16, "1": 1}
    assert j["peirce0_determinant_inertia"] == [1, 9, 0]
    assert j["control_split_cubic_peirce0_inertia"] == [5, 5]
    assert j["tripotent_sign_split"]["committed_split_Theta"] == {"False": 15, "True": 12}


def test_visible_surfaces_are_unique():
    docs = (ROOT / "docs/index.html").read_text(encoding="utf-8")
    tail = (ROOT / "analysis/W33_SHARED_FRONTIER_TAIL.tex").read_text(encoding="utf-8")
    assert docs.count('id="pass10949-freudenthal-quasiconformal-clock-cone"') == 1
    assert tail.count("PASS10949_FREUDENTHAL_QUASICONFORMAL_CLOCK_CONE_INSERT}%") == 1
