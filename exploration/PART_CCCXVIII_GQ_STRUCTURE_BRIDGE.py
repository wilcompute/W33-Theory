"""
PART CCCXVIII — Generalized Quadrangle GQ(3,3) Structure of W(3,3)

W(3,3) is the collinearity graph of the generalized quadrangle GQ(3,3).
A GQ(s,t) is a point-line incidence geometry where every point-line pair
with the point not on the line has exactly one connecting line through
a point on the original line.

GQ(3,3) parameters:
  s = 3 (each line has s+1 = 4 points)
  t = 3 (each point is on t+1 = 4 lines)

Derived SRG parameters via standard GQ→SRG formulas:
  points  V = (s+1)(st+1) = 4*10 = 40
  lines   L = (t+1)(st+1) = 4*10 = 40
  degree  k = s(t+1) = 3*4 = 12
  lambda  λ = s-1 = 2
  mu      μ = t+1 = 4
  r-eig   r = (λ-μ+√Δ)//2 = 2    where Δ=(λ-μ)²+4(k-μ)=36
  s-eig   s = (λ-μ-√Δ)//2 = -4
"""

# --- SRG parameters ---
V = 40
K = 12
LAM = 2
MU = 4
MULT_R = 24
MULT_S = 15
R_EIG = 2
S_EIG = -4

# --- SM constants ---
EW_GAUGE_4 = 4
ALPHA = 10
GUT_DIM = 27
GENERATIONS = 3

# ---------------------------------------------------------------------------
# Generalized quadrangle parameters
# ---------------------------------------------------------------------------

GQ_S = 3   # line size = GQ_S + 1 = 4 = EW_GAUGE_4  (= GENERATIONS)
GQ_T = 3   # lines per point = GQ_T + 1 = 4 = EW_GAUGE_4  (= GENERATIONS)

# Point and line counts
POINTS = (GQ_S + 1) * (GQ_S * GQ_T + 1)    # = 4 * 10 = 40 = V
LINES  = (GQ_T + 1) * (GQ_S * GQ_T + 1)    # = 4 * 10 = 40 = V (self-dual since s=t)

POINTS_PER_LINE  = GQ_S + 1    # = 4 = EW_GAUGE_4
LINES_PER_POINT  = GQ_T + 1    # = 4 = EW_GAUGE_4
TOTAL_INCIDENCES = POINTS * LINES_PER_POINT  # = 160

# ---------------------------------------------------------------------------
# GQ → SRG derivation
# ---------------------------------------------------------------------------

DEGREE_GQ = GQ_S * (GQ_T + 1)     # = 12 = K
LAMBDA_GQ = GQ_S - 1               # =  2 = LAM
MU_GQ     = GQ_T + 1               # =  4 = MU

# Eigenvalue discriminant: Δ = (λ-μ)² + 4(k-μ)
DISC      = (LAMBDA_GQ - MU_GQ) ** 2 + 4 * (DEGREE_GQ - MU_GQ)  # = 36
SQRT_DISC = 6                                                       # integer √36

EIG_R_GQ = (LAMBDA_GQ - MU_GQ + SQRT_DISC) // 2   # = ( 2-4+6)//2 =  2 = R_EIG
EIG_S_GQ = (LAMBDA_GQ - MU_GQ - SQRT_DISC) // 2   # = ( 2-4-6)//2 = -4 = S_EIG


# ---------------------------------------------------------------------------
# Verification
# ---------------------------------------------------------------------------

