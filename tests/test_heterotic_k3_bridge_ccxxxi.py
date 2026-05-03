"""
Part CCXXXI — Heterotic String Compactification on K3 from W(3,3)
==================================================================

Heterotic E₈×E₈ string theory compactified on the K3 surface.
Every numerical invariant — Hodge numbers, Betti numbers, Euler
characteristic, signature, standard embedding ranks, instanton numbers,
Wilson line moduli count, 6D supersymmetry charges, spacetime dimensions,
and the anomaly-cancellation identity — is derived with zero free parameters
from the SRG(40,12,2,4) constants.

Key bridges:
  B1: dim(E₈×E₈) = 496 = 2·(EDGES + 2·MU)
  B2: h¹¹(K3) = 20 = V//2; b₂(K3) = 22 = V//2 + LAM
  B3: χ(K3) = 24 = K·LAM
  B4: b₂⁺ = Q = 3; σ(K3) = −16 = −LAP_TOP
  B5: rank(E₆) + rank(SU(3)) = 8 = 2·MU = rank(E₈)
  B6: instanton per E₈ = 12 = K; total = 24 = χ(K3)
  B7: Wilson line moduli = 16 = LAP_TOP per E₈
  B8: 6D supercharges = 8 = 2·MU
  B9: d_het = 10; d_K3 = 4 = MU; d_external = 6
  B10: anomaly cancellation dim = 496

All 33 bridge checks pass; Verified = True.
"""

import math
import pytest

from PART_CCXXXI_HETEROTIC_K3_BRIDGE import (
    # SRG constants (via import chain)
    Q, V, K, LAM, MU, M_LAM,
    LAP_MID, LAP_TOP, EDGES,
    # Bridge 1: E₈×E₈ gauge group
    dim_E8_one, dim_E8xE8, dim_E8xE8_half,
    # Bridge 2: K3 Hodge numbers
    h11_K3, h20_K3, h21_K3, b2_K3, b2_K3_srg,
    # Bridge 3: Betti + Euler
    b0_K3, b2_full, b4_K3, chi_K3, chi_K3_srg,
    # Bridge 4: K3 signature
    b2_plus_K3, b2_minus_K3, b2_minus_check, sigma_K3,
    # Bridge 5: standard embedding
    rank_E6, rank_SU3, rank_E8, rank_std_embed,
    # Bridge 6: instanton numbers
    inst_per_E8, inst_total,
    # Bridge 7: Wilson line moduli
    wilson_per_E8, wilson_total,
    # Bridge 8: 6D SUSY
    susy_6D, susy_6D_alt,
    # Bridge 9: spacetime dimensions
    d_het, d_K3, d_external_K3, d_external_srg,
    # Bridge 10: anomaly cancellation
    anom_cancel, anom_cancel_ratio,
    # Verification
    checks, Verified,
)


# ═══════════════════════════════════════════════════════════════
# T0: BRIDGE METADATA
# ═══════════════════════════════════════════════════════════════
class TestBridgeMetadata:
    def test_verified_flag(self):
        assert Verified is True

    def test_all_33_checks_pass(self):
        passed = sum(1 for _, v in checks if v)
        assert passed == 33

    def test_no_failed_checks(self):
        failed = [lbl for lbl, v in checks if not v]
        assert failed == [], f"Failed: {failed}"

    def test_check_count(self):
        assert len(checks) == 33


# ═══════════════════════════════════════════════════════════════
# T1: SRG PARAMETERS
# ═══════════════════════════════════════════════════════════════
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

    def test_EDGES(self):
        assert EDGES == 240

    def test_LAP_TOP(self):
        assert LAP_TOP == 16

    def test_LAP_MID(self):
        assert LAP_MID == 10

    def test_M_LAM(self):
        assert M_LAM == 27

    def test_K_times_LAM(self):
        # χ(K3) seed
        assert K * LAM == 24


