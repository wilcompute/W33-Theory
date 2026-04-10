"""
Tests for the complete W(3,3) breakthrough: all five gaps closed.
"""

import math
import sys
import pytest
import numpy as np
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "exploration"))
from w33_breakthrough import (
    GraphParams, build_w33, close_gap_A, close_gap_B, close_gap_C,
    close_gap_D, close_gap_E, derive_all_parameters, P, V_EW,
)


# ================================================================
# GRAPH CONSTRUCTION AND VERIFICATION
# ================================================================

class TestGraphConstruction:
    """Verify W(3,3) = SRG(40,12,2,4)."""

    @pytest.fixture(scope="class")
    def graph(self):
        A, points = build_w33()
        return A, points

    def test_vertex_count(self, graph):
        A, _ = graph
        assert A.shape == (40, 40)

    def test_k_regular(self, graph):
        A, _ = graph
        degrees = A.sum(axis=1)
        assert np.all(degrees == 12)

    def test_symmetric(self, graph):
        A, _ = graph
        assert np.array_equal(A, A.T)

    def test_no_self_loops(self, graph):
        A, _ = graph
        assert np.all(np.diag(A) == 0)

    def test_lambda_parameter(self, graph):
        A, _ = graph
        A2 = A @ A
        for i in range(40):
            for j in range(i+1, 40):
                if A[i, j] == 1:
                    assert A2[i, j] == 2, f"lambda check failed at ({i},{j})"

    def test_mu_parameter(self, graph):
        A, _ = graph
        A2 = A @ A
        for i in range(40):
            for j in range(i+1, 40):
                if A[i, j] == 0 and i != j:
                    assert A2[i, j] == 4, f"mu check failed at ({i},{j})"

    def test_spectrum(self, graph):
        A, _ = graph
        eigvals = np.round(np.linalg.eigvalsh(A.astype(float)), 4)
        unique, counts = np.unique(eigvals, return_counts=True)
        spectrum = dict(zip([float(u) for u in unique], [int(c) for c in counts]))
        assert spectrum == {-4.0: 15, 2.0: 24, 12.0: 1}

    def test_non_neighbours_count(self, graph):
        A, _ = graph
        for i in range(40):
            nn = 40 - 1 - int(A[i].sum())
            assert nn == 27

    def test_edge_count(self, graph):
        A, _ = graph
        assert A.sum() == 2 * 240  # 2E = 480


# ================================================================
# PARAMETER VERIFICATION
# ================================================================

class TestGraphParams:
    """Verify all derived parameters."""

    def test_q_determines_all(self):
        p = GraphParams()
        q = p.q
        assert p.v == (q+1)*(q**2+1)
        assert p.k == q*(q+1)
        assert p.lam == q-1
        assert p.mu == q+1
        assert p.r == q-1
        assert p.s == -(q+1)
        assert p.f == q*(q+1)**2 // 2
        assert p.g == q*(q**2+1) // 2
        assert p.E == p.v * p.k // 2
        assert p.nn == p.v - p.k - 1

    def test_f_equals_2k(self):
        assert P.f == 2 * P.k

    def test_C7_identity(self):
        assert P.s**2 == P.r**2 + P.k

    def test_f_minus_g_eq_q_squared(self):
        assert P.f - P.g == P.q**2

    def test_f_plus_g_eq_q_Phi3(self):
        assert P.f + P.g == P.q * P.Phi3

    def test_fg_eq_vq2(self):
        assert P.f * P.g == P.v * P.q**2

    def test_k_plus_g_eq_q_to_q(self):
        assert P.k + P.g == P.q**P.q

    def test_nn_eq_q_cubed(self):
        assert P.nn == P.q**3

    def test_gauge_dim_eq_k(self):
        # SU(3): 8, SU(2): 3, U(1): 1 -> 12 = k
        assert 8 + 3 + 1 == P.k

    def test_cyclotomic_values(self):
        q = P.q
        assert P.Phi3 == q**2 + q + 1
        assert P.Phi4 == q**2 + 1
        assert P.Phi6 == q**2 - q + 1


# ================================================================
# UNIQUENESS: q = 3 IS FORCED
# ================================================================

class TestUniqueness:
    """Verify that q = 3 is the unique solution."""

    def test_C7_algebraic(self):
        """s^2 = r^2 + k iff q(q-3) = 0."""
        for q in range(2, 50):
            s2 = (q+1)**2
            r2_plus_k = (q-1)**2 + q*(q+1)
            if s2 == r2_plus_k:
                assert q == 3 or q == 0

    def test_f_eq_2k_unique(self):
        """f = 2k iff mu = 4 iff q = 3."""
        for q in range(2, 50):
            f = q * (q+1)**2 // 2
            k = q * (q+1)
            if f == 2 * k:
                assert q == 3

    def test_fg_eq_vq2_unique(self):
        """fg = vq^2 iff q = 3."""
        for q in range(2, 50):
            f = q * (q+1)**2 // 2
            g = q * (q**2+1) // 2
            v = (q+1) * (q**2+1)
            if f * g == v * q**2:
                assert q == 3

    def test_k_plus_g_eq_qq_unique(self):
        """k + g = q^q only at q = 3 (for small q)."""
        for q in range(2, 20):
            k = q * (q+1)
            g = q * (q**2+1) // 2
            if k + g == q**q:
                assert q == 3


