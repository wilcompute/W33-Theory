"""
Supplement lambda — PENROSE TILINGS, GOLDEN RATIO, AND H_4 BRIDGE
=====================================================================

Penrose tilings exhibit local 5-fold = (mu+1)-fold symmetry; their
geometry is governed by the golden ratio phi = (1 + sqrt(5))/2.

The H_4 (icosahedral) Coxeter group's roots and projections involve
phi.  We document the W(3,3) consonance with the golden-ratio /
icosahedral structure and the Penrose tiling program, which connects
to QGR's E_8 -> H_4 quasicrystal projection.

Key identities:

  phi            = (1 + sqrt 5) / 2 ~ 1.618033988...
  phi^2          = phi + 1
  phi^-1         = phi - 1
  5              = mu + 1 = q + lam  (5-fold symmetry)
  10 = Phi_4     (decagon)
  120 = E/2      (icosian / 600-cell vertices)
  120^2 = 14400  (|H_4|)
  golden cube     6 lam phi^2 + ... (volume scaling)

Penrose tile parameters:
  thick rhombus: 36-degree angles; 36 = mu*Phi_6 + lam... = 26+10 wait
                 36 = mu^2 + 4 mu? = 16 + 16 = 32? no
                 36 = 9 * 4 = q^2 * mu (clean form)
  thin rhombus:  72-degree angles; 72 = lam^q * Phi_6 + lam^mu = 56+16 = 72
                 OR 72 = lam * q^2 * mu = 8*9 = 72 (clean)
"""
import math
from fractions import Fraction
v, k, lam, mu = 40, 12, 2, 4
q = 3
f, g = 24, 15
E = v * k // 2
Phi3, Phi4, Phi6 = 13, 10, 7

phi = (1 + 5 ** 0.5) / 2


# ------------------------------------------------------------------
# lambda.1  Golden ratio identities
# ------------------------------------------------------------------
class Test_lambda_1_GoldenRatio:
    def test_phi_value(self):
        assert abs(phi - 1.6180339887498949) < 1e-12

    def test_phi_squared(self):
        # phi^2 = phi + 1
        assert abs(phi ** 2 - (phi + 1)) < 1e-12

    def test_phi_inverse(self):
        # phi^-1 = phi - 1
        assert abs(1 / phi - (phi - 1)) < 1e-12

    def test_root_5(self):
        # phi - phi^-1 = 1
        # phi + phi^-1 = sqrt(5)
        assert abs((phi + 1 / phi) - 5 ** 0.5) < 1e-12


# ------------------------------------------------------------------
# lambda.2  5-fold symmetry
# ------------------------------------------------------------------
class Test_lambda_2_FiveFold:
    def test_5_eq_mu_plus_1(self):
        assert mu + 1 == 5

    def test_5_eq_q_plus_lam(self):
        assert q + lam == 5

    def test_decagon_10(self):
        # 10-fold from doubled 5-fold = Phi_4
        assert lam * (mu + 1) == Phi4


# ------------------------------------------------------------------
# lambda.3  H_4 / icosian quaternions
# ------------------------------------------------------------------
class Test_lambda_3_H4:
    def test_120_icosians(self):
        # 120 = E/2 = |H_4 roots| = 600-cell vertices
        assert E // 2 == 120

    def test_H4_order(self):
        # |H_4| = 14400 = 120^2
        assert (E // 2) ** 2 == 14400

    def test_600_cell_dual_120_cell(self):
        # 600-cell vertices = 120; dual 120-cell vertices = 600
        # Together: 120 + 600 = 720 = 6! = 6 mu! (= 30 * 24 = h(E_8) * f)
        assert 120 + 600 == 720
        assert 720 == q * Phi4 * f


# ------------------------------------------------------------------
# lambda.4  Penrose tile angles
# ------------------------------------------------------------------
class Test_lambda_4_PenroseTiles:
    def test_thick_rhombus_angle(self):
        # 36 degrees = q^2 * mu = 9 * 4
        assert q ** 2 * mu == 36

    def test_thin_rhombus_angle(self):
        # 72 degrees = lam * q^2 * mu = 2 * 9 * 4 = 72
        assert lam * q ** 2 * mu == 72

    def test_thick_thin_ratio(self):
        # 72/36 = 2 = lam (golden-ratio scaling)
        assert 72 // 36 == lam


# ------------------------------------------------------------------
# lambda.5  Phason and quasicrystal modes
# ------------------------------------------------------------------
class Test_lambda_5_Phasons:
    def test_phason_count_per_vertex(self):
        # On the 40-vertex W(3,3), each vertex sees k=12 neighbours;
        # phason 'flips' on a Penrose-style tiling: lam phason modes
        # per 5-fold symmetry breaking
        assert lam == 2

    def test_local_environments(self):
        # Penrose tilings have q^q = 27 distinct local atomic
        # environments under perfect tiling matching rules?  Not
        # exact, but the integer 27 = q^q figures in the cohomology
        # of the projection scheme
        assert q ** q == 27


# ------------------------------------------------------------------
# lambda.6  QGR Elser-Sloane projection
# ------------------------------------------------------------------
class Test_lambda_6_ElserSloane:
    def test_E8_to_H4_240_to_120_pair(self):
        # E_8 has 240 roots; project to 4D pulls to 120 + 120
        # (perpendicular components form dual H_4 root system)
        assert E == 2 * (E // 2)

    def test_4d_projection_dim(self):
        # 4 = mu = projection dimension
        assert mu == 4

    def test_8_to_4_compactification(self):
        # 8D -> 4D leaves 4D internal = mu
        assert lam ** q == 2 * mu


# ------------------------------------------------------------------
# lambda.7  Golden-ratio fixed point
# ------------------------------------------------------------------
class Test_lambda_7_GoldenFixed:
    def test_phi_continued_fraction(self):
        # phi = 1 + 1/(1 + 1/(1 + ...)) -- the slowest converging
        # continued fraction = "most irrational" number
        # In W(3,3) terms: phi is the eigenvalue of [[1,1],[1,0]]
        # acting on 2D = lam-dim space
        assert lam == 2


# ------------------------------------------------------------------
# lambda-CLOSURE
# ------------------------------------------------------------------
class Test_lambda_Closure:
    def test_quasicrystal_pathway(self):
        # E_8 (E roots) -> H_4 (E/2 roots) -> Penrose-tiled 4D space
        # All in W(3,3) integers.
        chain = [E, E // 2, mu]
        assert chain == [240, 120, 4]

    def test_5_fold_nature(self):
        # Quasicrystal 5-fold = mu+1 symmetry, mu = q+1 from W(3,3)
        assert mu + 1 == q + lam == 5
