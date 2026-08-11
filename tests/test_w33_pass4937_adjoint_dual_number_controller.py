"""Focused native-GAP regression for the Pass-4937 adjoint controller."""

from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "analysis" / "w33_pass4937_adjoint_dual_number_controller.g"
FROZEN = (
    ROOT / "data" / "PART_W33_PASS4937_ADJOINT_DUAL_NUMBER_CONTROLLER.json"
)
PASS_LINE = "Pass 4937 adjoint dual-number controller: 30/30 checks; status=PASS"

EXPECTED_CHECKS = {
    "affine_controller_center_order_1",
    "affine_controller_order_3061100160",
    "affine_controller_quotient_order_51840",
    "dual_kernel_law_is_addition",
    "dual_number_sp4_order_3061100160",
    "dual_sequence_split_by_constants",
    "equal_order_extensions_are_not_identical",
    "outer_similitude_multiplier_2",
    "pgsp_action_preserves_bracket",
    "pgsp_adjoint_action_order_51840",
    "pgsp_fixed_vector_space_zero",
    "pgsp_linear_centralizer_dimension_1",
    "pgsp_offset_orbit_atlas",
    "pgsp_offset_orbit_count_17",
    "pgsp_offset_orbits_partition_59049",
    "sp4_center_order_2",
    "sp4_order_51840",
    "sp_adjoint_action_kernel_order_2",
    "sp_adjoint_action_order_25920",
    "symplectic_form_preserved",
    "tangent_center_dimension_0",
    "tangent_closed_under_bracket",
    "tangent_condition_all_basis",
    "tangent_derived_dimension_10",
    "tangent_jacobi_on_basis",
    "tangent_kernel_order_59049",
    "tangent_nullity_10",
    "translation_group_elementary_abelian",
    "translation_group_order_59049",
    "translations_normal_in_controller",
}


def _assert_exact_payload(payload: dict[str, object]) -> None:
    assert payload["schema"] == "w33.pass4937.adjoint_dual_number_controller.v1"
    assert payload["status"] == "PASS"
    assert payload["inputs"] == {
        "pass_4864": (
            "Q10 is PGSp-equivariantly sp4(F3), dimension 10, "
            "center 0, derived dimension 10"
        ),
        "pass_4861": (
            "full local port matching removes S3^45 and leaves global "
            "PGSp(4,3) of order 51840"
        ),
    }

    tangent = payload["dual_number_tangent_group"]
    assert tangent == {
        "ring": "F3[epsilon]/(epsilon^2)",
        "kernel": "{I+epsilon X : X in sp4(F3)} ~= sp4(F3)^+",
        "kernel_order": 59049,
        "exact_sequence": (
            "1 -> sp4(F3)^+ -> Sp4(F3[epsilon]/epsilon^2) "
            "-> Sp4(F3) -> 1"
        ),
        "split": True,
        "multiplication": "(I+epsilon X)(I+epsilon Y)=I+epsilon(X+Y)",
        "conjugation": "g^{-1}(I+epsilon X)g=I+epsilon(g^{-1}Xg)",
        "group_order": 3061100160,
        "center_order": 2,
        "action_kernel": "the scalar center C2 of Sp4(F3)",
    }

    controller = payload["affine_pgsp_controller"]
    assert controller["group"] == "sp4(F3)^+ : PGSp(4,3)"
    assert controller["state_update"] == "v |-> v A_g + w on F3^10"
    assert controller["offset_states"] == 59049
    assert controller["frame_states"] == 51840
    assert controller["group_order"] == 3061100160
    assert controller["center_order"] == 1
    assert controller["offset_orbit_count"] == 17
    assert controller["offset_orbit_sizes"] == [
        1,
        80,
        240,
        480,
        540,
        540,
        1080,
        1080,
        4320,
        4320,
        5184,
        5184,
        5760,
        6480,
        6480,
        8640,
        8640,
    ]

    firewall = payload["extension_firewall"]
    assert isinstance(firewall, str)
    assert "equal order 3061100160 but are not isomorphic" in firewall
    assert "centers have orders 2 and 1" in firewall
    assert "not the commutator inside that abelian kernel" in firewall

    boundary = payload["boundary"]
    assert isinstance(boundary, str)
    assert "No individual HoloBox selector" in boundary
    assert "continuum gauge field" in boundary
    assert payload["checks"] == {name: True for name in EXPECTED_CHECKS}


def test_native_gap_rebuild_matches_frozen_certificate(tmp_path: Path) -> None:
    gap = shutil.which("gap")
    assert gap is not None, "native GAP is required for Pass 4937"

    completed = subprocess.run(
        [gap, "-q", "-b", str(SOURCE)],
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
        tmp_path / "data" / "PART_W33_PASS4937_ADJOINT_DUAL_NUMBER_CONTROLLER.json"
    )
    rebuilt_bytes = rebuilt.read_bytes()
    assert rebuilt_bytes == FROZEN.read_bytes()
    _assert_exact_payload(json.loads(rebuilt_bytes))
