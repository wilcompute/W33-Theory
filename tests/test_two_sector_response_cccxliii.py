"""
Tests for PART CCCXLIII -- Eigenvalue-Graded Two-Sector Response Compiler
"""
import json
import math
import sys
from fractions import Fraction
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exploration"))
from PART_CCCXLIII_TWO_SECTOR_RESPONSE_BRIDGE import (
    V, K, LAM, MU, R_EIG, S_EIG, ABS_S,
    SECTOR_SCALE_RATIO, INTER_SECTOR_MASS_RATIO,
    M2_DIMLESS, EW_GAUGE_4, GENERATIONS, GUT_DIM, ALPHA,
    DEFAULT_TAU, DEFAULT_T, DEFAULT_S, DEFAULT_P,
    channels_from_scale, recover_scales, packet_consistent,
    max_channel_diff, build_two_sector_packets,
    r_to_s_prediction, s_to_r_prediction,
    verify_all, build_cccxliii_summary,
)


# ── Fixtures ──────────────────────────────────────────────────────────────────

KAPPA_REF = Fraction(7, 3)
LAMBDA_R = float(KAPPA_REF ** 2 * M2_DIMLESS)
LAMBDA_S = SECTOR_SCALE_RATIO * LAMBDA_R


@pytest.fixture(scope="module")
def r_packet():
    return channels_from_scale(LAMBDA_R)


@pytest.fixture(scope="module")
def s_packet():
    return channels_from_scale(LAMBDA_S)


@pytest.fixture(scope="module")
def two_packets():
    return build_two_sector_packets(LAMBDA_R)


@pytest.fixture(scope="module")
def verify_result():
    return verify_all()


@pytest.fixture(scope="module")
def summary():
    return build_cccxliii_summary()


# ── Group 1: W33 eigenvalue grading ──────────────────────────────────────────