# ═══════════════════════════════════════════════════════════════
# T2: E₈×E₈ GAUGE GROUP (Bridge 1)
# ═══════════════════════════════════════════════════════════════
class TestE8xE8GaugeGroup:
    def test_dim_E8_one_value(self):
        assert dim_E8_one == 248

    def test_dim_E8_one_formula(self):
        assert dim_E8_one == EDGES + 2 * MU

    def test_dim_E8xE8_value(self):
        assert dim_E8xE8 == 496

    def test_dim_E8xE8_formula(self):
        assert dim_E8xE8 == 2 * (EDGES + 2 * MU)

    def test_dim_E8xE8_half(self):
        assert dim_E8xE8_half == 248

    def test_dim_E8xE8_is_twice_E8(self):
        assert dim_E8xE8 == 2 * dim_E8_one


# ═══════════════════════════════════════════════════════════════
# T3: K3 HODGE NUMBERS (Bridge 2)
# ═══════════════════════════════════════════════════════════════
class TestK3HodgeNumbers:
    def test_h11_value(self):
        assert h11_K3 == 20

    def test_h11_formula(self):
        assert h11_K3 == V // 2

    def test_h20_value(self):
        assert h20_K3 == 1

    def test_h21_value(self):
        """K3 is rigid — no complex structure deformations."""
        assert h21_K3 == 0

    def test_b2_K3_value(self):
        assert b2_K3 == 22

    def test_b2_K3_srg_formula(self):
        assert b2_K3 == V // 2 + LAM

    def test_b2_K3_hodge_sum(self):
        """b₂ = h²⁰ + h¹¹ + h⁰² = 1 + 20 + 1."""
        assert b2_K3 == h20_K3 + h11_K3 + h20_K3

    def test_b2_srg_matches_hodge(self):
        assert b2_K3 == b2_K3_srg


# ═══════════════════════════════════════════════════════════════
# T4: K3 BETTI NUMBERS AND EULER CHARACTERISTIC (Bridge 3)
# ═══════════════════════════════════════════════════════════════
class TestK3BettiEuler:
    def test_b0_value(self):
        assert b0_K3 == 1

    def test_b2_full_value(self):
        assert b2_full == 22

    def test_b4_value(self):
        assert b4_K3 == 1

    def test_chi_K3_value(self):
        assert chi_K3 == 24

    def test_chi_K3_formula(self):
        assert chi_K3 == K * LAM

    def test_chi_K3_betti_sum(self):
        assert b0_K3 + b2_full + b4_K3 == 24

    def test_chi_K3_srg(self):
        assert chi_K3 == chi_K3_srg


# ═══════════════════════════════════════════════════════════════
# T5: K3 SIGNATURE (Bridge 4)
# ═══════════════════════════════════════════════════════════════
class TestK3Signature:
    def test_b2_plus_value(self):
        assert b2_plus_K3 == 3

    def test_b2_plus_is_Q(self):
        assert b2_plus_K3 == Q

    def test_b2_minus_value(self):
        assert b2_minus_K3 == 19

    def test_b2_minus_formula(self):
        """b₂⁻ = b₂ − b₂⁺ = 22 − 3 = 19 = LAP_TOP + Q."""
        assert b2_minus_K3 == LAP_TOP + Q

    def test_b2_minus_check_match(self):
        assert b2_minus_K3 == b2_minus_check

    def test_sigma_K3_value(self):
        assert sigma_K3 == -16

    def test_sigma_K3_neg_LAP_TOP(self):
        assert sigma_K3 == -LAP_TOP


# ═══════════════════════════════════════════════════════════════
# T6: STANDARD EMBEDDING (Bridge 5)
# ═══════════════════════════════════════════════════════════════
class TestStandardEmbedding:
    def test_rank_E6(self):
        assert rank_E6 == 6

    def test_rank_E6_formula(self):
        assert rank_E6 == K // 2

    def test_rank_SU3_is_LAM(self):
        assert rank_SU3 == LAM

    def test_rank_SU3_value(self):
        assert rank_SU3 == 2

    def test_rank_E8_is_2MU(self):
        assert rank_E8 == 2 * MU

    def test_rank_E8_value(self):
        assert rank_E8 == 8

    def test_rank_std_embed_equals_E8(self):
        assert rank_std_embed == rank_E8

    def test_rank_embed_sum(self):
        """rank(E₆) + rank(SU(3)) = rank(E₈)."""
        assert rank_E6 + rank_SU3 == rank_E8


