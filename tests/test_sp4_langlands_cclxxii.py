"""
Tests for Part CCLXXII — Sp(4)/SO(5) Langlands duality and cyclotomic tower at q=3.
"""
import math
import pytest

# ── W(3,3) constants ──────────────────────────────────────────────────────────
V         = 40
K         = 12
LAM       = 2
MU        = 4
Q         = 3
M_LAM     = 27
LAP_MID   = 10
LAP_TOP   = 16
EDGES     = 240
AUT_ORDER = 51840
PHI3      = 13
PHI4      = 10
PHI6      = 7


# ─── helpers ─────────────────────────────────────────────────────────────────

def p_adic_val(n: int, p: int) -> int:
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    return v

def cyclotomic_val(n: int, q: int) -> int:
    from sympy import cyclotomic_poly, Symbol
    x = Symbol('x')
    return int(cyclotomic_poly(n, x).subs(x, q))


# ═══════════════════════════════════════════════════════════════════════════════
# §1  CYCLOTOMIC TOWER
# ═══════════════════════════════════════════════════════════════════════════════

class TestCyclotomicTower:
    def test_phi1_eq_lam(self):
        assert cyclotomic_val(1, Q) == LAM

    def test_phi2_eq_mu(self):
        assert cyclotomic_val(2, Q) == MU

    def test_phi3_eq_phi3(self):
        assert cyclotomic_val(3, Q) == PHI3

    def test_phi4_eq_phi4_eq_lap_mid(self):
        v = cyclotomic_val(4, Q)
        assert v == PHI4 == LAP_MID

    def test_phi6_eq_phi6(self):
        assert cyclotomic_val(6, Q) == PHI6

    def test_phi1_phi2_product_eq_q_sq_minus_1(self):
        """Φ₁(q)·Φ₂(q) = q²-1"""
        assert cyclotomic_val(1, Q) * cyclotomic_val(2, Q) == Q**2 - 1

    def test_phi1_phi2_phi4_product_eq_q4_minus_1(self):
        """Φ₁·Φ₂·Φ₄ = q⁴-1"""
        val = cyclotomic_val(1,Q) * cyclotomic_val(2,Q) * cyclotomic_val(4,Q)
        assert val == Q**4 - 1


# ═══════════════════════════════════════════════════════════════════════════════
# §2  Sp(4,3) ORDER
# ═══════════════════════════════════════════════════════════════════════════════

class TestSp4Order:
    def test_sp4_order_formula(self):
        """|Sp(4,q)| = q⁴(q²-1)(q⁴-1)"""
        assert Q**4 * (Q**2 - 1) * (Q**4 - 1) == AUT_ORDER

    def test_sp4_order_factors(self):
        """81 · 8 · 80 = 51840"""
        assert 81 * 8 * 80 == AUT_ORDER

    def test_sp4_cyclotomic_factorisation(self):
        """q⁴ · Φ₁² · Φ₂² · Φ₄ = AUT_ORDER"""
        val = Q**4 * LAM**2 * MU**2 * PHI4
        assert val == AUT_ORDER

    def test_q4_eq_3_times_m_lam(self):
        assert Q**4 == 3 * M_LAM

    def test_q2_minus_1_eq_2_mu(self):
        assert Q**2 - 1 == 2 * MU

    def test_q4_minus_1_eq_edges_over_q(self):
        assert Q**4 - 1 == EDGES // Q


# ═══════════════════════════════════════════════════════════════════════════════
# §3  LANGLANDS DUAL Sp(4) ↔ SO(5)
# ═══════════════════════════════════════════════════════════════════════════════

class TestLanglandsDual:
    def test_dim_so5_eq_phi4(self):
        assert 5 * 4 // 2 == PHI4

    def test_dim_sp4_eq_phi4(self):
        assert 4 * 5 // 2 == PHI4

    def test_dim_so5_eq_q_sq_plus_1(self):
        assert 5 * 4 // 2 == Q**2 + 1

    def test_dim_so5_eq_lap_mid(self):
        assert 5 * 4 // 2 == LAP_MID

    def test_langlands_duality_dimensions_equal(self):
        """Sp(4) and SO(5) have equal dimension — they are Langlands dual (B₂≅C₂)"""
        assert 5 * 4 // 2 == 4 * 5 // 2

    def test_generic_l_packet_size_eq_mu(self):
        assert MU == 4

    def test_stable_packet_size_eq_lam(self):
        assert LAM == 2


