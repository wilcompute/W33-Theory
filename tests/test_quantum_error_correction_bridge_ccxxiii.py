"""
Regression tests for Part CCXXIII: Quantum Error Correction and Holographic Codes from W(3,3).

All tests import and validate the CCXXIII QEC bridge.
SRG(40,12,2,4) with |Aut|=51840=|W(E6)|. Zero free parameters.
"""

import pytest
import sys
import json
import math
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "exploration"))
from PART_CCXXIII_QUANTUM_ERROR_CORRECTION_BRIDGE import (
    Q, V, K, LAM, MU, M_LAM, M_NEG, XI_POS, XI_NEG,
    LAP_MID, LAP_TOP, EDGES, AUT_ORDER,
    results, checks, verified,
    code_n, code_k, code_d, code_rate, redundancy,
    t_errors, detectable, p_threshold,
    stabilizers, syndrome_log2, logical_ops,
    half_legs, entropy_per_leg,
    bulk_to_boundary, recovery_threshold, complement_size,
    min_shares, max_withheld, secret_size,
    erasure_threshold, dep_threshold,
    scrambling_time, log_aut_q,
    hp_recovery, page_time, q_capacity_proxy,
)


class TestBridgeMetadata:
    def test_part_label(self):
        assert results["Part"] == "CCXXIII"

    def test_verified(self):
        assert verified is True
        assert results["Verified"] is True

    def test_zero_free_parameters(self):
        assert results["FreeParameters"] == 0

    def test_all_checks_pass(self):
        assert all(c["pass"] for c in checks)

    def test_check_count(self):
        assert len(checks) == 26


class TestSRGParameters:
    def test_Q(self):
        assert Q == 3

    def test_V(self):
        assert V == 40

    def test_K(self):
        assert K == 12

    def test_LAM(self):
        assert LAM == 2

    def test_MU(self):
        assert MU == 4

    def test_M_LAM(self):
        assert M_LAM == 27

    def test_EDGES(self):
        assert EDGES == 240

    def test_AUT_ORDER(self):
        assert AUT_ORDER == 51840


class TestQECCodeParameters:
    """Bridge 1: [[n, k, d]] = [[40, 12, 4]] stabilizer code."""

    def test_code_n_equals_V(self):
        assert code_n == V
        assert code_n == 40

    def test_code_k_equals_K(self):
        assert code_k == K
        assert code_k == 12

    def test_code_d_equals_MU(self):
        assert code_d == MU
        assert code_d == 4

    def test_code_parameters_positive(self):
        assert code_n > 0
        assert code_k > 0
        assert code_d > 0

    def test_singleton_bound(self):
        # Singleton bound: k <= n - d + 1
        assert code_k <= code_n - code_d + 1

    def test_hamming_bound_d_gte_2(self):
        # Code distance >= 2 means at least 1 error is detectable
        assert code_d >= 2


class TestCodeRateAndRedundancy:
    """Bridge 2: Code rate and redundancy."""

    def test_code_rate(self):
        assert code_rate == pytest.approx(0.3, abs=1e-9)

    def test_code_rate_formula(self):
        assert code_rate == K / V

    def test_redundancy(self):
        assert redundancy == pytest.approx(V / K, abs=1e-10)

    def test_redundancy_value(self):
        assert round(redundancy, 2) == 3.33

    def test_rate_times_n_equals_k(self):
        assert round(code_rate * code_n) == code_k


class TestErrorCorrectionCapacity:
    """Bridge 3: Error correction and detection capacity."""

    def test_t_errors(self):
        assert t_errors == 1

    def test_t_formula(self):
        assert t_errors == (code_d - 1) // 2

    def test_detectable(self):
        assert detectable == 3

    def test_detectable_formula(self):
        assert detectable == code_d - 1

    def test_detectable_greater_than_correctable(self):
        assert detectable > t_errors

    def test_error_threshold(self):
        assert p_threshold == pytest.approx(0.1, abs=1e-9)

    def test_threshold_formula(self):
        assert p_threshold == code_d / code_n


class TestStabilizerStructure:
    """Bridge 4: Stabilizer generators and syndrome space."""

    def test_stabilizer_count(self):
        assert stabilizers == 28

    def test_stabilizer_formula(self):
        assert stabilizers == V - K

    def test_syndrome_log2(self):
        assert syndrome_log2 == 28

    def test_syndrome_equals_stabilizers(self):
        assert syndrome_log2 == stabilizers

    def test_logical_ops(self):
        assert logical_ops == K
        assert logical_ops == 12

    def test_stabilizers_plus_logical_equals_n(self):
        # n = (n-k) + k
        assert stabilizers + logical_ops == code_n


