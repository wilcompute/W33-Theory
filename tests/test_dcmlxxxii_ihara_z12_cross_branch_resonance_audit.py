from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcmlxxxii_ihara_z12_cross_branch_resonance_audit import (  # noqa: E402
    DATA_PATH,
    RESULT_PATH,
    build_bridge,
    write_bridge,
)


def test_part_metadata_and_static_remote_sources_are_pinned() -> None:
    payload = build_bridge()
    summary = payload["summary"]
    sources = payload["remote_main_sources"]
    ids = payload["identities"]

    assert summary["part"] == "DCMLXXXII"
    assert summary["decimal"] == 982
    assert summary["remote_main_commit"] == "ec327312"
    assert {source["file"] for source in sources} == {
        "NOTES/BREAKTHROUGH_MAY17_2026.md",
        "NOTES/HEEGNER_IHARA_BREAKTHROUGH_MAY18_2026.md",
        "NOTES/BREAKTHROUGH21_MASTER_THEOREM_MAY18.md",
    }
    assert all(source["commit"] == "ec327312" for source in sources)
    assert ids["part_number_is_982"] is True
    assert ids["remote_sources_are_static_inputs"] is True


def test_live_bass_11_and_coefficient_12_shadow_are_separate() -> None:
    payload = build_bridge()
    live = payload["live_bass_11"]
    shadow = payload["coefficient_12_shadow"]
    ids = payload["identities"]

    assert live["degree"] == 12
    assert live["bass_parameter"] == 11
    assert "11u^2" in live["factorization"]
    assert [sector["field_radicand"] for sector in live["nontrivial_sectors"]] == [-10, -7]
    assert [sector["pole_radius_squared"] for sector in live["nontrivial_sectors"]] == ["1/11", "1/11"]
    assert [sector["is_heegner_field"] for sector in live["nontrivial_sectors"]] == [False, True]

    assert shadow["status"] == "shadow_branch_not_live_graph_zeta"
    assert shadow["coefficient"] == 12
    assert "12u^2" in shadow["factorization"]
    assert [sector["field_radicand"] for sector in shadow["nontrivial_sectors"]] == [-11, -2]
    assert [sector["pole_radius_squared"] for sector in shadow["nontrivial_sectors"]] == ["1/12", "1/12"]
    assert ids["live_bass_parameter_is_11"] is True
    assert ids["live_fields_are_minus_10_and_minus_7"] is True
    assert ids["shadow_fields_are_minus_11_and_minus_2"] is True
    assert ids["only_live_s_sector_is_heegner"] is True


def test_bass_decrement_moves_shadow_fields_to_live_fields() -> None:
    payload = build_bridge()
    decrement = payload["bass_decrement"]
    ids = payload["identities"]

    assert [(row["sector"], row["lambda"]) for row in decrement] == [("r", 2), ("s", -4)]
    assert [row["shadow_discriminant"] for row in decrement] == [-44, -32]
    assert [row["live_discriminant"] for row in decrement] == [-40, -28]
    assert [row["shadow_field_radicand"] for row in decrement] == [-11, -2]
    assert [row["live_field_radicand"] for row in decrement] == [-10, -7]
    assert [row["live_lands_in_heegner_field"] for row in decrement] == [False, True]
    assert ids["bass_decrement_moves_discriminants"] is True


