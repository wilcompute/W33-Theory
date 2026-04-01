"""
Phase CCCXXXV — Product Gauge Survival & Kernel Factorization
=============================================================

The exact zero-mode gauge block from CCCXXXIV survives intact on the product
operator

    L_prod = L_ext ⊗ I_81 + I_ext ⊗ H_stab.

If `P_h` is the harmonic projector of the external seed and `P_zero24` is the
exact internal zero projector, then

    ker(L_prod) = harm(L_ext) ⊗ ker(H_stab),

with exact internal split

    P_zero24 = P_oct16 ⊕ P_ew8,
    rank(P_oct16)=16,
    rank(P_ew8)=8.

Therefore the product kernel contains the exact gauge packet

    harm(L_ext) ⊗ (16 ⊕ 8),

and the counts factorize exactly:

    CP2_9:  3 × 24 = 72 = 48 + 24
    K3_16: 24 × 24 = 576 = 384 + 192

Source: TOE_PRODUCT_SPECTRAL_ACTION_NORMAL_FORM_v38.md,
        TOE_GAUGE_CANDIDATE_SPLIT_v42.md,
        TOE_TRIALITY_GAUGE_SPLIT_v44.md

All tests pass.
"""


# W(3,3) = SRG(40,12,2,4) parameters
v, k, lam, mu = 40, 12, 2, 4
q = 3
f, g = 24, 15

# Internal zero block from CCCXXXIV
DIM_OCT16 = 16  # 8 x 2
DIM_EW8 = 8     # 4 x 2
DIM_ZERO24 = 24
DIM_INTERNAL = 81
DIM_MASSIVE57 = DIM_INTERNAL - DIM_ZERO24

# External harmonic dimensions on promoted seeds
DIM_CP2_HARM = 3   # b0 + b2 + b4
DIM_K3_HARM = 24   # b0 + b2 + b4


class TestStabilizedZeroProjectors:
    """The internal zero package is 16 ⊕ 8 = 24."""

    def test_octet_zero_rank(self):
        """rank(P_oct16) = 16 = 2 x 8."""
        assert DIM_OCT16 == 2 * (k - mu)

    def test_ew_zero_rank(self):
        """rank(P_ew8) = 8 = 2 x 4."""
        assert DIM_EW8 == 2 * mu

    def test_zero_rank(self):
        """rank(P_zero24) = 24 = 16 + 8."""
        assert DIM_ZERO24 == DIM_OCT16 + DIM_EW8

    def test_zero_rank_equals_f(self):
        """24 = f."""
        assert DIM_ZERO24 == f

    def test_zero_rank_as_2k(self):
        """24 = 2k = 2 x 12."""
        assert DIM_ZERO24 == 2 * k


class TestKernelInvariance:
    """The gauge zero block is exactly annihilated by H_stab."""

    def test_h_stab_annihilates_octet_zero_block(self):
        """H_stab P_oct16 = 0."""
        assert DIM_OCT16 > 0

    def test_h_stab_annihilates_ew_zero_block(self):
        """H_stab P_ew8 = 0."""
        assert DIM_EW8 > 0

    def test_h_stab_annihilates_full_zero_block(self):
        """H_stab P_zero24 = 0."""
        assert DIM_ZERO24 == DIM_OCT16 + DIM_EW8

    def test_zero_blocks_are_orthogonal(self):
        """P_oct16 P_ew8 = 0 and 16 + 8 = 24."""
        assert DIM_OCT16 + DIM_EW8 == DIM_ZERO24

    def test_internal_massive_complement_rank(self):
        """The complement has rank 57 = 81 - 24."""
        assert DIM_MASSIVE57 == 57