# ═══════════════════════════════════════════════════════════════
# T7: INSTANTON NUMBERS (Bridge 6)
# ═══════════════════════════════════════════════════════════════
class TestInstantonNumbers:
    def test_inst_per_E8_value(self):
        assert inst_per_E8 == 12

    def test_inst_per_E8_is_K(self):
        assert inst_per_E8 == K

    def test_inst_per_E8_half_chi(self):
        assert inst_per_E8 == chi_K3 // 2

    def test_inst_total_value(self):
        assert inst_total == 24

    def test_inst_total_is_chi_K3(self):
        assert inst_total == chi_K3

    def test_inst_total_is_K_LAM(self):
        assert inst_total == K * LAM

    def test_instanton_split_equal(self):
        """Equal split between the two E₈ factors."""
        assert inst_per_E8 * 2 == inst_total


# ═══════════════════════════════════════════════════════════════
# T8: WILSON LINE MODULI (Bridge 7)
# ═══════════════════════════════════════════════════════════════
class TestWilsonLineModuli:
    def test_wilson_per_E8_value(self):
        assert wilson_per_E8 == 16

    def test_wilson_per_E8_is_LAP_TOP(self):
        assert wilson_per_E8 == LAP_TOP

    def test_wilson_total_value(self):
        assert wilson_total == 32

    def test_wilson_total_is_2_LAP_TOP(self):
        assert wilson_total == 2 * LAP_TOP

    def test_wilson_total_double_per_E8(self):
        assert wilson_total == 2 * wilson_per_E8


# ═══════════════════════════════════════════════════════════════
# T9: 6D SUPERSYMMETRY (Bridge 8)
# ═══════════════════════════════════════════════════════════════
class TestSUSY6D:
    def test_susy_6D_value(self):
        assert susy_6D == 8

    def test_susy_6D_is_2MU(self):
        assert susy_6D == 2 * MU

    def test_susy_6D_alt_value(self):
        assert susy_6D_alt == 2

    def test_susy_6D_is_rank_E8(self):
        assert susy_6D == rank_E8


# ═══════════════════════════════════════════════════════════════
# T10: SPACETIME DIMENSIONS (Bridge 9)
# ═══════════════════════════════════════════════════════════════
class TestSpacetimeDimensions:
    def test_d_het_value(self):
        assert d_het == 10

    def test_d_het_is_LAP_MID(self):
        assert d_het == LAP_MID

    def test_d_K3_value(self):
        assert d_K3 == 4

    def test_d_K3_is_MU(self):
        assert d_K3 == MU

    def test_d_external_K3_value(self):
        assert d_external_K3 == 6

    def test_d_external_is_rank_E6(self):
        assert d_external_K3 == rank_E6

    def test_d_external_srg_formula(self):
        assert d_external_srg == K // 2

    def test_dimension_budget(self):
        """d_het = d_K3 + d_external."""
        assert d_het == d_K3 + d_external_K3


# ═══════════════════════════════════════════════════════════════
# T11: ANOMALY CANCELLATION (Bridge 10)
# ═══════════════════════════════════════════════════════════════
class TestAnomalyCancellation:
    def test_anom_cancel_value(self):
        assert anom_cancel == 496

    def test_anom_cancel_is_dim_E8xE8(self):
        assert anom_cancel == dim_E8xE8

    def test_anom_cancel_ratio_value(self):
        assert anom_cancel_ratio == 2

    def test_anom_cancel_ratio_formula(self):
        assert anom_cancel == 2 * dim_E8_one
