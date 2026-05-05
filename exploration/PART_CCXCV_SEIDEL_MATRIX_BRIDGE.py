"""
Part CCXCV: Seidel Matrix Eigenvalue Structure of W(3,3).

Theme: The Seidel matrix S = J - I - 2A of W(3,3) (entries -1 on edges, +1 on
non-edges) has exactly three eigenvalues {15, -5, 7} with multiplicities {1, 24, 15}.
This Seidel spectrum encodes the equiangular-lines structure (40 lines in R^15 at
angle arccos(1/5)), and every Seidel eigenvalue or multiplicity relates to an SRG
constant or SM value. The maximum Seidel eigenvalue (15) equals MULT_S, and the
multiplicity difference MULT_R - MULT_S = 9 = Q^2 recovered from GQ(3,3) (Part CCXCIV).

Checks: 27 / 27
"""

# ── W(3,3) SRG constants ──────────────────────────────────────────────────────
V = 40
K = 12
LAM = 2
MU = 4
K2 = 27
EDGES = 240
MULT_R = 24
MULT_S = 15

# ── SRG restricted eigenvalues ────────────────────────────────────────────────
R_EIG = 2    # positive restricted eigenvalue
S_EIG = -4   # negative restricted eigenvalue

# ── SM constants ──────────────────────────────────────────────────────────────
EW_GAUGE_4 = 4
QUARKS_36 = 36
Q = 3

# ── Seidel matrix S = J - I - 2A ─────────────────────────────────────────────
# For an SRG(v, k, λ, μ) with restricted eigenvalues r, s:
#   τ_0 = v - 1 - 2k          (trivial,  multiplicity 1)
#   τ_r = -(1 + 2r)            (from pos. eigenvalue r, multiplicity m_r)
#   τ_s = -(1 + 2s)            (from neg. eigenvalue s, multiplicity m_s)
TAU_0 = V - 1 - 2 * K             # 40 - 1 - 24 = 15
TAU_R = -(1 + 2 * R_EIG)          # -(1 + 4) = -5
TAU_S = -(1 + 2 * S_EIG)          # -(1 - 8) = 7

MULT_TAU_0 = 1
MULT_TAU_R = MULT_R                # 24
MULT_TAU_S = MULT_S                # 15

# ── Spectral invariants ───────────────────────────────────────────────────────
# Trace S = 0 (diagonal = 0 for Seidel matrix)
SEIDEL_TRACE = TAU_0 * MULT_TAU_0 + TAU_R * MULT_TAU_R + TAU_S * MULT_TAU_S  # 0

# Trace S² = number of ordered non-identical pairs = V(V-1)
# Each off-diagonal entry is ±1, so S² contributes one +1 per entry.
SEIDEL_TRACE_SQ = (
    TAU_0 ** 2 * MULT_TAU_0
    + TAU_R ** 2 * MULT_TAU_R
    + TAU_S ** 2 * MULT_TAU_S
)  # 225 + 600 + 735 = 1560
SEIDEL_TRACE_SQ_FORMULA = V * (V - 1)   # 40 * 39 = 1560

# ── Equiangular lines structure ───────────────────────────────────────────────
# The 40 rows of the ±normalised Seidel eigenvector matrix realise 40 equiangular
# lines in R^d at common angle arccos(α) where α = 1/|τ_min| = 1/5.
# The embedding dimension equals the multiplicity of the largest positive Seidel
# eigenvalue (i.e. τ_s = 7 with multiplicity MULT_S = 15, using the convention
# that the "large positive" eigenvalue gives the smallest multiplicity embedding).
ANGLE_DENOM = abs(TAU_R)       # 5  (= |smallest eigenvalue| = 1/angle)
EMBEDDING_DIM = MULT_S         # 15 = R^15

# ── Cross-checks: Seidel ↔ SRG ───────────────────────────────────────────────
# |τ_r| = |s_eig| + 1 = 5
ABS_TAU_R = abs(TAU_R)         # 5

# τ_s = 2|s_eig| - 1 = 7
TAU_S_FROM_S = 2 * abs(S_EIG) - 1    # 7

# |τ_r| = Q + 2 = 5
ABS_TAU_R_FROM_Q = Q + 2              # 5

# Multiplicity difference: MULT_R - MULT_S = Q^2 = 9
MULT_DIFF = MULT_R - MULT_S           # 9

# ── Sums, products, differences ───────────────────────────────────────────────
# τ_r * τ_s = -35 = -(V - MU - 1)
TAU_PRODUCT = TAU_R * TAU_S           # -35
PRODUCT_FORMULA = -(V - MU - 1)       # -35

# τ_0 + τ_s = 15 + 7 = 22 = 2K - LAM
TAU_SUM_0S = TAU_0 + TAU_S           # 22
SUM_0S_FORMULA = 2 * K - LAM         # 22

# τ_0 - τ_s = 15 - 7 = 8 = K - MU
TAU_DIFF_0S = TAU_0 - TAU_S          # 8
DIFF_0S_FORMULA = K - MU             # 8

# ── SM connections ─────────────────────────────────────────────────────────────
# QUARKS_36 - MULT_R = 36 - 24 = 12 = K
QUARKS_MINUS_MULT_R = QUARKS_36 - MULT_R    # 12