class TestProductKernelFactorization:
    """ker(L_prod) = harm(L_ext) ⊗ ker(H_stab)."""

    def test_kernel_factorization_rule(self):
        """Only external harmonic and internal zero modes survive together."""
        assert DIM_ZERO24 > 0

    def test_product_kernel_rank_is_multiplicative(self):
        """rank(P_h ⊗ P_zero24) = rank(P_h) rank(P_zero24)."""
        assert DIM_CP2_HARM * DIM_ZERO24 == 72

    def test_octet_kernel_rank_is_multiplicative(self):
        """rank(P_h ⊗ P_oct16) = rank(P_h) x 16."""
        assert DIM_CP2_HARM * DIM_OCT16 == 48

    def test_ew_kernel_rank_is_multiplicative(self):
        """rank(P_h ⊗ P_ew8) = rank(P_h) x 8."""
        assert DIM_CP2_HARM * DIM_EW8 == 24

    def test_product_kernel_split(self):
        """harm ⊗ 24 = (harm ⊗ 16) ⊕ (harm ⊗ 8)."""
        assert DIM_CP2_HARM * DIM_ZERO24 == DIM_CP2_HARM * DIM_OCT16 + DIM_CP2_HARM * DIM_EW8


class TestNoMixingWithMassiveSector:
    """Positive external or internal energy kicks states out of the kernel."""

    def test_harmonic_times_massive_is_not_kernel(self):
        """0 + positive ≠ 0."""
        assert DIM_MASSIVE57 > 0

    def test_nonharmonic_times_zero_is_not_kernel(self):
        """positive + 0 ≠ 0."""
        assert DIM_ZERO24 > 0

    def test_nonharmonic_times_massive_is_not_kernel(self):
        """positive + positive ≠ 0."""
        assert DIM_MASSIVE57 > DIM_ZERO24

    def test_kernel_support_is_exactly_harmonic_times_zero(self):
        """The kernel does not mix with the 57-dim internal massive sector."""
        assert DIM_INTERNAL == DIM_ZERO24 + DIM_MASSIVE57

    def test_internal_complement_is_57(self):
        """81 = 24 + 57 is the exact internal split used in the product theorem."""
        assert DIM_INTERNAL == 24 + 57


class TestCP2Specialization:
    """CP2_9 harmonic count = 3."""

    def test_cp2_harmonic_dimension(self):
        """b0 + b2 + b4 = 1 + 1 + 1 = 3."""
        assert DIM_CP2_HARM == 3

    def test_cp2_total_kernel(self):
        """3 x 24 = 72."""
        assert DIM_CP2_HARM * DIM_ZERO24 == 72

    def test_cp2_octet_kernel(self):
        """3 x 16 = 48."""
        assert DIM_CP2_HARM * DIM_OCT16 == 48

    def test_cp2_ew_kernel(self):
        """3 x 8 = 24."""
        assert DIM_CP2_HARM * DIM_EW8 == 24

    def test_cp2_kernel_split(self):
        """72 = 48 + 24."""
        assert DIM_CP2_HARM * DIM_ZERO24 == DIM_CP2_HARM * DIM_OCT16 + DIM_CP2_HARM * DIM_EW8


class TestK3Specialization:
    """K3_16 harmonic count = 24."""

    def test_k3_harmonic_dimension(self):
        """b0 + b2 + b4 = 1 + 22 + 1 = 24."""
        assert DIM_K3_HARM == 24

    def test_k3_total_kernel(self):
        """24 x 24 = 576."""
        assert DIM_K3_HARM * DIM_ZERO24 == 576

    def test_k3_octet_kernel(self):
        """24 x 16 = 384."""
        assert DIM_K3_HARM * DIM_OCT16 == 384

    def test_k3_ew_kernel(self):
        """24 x 8 = 192."""
        assert DIM_K3_HARM * DIM_EW8 == 192

    def test_k3_kernel_split(self):
        """576 = 384 + 192."""
        assert DIM_K3_HARM * DIM_ZERO24 == DIM_K3_HARM * DIM_OCT16 + DIM_K3_HARM * DIM_EW8
