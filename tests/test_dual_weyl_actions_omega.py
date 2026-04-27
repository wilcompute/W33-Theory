"""
Supplement omega -- THE DUAL WEYL ACTIONS OF 27 AND 40
======================================================

G = Sp(4, F_3) = W(E_6) of order 51840 has two canonical transitive
permutation actions that now sit on equal footing in the W(3,3) programme:

   degree 27: action on the 27 lines of a smooth cubic surface
   degree 40: action on Sylow_3(G), hence on V(W(3,3))

The bridge is a shared local factor 48:
   51840/27 = 1920 = 40*48
   51840/40 = 1296 = 27*48

Equivalently:
   |W(E_6)| = 27*40*48.

The Schlaefli graph on the 27 cubic-surface lines has parameters
SRG(27,16,10,8), and all four parameters are pure W(3,3) constants:
   27 = q^q
   16 = lam^mu
   10 = Phi_4
   8  = 2^q

Its edge count is 27*16/2 = 216, exactly the edge stabilizer size of
W(3,3); dually, the 240 edges of W(3,3) are the Schlaefli edge stabilizer:
   51840 = 240 * 216.
"""
import math
from fractions import Fraction

v, k, lam, mu = 40, 12, 2, 4
q = 3
f, g = 24, 15
E = v * k // 2
AUT = 51840
Phi3, Phi4, Phi6 = 13, 10, 7

SCH_V = q ** q
SCH_K = lam ** mu
SCH_LAM = Phi4
SCH_MU = 2 ** q
SCH_E = SCH_V * SCH_K // 2

N2 = q ** 2 * (q ** 2 + 1) // 2
N3 = v

ORDERED_NONEDGES = v * (v - 1 - k)
STAB_27 = AUT // SCH_V
STAB_40 = AUT // v
BRIDGE_48 = AUT // ORDERED_NONEDGES


# ------------------------------------------------------------------
# omega.1  The 27-action and the 40-action
# ------------------------------------------------------------------
class Test_omega_1_DualActions:
    def test_degree_27_action(self):
        assert SCH_V == 27
        assert SCH_V == v - k - 1

    def test_degree_40_action(self):
        assert N3 == 40
        assert N3 == v

    def test_orbit_stabilizers(self):
        assert STAB_27 == 1920
        assert STAB_40 == 1296

    def test_stabilizers_as_bridge_multiples(self):
        assert STAB_27 == v * BRIDGE_48
        assert STAB_40 == SCH_V * BRIDGE_48


# ------------------------------------------------------------------
# omega.2  The shared 48 bridge
# ------------------------------------------------------------------
class Test_omega_2_Common48:
    def test_ordered_nonedge_count(self):
        assert ORDERED_NONEDGES == v * (v - 1 - k)
        assert ORDERED_NONEDGES == 40 * 27 == 1080

    def test_48_as_stabilizer(self):
        assert BRIDGE_48 == 48
        assert AUT // ORDERED_NONEDGES == BRIDGE_48

    def test_48_in_w33_forms(self):
        assert BRIDGE_48 == q * lam ** mu
        assert BRIDGE_48 == math.factorial(q) * (2 ** q)
        assert BRIDGE_48 == mu * k
        assert BRIDGE_48 == lam * f

    def test_stabilizer_ratio(self):
        assert STAB_27 // v == BRIDGE_48
        assert STAB_40 // SCH_V == BRIDGE_48
        assert Fraction(STAB_27, STAB_40) == Fraction(v, SCH_V)


# ------------------------------------------------------------------
# omega.3  Schlaefli parameters from W(3,3)
# ------------------------------------------------------------------
class Test_omega_3_SchlaefliDictionary:
    def test_parameter_dictionary(self):
        assert (SCH_V, SCH_K, SCH_LAM, SCH_MU) == (27, 16, 10, 8)

    def test_all_four_are_w33_constants(self):
        assert SCH_V == q ** q
        assert SCH_K == lam ** mu
        assert SCH_LAM == Phi4
        assert SCH_MU == 2 ** q

    def test_srg_feasibility(self):
        lhs = SCH_K * (SCH_K - SCH_LAM - 1)
        rhs = (SCH_V - SCH_K - 1) * SCH_MU
        assert lhs == rhs == 80


# ------------------------------------------------------------------
# omega.4  Edge reciprocity 240 <-> 216
# ------------------------------------------------------------------
class Test_omega_4_EdgeReciprocity:
    def test_schlaefli_edge_count(self):
        assert SCH_E == 27 * 16 // 2 == 216

    def test_w33_edge_count(self):
        assert E == 40 * 12 // 2 == 240

    def test_edge_duality(self):
        assert AUT == E * SCH_E
        assert AUT // E == SCH_E
        assert AUT // SCH_E == E


# ------------------------------------------------------------------
# omega.5  GQ(2,4) line count and Sylow_2
# ------------------------------------------------------------------
class Test_omega_5_GQ24AndSylow2:
    def test_gq24_point_count(self):
        # |Pts(GQ(2,4))| = (s+1)(st+1)
        assert (2 + 1) * (2 * 4 + 1) == SCH_V

    def test_gq24_line_count(self):
        # |Lines(GQ(2,4))| = (t+1)(st+1)
        assert (4 + 1) * (2 * 4 + 1) == 45

    def test_line_count_matches_sylow_2(self):
        assert N2 == 45
        assert N2 == (4 + 1) * (2 * 4 + 1)


# ------------------------------------------------------------------
# omega-CLOSURE
# ------------------------------------------------------------------
class Test_omega_Closure:
    def test_weyl_rectangle_identity(self):
        assert AUT == SCH_V * v * BRIDGE_48

    def test_dual_factorizations(self):
        assert AUT == 27 * 40 * 48
        assert AUT == 240 * 216

    def test_sylow_weyl_dictionary(self):
        summary = {
            '27_lines': SCH_V,
            'n_2': N2,
            'n_3': N3,
            'bridge_48': BRIDGE_48,
        }
        assert summary['27_lines'] == 27
        assert summary['n_2'] == 45
        assert summary['n_3'] == 40
        assert summary['bridge_48'] == 48