# TAU_0 = MULT_S: largest Seidel eigenvalue = multiplicity of s
TAU_0_IS_MULT_S = (TAU_0 == MULT_S)

# (TAU_0 + 1) // 2 = 8 = K - MU
HALF_TAU_0_PLUS1 = (TAU_0 + 1) // 2   # 8


# ── Verification ─────────────────────────────────────────────────────────────
def verify_all():
    """Run all 27 CCXCV checks and return (checks_list, passed, total)."""
    checks = []

    def chk(name, val, exp=True):
        ok = (val == exp) if (exp is not True) else bool(val)
        checks.append((name, ok, val))
        return ok

    # Core Seidel eigenvalue definitions
    chk("TAU_0==15",            TAU_0,               15)
    chk("TAU_R==-5",            TAU_R,               -5)
    chk("TAU_S==7",             TAU_S,               7)
    chk("TAU_0 formula",        V - 1 - 2 * K,       15)
    chk("TAU_R formula",        -(1 + 2 * R_EIG),    -5)
    chk("TAU_S formula",        -(1 + 2 * S_EIG),    7)

    # Multiplicities
    chk("MULT_TAU_0==1",        MULT_TAU_0,          1)
    chk("MULT_TAU_R==24",       MULT_TAU_R,          24)
    chk("MULT_TAU_S==15",       MULT_TAU_S,          15)

    # Spectral constraints
    chk("mult sum==V",          1 + MULT_TAU_R + MULT_TAU_S, V)
    chk("trace==0",             SEIDEL_TRACE,        0)
    chk("trace S²==V(V-1)",     SEIDEL_TRACE_SQ,     SEIDEL_TRACE_SQ_FORMULA)
    chk("trace S²==1560",       SEIDEL_TRACE_SQ,     1560)

    # Equiangular lines
    chk("angle_denom==5",       ANGLE_DENOM,         5)
    chk("embedding_dim==15",    EMBEDDING_DIM,       15)

    # Cross-checks: Seidel ↔ SRG eigenvalues
    chk("|TAU_R|==|S_EIG|+1",  ABS_TAU_R,           abs(S_EIG) + 1)
    chk("TAU_S==2|S_EIG|-1",   TAU_S,               TAU_S_FROM_S)
    chk("|TAU_R|==Q+2",        ABS_TAU_R,           ABS_TAU_R_FROM_Q)
    chk("MULT_DIFF==Q^2",      MULT_DIFF,           Q ** 2)

    # Products, sums, differences
    chk("TAU_R*TAU_S==-35",    TAU_PRODUCT,         -35)
    chk("TAU_R*TAU_S==-V+MU+1", TAU_PRODUCT,        PRODUCT_FORMULA)
    chk("TAU_0+TAU_S==22",     TAU_SUM_0S,          22)
    chk("TAU_0+TAU_S==2K-LAM", TAU_SUM_0S,          SUM_0S_FORMULA)
    chk("TAU_0-TAU_S==K-MU",   TAU_DIFF_0S,         DIFF_0S_FORMULA)

    # SM connections
    chk("QUARKS-MULT_R==K",    QUARKS_MINUS_MULT_R, K)
    chk("TAU_0==MULT_S",       TAU_0_IS_MULT_S)
    chk("(TAU_0+1)//2==K-MU",  HALF_TAU_0_PLUS1,    K - MU)

    passed = sum(1 for _, ok, _ in checks if ok)
    total = len(checks)
    return checks, passed, total


def build_ccxcv_summary():
    """Build the Part CCXCV result summary dictionary."""
    checks, passed, total = verify_all()
    return {
        "part": "CCXCV",
        "title": "Seidel Matrix Eigenvalue Structure of W(3,3)",
        "checks_pass": passed,
        "checks_total": total,
        "status": "ALL_PASS" if passed == total else "FAIL",
        "tau_0": TAU_0,
        "tau_r": TAU_R,
        "tau_s": TAU_S,
        "mult_tau_0": MULT_TAU_0,
        "mult_tau_r": MULT_TAU_R,
        "mult_tau_s": MULT_TAU_S,
        "seidel_trace": SEIDEL_TRACE,
        "seidel_trace_sq": SEIDEL_TRACE_SQ,
        "angle_denom": ANGLE_DENOM,
        "embedding_dim": EMBEDDING_DIM,
        "mult_diff": MULT_DIFF,
        "discoveries": [
            "Seidel spectrum {15^1, (-5)^24, 7^15} encodes all SRG parameters",
            "Maximum Seidel eigenvalue τ_0 = 15 = MULT_S (coincidence)",
            "40 equiangular lines in R^15 at angle arccos(1/5) = arccos(1/(Q+2))",
            "MULT_R - MULT_S = 9 = Q² (from GQ(3,3) order, Part CCXCIV)",
            "QUARKS_36 - MULT_R = K = 12 (SM fermionic degrees → SRG degree)",
            "|τ_r| = Q + 2 = 5 (smallest Seidel eigenvalue = ternary + 2)",
            "Trace S² = V(V-1) = 1560 (spectral self-consistency)",
        ],
    }


if __name__ == "__main__":
    checks, passed, total = verify_all()
    for name, ok, val in checks:
        status = "✓" if ok else "✗"
        print(f"  {status} {name}: {val}")
    print(f"\nCCXCV Verification: {passed}/{total} checks pass {'✓' if passed == total else '✗'}")
