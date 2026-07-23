from __future__ import annotations

import json
import math
from pathlib import Path

from analysis.w33_debranges_cocycle_kernel import (
    closed_defect_energy,
    hb_gap_closed,
    kernel_defect_energy,
)
from analysis.w33_norm11_local_global import (
    count_points_mod_p,
    frobenius_power_sum,
    hashimoto_power_sum,
)
from analysis.w33_prime_weight_discovery import prime_second_difference
from analysis.w33_weil_cocycle_positivity import closed_energy, gram_difference_energy

ROOT = Path(__file__).resolve().parents[1]
CERTIFICATES = (
    "w33_weil_cocycle_positivity_certificate.json",
    "w33_prime_weight_discovery_certificate.json",
    "w33_infinite_phase_operator_certificate.json",
    "w33_debranges_cocycle_kernel_certificate.json",
    "w33_norm11_local_global_certificate.json",
)


def load_certificate(name: str) -> dict:
    return json.loads((ROOT / "data" / name).read_text(encoding="utf-8"))


def test_all_five_immutable_certificates_pass():
    for name in CERTIFICATES:
        payload = load_certificate(name)
        assert payload["status"] == "PASS", name
        assert all(payload["checks"].values()), name


def test_weil_laplace_gram_identity():
    for a, delta in ((0.5, 0.0), (0.5, 0.1), (0.8, -0.2)):
        assert math.isclose(
            closed_energy(a, delta), gram_difference_energy(a, delta), rel_tol=1e-12
        )


def test_prime_second_difference_positive_in_convergence_region():
    assert prime_second_difference(1.0, 0.2) > 0
    certificate = load_certificate("w33_prime_weight_discovery_certificate.json")
    assert certificate["convergence"]["casey_boundary_sigma_1"].startswith("fails")


def test_infinite_operator_interpolates_then_fails_S8():
    certificate = load_certificate("w33_infinite_phase_operator_certificate.json")
    error = float(certificate["out_of_sample_result"]["S8_relative_error"])
    assert error > 0.4


def test_debranges_audit_separates_two_positivities():
    assert math.isclose(
        kernel_defect_energy(0.5, 0.2), closed_defect_energy(0.5, 0.2), rel_tol=1e-12
    )
    assert hb_gap_closed(0.3, 0.7, 0.2, 14.0) > 0
    certificate = load_certificate("w33_debranges_cocycle_kernel_certificate.json")
    assert certificate["checks"]["off_line_quartets_still_admit_HB_polynomials"]


def test_norm11_elliptic_local_factors_and_recurrence():
    assert count_points_mod_p(1, -1) == 10
    assert count_points_mod_p(1, 2) == 16
    for trace in (2, -4):
        for n in range(13):
            assert frobenius_power_sum(trace, n) == hashimoto_power_sum(trace, n)