class TestW33EigenvalueGrading:
    def test_r_eig_value(self):
        assert R_EIG == 2

    def test_s_eig_value(self):
        assert S_EIG == -4

    def test_abs_s_value(self):
        assert ABS_S == 4

    def test_abs_s_equals_two_r(self):
        assert ABS_S == 2 * R_EIG

    def test_sector_scale_ratio_value(self):
        assert SECTOR_SCALE_RATIO == 4

    def test_sector_scale_ratio_formula(self):
        assert SECTOR_SCALE_RATIO == (ABS_S // R_EIG) ** 2

    def test_inter_sector_mass_ratio(self):
        assert INTER_SECTOR_MASS_RATIO == 2

    def test_inter_mass_ratio_formula(self):
        assert INTER_SECTOR_MASS_RATIO == ABS_S // R_EIG

    def test_eigenvalue_sum_half_k(self):
        assert R_EIG + ABS_S == K // 2

    def test_m2_dimless_exact(self):
        assert M2_DIMLESS == Fraction(5049, 4)

    def test_m2_dimless_type(self):
        assert isinstance(M2_DIMLESS, Fraction)

    def test_lambda_r_positive(self):
        assert LAMBDA_R > 0

    def test_lambda_s_positive(self):
        assert LAMBDA_S > 0

    def test_lambda_s_equals_ratio_times_lambda_r(self):
        assert abs(LAMBDA_S - SECTOR_SCALE_RATIO * LAMBDA_R) < 1e-12


# ── Group 2: Packet builder ───────────────────────────────────────────────────

class TestChannelBuilder:
    def test_packet_has_mass(self, r_packet):
        assert "mass" in r_packet

    def test_packet_has_gap(self, r_packet):
        assert "gap" in r_packet

    def test_packet_has_heat_trace(self, r_packet):
        assert "heat_trace" in r_packet

    def test_packet_has_spinor_trace(self, r_packet):
        assert "spinor_trace" in r_packet

    def test_packet_has_resolvent_trace(self, r_packet):
        assert "resolvent_trace" in r_packet

    def test_packet_has_zeta(self, r_packet):
        assert "zeta" in r_packet

    def test_packet_has_samples(self, r_packet):
        assert "samples" in r_packet

    def test_mass_equals_sqrt_scale(self, r_packet):
        assert abs(r_packet["mass"] - math.sqrt(LAMBDA_R)) < 1e-12

    def test_gap_equals_twice_mass(self, r_packet):
        assert abs(r_packet["gap"] - 2.0 * r_packet["mass"]) < 1e-12

    def test_heat_trace_formula(self, r_packet):
        expected = 2.0 * math.exp(-LAMBDA_R * DEFAULT_TAU)
        assert abs(r_packet["heat_trace"] - expected) < 1e-14


# ── Group 3: R-sector self-consistency ───────────────────────────────────────

class TestRSectorConsistency:
    def test_r_packet_consistent(self, r_packet):
        assert packet_consistent(r_packet)

    def test_r_mass_scale_equals_heat_scale(self, r_packet):
        scales = recover_scales(r_packet)
        assert abs(scales["mass"] - scales["heat_trace"]) < 1e-8

    def test_r_gap_scale_equals_heat_scale(self, r_packet):
        scales = recover_scales(r_packet)
        assert abs(scales["gap"] - scales["heat_trace"]) < 1e-8

    def test_r_spinor_scale_equals_heat_scale(self, r_packet):
        scales = recover_scales(r_packet)
        assert abs(scales["spinor_trace"] - scales["heat_trace"]) < 1e-8

    def test_r_resolvent_scale_equals_heat_scale(self, r_packet):
        scales = recover_scales(r_packet)
        assert abs(scales["resolvent_trace"] - scales["heat_trace"]) < 1e-8

    def test_r_zeta_scale_equals_heat_scale(self, r_packet):
        scales = recover_scales(r_packet)
        assert abs(scales["zeta"] - scales["heat_trace"]) < 1e-8

    def test_r_all_six_scales_agree(self, r_packet):
        scales = recover_scales(r_packet)
        vals = list(scales.values())
        assert max(abs(v - vals[0]) for v in vals) < 1e-8


# ── Group 4: S-sector self-consistency ───────────────────────────────────────

class TestSSectorConsistency:
    def test_s_packet_consistent(self, s_packet):
        assert packet_consistent(s_packet)

    def test_s_mass_scale_equals_heat_scale(self, s_packet):
        scales = recover_scales(s_packet)
        assert abs(scales["mass"] - scales["heat_trace"]) < 1e-8

    def test_s_gap_scale_equals_heat_scale(self, s_packet):
        scales = recover_scales(s_packet)
        assert abs(scales["gap"] - scales["heat_trace"]) < 1e-8

    def test_s_spinor_scale_equals_heat_scale(self, s_packet):
        scales = recover_scales(s_packet)
        assert abs(scales["spinor_trace"] - scales["heat_trace"]) < 1e-8

    def test_s_resolvent_scale_equals_heat_scale(self, s_packet):
        scales = recover_scales(s_packet)
        assert abs(scales["resolvent_trace"] - scales["heat_trace"]) < 1e-8

    def test_s_zeta_scale_equals_heat_scale(self, s_packet):
        scales = recover_scales(s_packet)
        assert abs(scales["zeta"] - scales["heat_trace"]) < 1e-8

    def test_s_all_six_scales_agree(self, s_packet):
        scales = recover_scales(s_packet)
        vals = list(scales.values())
        assert max(abs(v - vals[0]) for v in vals) < 1e-8


# ── Group 5: Cross-sector coupling ───────────────────────────────────────────

class TestCrossSectorCoupling:
    def test_two_packets_returns_tuple_of_two(self, two_packets):
        r_pkt, s_pkt = two_packets
        assert r_pkt is not None and s_pkt is not None

    def test_scale_ratio_exact(self, r_packet, s_packet):
        r_scale = recover_scales(r_packet)["mass"]
        s_scale = recover_scales(s_packet)["mass"]
        assert abs(s_scale / r_scale - SECTOR_SCALE_RATIO) < 1e-8

    def test_mass_ratio_exact(self, r_packet, s_packet):
        ratio = s_packet["mass"] / r_packet["mass"]
        assert abs(ratio - INTER_SECTOR_MASS_RATIO) < 1e-10

    def test_gap_ratio_exact(self, r_packet, s_packet):
        ratio = s_packet["gap"] / r_packet["gap"]
        assert abs(ratio - INTER_SECTOR_MASS_RATIO) < 1e-10

    def test_r_to_s_forward_prediction(self, r_packet, s_packet):
        pred = r_to_s_prediction(r_packet)
        diff = max_channel_diff(pred, s_packet)
        assert diff < 1e-10

    def test_s_to_r_reverse_prediction(self, r_packet, s_packet):
        pred = s_to_r_prediction(s_packet)
        diff = max_channel_diff(pred, r_packet)
        assert diff < 1e-10

    def test_forward_mass_channel(self, r_packet, s_packet):
        pred = r_to_s_prediction(r_packet)
        assert abs(pred["mass"] - s_packet["mass"]) < 1e-10

    def test_forward_gap_channel(self, r_packet, s_packet):
        pred = r_to_s_prediction(r_packet)
        assert abs(pred["gap"] - s_packet["gap"]) < 1e-10

    def test_forward_heat_channel(self, r_packet, s_packet):
        pred = r_to_s_prediction(r_packet)
        assert abs(pred["heat_trace"] - s_packet["heat_trace"]) < 1e-10

    def test_forward_spinor_channel(self, r_packet, s_packet):
        pred = r_to_s_prediction(r_packet)
        assert abs(pred["spinor_trace"] - s_packet["spinor_trace"]) < 1e-10

    def test_forward_resolvent_channel(self, r_packet, s_packet):
        pred = r_to_s_prediction(r_packet)
        assert abs(pred["resolvent_trace"] - s_packet["resolvent_trace"]) < 1e-10

    def test_forward_zeta_channel(self, r_packet, s_packet):
        pred = r_to_s_prediction(r_packet)
        assert abs(pred["zeta"] - s_packet["zeta"]) < 1e-10

    def test_corrupted_s_fails_prediction(self, r_packet, s_packet):
        pred = r_to_s_prediction(r_packet)
        corrupt = dict(s_packet)
        corrupt["mass"] = s_packet["mass"] * 1.001
        assert max_channel_diff(pred, corrupt) > 1e-4

    def test_different_lambda_r_still_works(self):
        r2, s2 = build_two_sector_packets(1.0)
        pred_s = r_to_s_prediction(r2)
        assert max_channel_diff(pred_s, s2) < 1e-10

    def test_reverse_prediction_second_scale(self):
        r2, s2 = build_two_sector_packets(0.5)
        pred_r = s_to_r_prediction(s2)
        assert max_channel_diff(pred_r, r2) < 1e-10


# ── Group 6: SM encodings ─────────────────────────────────────────────────────

class TestSMEncodings:
    def test_r_eig_equals_lam(self):
        assert R_EIG == LAM

    def test_abs_s_equals_mu(self):
        assert ABS_S == MU

    def test_abs_s_equals_ew_gauge_4(self):
        assert ABS_S == EW_GAUGE_4

    def test_sector_scale_ratio_equals_mu(self):
        assert SECTOR_SCALE_RATIO == MU

    def test_r_eig_equals_generations_minus_1(self):
        assert R_EIG == GENERATIONS - 1

    def test_inter_mass_ratio_equals_lam(self):
        assert INTER_SECTOR_MASS_RATIO == LAM

    def test_abs_s_over_r_eig_equals_lam(self):
        assert ABS_S // R_EIG == LAM

    def test_r_eig_times_abs_s_equals_k_minus_mu(self):
        # R * |S| = 2*4 = 8 = K - MU = 12 - 4 = 8
        assert R_EIG * ABS_S == K - MU

    def test_abs_s_plus_r_eig_equals_k_half(self):
        assert ABS_S + R_EIG == K // 2


# ── Group 7: verify_all and summary ──────────────────────────────────────────

class TestVerifyAll:
    def test_verify_all_returns_tuple(self, verify_result):
        checks, passed, total = verify_result
        assert isinstance(checks, list)
        assert isinstance(passed, int)
        assert isinstance(total, int)

    def test_verify_all_total_27(self, verify_result):
        _, _, total = verify_result
        assert total == 27

    def test_verify_all_passed_27(self, verify_result):
        _, passed, _ = verify_result
        assert passed == 27

    def test_verify_all_no_failures(self, verify_result):
        checks, _, _ = verify_result
        failures = [c["name"] for c in checks if not c["passed"]]
        assert failures == []

    def test_all_checks_have_name(self, verify_result):
        checks, _, _ = verify_result
        assert all("name" in c for c in checks)

    def test_all_checks_have_passed_field(self, verify_result):
        checks, _, _ = verify_result
        assert all("passed" in c for c in checks)

    def test_summary_status_pass(self, summary):
        assert summary["status"] == "PASS"

    def test_summary_checks_pass_27(self, summary):
        assert summary["checks_pass"] == 27

    def test_summary_checks_total_27(self, summary):
        assert summary["checks_total"] == 27

    def test_summary_part_label(self, summary):
        assert summary["part"] == "CCCXLIII"

    def test_summary_has_discoveries(self, summary):
        assert len(summary["discoveries"]) >= 5

    def test_json_output_exists(self):
        out = Path(__file__).resolve().parents[1] / "PART_CCCXLIII_two_sector_response_results.json"
        assert out.exists()

    def test_json_output_valid(self):
        out = Path(__file__).resolve().parents[1] / "PART_CCCXLIII_two_sector_response_results.json"
        data = json.loads(out.read_text(encoding="utf-8"))
        assert data["status"] == "PASS"
        assert data["checks_pass"] == 27