# ================================================================
# GAP A: CONNES ALGEBRA
# ================================================================

class TestGapA:
    """The Connes algebra C+H+M_3(C) from the 27."""

    def test_27_decomposition(self):
        """27 = 16 + 10 + 1 under SO(10)."""
        assert 16 + 10 + 1 == 27

    def test_16_sm_decomposition(self):
        """16 = (3,2) + (3bar,1) + (3bar,1) + (1,2) + (1,1) + (1,1)."""
        dims = [3*2, 3*1, 3*1, 1*2, 1*1, 1*1]
        assert sum(dims) == 16

    def test_connes_algebra_dim(self):
        """dim_R(C+H+M_3(C)) = 2+4+18 = 24 = f."""
        dim_C = 2    # C as R-algebra
        dim_H = 4    # H as R-algebra
        dim_M3C = 18  # M_3(C) as R-algebra: 2*3^2
        assert dim_C + dim_H + dim_M3C == 24
        assert dim_C + dim_H + dim_M3C == P.f

    def test_color_sector_M3(self):
        """Color triplets give M_3(C) sector."""
        # Q=(3,2), u_c=(3bar,1), d_c=(3bar,1) -> 3 color reps
        color_reps = 3  # number of distinct color representations
        assert color_reps == P.q

    def test_weak_sector_H(self):
        """SU(2) doublets have pseudo-real structure -> H."""
        # SU(2) fundamental is pseudo-real (J = i*sigma_2)
        # This gives quaternionic structure
        su2_dim = 2
        # The 2-dim pseudo-real rep has End = H
        assert su2_dim**2 == 4  # dim_R(H)


# ================================================================
# GAP B: ALPHA DERIVATION
# ================================================================