class TestPerfectTensorProperties:
    """Bridge 5: Perfect tensor (HaPPY-code ingredient)."""

    def test_half_legs(self):
        assert half_legs == 6

    def test_half_legs_formula(self):
        assert half_legs == K // 2

    def test_entropy_per_leg(self):
        assert entropy_per_leg == pytest.approx(math.log(Q), abs=1e-9)

    def test_entropy_per_leg_positive(self):
        assert entropy_per_leg > 0

    def test_total_entropy_K_legs(self):
        # Total entropy for K legs = K * ln(Q)
        total = K * math.log(Q)
        assert total == pytest.approx(K * entropy_per_leg, abs=1e-9)


class TestHAPPYHolographicCode:
    """Bridge 6: HaPPY holographic code / AdS-CFT QEC."""

    def test_bulk_to_boundary(self):
        assert round(bulk_to_boundary, 2) == 3.33

    def test_bulk_to_boundary_formula(self):
        assert bulk_to_boundary == pytest.approx(V / K, abs=1e-10)

    def test_recovery_threshold(self):
        assert recovery_threshold == 13

    def test_recovery_threshold_formula(self):
        assert recovery_threshold == K + 1

    def test_complement_size(self):
        assert complement_size == M_LAM
        assert complement_size == 27

    def test_complement_formula(self):
        assert complement_size == V - recovery_threshold

    def test_threshold_plus_complement_equals_V(self):
        assert recovery_threshold + complement_size == V


class TestQuantumSecretSharing:
    """Bridge 7: Quantum secret sharing threshold scheme."""

    def test_min_shares(self):
        assert min_shares == 4
        assert min_shares == code_d

    def test_max_withheld(self):
        assert max_withheld == 36
        assert max_withheld == V - code_d

    def test_min_plus_max_equals_V(self):
        assert min_shares + max_withheld == V

    def test_secret_size(self):
        assert secret_size == K
        assert secret_size == 12


class TestQuantumChannelCapacity:
    """Bridge 8: Erasure and depolarizing channel thresholds."""

    def test_erasure_threshold(self):
        assert erasure_threshold == pytest.approx(0.05, abs=1e-10)

    def test_erasure_threshold_formula(self):
        assert erasure_threshold == code_d / (2 * code_n)

    def test_dep_threshold(self):
        assert dep_threshold == pytest.approx(0.1, abs=1e-10)

    def test_dep_threshold_formula(self):
        assert dep_threshold == code_d / code_n

    def test_dep_equals_p_threshold(self):
        assert dep_threshold == p_threshold

    def test_erasure_half_dep(self):
        assert erasure_threshold == pytest.approx(dep_threshold / 2, abs=1e-10)


class TestScramblingTime:
    """Bridge 9: Scrambling time and quantum chaos."""

    def test_scrambling_time(self):
        expected = (K / Q) * math.log(Q)
        assert scrambling_time == pytest.approx(expected, abs=1e-9)

    def test_scrambling_time_value(self):
        assert round(scrambling_time, 3) == pytest.approx(4.394, abs=0.001)

    def test_log_aut_q(self):
        expected = math.log(AUT_ORDER) / math.log(Q)
        assert log_aut_q == pytest.approx(expected, abs=1e-9)

    def test_log_aut_q_about_10(self):
        # ln(51840)/ln(3) ≈ 9.9 — near 10
        assert 9.0 < log_aut_q < 11.0


class TestHaydenPreskill:
    """Bridge 10: Hayden-Preskill recovery and Page time."""

    def test_hp_recovery(self):
        assert hp_recovery == 32

    def test_hp_recovery_formula(self):
        assert hp_recovery == code_k + V // 2

    def test_page_time(self):
        assert page_time == 20

    def test_page_time_formula(self):
        assert page_time == V // 2

    def test_q_capacity_proxy(self):
        assert q_capacity_proxy == pytest.approx(0.7, abs=1e-9)

    def test_q_capacity_formula(self):
        assert q_capacity_proxy == stabilizers / V


class TestJSONExport:
    def test_json_file_exists(self):
        json_file = Path(__file__).parent.parent / "PART_CCXXIII_quantum_error_correction_results.json"
        assert json_file.exists()

    def test_json_content(self):
        json_file = Path(__file__).parent.parent / "PART_CCXXIII_quantum_error_correction_results.json"
        with open(json_file) as f:
            data = json.load(f)
        assert data["Part"] == "CCXXIII"
        assert data["Verified"] is True
        assert len(data["Checks"]) == 26

    def test_json_bridges(self):
        json_file = Path(__file__).parent.parent / "PART_CCXXIII_quantum_error_correction_results.json"
        with open(json_file) as f:
            data = json.load(f)
        bridges = data["Bridges"]
        assert "1_code_n" in bridges
        assert "5_half_legs" in bridges
        assert "10_hp_recovery" in bridges
