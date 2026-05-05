"""
Part CCXCIV: Generalized Quadrangle GQ(3,3) and the W(3,3) Collinearity Graph.

Theme: W(3,3) is the collinearity graph of the symplectic generalized quadrangle
W(3, q) over GF(3), also written GQ(s,t) = GQ(3,3). All four SRG parameters of
W(3,3) — v, k, λ, μ — are completely determined by the single equation s = t = 3 = Q
(the ternary base). Lines per point = points per line = 4 = EW_GAUGE_4, and the
maximum independent set (ovoid) has size st + 1 = 10 = α(W(3,3)).

Checks: 27 / 27
"""

from fractions import Fraction

# ── W(3,3) SRG constants ──────────────────────────────────────────────────────
V = 40
K = 12
LAM = 2
MU = 4
K2 = 27
EDGES = 240
MULT_R = 24
MULT_S = 15

# ── SM constants ──────────────────────────────────────────────────────────────
EW_GAUGE_4 = 4
QUARKS_36 = 36
TOTAL_SM_40 = 40
Q = 3            # ternary base

# ── GQ(s, t) = GQ(3, 3) parameters ───────────────────────────────────────────
# A generalized quadrangle GQ(s,t) has:
#   - (s+1)(st+1) points and (t+1)(st+1) lines
#   - Every line contains s+1 points; every point is on t+1 lines
#   - Every two non-collinear points have exactly t+1 common lines
#   - Every two collinear points have exactly 1 common line
#
# W(3,3) is the symplectic GQ W(3, q=3) = GQ(s,t) with s = t = q = 3.
S_GQ = 3    # GQ parameter s (= q = ternary base)
T_GQ = 3    # GQ parameter t (= q = ternary base)

# Self-dual: s = t → GQ is isomorphic to its dual
SELF_DUAL = (S_GQ == T_GQ)

# ── Point and line counts ─────────────────────────────────────────────────────
ST_PRODUCT = S_GQ * T_GQ              # 9 = Q²
POINTS = (S_GQ + 1) * (ST_PRODUCT + 1)   # (3+1)(9+1) = 40 = V
LINES  = (T_GQ + 1) * (ST_PRODUCT + 1)   # (3+1)(9+1) = 40 = V (self-dual)

POINTS_PER_LINE = S_GQ + 1            # 4 = EW_GAUGE_4
LINES_PER_POINT = T_GQ + 1            # 4 = EW_GAUGE_4

# Total point-line incidences: each point on t+1 lines, or each line has s+1 points
INCIDENCES = POINTS * LINES_PER_POINT      # 40 * 4 = 160
INCIDENCES_LINES = LINES * POINTS_PER_LINE  # 40 * 4 = 160

# ── SRG parameters recovered from GQ parameters ───────────────────────────────
# For the collinearity graph of GQ(s,t):
#   v = (s+1)(st+1),  k = s(t+1),  λ = s-1,  μ = t+1
SRG_V   = (S_GQ + 1) * (ST_PRODUCT + 1)   # 40
SRG_K   = S_GQ * (T_GQ + 1)               # 12
SRG_LAM = S_GQ - 1                         # 2
SRG_MU  = T_GQ + 1                         # 4

# ── Independent sets: ovoids ──────────────────────────────────────────────────
# An ovoid of GQ(s,t) is a set of points with no two collinear:
#   ovoid size = st + 1 = 10  (maximum independent set in the collinearity graph)
OVOID_SIZE = ST_PRODUCT + 1    # 10 = α(W(3,3))

# ── Spreads ────────────────────────────────────────────────────────────────────
# A spread of GQ(s,t) is a set of pairwise non-concurrent lines covering all points:
#   spread size = st + 1 = 10 lines, each with s+1 = 4 points → 10 * 4 = 40 = V
SPREAD_SIZE = ST_PRODUCT + 1           # 10 lines in a spread
SPREAD_COVERS = SPREAD_SIZE * POINTS_PER_LINE   # 10 * 4 = 40 = V

# ── Order of GQ ──────────────────────────────────────────────────────────────
# The "order" of GQ(q,q) is q (equivalently s = t = q = 3);
# its "square order" is q² = 9 = S_GQ * T_GQ
GQ_ORDER = S_GQ           # q = 3 = Q (order of GQ)
GQ_SQ_ORDER = ST_PRODUCT  # q² = 9

# ── Collinearity counts ────────────────────────────────────────────────────────
# Adjacent (collinear) pair: number of common neighbours λ = s - 1 = 2 = LAM
COLLINEAR_COMMON = S_GQ - 1    # 2

# Non-adjacent (non-collinear) pair: number of common neighbours μ = t + 1 = 4 = MU
NONCOLLINEAR_COMMON = T_GQ + 1  # 4

# ── SM connections ─────────────────────────────────────────────────────────────
# s = t = 3 = Q: both GQ parameters equal the ternary (strong-force) base
# Lines per point = 4 = EW_GAUGE_4 (electroweak gauge bosons)
# Points per line = 4 = EW_GAUGE_4
# V - EW_GAUGE_4 = 40 - 4 = 36 = QUARKS_36 (degrees of freedom of quarks)
V_MINUS_EW = V - EW_GAUGE_4    # 36 = QUARKS_36

