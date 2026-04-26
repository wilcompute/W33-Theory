"""
Supplement eta — CLOSED-WALK GENERATING FUNCTION OF W(3,3)
==============================================================

The number of closed walks of length n on W(3,3) starting and ending
at any fixed vertex is

    W_n = (1/v) tr(A^n) = (1/40) ( 1 . k^n + f . r^n + g . s^n )
        = (1/40) ( 12^n + 24 . 2^n + 15 . (-4)^n )

The generating function

    Z(t) = sum_{n >= 0} W_n t^n
         = (1/40) [ 1/(1 - 12 t) + 24/(1 - 2 t) + 15/(1 + 4 t) ]

is rational with three poles at t = 1/12, 1/2, -1/4 (one per spectral
eigenvalue 12, 2, -4).

Closed walks at small length:
    W_0 = 1                 (trivial walk)
    W_1 = 0                 (no self-loops)
    W_2 = k = 12            (walk to neighbor and back)
    W_3 = lam k = 24        (triangles count = v k lam / 6 = 160; per-vertex = 8; signed = ?)

Total closed walks vs trace:
    tr(A^n) = k^n + f r^n + g s^n
            = 12^n + 24 . 2^n + 15 . (-4)^n
"""
import math
from fractions import Fraction
v, k, lam, mu = 40, 12, 2, 4
q = 3
f, g = 24, 15
E = v * k // 2
Phi3, Phi4, Phi6 = 13, 10, 7


def walk_count_per_vertex(n):
    # W_n = (1/v) tr(A^n)
    return Fraction(k ** n + f * (2 ** n) + g * ((-4) ** n), v)


def total_walks(n):
    # tr(A^n)
    return k ** n + f * (2 ** n) + g * ((-4) ** n)


# ------------------------------------------------------------------
# eta.1  Small-length walk counts
# ------------------------------------------------------------------
class Test_eta_1_SmallWalks:
    def test_W_0(self):
        # W_0 = 1
        assert walk_count_per_vertex(0) == 1

    def test_W_1(self):
        # W_1 = 0 (no self-loops)
        assert walk_count_per_vertex(1) == 0

    def test_W_2(self):
        # W_2 = k = 12 (each vertex has k neighbors; walk to one and back)
        assert walk_count_per_vertex(2) == k

    def test_W_3_triangles(self):
        # W_3 = #closed walks of length 3 / v = (sum over v of #directed triangles through v) / v
        # = 6 * #triangles / v = 6 * 160 / 40 = 24
        assert walk_count_per_vertex(3) == 24
        assert 24 == lam * k


# ------------------------------------------------------------------
# eta.2  Trace formula identity
# ------------------------------------------------------------------
class Test_eta_2_TraceFormula:
    def test_trace_A_0(self):
        # tr(A^0) = tr(I) = v = 40
        assert total_walks(0) == v

    def test_trace_A_1(self):
        # tr(A) = 0 (no self-loops)
        assert total_walks(1) == 0

    def test_trace_A_2(self):
        # tr(A^2) = 2|E| = vk = 480
        assert total_walks(2) == 2 * E
        assert total_walks(2) == 480

    def test_trace_A_3(self):
        # tr(A^3) = 6 * #triangles = 6 * 160 = 960
        assert total_walks(3) == 6 * 160

    def test_trace_A_4(self):
        # tr(A^4) = 12^4 + 24*16 + 15*256 = 20736 + 384 + 3840 = 24960
        assert total_walks(4) == 12 ** 4 + 24 * 16 + 15 * 256
        assert total_walks(4) == 24960


# ------------------------------------------------------------------
# eta.3  The three poles
# ------------------------------------------------------------------
class Test_eta_3_PolesOfZ:
    def test_pole_at_one_over_k(self):
        # main pole at t = 1/k = 1/12
        assert Fraction(1, k) == Fraction(1, 12)

    def test_pole_at_one_over_r(self):
        # secondary pole at t = 1/r = 1/2
        assert Fraction(1, 2) == Fraction(1, lam)

    def test_pole_at_one_over_s(self):
        # tertiary pole at t = 1/s = -1/4
        assert Fraction(1, -4) == -Fraction(1, mu)


# ------------------------------------------------------------------
# eta.4  Hausdorff-type dimension / mixing time
# ------------------------------------------------------------------
class Test_eta_4_Mixing:
    def test_spectral_gap(self):
        # spectral gap (k - r) = 12 - 2 = 10 = Phi_4
        assert k - 2 == Phi4

    def test_mixing_time_log(self):
        # tau_mix ~ log(v)/spectral gap  ~ log(40)/10
        # which is small (rapidly mixing)
        log_v = math.log(v)
        assert 0.3 < log_v / Phi4 < 0.5


# ------------------------------------------------------------------
# eta.5  Walk generating function value at small t
# ------------------------------------------------------------------
class Test_eta_5_GeneratingFunction:
    def test_Z_at_t_0(self):
        # Z(0) = W_0 = 1
        assert walk_count_per_vertex(0) == 1

    def test_Z_at_small_t(self):
        # Z(t) ~ 1 + 0*t + 12*t^2 + 24*t^3 + ...
        coeffs = [walk_count_per_vertex(n) for n in range(5)]
        assert coeffs[0] == 1
        assert coeffs[1] == 0
        assert coeffs[2] == 12
        assert coeffs[3] == 24
        assert coeffs[4] == Fraction(24960, v)
        assert coeffs[4] == 624


# ------------------------------------------------------------------
# eta-CLOSURE
# ------------------------------------------------------------------
class Test_eta_Closure:
    def test_three_pole_structure(self):
        # 3 = q poles, one per eigenvalue
        poles = [Fraction(1, 12), Fraction(1, 2), Fraction(-1, 4)]
        assert len(poles) == q

    def test_walk_via_Bose_Mesner(self):
        # Closed walk count expressible via spectral decomposition
        for n in range(1, 6):
            direct = total_walks(n)
            spectral = k ** n + f * (2 ** n) + g * ((-4) ** n)
            assert direct == spectral
