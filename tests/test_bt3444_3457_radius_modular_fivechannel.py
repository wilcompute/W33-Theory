import json
from pathlib import Path

from analysis.bt3444_3457_radius_modular_fivechannel import build_certificate


ROOT = Path(__file__).resolve().parents[1]
FROZEN = ROOT / "data/PART_BT3444_BT3457_RADIUS_MODULAR_FIVECHANNEL_results.json"


def test_exact_structural_closure():
    result = build_certificate()
    assert result["status"] == "PASS"
    assert all(result["checks"].values())

    radius = result["sections"]["generalized_covering_radius"]
    assert radius["bounds"]["exact_interval"] == [389, 436]
    assert radius["bounds"]["ordinary_F243_Hamming_sphere_lower_bound"] == 347
    assert radius["local_A2_metric"]["strongly_regular_parameters"] == {
        "vertices": 59049,
        "degree": 726,
        "lambda": 243,
        "mu": 6,
        "spectrum": {"726": 1, "240": 726, "-3": 58322},
    }

    modular = result["sections"]["modular_exact_sequence"]
    assert [
        modular["face_relation_rank"],
        modular["vertex_incidence_rank"],
        modular["combined_rank"],
    ] == [240, 45, 284]
    assert modular["intersection_dimension"] == 1
    assert modular["cohomology_dimension"] == 436

    five = result["sections"]["five_channel_and_amplitudes"]
    assert five["amplitude_algebra_dimensions"] == {
        "torus_commutative": 4,
        "plus_swap": 6,
        "plus_conic_dual_sign": 8,
        "plus_swap_and_conic_dual_sign": 16,
    }
    assert five["mod3_collapse"]["order"] == 3
    assert five["mod3_collapse"]["nilpotent_ranks_N_N2_N3"] == [2, 1, 0]

    bridge = result["sections"]["S4_crosswalk"]
    assert bridge["conic"]["faithful_action_order"] == 24
    assert bridge["fano"]["point_stabilizer_order"] == 24

    product_code = result["sections"]["A2_conic_product_code"]
    assert product_code["parameters"] == "[12,6,4]_3"
    assert product_code["dual_parameters"] == "[12,6,3]_3"


def test_frozen_semantic_certificate():
    frozen = json.loads(FROZEN.read_text(encoding="utf-8"))
    assert frozen["status"] == "PASS"
    assert all(frozen["checks"].values())
    assert frozen["generalized_covering_radius"]["exact_interval"] == [389, 436]
    assert frozen["modular_exact_sequence"]["combined_rank"] == 284
    assert frozen["five_channel"]["amplitude_algebra_dimensions"] == [4, 6, 8, 16]
    assert frozen["five_channel"]["mod3_order"] == 3
    assert frozen["A2_conic_product_code"]["parameters"] == [12, 6, 4]
