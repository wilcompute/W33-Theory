import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCER = ROOT / "analysis/w33_pass10946_clock_code_cone_objectwise.py"
CERT = ROOT / "data/w33_pass10946_clock_code_cone_objectwise.json"


def load():
    return json.loads(CERT.read_text(encoding="utf-8"))


def test_producer_replays():
    subprocess.run([sys.executable, str(PRODUCER)], cwd=ROOT, check=True,
                   capture_output=True, text=True, timeout=40)


def test_evaluation_code_is_exact_frozen_tetracode():
    x = load()
    assert x["status"] == "PASS_CLOCK_CODE_CONE_OBJECTWISE_THEOREM"
    t = x["tetracode"]
    assert t["evaluation_code_equals_repo_standard_exactly"] is True
    assert t["size"] == 9
    assert t["weight_enumerator"] == {"0": 1, "3": 8}
    assert len(t["four_opposite_pairs_by_omitted_clock"]) == 4
def test_four_clock_rays_are_existing_null_directions_objectwise():
    x = load()["cone_dictionary"]
    assert x["all_four_images_null"] is True
    assert x["matches_existing_M36_Hesse_null_atlas_objectwise"] is True
    assert x["M36_family_order_in_tetracode_coordinates"] == ["B", "A", "C", "D"]
    rows = x["coordinate_to_existing_geometry"]
    assert [r["symmetric_square_null_ray"] for r in rows] == [
        [1, 0, 0], [0, 0, 1], [1, 1, 1], [1, 2, 1]
    ]


def test_orientation_lift_and_s4_symmetry():
    x = load()
    lifts = x["clock_line"]["orientation_lifts"]
    assert [r["orientation_scalar"] for r in lifts] == [1, 1, 1, 2]
    s = x["symmetry"]
    assert s["GL2_order"] == 48
    assert s["distinct_monomial_tetracode_actions"] == 48
    assert s["projective_permutation_image_order"] == 24
    assert s["same_projective_permutation_has_two_global_sign_lifts"] is True
    assert s["complete_clock_calibrations"] == 24