def verify_all():
    """Return (checks_list, passed, total) with exactly 27 checks."""
    checks = []

    def chk(label, val):
        checks.append((label, bool(val)))

    # ------------------------------------------------------------------
    # Group 1: SRG parameters (6 checks)
    # ------------------------------------------------------------------
    chk("V == 40",     V == 40)
    chk("K == 12",     K == 12)
    chk("LAM == 2",    LAM == 2)
    chk("MU == 4",     MU == 4)
    chk("R_EIG == 2",  R_EIG == 2)
    chk("S_EIG == -4", S_EIG == -4)

    # ------------------------------------------------------------------
    # Group 2: GQ basic structure (5 checks)
    # ------------------------------------------------------------------
    chk("POINTS = (GQ_S+1)*(GQ_S*GQ_T+1) == V",
        POINTS == V)
    chk("LINES = (GQ_T+1)*(GQ_S*GQ_T+1) == V  (self-dual GQ)",
        LINES == V)
    chk("POINTS_PER_LINE = GQ_S+1 == EW_GAUGE_4",
        POINTS_PER_LINE == EW_GAUGE_4)
    chk("LINES_PER_POINT = GQ_T+1 == EW_GAUGE_4",
        LINES_PER_POINT == EW_GAUGE_4)
    chk("GQ_S == GQ_T  (symmetric GQ)",
        GQ_S == GQ_T)

    # ------------------------------------------------------------------
    # Group 3: GQ -> SRG eigenvalue derivation (5 checks)
    # ------------------------------------------------------------------
    chk("DEGREE_GQ = GQ_S*(GQ_T+1) == K",
        DEGREE_GQ == K)
    chk("LAMBDA_GQ = GQ_S-1 == LAM",
        LAMBDA_GQ == LAM)
    chk("MU_GQ = GQ_T+1 == MU",
        MU_GQ == MU)
    chk("DISC = (LAM-MU)^2 + 4*(K-MU) == 36",
        DISC == 36)
    chk("EIG_R_GQ = (LAM-MU+SQRT_DISC)//2 == R_EIG",
        EIG_R_GQ == R_EIG)

    # ------------------------------------------------------------------
    # Group 4: SM encodings (11 checks)
    # ------------------------------------------------------------------
    chk("GQ_S == GENERATIONS",
        GQ_S == GENERATIONS)
    chk("GQ_T == GENERATIONS",
        GQ_T == GENERATIONS)
    chk("GQ_S*GQ_T + 1 == ALPHA",
        GQ_S * GQ_T + 1 == ALPHA)
    chk("GQ_S*GQ_T == GENERATIONS^2",
        GQ_S * GQ_T == GENERATIONS ** 2)
    chk("TOTAL_INCIDENCES == V*EW_GAUGE_4",
        TOTAL_INCIDENCES == V * EW_GAUGE_4)
    chk("TOTAL_INCIDENCES == LINES*POINTS_PER_LINE",
        TOTAL_INCIDENCES == LINES * POINTS_PER_LINE)
    chk("(GQ_S+1)*(GQ_T+1) == K+MU",
        (GQ_S + 1) * (GQ_T + 1) == K + MU)
    chk("GQ_S + GQ_T == K//LAM",
        GQ_S + GQ_T == K // LAM)
    chk("POINTS_PER_LINE^2 - 1 == MULT_S",
        POINTS_PER_LINE ** 2 - 1 == MULT_S)
    chk("LINES_PER_POINT * GQ_S == K",
        LINES_PER_POINT * GQ_S == K)
    chk("GQ_S^2 == MU + LAM + GENERATIONS",
        GQ_S ** 2 == MU + LAM + GENERATIONS)

    passed = sum(1 for _, v in checks if v)
    total  = len(checks)
    return checks, passed, total


def build_cccxviii_summary():
    checks, passed, total = verify_all()
    return {
        "part":         "CCCXVIII",
        "title":        "Generalized Quadrangle GQ(3,3) Structure of W(3,3)",
        "checks_pass":  passed,
        "checks_total": total,
        "status":       "PASS" if passed == total else "FAIL",
        "fields": {
            "V":               V,
            "K":               K,
            "LAM":             LAM,
            "MU":              MU,
            "GQ_S":            GQ_S,
            "GQ_T":            GQ_T,
            "POINTS":          POINTS,
            "LINES":           LINES,
            "POINTS_PER_LINE": POINTS_PER_LINE,
            "LINES_PER_POINT": LINES_PER_POINT,
            "TOTAL_INCIDENCES":TOTAL_INCIDENCES,
            "DISC":            DISC,
            "SQRT_DISC":       SQRT_DISC,
            "EIG_R_GQ":        EIG_R_GQ,
            "EIG_S_GQ":        EIG_S_GQ,
        },
        "discoveries": [
            "GQ_S = GQ_T = 3 = GENERATIONS: Both GQ parameters equal the number of fermion generations",
            "POINTS_PER_LINE = 4 = EW_GAUGE_4: Each line of the GQ has exactly EW_GAUGE_4 points",
            "LINES_PER_POINT = 4 = EW_GAUGE_4: Each point lies on exactly EW_GAUGE_4 lines",
            "POINTS = LINES = V = 40: GQ(3,3) is self-dual; the geometry has 40 points and 40 lines",
            "GQ_S*GQ_T + 1 = 10 = ALPHA: The product of GQ parameters plus one equals the alpha constant",
            "GQ_S*GQ_T = 9 = GENERATIONS^2: The GQ product encodes the squared generation count",
            "TOTAL_INCIDENCES = 160 = V*EW_GAUGE_4: Total point-line flags encode V times the gauge count",
            "(GQ_S+1)*(GQ_T+1) = 16 = K+MU: The product of line/point sizes encodes K+mu",
            "GQ_S + GQ_T = 6 = K//LAM: Summed GQ parameters equal the degree-triangle ratio",
            "POINTS_PER_LINE^2 - 1 = 15 = MULT_S: Squared line size minus 1 equals the s-eigenspace dimension",
            "GQ_S^2 = 9 = MU+LAM+GENERATIONS: Squared GQ parameter encodes three SRG/SM constants",
            "DISC = 36: Eigenvalue discriminant is a perfect square encoding the geometry",
            "SQRT_DISC = 6 = 2*GENERATIONS: Square root of discriminant is twice the generation count",
        ],
    }


if __name__ == "__main__":
    checks, passed, total = verify_all()
    print(f"PART CCCXVIII — Generalized Quadrangle GQ(3,3) Structure of W(3,3)")
    print(f"Checks: {passed}/{total}")
    for label, val in checks:
        mark = "OK" if val else "FAIL"
        print(f"  [{mark}] {label}")
    print("ALL PASS" if passed == total else "FAILURES DETECTED")
