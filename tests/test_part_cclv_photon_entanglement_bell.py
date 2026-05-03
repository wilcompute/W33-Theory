"""Tests for Part CCLV — Photon Entanglement and Bell Inequalities Bridge."""

import math
import pytest

from PART_CCLV_PHOTON_ENTANGLEMENT_BELL_BRIDGE import (
    Q, V, K, LAM, MU,
    epr_pair_count, bell_states_count, chsh_correlators, chsh_classical_bound,
    tsirelson_int_factor, tsirelson_sqrt_arg, tsirelson_bound_sq,
    chsh_quantum_bound_sq,
    bell_angle_denom,
    ghz_qubits, ghz_hilbert_dim, w_state_qubits,
    teleport_cbits, superdense_bits, superdense_check,
    epr_hilbert_dim, entanglement_entropy,
    e91_settings_per_party, e91_correlator_pairs,
    mermin_parties, mermin_classical_bound, mermin_quantum_max,
    schmidt_rank, schmidt_coeff_denom,
    checks, Verified,
)


def test_verified():
    assert Verified


def test_all_checks():
    failed = [lbl for lbl, v in checks if not v]
    assert failed == [], f"Failed checks: {failed}"


class TestBellStates:
    def test_epr_pair_count(self):
        assert epr_pair_count == LAM == 2

    def test_bell_states_count(self):
        assert bell_states_count == MU == 4

    def test_chsh_correlators(self):
        assert chsh_correlators == MU == 4

    def test_chsh_classical_bound(self):
        assert chsh_classical_bound == LAM == 2


class TestTsirelson:
    def test_int_factor(self):
        assert tsirelson_int_factor == LAM == 2

    def test_sqrt_arg(self):
        assert tsirelson_sqrt_arg == LAM == 2

    def test_tsirelson_value(self):
        # 2√2 ≈ 2.828
        val = tsirelson_int_factor * math.sqrt(tsirelson_sqrt_arg)
        assert abs(val - 2 * math.sqrt(2)) < 1e-12

    def test_tsirelson_squared(self):
        assert tsirelson_bound_sq == 8

    def test_quantum_bound_sq(self):
        assert chsh_quantum_bound_sq == 8

    def test_bell_angle_denom(self):
        assert bell_angle_denom == MU == 4


class TestGHZ:
    def test_ghz_qubits(self):
        assert ghz_qubits == Q == 3

    def test_ghz_hilbert_dim(self):
        assert ghz_hilbert_dim == 8

    def test_ghz_hilbert_dim_formula(self):
        assert ghz_hilbert_dim == LAM ** Q

    def test_w_state_qubits(self):
        assert w_state_qubits == Q == 3


class TestProtocols:
    def test_teleport_cbits(self):
        assert teleport_cbits == LAM == 2

    def test_superdense_bits(self):
        assert superdense_bits == LAM == 2

    def test_superdense_log2(self):
        assert superdense_check == LAM == int(math.log2(MU))

    def test_epr_hilbert_dim(self):
        assert epr_hilbert_dim == MU == 4

    def test_epr_hilbert_formula(self):
        assert epr_hilbert_dim == LAM ** LAM


class TestEntanglement:
    def test_entanglement_entropy(self):
        assert entanglement_entropy == 1

    def test_entanglement_entropy_formula(self):
        assert entanglement_entropy == int(math.log2(LAM))

    def test_schmidt_rank(self):
        assert schmidt_rank == LAM == 2

    def test_schmidt_coeff_denom(self):
        assert schmidt_coeff_denom == LAM == 2


class TestE91:
    def test_e91_settings(self):
        assert e91_settings_per_party == Q == 3

    def test_e91_correlator_pairs(self):
        assert e91_correlator_pairs == Q == 3


class TestMermin:
    def test_mermin_parties(self):
        assert mermin_parties == Q == 3

    def test_mermin_classical_bound(self):
        assert mermin_classical_bound == LAM == 2

    def test_mermin_quantum_max(self):
        assert mermin_quantum_max == MU == 4

    def test_mermin_quantum_formula(self):
        assert mermin_quantum_max == LAM ** LAM