def test_z12_norm_packet_preserves_exact_and_shadow_layers() -> None:
    payload = build_bridge()
    z12 = payload["z12_709_norm_packet"]
    alpha = payload["alpha_heegner_boundary"]
    ids = payload["identities"]

    assert z12["coefficients"] == [1, 2, 6, 4]
    assert z12["algebraic_norm"] == 709
    assert z12["script_squared_norm_artifact"] == 709 * 709
    assert z12["eisenstein_shadow"]["as_a_plus_b_omega"] == [-1, -4]
    assert z12["eisenstein_shadow"]["norm"] == 13
    assert z12["identity_embedding_abs2"]["exact"] == "71 + 38*sqrt(3)"
    assert z12["identity_embedding_abs2"]["nearest_integer"] == 137
    assert z12["identity_embedding_abs2"]["is_exact_integer_137"] is False
    assert z12["classification"] == {
        "709": "exact Z12 algebraic norm",
        "13": "exact Eisenstein shadow norm",
        "137": "rounded identity-sheet shadow for this Z12 element",
    }

    assert alpha["alpha_inverse"] == 137
    assert alpha["gaussian_norm"] == [11, 4]
    assert alpha["splitting_roots"]["Q_sqrt_minus_7"]
    assert alpha["splitting_roots"]["Q_sqrt_minus_11"]
    assert ids["z12_norm_is_709"] is True
    assert ids["eisenstein_shadow_norm_is_13"] is True
    assert ids["identity_shadow_rounds_to_137_but_is_not_exact"] is True
    assert ids["alpha_inverse_is_bass_mu_gaussian_norm"] is True
    assert ids["alpha_splits_on_minus_7_and_minus_11_sheets"] is True


def test_709_resonance_distinguishes_live_and_shadow_branches() -> None:
    payload = build_bridge()
    comparison = payload["z12_709_resonance_comparison"]
    live = comparison["live_bass_11_scan"]
    shadow = comparison["coefficient_12_shadow_scan"]
    ids = payload["identities"]

    assert comparison["primitive_factor_prime_support"] == [2, 3, 5, 7, 11]
    assert comparison["target_prime_intersection"] == [7]
    assert live["mod_zero_coefficient_degrees"] == [1, 2, 338, 479]
    assert live["exact_zero_coefficient_degrees"] == [1, 2, 479]
    assert live["nonstructural_mod_zero_coefficient_degrees"] == [338]
    assert live["coefficient_certificates"]["338"]["exact_zero"] is False
    assert live["coefficient_certificates"]["338"]["coefficient_mod_709"] == 0
    assert live["coefficient_certificates"]["338"]["coefficient_mod_1000003"] != 0

    assert shadow["mod_zero_coefficient_degrees"] == [1, 424, 479]
    assert shadow["exact_zero_coefficient_degrees"] == [1, 479]
    assert shadow["nonstructural_mod_zero_coefficient_degrees"] == [424]
    assert shadow["coefficient_certificates"]["424"]["exact_zero"] is False
    assert shadow["coefficient_certificates"]["424"]["coefficient_mod_709"] == 0
    assert shadow["coefficient_certificates"]["424"]["coefficient_mod_1000003"] != 0
    assert ids["primitive_support_excludes_13_137_709"] is True
    assert ids["live_709_resonance_is_degree_338"] is True
    assert ids["shadow_709_resonance_is_degree_424"] is True
    assert ids["live_and_shadow_resonances_are_distinct"] is True


def test_classical_rh_boundary_remains_open() -> None:
    payload = build_bridge()
    boundary = payload["rh_boundary"]
    ids = payload["identities"]

    assert boundary == {
        "finite_w33_graph_ihara_rh": "PROVED",
        "zeta_W_equals_riemann_zeta": "OPEN",
        "classical_riemann_hypothesis": "OPEN",
        "next_proof_target": "adelic/projective-limit identification bridge",
    }
    assert payload["summary"]["classical_rh_status"] == "OPEN"
    assert ids["classical_rh_boundary_remains_open"] is True


def test_write_and_reload() -> None:
    data_path, result_path = write_bridge()
    assert data_path == DATA_PATH
    assert result_path == RESULT_PATH

    data = json.loads(data_path.read_text(encoding="utf-8"))
    result = json.loads(result_path.read_text(encoding="utf-8"))
    assert data["summary"]["all_identities_hold"] is True
    assert result["decimal"] == 982
    assert result["status"].startswith("VERIFIED")


def test_public_index_exposes_cross_branch_audit() -> None:
    index = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    compact = " ".join(index.split())

    assert "Ihara/Z12 Cross-Branch Resonance Audit" in index
    assert "Bass-11 resonance" in index
    assert "degree <code>338</code>" in compact
    assert "coefficient-12 shadow resonance" in index
    assert "degree <code>424</code>" in compact
    assert "classical Riemann RH remains open" in compact