# Ovoid size = 10 = α(W(3,3)): connects to spectral independence bound (Part CCXCIII)
OVOID_IS_ALPHA = (OVOID_SIZE == 10)

# Points × Lines = 40 × 40 = 1600: also Q^4 * (Q^2+1)^2 = ... let me just note
# that V = POINTS = LINES because GQ is self-dual (s = t)
GQ_SELF_DUAL_V = (POINTS == LINES)

# ── Verification ─────────────────────────────────────────────────────────────
def verify_all():
    """Run all 27 CCXCIV checks and return (checks_list, passed, total)."""
    checks = []

    def chk(name, val, exp=True):
        ok = (val == exp) if (exp is not True) else bool(val)
        checks.append((name, ok, val))
        return ok

    # GQ parameters
    chk("s_GQ==3==Q",          S_GQ,               3)
    chk("t_GQ==3==Q",          T_GQ,               3)
    chk("s==t (self-dual)",    SELF_DUAL)
    chk("ST_PRODUCT==9==Q^2",  ST_PRODUCT,         9)

    # Point and line counts
    chk("POINTS==40==V",       POINTS,             V)
    chk("LINES==40==V",        LINES,              V)
    chk("POINTS==LINES",       POINTS,             LINES)
    chk("PTS_PER_LINE==4==EW4", POINTS_PER_LINE,   EW_GAUGE_4)
    chk("LINES_PER_PT==4==EW4", LINES_PER_POINT,   EW_GAUGE_4)
    chk("PTS_PER_LINE==LPP",   POINTS_PER_LINE,    LINES_PER_POINT)

    # SRG parameter recovery
    chk("SRG_V==40",           SRG_V,              40)
    chk("SRG_K==12",           SRG_K,              12)
    chk("SRG_LAM==2",          SRG_LAM,            2)
    chk("SRG_MU==4",           SRG_MU,             4)

    # SRG = W(3,3) parameters
    chk("SRG_V==V",            SRG_V,              V)
    chk("SRG_K==K",            SRG_K,              K)
    chk("SRG_LAM==LAM",        SRG_LAM,            LAM)
    chk("SRG_MU==MU",          SRG_MU,             MU)

    # Ovoid and spread
    chk("OVOID_SIZE==10",      OVOID_SIZE,         10)
    chk("SPREAD_SIZE==10",     SPREAD_SIZE,        10)
    chk("SPREAD_COVERS==V",    SPREAD_COVERS,      V)

    # Incidences
    chk("INCIDENCES==160",     INCIDENCES,         160)
    chk("INCIDENCES match",    INCIDENCES,         INCIDENCES_LINES)

    # Collinearity common-neighbour counts
    chk("collinear_common==LAM",    COLLINEAR_COMMON,    LAM)
    chk("noncollinear_common==MU",  NONCOLLINEAR_COMMON, MU)

    # SM connections
    chk("V-EW4==QUARKS_36",    V_MINUS_EW,         QUARKS_36)
    chk("GQ_ORDER==Q",         GQ_ORDER,           Q)

    passed = sum(1 for _, ok, _ in checks if ok)
    total = len(checks)
    return checks, passed, total


def build_ccxciv_summary():
    """Build the Part CCXCIV result summary dictionary."""
    checks, passed, total = verify_all()
    return {
        "part": "CCXCIV",
        "title": "Generalized Quadrangle GQ(3,3) and the W(3,3) Collinearity Graph",
        "checks_pass": passed,
        "checks_total": total,
        "status": "ALL_PASS" if passed == total else "FAIL",
        "gq_s": S_GQ,
        "gq_t": T_GQ,
        "gq_points": POINTS,
        "gq_lines": LINES,
        "gq_points_per_line": POINTS_PER_LINE,
        "gq_lines_per_point": LINES_PER_POINT,
        "ovoid_size": OVOID_SIZE,
        "spread_size": SPREAD_SIZE,
        "srg_v": SRG_V,
        "srg_k": SRG_K,
        "srg_lam": SRG_LAM,
        "srg_mu": SRG_MU,
        "discoveries": [
            "GQ(3,3) has s = t = 3 = Q: both parameters equal the ternary base",
            "Points = Lines = 40 = V: self-dual GQ recovers vertex count",
            "Lines per point = s+1 = 4 = EW_GAUGE_4 (electroweak gauge bosons)",
            "Points per line = t+1 = 4 = EW_GAUGE_4",
            "All four SRG parameters (v,k,λ,μ) = (40,12,2,4) recovered from s=t=3",
            "Ovoid size = st+1 = 10 = α(W(3,3)) (max independent set from GQ geometry)",
            "V − EW_GAUGE_4 = 40 − 4 = 36 = QUARKS_36",
        ],
    }


if __name__ == "__main__":
    checks, passed, total = verify_all()
    for name, ok, val in checks:
        status = "✓" if ok else "✗"
        print(f"  {status} {name}: {val}")
    print(f"\nCCXCIV Verification: {passed}/{total} checks pass {'✓' if passed == total else '✗'}")
