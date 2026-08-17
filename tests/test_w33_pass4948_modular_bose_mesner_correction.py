"""Focused native-GAP regression for the Pass-4948 correction theorem."""

from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "analysis" / "w33_pass4948_modular_bose_mesner_correction.g"
FROZEN = (
    ROOT / "data" / "PART_W33_PASS4948_MODULAR_BOSE_MESNER_CORRECTION.json"
)
PASS_LINE = "Pass 4948 modular Bose-Mesner correction: 30/30 checks; status=PASS"

EXPECTED_CHECKS = {
    "adjoint_action_orders_25920_51840",
    "augmentation_dimension_39",
    "augmentation_image_10_kernel_29",
    "augmentation_layers_10_19_10",
    "augmentation_nilpotent_square_zero",
    "corrected_dual_radius_interval_6_36",
    "local_port_compiler_order_6912",
    "modular_algebra_radical_dimension_1",
    "modular_bose_mesner_dimension_3_not_2",
    "modular_idempotent_ranks_only_0_1_39_40",
    "modular_minimal_polynomial_x_xplus1_squared",
    "modular_relation_A_plus_I_squared_equals_J",
    "no_modular_scheme_projector_rank_24_or_15",
    "order_1440_involution_and_order8_firewall",
    "order_1440_targets_are_split_and_AutS6",
    "pgsp_sign_twisted_hom_dimension_1",
    "pgsp_sign_twisted_intertwiner_rank_10",
    "pgsp_untwisted_hom_dimension_0",
    "point_action_orders_25920_51840",
    "psp_radical_adjoint_intertwiner_rank_10",
    "psp_radical_to_adjoint_hom_dimension_1",
    "radical_image_equals_augmentation_nilpotent_image",
    "radical_operator_rank_10_square_zero",
    "rational_projector_ranks_1_24_15",
    "rational_projectors_sum_to_identity",
    "sphere_covering_lower_bound_is_6",
    "syndrome_basis_upper_bound_is_36",
    "w33_points_40",
    "w33_srg_40_12_2_4",
    "wreath_S3_power6_semidirect_S6_order_33592320",
}


def _assert_exact_payload(payload: dict[str, object]) -> None:
    assert payload["schema"] == "w33.pass4948.modular_bose_mesner_correction.v1"
    assert payload["status"] == "PASS"
    assert payload["characteristic_zero"] == {
        "W33_spectrum": "12^1,2^24,(-4)^15",
        "projector_ranks": [1, 24, 15],
    }

    characteristic_three = payload["characteristic_three"]
    assert characteristic_three["bose_mesner_vector_space_dimension"] == 3
    assert characteristic_three["semisimple_quotient_dimension"] == 2
    assert characteristic_three["minimal_polynomial"] == "x(x+1)^2"
    assert characteristic_three["augmentation_filtration_dimensions"] == [
        10,
        29,
        39,
    ]
    assert characteristic_three["augmentation_layer_dimensions"] == [10, 19, 10]
    assert characteristic_three["scheme_idempotent_ranks"] == [0, 1, 39, 40]
    assert characteristic_three["rank_24_or_15_modular_scheme_idempotent_exists"] is False

    bridge = payload["adjoint_bridge"]
    assert bridge["Hom_PSp_dimension"] == 1
    assert bridge["intertwiner_rank"] == 10
    assert bridge["Hom_PGSp_untwisted_dimension"] == 0
    assert bridge["Hom_PGSp_sign_twisted_dimension"] == 1
    assert "outer-odd adjoint" in bridge["reading"]

    assert payload["corrected_finite_values"] == {
        "dual_radius_interval": [6, 36],
        "S3_wreath_S6_order": 33592320,
        "local_port_compiler_order": 6912,
        "order1440_groups": ["S6xC2", "Aut(S6)"],
    }
    assert payload["checks"] == {name: True for name in EXPECTED_CHECKS}

    audit = payload["audit"]
    assert audit["Pass4878"].startswith("CORRECTED")
    assert audit["Pass4879"].startswith("CORRECTED")
    assert audit["Pass4880"].startswith("WITHDRAWN")
    assert audit["Pass4881"].startswith("WITHDRAWN")
    assert audit["Pass4882"].startswith("OPEN_REFRAMED")
    boundary = payload["boundary"]
    assert "does not construct a marked-chart splitting" in boundary
    assert "does not identify a Witting graph" in boundary


def test_native_gap_rebuild_matches_frozen_certificate(tmp_path: Path) -> None:
    gap = shutil.which("gap")
    assert gap is not None, "native GAP is required for Pass 4948"

    completed = subprocess.run(
        [gap, "-q", str(SOURCE)],
        cwd=tmp_path,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=300,
    )
    assert completed.returncode == 0, completed.stdout[-6000:]
    assert PASS_LINE in completed.stdout.splitlines(), completed.stdout[-6000:]
    assert "Syntax warning" not in completed.stdout

    rebuilt = (
        tmp_path
        / "data"
        / "PART_W33_PASS4948_MODULAR_BOSE_MESNER_CORRECTION.json"
    )
    rebuilt_bytes = rebuilt.read_bytes()
    assert rebuilt_bytes == FROZEN.read_bytes()
    _assert_exact_payload(json.loads(rebuilt_bytes))