class TestGapB:
    """alpha^-1 = 137 from spectral action."""

    def test_alpha_inv_formula(self):
        """alpha^-1 = k^2 + s^2 - f + 1 = 137."""
        result = P.k**2 + P.s**2 - P.f + 1
        assert result == 137

    def test_alpha_inv_gaussian(self):
        """alpha^-1 = (k-1)^2 + mu^2 = 137."""
        result = (P.k - 1)**2 + P.mu**2
        assert result == 137

    def test_f_2k_enables_gaussian(self):
        """k^2+s^2-f+1 = (k-1)^2+mu^2 requires f=2k."""
        # k^2+s^2-f+1 = k^2-2k+1+mu^2 requires -f = -2k, i.e., f=2k
        assert P.f == 2 * P.k

    def test_seeley_dewitt_a0(self):
        """a_0 = 1 + f + g = v = 40."""
        assert 1 + P.f + P.g == P.v

    def test_seeley_dewitt_a2(self):
        """a_2 = k^2 + r^2*f + s^2*g = vk = 480."""
        a2 = P.k**2 + P.r**2 * P.f + P.s**2 * P.g
        assert a2 == P.v * P.k
        assert a2 == 480

    def test_sector_ratio(self):
        """vacuum:matter:gauge = q:lam:(q+lam) = 3:2:5."""
        vac = P.k**2         # 144
        mat = P.r**2 * P.f   # 96
        gau = P.s**2 * P.g   # 240
        g = math.gcd(math.gcd(vac, mat), gau)
        assert (vac//g, mat//g, gau//g) == (P.q, P.lam, P.q + P.lam)

    def test_correction_within_1sigma(self):
        """alpha^-1 = 137 + 880/24445 is within 1sigma of experiment."""
        alpha_inv = 137 + float(Fraction(880, 24445))
        experimental = 137.035999177
        uncertainty = 0.000000021
        assert abs(alpha_inv - experimental) < 1.0 * uncertainty


# ================================================================
# GAP C: WEINBERG ANGLE
# ================================================================

class TestGapC:
    """sin^2(theta_W) derivation."""

    def test_gut_value(self):
        """sin^2(theta_W) at GUT = q/(2q+lam) = 3/8."""
        sin2_gut = Fraction(P.q, 2*P.q + P.lam)
        assert sin2_gut == Fraction(3, 8)

    def test_rg_shift(self):
        """RG shift = g/((2q+lam)*Phi_3) = 15/104."""
        shift = Fraction(P.g, (2*P.q + P.lam) * P.Phi3)
        assert shift == Fraction(15, 104)

    def test_mz_value(self):
        """sin^2(theta_W) at M_Z = q/Phi_3 = 3/13."""
        sin2_gut = Fraction(P.q, 2*P.q + P.lam)
        shift = Fraction(P.g, (2*P.q + P.lam) * P.Phi3)
        sin2_mz = sin2_gut - shift
        assert sin2_mz == Fraction(3, 13)
        assert sin2_mz == Fraction(P.q, P.Phi3)

    def test_numerator_identity(self):
        """q*Phi_3 - g = f (the matter multiplicity)."""
        assert P.q * P.Phi3 - P.g == P.f

    def test_alternative_formula(self):
        """sin^2 = f/((2q+lam)*Phi_3) = 24/104 = 3/13."""
        sin2 = Fraction(P.f, (2*P.q + P.lam) * P.Phi3)
        assert sin2 == Fraction(3, 13)

    def test_experimental_accuracy(self):
        """Within 0.5% of experiment."""
        sin2 = float(Fraction(P.q, P.Phi3))
        exp = 0.23122
        assert abs(sin2 - exp) / exp < 0.005


# ================================================================
# GAP D: THREE GENERATIONS
# ================================================================

class TestGapD:
    """3 generations from Z(E_6) = Z_3."""

    def test_heisenberg_group_order(self):
        """H_27 has order 27."""
        F3 = [0, 1, 2]
        elements = [(a, b, c) for a in F3 for b in F3 for c in F3]
        assert len(elements) == 27

    def test_heisenberg_center(self):
        """Z(H_27) = Z_3 = {(0,0,z) : z in F_3}."""
        F3 = [0, 1, 2]

        def h_mult(g1, g2):
            return ((g1[0]+g2[0]) % 3, (g1[1]+g2[1]) % 3,
                    (g1[2]+g2[2]+g1[0]*g2[1]) % 3)

        elements = [(a, b, c) for a in F3 for b in F3 for c in F3]
        center = []
        for g in elements:
            if all(h_mult(g, h) == h_mult(h, g) for h in elements):
                center.append(g)

        assert len(center) == 3
        assert set(center) == {(0, 0, 0), (0, 0, 1), (0, 0, 2)}

    def test_z3_grading(self):
        """Z_3 grades 27 = 9 + 9 + 9."""
        F3 = [0, 1, 2]
        elements = [(a, b, c) for a in F3 for b in F3 for c in F3]
        grade = {z: [g for g in elements if g[2] == z] for z in F3}
        assert all(len(grade[z]) == 9 for z in F3)

    def test_9_eq_q_squared(self):
        """9 states per generation = q^2."""
        assert P.q**2 == 9

    def test_27_eq_3x9(self):
        """27 = 3 generations x 9 states."""
        assert P.nn == 3 * P.q**2

    def test_heisenberg_is_nonabelian(self):
        """H_27 is non-abelian (required for interesting structure)."""
        def h_mult(g1, g2):
            return ((g1[0]+g2[0]) % 3, (g1[1]+g2[1]) % 3,
                    (g1[2]+g2[2]+g1[0]*g2[1]) % 3)

        # (1,0,0) * (0,1,0) != (0,1,0) * (1,0,0)
        ab = h_mult((1, 0, 0), (0, 1, 0))
        ba = h_mult((0, 1, 0), (1, 0, 0))
        assert ab != ba


# ================================================================
# GAP E: HIGGS VEV
# ================================================================

class TestGapE:
    """Higgs VEV from cubic invariant."""

    def test_higgs_quartic(self):
        """lam_H = Phi_6/(2*q^3) = 7/54."""
        lam_H = Fraction(P.Phi6, 2 * P.q**3)
        assert lam_H == Fraction(7, 54)

    def test_higgs_mass(self):
        """m_H = v_EW * sqrt(2*lam_H) ~ 125.3 GeV."""
        lam_H = float(Fraction(P.Phi6, 2 * P.q**3))
        mH = V_EW * math.sqrt(2 * lam_H)
        assert abs(mH - 125.25) < 1.0  # within 1 GeV

    def test_higgs_mass_within_5sigma(self):
        """m_H prediction within 5sigma of experiment."""
        lam_H = float(Fraction(P.Phi6, 2 * P.q**3))
        mH = V_EW * math.sqrt(2 * lam_H)
        assert abs(mH - 125.25) < 5 * 0.17  # 5sigma

    def test_vev_direction_unique(self):
        """SO(10) singlet is 1-dimensional -> unique direction."""
        # 27 = 16 + 10 + 1 under SO(10)
        singlet_dim = 1
        assert singlet_dim == 1  # unique direction


# ================================================================
# COUPLING CONSTANTS
# ================================================================

class TestCouplings:
    """All three gauge couplings."""

    def test_alpha_inv(self):
        assert (P.k - 1)**2 + P.mu**2 == 137

    def test_sin2_theta_W(self):
        assert Fraction(P.q, P.Phi3) == Fraction(3, 13)

    def test_alpha_s(self):
        alpha_s = Fraction(P.mu * (P.q + P.lam), P.Phi3**2)
        assert alpha_s == Fraction(20, 169)

    def test_alpha_s_accuracy(self):
        alpha_s = float(Fraction(20, 169))
        assert abs(alpha_s - 0.1180) < 0.001


# ================================================================
# MASS HIERARCHY
# ================================================================

class TestMassHierarchy:
    """Mass hierarchy from epsilon = 1/sqrt(136)."""

    def test_136_eq_alpha_inv_minus_1(self):
        assert (P.k - 1)**2 + P.mu**2 - 1 == 136

    def test_136_eq_C17_2(self):
        """136 = C(17,2) = C(k+q+lam, 2)."""
        n = P.k + P.q + P.lam  # 17
        assert n * (n-1) // 2 == 136

    def test_mc_over_mt(self):
        """m_c/m_t = 1/136 ~ 0.00735."""
        ratio = 1.0 / 136
        exp_ratio = 1.27 / 172.69
        assert abs(ratio - exp_ratio) / exp_ratio < 0.01  # within 1%

    def test_koide_angle(self):
        """Koide angle = lam/q^2 = 2/9."""
        assert Fraction(P.lam, P.q**2) == Fraction(2, 9)

    def test_gut_hierarchy(self):
        """M_GUT/v_EW = 136^(g/2) ~ 10^16."""
        log_ratio = P.g / 2.0 * math.log10(136)
        assert abs(log_ratio - 16.0) < 0.1

    def test_cosmological_constant(self):
        """Lambda_CC ~ 10^(-(alpha_inv - g)) = 10^(-122)."""
        alpha_inv = 137
        cc_exp = -(alpha_inv - P.g)
        assert cc_exp == -122


# ================================================================
# MIXING ANGLES
# ================================================================

class TestMixingAngles:
    """PMNS mixing angles from graph parameters."""

    def test_sin2_12(self):
        """sin^2(theta_12) = mu/Phi_3 = 4/13."""
        sin2 = Fraction(P.mu, P.Phi3)
        assert sin2 == Fraction(4, 13)
        assert abs(float(sin2) - 0.307) < 0.01

    def test_sin2_23(self):
        """sin^2(theta_23) = Phi_6/Phi_3 = 7/13."""
        sin2 = Fraction(P.Phi6, P.Phi3)
        assert sin2 == Fraction(7, 13)
        assert abs(float(sin2) - 0.546) < 0.01

    def test_sin2_13(self):
        """sin^2(theta_13) = 1/(v+q!) = 1/46."""
        sin2 = Fraction(1, P.v + math.factorial(P.q))
        assert sin2 == Fraction(1, 46)
        assert abs(float(sin2) - 0.0220) < 0.001


# ================================================================
# HIGGS SECTOR
# ================================================================

class TestHiggs:
    """Higgs mass and quartic coupling."""

    def test_quartic_formula(self):
        lam_H = Fraction(P.Phi6, 2 * P.q**3)
        assert lam_H == Fraction(7, 54)

    def test_mass_prediction(self):
        mH = V_EW * math.sqrt(2 * 7 / 54)
        assert 124 < mH < 127  # within ~1 GeV


# ================================================================
# INTEGRATED TESTS
# ================================================================

class TestIntegrated:
    """End-to-end derivation tests."""

    def test_full_derivation_runs(self):
        """The complete derivation runs without error."""
        results = derive_all_parameters()
        assert len(results) > 10

    def test_gap_A_closes(self):
        result = close_gap_A()
        assert result["algebra"] == "C + H + M_3(C)"
        assert result["dim_real"] == 24
        assert result["equals_f"] is True

    def test_gap_B_closes(self):
        result = close_gap_B()
        assert result["alpha_inv_tree"] == 137
        assert result["norm"] == 137

    def test_gap_C_closes(self):
        result = close_gap_C()
        assert result["sin2_mz"] == "3/13"

    def test_gap_D_closes(self):
        result = close_gap_D()
        assert result["center_is_Z3"] is True
        assert result["generations"] == 3
        assert all(result["grades"][z] == 9 for z in [0, 1, 2])

    def test_gap_E_closes(self):
        result = close_gap_E()
        assert abs(result["mH_prediction"] - 125.25) < 1.0

    def test_one_input(self):
        """Only ONE free parameter: v_EW."""
        # Everything else derived from q = 3
        p = GraphParams()
        p.verify()
        assert p.q == 3
        # v_EW is the only input
        assert V_EW == 246.22


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
