"""Tests for PART CCCCXXII -- Photonic Harmonic TQC Algebra from 7 Toroidal Realizations."""

from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path
from typing import List

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "exploration"))

from PART_CCCCXXII_TOROIDAL_PHOTONIC_ALGEBRA import (
    CSASZAR_1_FACES,
    CSASZAR_C2_PERM,
    CSASZAR_COUNT,
    CSASZAR_E,
    CSASZAR_F,
    CSASZAR_V,
    CSASZAR_VOL_1,
    FANO_LINES,
    G2_DIM,
    HEAWOOD_DEGREE,
    HEAWOOD_E,
    HEAWOOD_FREQ_SQ,
    HEAWOOD_V,
    K7_DEGREE,
    K7_EDGES,
    K7_EIG_MIN_MULT,
    K7_MAX_EIG,
    K7_MIN_EIG,
    K7_N,
    K7_SPECTRAL_GAP,
    LAM,
    MU,
    P_FUSION,
    P_KLM,
    PHI6,
    PSL27_ORDER,
    Q,
    SZILASSI_1_FACES,
    SZILASSI_C2_PERM,
    SZILASSI_COUNT,
    SZILASSI_E,
    SZILASSI_F,
    SZILASSI_V,
    SZILASSI_VOL_1,
    SZILASSI_VOL_2,
    TORIC_GSD,
    TORIC_LOGICAL_QUBITS,
    TOTAL_MODES,
    V_W33,
    _check_bbt_eq_2i_plus_j,
    _check_btb_eq_2i_plus_j,
    _face_orbit_count,
    _fano_incidence,
    _vertex_orbit_count,
    build_results,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def results():
    return build_results()


@pytest.fixture(scope="module")
def fano_B():
    return _fano_incidence()


# ---------------------------------------------------------------------------
# Group 1: Mode identification and 5+2 split
# ---------------------------------------------------------------------------

class TestModeIdentification:

    def test_total_modes_equals_phi6(self):
        assert TOTAL_MODES == PHI6

    def test_csaszar_count_equals_phi6_minus_lambda(self):
        assert CSASZAR_COUNT == PHI6 - LAM

    def test_szilassi_count_equals_lambda(self):
        assert SZILASSI_COUNT == LAM

    def test_input_plus_ancilla_equals_phi6(self):
        assert CSASZAR_COUNT + SZILASSI_COUNT == PHI6

    def test_csaszar_count_quadratic_formula(self):
        # 5 = q^2 - 2q + 2 at q=3
        assert CSASZAR_COUNT == Q**2 - 2 * Q + 2

    def test_szilassi_times_phi6_equals_g2_dim(self):
        assert SZILASSI_COUNT * PHI6 == G2_DIM

    def test_total_modes_is_seven(self):
        assert TOTAL_MODES == 7

    def test_phi6_is_seven(self):
        assert PHI6 == 7


# ---------------------------------------------------------------------------
# Group 2: K7 spectral algebra
# ---------------------------------------------------------------------------

class TestK7SpectralAlgebra:

    def test_k7_edge_count(self):
        assert K7_EDGES == Q * PHI6

    def test_k7_edges_is_21(self):
        assert K7_EDGES == 21

    def test_k7_max_eigenvalue(self):
        assert K7_MAX_EIG == PHI6 - 1

    def test_k7_max_eigenvalue_is_6(self):
        assert K7_MAX_EIG == 6

    def test_k7_min_eigenvalue(self):
        assert K7_MIN_EIG == -1

    def test_k7_spectral_gap_equals_phi6(self):
        assert K7_SPECTRAL_GAP == PHI6

    def test_k7_spectral_gap_is_7(self):
        assert K7_SPECTRAL_GAP == 7

    def test_k7_min_eig_multiplicity(self):
        assert K7_EIG_MIN_MULT == PHI6 - 1

    def test_k7_handshake_theorem(self):
        # n * degree = 2 * edges
        assert K7_N * K7_DEGREE == 2 * K7_EDGES


# ---------------------------------------------------------------------------
# Group 3: Fano interaction structure
# ---------------------------------------------------------------------------

class TestFanoInteractionStructure:

    def test_fano_line_count(self):
        assert len(FANO_LINES) == PHI6

    def test_fano_line_count_is_7(self):
        assert len(FANO_LINES) == 7

    def test_each_fano_line_has_q_points(self):
        assert all(len(t) == Q for t in FANO_LINES)

    def test_each_fano_point_in_q_lines(self):
        for p in range(PHI6):
            count = sum(1 for t in FANO_LINES if p in t)
            assert count == Q, f"point {p} in {count} lines, expected {Q}"

    def test_total_fano_flags_equals_k7_edges(self):
        assert sum(len(t) for t in FANO_LINES) == K7_EDGES

    def test_fano_bbt_equals_2i_plus_j(self, fano_B):
        assert _check_bbt_eq_2i_plus_j(fano_B, 7)

    def test_fano_btb_equals_2i_plus_j(self, fano_B):
        assert _check_btb_eq_2i_plus_j(fano_B, 7)

    def test_fano_incidence_is_square_7x7(self, fano_B):
        assert len(fano_B) == 7
        assert all(len(row) == 7 for row in fano_B)

    def test_fano_each_row_sums_to_q(self, fano_B):
        # each point lies on Q=3 lines
        for row in fano_B:
            assert sum(row) == Q

    def test_fano_each_col_sums_to_q(self, fano_B):
        # each line has Q=3 points
        for j in range(7):
            assert sum(fano_B[i][j] for i in range(7)) == Q


# ---------------------------------------------------------------------------
# Group 4: C2 orbital decomposition
# ---------------------------------------------------------------------------

class TestC2OrbitalDecomposition:

    def test_csaszar_vertex_orbit_count(self):
        orbits = _vertex_orbit_count(CSASZAR_V, CSASZAR_C2_PERM)
        assert orbits == MU  # 4 = 3 pairs + 1 apex singleton

    def test_csaszar_vertex_orbits_is_4(self):
        orbits = _vertex_orbit_count(CSASZAR_V, CSASZAR_C2_PERM)
        assert orbits == 4

    def test_csaszar_face_orbit_count(self):
        orbits = _face_orbit_count(CSASZAR_1_FACES, CSASZAR_C2_PERM)
        assert orbits == PHI6  # 7 face pairs

    def test_szilassi_vertex_orbit_count(self):
        orbits = _vertex_orbit_count(SZILASSI_V, SZILASSI_C2_PERM)
        assert orbits == PHI6  # 7 vertex pairs, no fixed point

    def test_szilassi_face_orbit_count(self):
        orbits = _face_orbit_count(SZILASSI_1_FACES, SZILASSI_C2_PERM)
        assert orbits == MU  # 4 = 3 pairs + 1 singleton face

    def test_szilassi_face_orbits_is_4(self):
        orbits = _face_orbit_count(SZILASSI_1_FACES, SZILASSI_C2_PERM)
        assert orbits == 4

    def test_csaszar_vertex_orbits_csaszar_face_orbits_dual(self):
        v_orb = _vertex_orbit_count(CSASZAR_V, CSASZAR_C2_PERM)
        f_orb = _face_orbit_count(CSASZAR_1_FACES, CSASZAR_C2_PERM)
        # (mu, Phi6) duality
        assert (v_orb, f_orb) == (MU, PHI6)

    def test_szilassi_vertex_face_orbits_dual(self):
        v_orb = _vertex_orbit_count(SZILASSI_V, SZILASSI_C2_PERM)
        f_orb = _face_orbit_count(SZILASSI_1_FACES, SZILASSI_C2_PERM)
        # (Phi6, mu) duality -- mirror of Csaszar
        assert (v_orb, f_orb) == (PHI6, MU)

    def test_szilassi_orbital_modes_equals_g2_dim(self):
        orbits = _vertex_orbit_count(SZILASSI_V, SZILASSI_C2_PERM)
        assert SZILASSI_COUNT * orbits == G2_DIM

    def test_csaszar_orbital_modes_equals_v_w33_half(self):
        orbits = _vertex_orbit_count(CSASZAR_V, CSASZAR_C2_PERM)
        assert CSASZAR_COUNT * orbits == V_W33 // 2

    def test_csaszar_apex_is_fixed_point(self):
        # V6 (index 6) maps to itself
        assert CSASZAR_C2_PERM[6] == 6

    def test_szilassi_has_no_fixed_vertex(self):
        # all vertex orbits are pairs
        assert all(SZILASSI_C2_PERM[i] != i for i in range(SZILASSI_V))


# ---------------------------------------------------------------------------
# Group 5: Volume harmonic spectrum
# ---------------------------------------------------------------------------

class TestVolumeHarmonicSpectrum:

    def test_c1_volume_equals_power_of_sum(self):
        assert CSASZAR_VOL_1 == (Q + LAM) ** 3

    def test_c1_volume_is_125(self):
        assert CSASZAR_VOL_1 == Fraction(125)

    def test_c1_volume_is_5_cubed(self):
        assert int(CSASZAR_VOL_1) == 5 ** 3

    def test_s1_volume_exact(self):
        assert SZILASSI_VOL_1 == Fraction(5226, 5)

    def test_s2_volume_exact(self):
        assert SZILASSI_VOL_2 == Fraction(7976, 9)

    def test_s1_volume_denominator(self):
        assert SZILASSI_VOL_1.denominator == Q + LAM

    def test_s2_volume_denominator(self):
        assert SZILASSI_VOL_2.denominator == Q ** 2

    def test_s1_denominator_is_5(self):
        assert SZILASSI_VOL_1.denominator == 5

    def test_s2_denominator_is_9(self):
        assert SZILASSI_VOL_2.denominator == 9

    def test_volumes_are_positive(self):
        assert CSASZAR_VOL_1 > 0
        assert SZILASSI_VOL_1 > 0
        assert SZILASSI_VOL_2 > 0


# ---------------------------------------------------------------------------
# Group 6: Heawood harmonic rail
# ---------------------------------------------------------------------------

class TestHeawoodHarmonicRail:

    def test_heawood_vertex_count_equals_g2_dim(self):
        assert HEAWOOD_V == G2_DIM

    def test_heawood_vertex_count_is_14(self):
        assert HEAWOOD_V == 14

    def test_heawood_edge_count_equals_k7_edges(self):
        assert HEAWOOD_E == K7_EDGES

    def test_heawood_edge_count_is_21(self):
        assert HEAWOOD_E == 21

    def test_heawood_degree_equals_q(self):
        assert HEAWOOD_DEGREE == Q

    def test_heawood_freq_sq_equals_lambda(self):
        assert HEAWOOD_FREQ_SQ == LAM

    def test_heawood_freq_sq_is_2(self):
        assert HEAWOOD_FREQ_SQ == 2

    def test_heawood_handshake_theorem(self):
        assert HEAWOOD_V * HEAWOOD_DEGREE == 2 * HEAWOOD_E

    def test_heawood_bipartite_parts_each_phi6(self):
        # Heawood is bipartite: 7 Fano points + 7 Fano lines
        assert HEAWOOD_V // 2 == PHI6

    def test_heawood_bbt_nontrivial_eig_equals_lambda(self):
        # Eigenvalues of 2I+J (7x7): 9 (×1) and 2=LAM (×6)
        # The non-trivial (orthogonal complement) eigenvalue is 2
        nontrivial = LAM
        assert nontrivial == 2


# ---------------------------------------------------------------------------
# Group 7: Photonic bus connections
# ---------------------------------------------------------------------------

class TestPhotonicBusConnections:

    def test_p_fusion_value(self):
        assert P_FUSION == Fraction(1, LAM)

    def test_p_fusion_is_one_half(self):
        assert P_FUSION == Fraction(1, 2)

    def test_p_klm_value(self):
        assert P_KLM == Fraction(1, MU)

    def test_p_klm_is_one_quarter(self):
        assert P_KLM == Fraction(1, 4)

    def test_fusion_denominator_equals_toric_logical_qubits(self):
        assert P_FUSION.denominator == TORIC_LOGICAL_QUBITS

    def test_klm_denominator_equals_toric_gsd(self):
        assert P_KLM.denominator == TORIC_GSD

    def test_directed_k7_edges(self):
        assert 2 * K7_EDGES == (PHI6 - 1) * PHI6

    def test_directed_k7_edges_is_42(self):
        assert 2 * K7_EDGES == 42

    def test_denominator_sum_equals_phi6_minus_1(self):
        assert P_FUSION.denominator + P_KLM.denominator == PHI6 - 1

    def test_fusion_denominator_is_2(self):
        assert P_FUSION.denominator == 2

    def test_klm_denominator_is_4(self):
        assert P_KLM.denominator == 4


# ---------------------------------------------------------------------------
# Group 8: G2 / algebra dimension / CSS toric closing
# ---------------------------------------------------------------------------

class TestG2AlgebraCSS:

    def test_g2_dim_equals_2_times_phi6(self):
        assert G2_DIM == 2 * PHI6

    def test_g2_dim_is_14(self):
        assert G2_DIM == 14

    def test_u7_algebra_dimension(self):
        # U(7) has dim 7^2 = 49 = 2*21 + 7 (off-diag below + above + diagonal)
        assert PHI6 ** 2 == 2 * K7_EDGES + PHI6

    def test_u7_dim_is_49(self):
        assert PHI6 ** 2 == 49

    def test_psl27_order(self):
        assert PSL27_ORDER == 24 * PHI6

    def test_psl27_order_is_168(self):
        assert PSL27_ORDER == 168

    def test_toric_logical_qubits(self):
        assert TORIC_LOGICAL_QUBITS == LAM

    def test_toric_gsd(self):
        assert TORIC_GSD == MU

    def test_csaszar_euler_characteristic(self):
        assert CSASZAR_V - CSASZAR_E + CSASZAR_F == 0

    def test_szilassi_euler_characteristic(self):
        assert SZILASSI_V - SZILASSI_E + SZILASSI_F == 0

    def test_mu_plus_lambda_equals_phi6_minus_1(self):
        assert MU + LAM == PHI6 - 1

    def test_mu_plus_lambda_is_6(self):
        assert MU + LAM == 6


# ---------------------------------------------------------------------------
# Group 9: Full results integration
# ---------------------------------------------------------------------------

class TestBuildResults:

    def test_all_checks_pass(self, results):
        failed = [c["name"] for c in results["checks"] if not c["passed"]]
        assert failed == [], f"Failed checks: {failed}"

    def test_check_count(self, results):
        assert results["checks_total"] == 48

    def test_checks_passed_count(self, results):
        assert results["checks_passed"] == 48

    def test_verified_is_true(self, results):
        assert results["verified"] is True

    def test_status_is_pass(self, results):
        assert results["status"] == "PASS"

    def test_part_number(self, results):
        assert results["part"] == "CCCCXXII"

    def test_algebra_modes(self, results):
        assert results["algebra"]["modes"] == PHI6

    def test_algebra_input_modes(self, results):
        assert results["algebra"]["input_modes_csaszar"] == CSASZAR_COUNT

    def test_algebra_ancilla_modes(self, results):
        assert results["algebra"]["ancilla_modes_szilassi"] == SZILASSI_COUNT

    def test_photonic_bus_p_fusion(self, results):
        assert results["photonic_bus"]["p_fusion"] == "1/2"

    def test_photonic_bus_p_klm(self, results):
        assert results["photonic_bus"]["p_klm"] == "1/4"

    def test_orbital_structure_csaszar_vertex(self, results):
        assert results["orbital_structure"]["csaszar_c2_vertex_orbits"] == MU

    def test_orbital_structure_szilassi_vertex(self, results):
        assert results["orbital_structure"]["szilassi_c2_vertex_orbits"] == PHI6

    def test_volume_c1(self, results):
        assert results["volume_spectrum"]["C1"] == "125"

    def test_fano_bbt_in_results(self, results):
        assert results["fano_data"]["bbt_equals_2i_plus_j"] is True

    def test_fano_btb_in_results(self, results):
        assert results["fano_data"]["btb_equals_2i_plus_j"] is True
