from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis/w33_20260923_execute_five_post_frontier_attacks.py"
FROZEN = ROOT / "data/w33_20260923_execute_five_post_frontier_attacks_frozen.json"


def load_module():
    spec = importlib.util.spec_from_file_location("w33_execute_five_post_frontier", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_execute_five_post_frontier_attacks():
    m = load_module()
    out = m.main(write=False)
    frozen = json.loads(FROZEN.read_text())

    assert out["status"] == frozen["status"]
    assert all(out["checks"].values())

    # 1. Geometric Hodge attack.
    assert out["attack1"]["spherical_embedding"]["gram_rank"] == 24
    assert out["attack1"]["metric_uniqueness"]["transvection_edge_orbit_size"] == 240
    assert out["attack1"]["spherical_embedding"]["edge_length_squared"] == "5/3"
    assert all(w > 0 for w in out["attack1"]["local_regular_tetrahedron"]["hodge_weights_numeric_k0_to3"])
    assert "not a 3-manifold" in out["attack1"]["hard_boundary"]

    # 2. Explicit minimal full-similitude completions.
    assert out["attack2"]["q5"]["dimension"] == 20
    assert out["attack2"]["q9"]["dimension"] == 72
    assert out["attack2"]["q5"]["primitive_sector_cycle_length"] == 4
    assert out["attack2"]["q9"]["primitive_sector_cycle_length"] == 8
    assert out["attack2"]["q5"]["max_generator_covariance_error"] < 1e-9
    assert out["attack2"]["q9"]["max_generator_covariance_error"] < 1e-9
    assert out["attack2"]["strict_lower_bound"] == "dim >= q(q-1), attained exactly"

    # 3. Kramers/E8 no-go.
    assert out["attack3"]["nonzero_source_bracket_pairs"]["g1_g1_to_g2"] == 810
    assert out["attack3"]["nonzero_source_bracket_pairs"]["g2_g2_to_g1"] == 810
    assert out["attack3"]["automorphism_sign_violations"] == 1620

    # 4. Physical pulse lowering and fail-closed accumulated leakage.
    assert out["attack4"]["four_tick_resources"]["raw_primitive_count"] == 20
    assert out["attack4"]["four_tick_resources"]["F3_or_inverse_traversals"] == 8
    assert out["attack4"]["four_tick_resources"]["120_degree_phase_masks"] == 12
    assert out["attack4"]["exact_matrix_checks"]["norm_UF4_minus_omegaI"] < 1e-12
    assert out["attack4"]["leakage_budget"]["admission"].startswith("FAIL_CLOSED")

    # 5. Profile likelihood.
    minimum = out["attack5"]["minimal_detected_events_for_both_three_sigma_box_errors_below_5sigma_alpha"]
    assert minimum["N"] == 87
    assert minimum["threshold_k_ge_means_allowed"] == 31
    alpha = out["attack5"]["one_sided_5sigma_alpha"]
    assert minimum["three_sigma_box_worst_allowed_to_forbidden_error"] < alpha
    assert minimum["three_sigma_box_worst_forbidden_to_allowed_error"] < alpha
    assert max(
        out["attack5"]["N128"]["three_sigma_box_worst_allowed_to_forbidden_error"],
        out["attack5"]["N128"]["three_sigma_box_worst_forbidden_to_allowed_error"],
    ) < 1e-9
