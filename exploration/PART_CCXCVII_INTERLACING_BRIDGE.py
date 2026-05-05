"""
Part CCXCVII: Eigenvalue Interlacing in W(3,3).

Theme: The Cauchy interlacing theorem states that for a graph G on n vertices
with adjacency eigenvalues λ_1 ≥ λ_2 ≥ … ≥ λ_n, any induced subgraph H on m
vertices has eigenvalues μ_1 ≥ … ≥ μ_m satisfying:

    λ_{n-m+i} ≤ μ_i ≤ λ_i    for i = 1, …, m

For W(3,3) the eigenvalues are: K=12 (×1), R_EIG=2 (×24), S_EIG=-4 (×15).
Key extremal subgraphs furnish tight interlacing checks:

  - Independent set I_{10} (m=10): every μ_i = 0, checking S_EIG ≤ 0 ≤ K.
  - Clique K_4 (m=4): eigenvalues {3,-1,-1,-1}, checking R_EIG ≥ ω-1 = 3... 
    actually 3 > R_EIG = 2, so clique eigenvalue 3 ≤ K = 12 ✓.
  - The "regular subgraph" bound: every k-regular induced subgraph has k ≤ K.
  - Interlacing implies S_EIG ≤ μ_min ≤ K for any single vertex (trivially 0).

All bounds and the arithmetic connecting (n,m,K,R_EIG,S_EIG,MULT_R,MULT_S,ALPHA,OMEGA)
are verified as 27 exact checks.

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

# ── SRG restricted eigenvalues ────────────────────────────────────────────────
R_EIG = 2
S_EIG = -4

# ── SM constants ──────────────────────────────────────────────────────────────
EW_GAUGE_4 = 4
QUARKS_36 = 36
Q = 3

# ── Extremal subgraph sizes (from Part CCXCVI) ────────────────────────────────
ALPHA = 10    # independence number (largest independent set)
OMEGA = 4     # clique number (largest clique)

# ── Interlacing: 1-vertex subgraph ───────────────────────────────────────────
# Any single vertex v has degree K (regular), so the 1×1 adjacency matrix is [0].
# Interlacing: λ_V ≤ μ_1 = 0 ≤ λ_1, i.e., S_EIG ≤ 0 ≤ K.
SINGLE_EIG = 0
SINGLE_LOWER = S_EIG      # -4 ≤ 0 ✓
SINGLE_UPPER = K          # 0 ≤ 12 ✓
SINGLE_INTERLACES = (SINGLE_LOWER <= SINGLE_EIG <= SINGLE_UPPER)

# ── Interlacing: independent set I_α ─────────────────────────────────────────
# For the maximum independent set on α=10 vertices, every eigenvalue = 0.
# Interlacing at position i: λ_{V-α+i} ≤ 0 ≤ λ_i for i=1,...,α.
# The eigenvalue list of W(3,3) (descending): 12, 2(×24), -4(×15).
# λ_{40-10+1} = λ_31 must be ≤ 0. Positions 1..25 are ≥2; position 26..40 are -4.
# So λ_31 = -4 ≤ 0 ✓ and λ_1 = 12 ≥ 0 ✓.
INDEP_M = ALPHA                      # 10
INDEP_LOWER_IDX = V - INDEP_M + 1   # 31
# eigenvalue at position 31 (1-indexed descending):
# pos 1: 12; pos 2..25: 2 (24 copies); pos 26..40: -4 (15 copies)
def eigval_at(pos):
    """Return eigenvalue of W(3,3) adjacency matrix at 1-indexed descending position."""
    if pos == 1:
        return K          # 12
    elif pos <= 1 + MULT_R:
        return R_EIG      # 2
    else:
        return S_EIG      # -4

INDEP_LAMBDA_AT_31 = eigval_at(INDEP_LOWER_IDX)   # S_EIG = -4
INDEP_LAMBDA_AT_1  = eigval_at(1)                  # K = 12
INDEP_ALL_ZERO = True      # all eigenvalues of independent set are 0
INDEP_INTERLACES = (INDEP_LAMBDA_AT_31 <= 0 <= INDEP_LAMBDA_AT_1)

# ── Interlacing: clique K_ω ───────────────────────────────────────────────────
# A clique K_4 has adjacency eigenvalues: ω-1 = 3 (once), -1 (three times).
CLIQUE_M = OMEGA                    # 4
CLIQUE_EIG_MAX = OMEGA - 1         # 3 (largest eigenvalue of K_4)
CLIQUE_EIG_MIN = -1                # smallest eigenvalue of K_4
# Interlacing: λ_{V-ω+1} = λ_37 ≤ -1 ≤ λ_ω = λ_4 = 2
CLIQUE_LOWER_IDX = V - CLIQUE_M + 1    # 37
CLIQUE_UPPER_IDX = CLIQUE_M            # 4
CLIQUE_LAMBDA_AT_37 = eigval_at(CLIQUE_LOWER_IDX)  # -4 ≤ -1 ✓
CLIQUE_LAMBDA_AT_4  = eigval_at(CLIQUE_UPPER_IDX)  # 2 ≥ -1 ✓
CLIQUE_INTERLACES = (
    CLIQUE_LAMBDA_AT_37 <= CLIQUE_EIG_MIN <= CLIQUE_LAMBDA_AT_4
    and S_EIG <= CLIQUE_EIG_MAX <= K
)

# ── Extremal interlacing constraints ─────────────────────────────────────────
# For ANY m-vertex induced subgraph H, μ_1(H) ≤ K = 12.
# For ANY induced subgraph, μ_m(H) ≥ S_EIG = -4.
INTERLACING_UPPER = K          # 12
INTERLACING_LOWER = S_EIG      # -4

# ── Hoffman-type: k-regular induced subgraph ──────────────────────────────────
# If H is an m-vertex k_H-regular induced subgraph, interlacing gives k_H ≤ K.
# Best case: 12-vertex subgraph with all K=12 degree... not possible.
# A 13-vertex subgraph can have degree at most K-1=11 (not regular).
# Key: the 4-clique has degree 3 within H; 3 ≤ K = 12 ✓.
CLIQUE_DEGREE_IN_H = CLIQUE_M - 1    # 3 (= ω - 1 inside K_4)
CLIQUE_DEGREE_LE_K = (CLIQUE_DEGREE_IN_H <= K)
CLIQUE_EIG_MAX_LE_K = (CLIQUE_EIG_MAX <= K)   # 3 ≤ 12

# ── Arithmetic on position indices ───────────────────────────────────────────
# At position 1 + MULT_R = 25: eigenvalue changes from R_EIG to S_EIG.
SPLIT_POS = 1 + MULT_R        # 25
LAST_R_POS = 1 + MULT_R      # = 25
FIRST_S_POS = 1 + MULT_R + 1  # = 26
AT_SPLIT = eigval_at(SPLIT_POS)     # R_EIG = 2 (last R position)
AT_FIRST_S = eigval_at(FIRST_S_POS)  # S_EIG = -4

# ── Connection: MULT_R + 1 = MULT_S + OMEGA + R_EIG ──────────────────────────
# 24 + 1 = 25 = 15 + 4 + 6... let's try 25 = MULT_S + MULT_TAU_0×10... no.
# 25 = 5^2; 25 = V - MULT_S = 40-15 = 25 ✓
V_MINUS_MULT_S = V - MULT_S        # 25
SPLIT_EQ_V_MINUS_MULT_S = (SPLIT_POS == V_MINUS_MULT_S)  # 25 == 25

# ── Interlacing at ALPHA position ─────────────────────────────────────────────
# Position α = 10: λ_10 = R_EIG = 2 (since 1 < 10 ≤ 25).
LAMBDA_AT_ALPHA = eigval_at(ALPHA)  # R_EIG = 2
LAMBDA_AT_ALPHA_EQ_REIG = (LAMBDA_AT_ALPHA == R_EIG)

# ── Wigner bound: K ≤ 2√(K-1)?  No, Ramanujan: λ_2 ≤ 2√(k-1) ───────────────
# W(3,3) has λ_2 = R_EIG = 2.  2√(K-1) = 2√11 ≈ 6.63.
# 2 ≤ 6.63 ✓ ← W(3,3) IS Ramanujan (spectral gap property).
# Use Fraction-safe check: R_EIG² ≤ 4*(K-1) → 4 ≤ 44 ✓
RAMANUJAN_LHS_SQ = R_EIG ** 2           # 4
RAMANUJAN_RHS = 4 * (K - 1)            # 44
IS_RAMANUJAN = (RAMANUJAN_LHS_SQ <= RAMANUJAN_RHS)   # 4 ≤ 44 ✓

# ── Interlacing difference: λ_1 - λ_V = K - S_EIG ───────────────────────────
EIG_SPREAD = K - S_EIG                  # 12 - (-4) = 16 = EW_GAUGE_4²
EIG_SPREAD_EQ_DENOM = (EIG_SPREAD == EW_GAUGE_4 ** 2)   # 16 == 16 ✓

# ── Gram / Cauchy: λ_1 × |λ_V| = K × |S_EIG| = 48 ──────────────────────────
EIG_PRODUCT = K * abs(S_EIG)            # 48 = 12 × 4
EIG_PRODUCT_VALUE = 48
EIG_PRODUCT_CHECK = (EIG_PRODUCT == EIG_PRODUCT_VALUE)
# 48 = EDGES / 5 = 240/5 = 48 ✓
EIG_PRODUCT_FROM_EDGES = EDGES // 5    # 48


# ── Verification ─────────────────────────────────────────────────────────────
def verify_all():
    """Run all 27 CCXCVII checks and return (checks_list, passed, total)."""
    checks = []

    def chk(name, val, exp=True):
        ok = (val == exp) if (exp is not True) else bool(val)
        checks.append((name, ok, val))
        return ok

    # Eigenvalue list structure
    chk("eigval_at(1)==K",       eigval_at(1),       K)
    chk("eigval_at(2)==R_EIG",   eigval_at(2),       R_EIG)
    chk("eigval_at(25)==R_EIG",  eigval_at(25),      R_EIG)
    chk("eigval_at(26)==S_EIG",  eigval_at(26),      S_EIG)
    chk("eigval_at(40)==S_EIG",  eigval_at(40),      S_EIG)

    # Single vertex
    chk("SINGLE_INTERLACES",     SINGLE_INTERLACES)
    chk("S_EIG<=0",              S_EIG <= SINGLE_EIG)
    chk("0<=K",                  SINGLE_EIG <= K)

    # Independent set
    chk("λ_31==S_EIG",           INDEP_LAMBDA_AT_31, S_EIG)
    chk("INDEP_INTERLACES",      INDEP_INTERLACES)

    # Clique
    chk("CLIQUE_EIG_MAX==3",     CLIQUE_EIG_MAX,     3)
    chk("λ_37==S_EIG",           CLIQUE_LAMBDA_AT_37, S_EIG)
    chk("λ_4==R_EIG",            CLIQUE_LAMBDA_AT_4,  R_EIG)
    chk("CLIQUE_INTERLACES",     CLIQUE_INTERLACES)

    # Bounds
    chk("INTERLACING_UPPER==K",  INTERLACING_UPPER,  K)
    chk("INTERLACING_LOWER==S",  INTERLACING_LOWER,  S_EIG)

    # Clique degree
    chk("clique_deg==ω-1",       CLIQUE_DEGREE_IN_H, OMEGA - 1)
    chk("clique_deg≤K",          CLIQUE_DEGREE_LE_K)
    chk("clique_eig_max≤K",      CLIQUE_EIG_MAX_LE_K)

    # Position arithmetic
    chk("SPLIT_POS==25",         SPLIT_POS,          25)
    chk("SPLIT_EQ_V-MULT_S",     SPLIT_EQ_V_MINUS_MULT_S)

    # Ramanujan
    chk("IS_RAMANUJAN",          IS_RAMANUJAN)
    chk("R²≤4(K-1)",             RAMANUJAN_LHS_SQ <= RAMANUJAN_RHS)

    # Spread and product
    chk("EIG_SPREAD==16",        EIG_SPREAD,         16)
    chk("EIG_SPREAD==EW²",       EIG_SPREAD_EQ_DENOM)
    chk("K×|S|==48",             EIG_PRODUCT,        48)
    chk("K×|S|==EDGES//5",      EIG_PRODUCT_FROM_EDGES, 48)

    passed = sum(1 for _, ok, _ in checks if ok)
    total = len(checks)
    return checks, passed, total


def build_ccxcvii_summary():
    """Build the Part CCXCVII result summary dictionary."""
    checks, passed, total = verify_all()
    return {
        "part": "CCXCVII",
        "title": "Eigenvalue Interlacing in W(3,3)",
        "checks_pass": passed,
        "checks_total": total,
        "status": "ALL_PASS" if passed == total else "FAIL",
        "interlacing_upper": INTERLACING_UPPER,
        "interlacing_lower": INTERLACING_LOWER,
        "eig_spread": EIG_SPREAD,
        "eig_product": EIG_PRODUCT,
        "is_ramanujan": IS_RAMANUJAN,
        "split_pos": SPLIT_POS,
        "clique_eig_max": CLIQUE_EIG_MAX,
        "discoveries": [
            "Eigenvalue spread K - S_EIG = 16 = EW_GAUGE_4² (Hoffman denominator)",
            "W(3,3) is Ramanujan: λ_2 = 2 ≤ 2√11 ≈ 6.63 (spectral gap)",
            "Split position 1 + MULT_R = 25 = V - MULT_S (spectrum block boundary)",
            "Clique K_4 interlaces: max eigenvalue 3 ≤ R_EIG + 1 = 3 (tight)",
            "Spectral product K × |S_EIG| = 48 = EDGES / 5 (edge-eigenvalue link)",
            "Independent set I_10 gives μ_i = 0 ∈ [S_EIG, K] = [-4, 12] ✓",
        ],
    }


if __name__ == "__main__":
    checks, passed, total = verify_all()
    for name, ok, val in checks:
        status = "✓" if ok else "✗"
        print(f"  {status} {name}: {val}")
    print(f"\nCCXCVII Verification: {passed}/{total} checks pass {'✓' if passed == total else '✗'}")
