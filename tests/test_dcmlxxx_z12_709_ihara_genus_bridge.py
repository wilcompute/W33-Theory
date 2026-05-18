from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcmlxxx_z12_709_ihara_genus_bridge import (  # noqa: E402
    DATA_PATH,
    RESULT_PATH,
    build_bridge,
    write_bridge,
)


def test_z12_element_has_exact_norm_709_not_709_squared() -> None:
    payload = build_bridge()
    z12 = payload["z12_unified_element"]
    ids = payload["identities"]

    assert payload["summary"]["part"] == "DCMLXXX"
    assert payload["summary"]["decimal"] == 980
    assert z12["coefficients"] == [1, 2, 6, 4]
    assert z12["algebraic_norm"] == 709
    assert z12["script_squared_norm"] == 709 * 709
    assert z12["splitting_709"]["splits_completely_in_Q_zeta12"] is True
    assert z12["splitting_709"]["minus_one_over_12"] == 59
    assert ids["z12_norm_is_709"] is True
    assert ids["script_full_norm_is_norm_squared"] is True


def test_z12_shadows_separate_exact_from_rounded_claims() -> None:
    payload = build_bridge()
    z12 = payload["z12_unified_element"]
    ids = payload["identities"]

    assert z12["identity_embedding_abs2"]["exact"] == "71 + 38*sqrt(3)"
    assert z12["identity_embedding_abs2"]["nearest_integer"] == 137
    assert z12["identity_embedding_abs2"]["is_exact_integer_137"] is False
    assert z12["eisenstein_shadow"]["as_a_plus_b_omega"] == [-1, -4]
    assert z12["eisenstein_shadow"]["norm"] == 13
    assert z12["relative_norms"]["relative_norm_to_Q_i"]["as_gaussian_integer"] == [15, 22]
    assert z12["relative_norms"]["relative_norm_to_Q_i"]["norm"] == 709
    assert z12["relative_norms"]["relative_norm_to_Q_omega"]["as_eisenstein_integer"] == [25, 28]
    assert z12["relative_norms"]["relative_norm_to_Q_omega"]["norm"] == 709
    assert ids["identity_shadow_rounds_to_137_but_is_not_exact"] is True
    assert ids["eisenstein_shadow_norm_is_13"] is True
    assert ids["relative_norms_have_norm_709"] is True


def test_709_arithmetic_curios_are_verified_locally() -> None:
    payload = build_bridge()
    z12 = payload["z12_unified_element"]
    curio = z12["prime_cube_curio"]
    ids = payload["identities"]

    assert curio["first_prime"] == 709
    assert curio["triple"] == [193, 461, 631]
    assert 709**3 == 193**3 + 461**3 + 631**3
    assert ids["prime_709_is_first_59n_plus_1_prime"] is True
    assert ids["prime_709_cube_prime_cube_identity"] is True


def test_w33_ihara_alignment_finds_secondary_709_resonance() -> None:
    payload = build_bridge()
    ihara = payload["w33_ihara_alignment"]
    ids = payload["identities"]

    assert ihara["primitive_factor_prime_support"] == [2, 3, 5, 7, 11]
    assert ihara["target_prime_intersection"] == [7]
    assert ihara["expanded_mod_709_scan"] == {
        "modulus": 709,
        "degree": 480,
        "exact_zero_coefficient_degrees": [1, 2, 479],
        "mod_zero_coefficient_degrees": [1, 2, 338, 479],
        "nonstructural_mod_zero_coefficient_degrees": [338],
        "nonstructural_nonzero_certificate_prime": 1_000_003,
        "certificate_nonzero_degrees": [338],
        "exact_zero_coefficient_count": 3,
        "mod_zero_coefficient_count": 4,
        "nonstructural_mod_zero_coefficient_count": 1,
    }
    assert ids["w33_ihara_primitive_support_excludes_13_137_709"] is True
    assert ids["w33_ihara_expanded_mod_709_has_unique_zero_coefficient"] is True


def test_spectral_genus_identity_and_axis_are_not_conflated() -> None:
    payload = build_bridge()
    genus = payload["spectral_genus"]
    ids = payload["identities"]

    assert genus["critical_line_re_n"] == "5"
    assert genus["im_H_identity_on_critical_line"] == "Im H(3+4(1/2+it)) = t"
    assert genus["genus_axis_re_n"] == "7/2"
    assert genus["genus_axis_re_s_under_n_3_plus_4s"] == "1/8"
    assert genus["axis_claim_for_n_3_plus_4s_is_false"] is True
    assert genus["H_minus_1_over_12"]["value"] == "1813/1728"
    assert genus["H_minus_1_over_12"]["denominator"] == 1728
    assert ids["spectral_genus_imaginary_identity_has_non_axis_map"] is True
    assert ids["H_minus_1_over_12_is_1813_over_1728"] is True


def test_write_and_reload() -> None:
    data_path, result_path = write_bridge()
    assert data_path == DATA_PATH
    assert result_path == RESULT_PATH

    data = json.loads(data_path.read_text(encoding="utf-8"))
    result = json.loads(result_path.read_text(encoding="utf-8"))
    assert data["summary"]["all_identities_hold"] is True
    assert result["decimal"] == 980
    assert result["status"].startswith("VERIFIED")


def test_public_index_exposes_z12_709_corrections() -> None:
    index = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    compact_index = " ".join(index.split())

    assert "Z12 709 / Ihara / Genus Bridge" in index
    assert "the exact algebraic norm is <code>709</code>" in index
    assert "squared-magnitude artifact" in index
    assert (
        "unique nonstructural expanded-coefficient resonance modulo <code>709</code> "
        "at degree <code>338</code>"
    ) in compact_index
    assert "mapping the critical line to <code>Re(n)=5</code>" in index
