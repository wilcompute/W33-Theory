from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcmlxxxi_heegner_ihara_gaussian_audit import (  # noqa: E402
    DATA_PATH,
    RESULT_PATH,
    build_bridge,
    write_bridge,
)


def test_correct_w33_ihara_uses_bass_11_not_degree_12() -> None:
    payload = build_bridge()
    summary = payload["summary"]
    correct = payload["correct_w33_ihara"]
    ids = payload["identities"]

    assert summary["part"] == "DCMLXXXI"
    assert summary["decimal"] == 981
    assert summary["bass_parameter"] == 11
    assert "11u^2" in correct["factorization"]
    assert "12u^2)^24" not in correct["factorization"]
    assert ids["bass_parameter_is_degree_minus_one"] is True
    assert ids["corrected_ihara_uses_11_not_12"] is True


def test_actual_ihara_fields_and_radius_are_not_the_coefficient_12_shadow() -> None:
    payload = build_bridge()
    correct = payload["correct_w33_ihara"]["nontrivial_sectors"]
    shadow = payload["coefficient_12_shadow"]["nontrivial_sectors"]
    ids = payload["identities"]

    assert [sector["discriminant"] for sector in correct] == [-40, -28]
    assert [sector["field_radicand"] for sector in correct] == [-10, -7]
    assert [sector["pole_radius_squared"] for sector in correct] == ["1/11", "1/11"]
    assert [sector["is_heegner_field"] for sector in correct] == [False, True]

    assert [sector["discriminant"] for sector in shadow] == [-44, -32]
    assert [sector["field_radicand"] for sector in shadow] == [-11, -2]
    assert [sector["pole_radius_squared"] for sector in shadow] == ["1/12", "1/12"]
    assert ids["actual_ihara_fields_are_minus_10_and_minus_7"] is True
    assert ids["only_actual_s_sector_is_heegner"] is True


def test_gaussian_division_by_137_prime_factor_fails() -> None:
    payload = build_bridge()
    gaussian = payload["gaussian_alpha_packet"]
    division = gaussian["division_160_221_by_4_11"]
    conjugate = gaussian["division_160_221_by_4_minus_11"]
    ids = payload["identities"]

    assert division["quotient_real"] == "3071/137"
    assert division["quotient_imag"] == "-876/137"
    assert division["real_remainder_mod_norm"] == 57
    assert division["imag_remainder_mod_norm"] == 83
    assert division["is_gaussian_integer"] is False
    assert conjugate["is_gaussian_integer"] is False
    assert gaussian["norm_137_divides_norm_74441"] is False
    assert ids["gaussian_division_not_integral"] is True
    assert ids["norm_137_does_not_divide_74441"] is True


def test_alpha_fraction_is_gaussian_sheet_ratio_but_not_137_multiple() -> None:
    payload = build_bridge()
    gaussian = payload["gaussian_alpha_packet"]
    primes = gaussian["primes"]
    alpha = gaussian["alpha_fraction"]
    ids = payload["identities"]

    assert primes["137"]["sum_of_two_squares"] == [4, 11]
    assert primes["4889"]["sum_of_two_squares"] == [20, 67]
    assert primes["74441"]["sum_of_two_squares"] == [160, 221]
    assert {packet["mod_12"] for packet in primes.values()} == {5}
    assert alpha["numerator_factorization"] == {3: 2, 74441: 1}
    assert alpha["denominator_factorization"] == {4889: 1}
    assert alpha["numerator_gaussian_norm"] == [480, 663]
    assert alpha["denominator_gaussian_norm"] == [20, 67]
    assert ids["gaussian_primes_share_mod_12_class"] is True
    assert ids["alpha_numerator_is_scaled_gaussian_norm"] is True


def test_public_index_exposes_heegner_ihara_audit() -> None:
    index = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    compact = " ".join(index.split())

    assert "Heegner / Ihara / Gaussian Audit" in index
    assert "Bass coefficient <code>11</code>, not <code>12</code>" in compact
    assert "not a Gaussian integer" in index
    assert "Q(&radic;-10)" in index
    assert "Q(&radic;-7)" in index


def test_write_and_reload() -> None:
    data_path, result_path = write_bridge()
    assert data_path == DATA_PATH
    assert result_path == RESULT_PATH

    data = json.loads(data_path.read_text(encoding="utf-8"))
    result = json.loads(result_path.read_text(encoding="utf-8"))
    assert data["summary"]["all_identities_hold"] is True
    assert result["decimal"] == 981
    assert result["status"].startswith("VERIFIED")