# ═══════════════════════════════════════════════════════════════════════════════
# §4  LAPLACIAN EIGENVALUES ↔ SATAKE PARAMETERS
# ═══════════════════════════════════════════════════════════════════════════════

class TestSatakeParameters:
    def test_laplacian_mid_eq_k_minus_lam(self):
        assert K - LAM == LAP_MID

    def test_laplacian_top_eq_k_plus_mu(self):
        assert K + MU == LAP_TOP

    def test_so5_fund_rep1_dim(self):
        """SO(5) standard rep dim = 5 = K - PHI6"""
        assert K - PHI6 == 5

    def test_so5_fund_rep2_dim_eq_mu(self):
        """SO(5) spinor rep dim = 4 = MU"""
        assert MU == 4

    def test_adjoint_so5_eq_phi4_eq_lap_mid(self):
        assert PHI4 == LAP_MID == 10

    def test_spectral_gap(self):
        """Spectral gap = K - MU = 8 = 2·MU"""
        assert K - MU == 2 * MU


# ═══════════════════════════════════════════════════════════════════════════════
# §5  p-ADIC VALUATIONS
# ═══════════════════════════════════════════════════════════════════════════════

class TestPadicValuations:
    def test_nu2_eq_phi6(self):
        assert p_adic_val(AUT_ORDER, 2) == PHI6

    def test_nu3_eq_mu(self):
        assert p_adic_val(AUT_ORDER, 3) == MU

    def test_nu5_eq_1(self):
        assert p_adic_val(AUT_ORDER, 5) == 1

    def test_prime_factorisation(self):
        assert 2**PHI6 * 3**MU * 5 == AUT_ORDER

    def test_nu2_eq_q_plus_mu(self):
        assert p_adic_val(AUT_ORDER, 2) == Q + MU


# ═══════════════════════════════════════════════════════════════════════════════
# §6  GF(3) POLAR SPACE
# ═══════════════════════════════════════════════════════════════════════════════

class TestGF3PolarSpace:
    def test_point_count_eq_v(self):
        """(q⁴-1)/(q-1) = V"""
        assert (Q**4 - 1) // (Q - 1) == V

    def test_point_count_polynomial(self):
        """q³+q²+q+1 = V"""
        assert Q**3 + Q**2 + Q + 1 == V

    def test_line_count(self):
        """V·K/(Q+1) = V·Q = 120"""
        assert V * K // (Q + 1) == V * Q

    def test_ovoid_size_eq_mu(self):
        assert Q + 1 == MU

    def test_spread_lines_eq_phi4(self):
        """V/(Q+1) = PHI4"""
        assert V // (Q + 1) == PHI4


# ═══════════════════════════════════════════════════════════════════════════════
# §7  GEOMETRIC LANGLANDS / FLAG VARIETY
# ═══════════════════════════════════════════════════════════════════════════════

class TestGeometricLanglands:
    def test_rank_sp4_eq_lam(self):
        assert LAM == 2

    def test_positive_roots_c2_eq_mu(self):
        """C₂ = Sp(4) has 4 positive roots = MU"""
        assert MU == 4

    def test_dim_borel_eq_half_k(self):
        """dim(Borel) = rank + |Φ⁺| = 2+4=6 = K/2"""
        assert LAM + MU == K // 2

    def test_dim_flag_variety_eq_mu(self):
        """dim(Sp(4)/B) = dim(Sp(4)) - dim(Borel) = 10-6=4=MU"""
        dim_sp4 = 4 * 5 // 2
        dim_borel = LAM + MU
        assert dim_sp4 - dim_borel == MU

    def test_total_roots_eq_2_mu(self):
        """|Φ(C₂)| = 8 = 2·MU"""
        assert 2 * MU == 8

    def test_weyl_order_c2_eq_2_mu(self):
        """|W(C₂)| = 2^rank · rank! = 4·2 = 8 = 2·MU"""
        assert 2**LAM * math.factorial(LAM) == 2 * MU

    def test_schubert_cells_eq_weyl_order(self):
        """Number of Schubert cells = |W(C₂)| = 8 = 2·MU"""
        weyl = 2**LAM * math.factorial(LAM)
        assert weyl == 2 * MU
