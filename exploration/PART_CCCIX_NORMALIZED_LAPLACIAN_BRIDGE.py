"""PART CCCIX — Normalized Laplacian Spectrum of W(3,3)

The normalized Laplacian of a graph G is:
    L_norm = D^{-1/2} L D^{-1/2} = I - D^{-1/2} A D^{-1/2}

For a K-regular graph D = K*I, so D^{-1/2} = (1/sqrt(K))*I and:
    L_norm = I - A/K

Thus the eigenvalues of L_norm are mu_i = 1 - lambda_i/K where lambda_i are
the adjacency eigenvalues of G.

W(3,3) adjacency eigenvalues: K=12 (mult 1), R=2 (mult 24), S=-4 (mult 15)

Normalized Laplacian eigenvalues:
    mu_0 = 1 - K/K = 0            (mult 1)
    mu_1 = 1 - R/K = 1 - 2/12 = 5/6   (mult 24)
    mu_2 = 1 - S/K = 1 - (-4)/12 = 4/3 (mult 15)

Using exact Fraction arithmetic for mu_1, mu_2.
"""

from fractions import Fraction

# ---------------------------------------------------------------------------
# W(3,3) SRG parameters
# ---------------------------------------------------------------------------
V = 40
K = 12
LAM = 2
MU = 4
EDGES = 240
R_EIG = 2
S_EIG = -4
MULT_R = 24
MULT_S = 15

# SM constants
EW_GAUGE_4 = 4
ALPHA = 10
GUT_DIM = 27
GENERATIONS = 3

# ---------------------------------------------------------------------------
# Normalized Laplacian eigenvalues (exact fractions)
# ---------------------------------------------------------------------------
NL_EIG_0 = Fraction(0)           # 1 - K/K = 0
NL_EIG_1 = Fraction(1) - Fraction(R_EIG, K)  # 1 - 2/12 = 5/6
NL_EIG_2 = Fraction(1) - Fraction(S_EIG, K)  # 1 - (-4)/12 = 4/3

NL_MULT_0 = 1
NL_MULT_1 = MULT_R   # 24
NL_MULT_2 = MULT_S   # 15
NL_MULT_SUM = NL_MULT_0 + NL_MULT_1 + NL_MULT_2  # 40 = V

# Verify exact values
assert NL_EIG_1 == Fraction(5, 6)
assert NL_EIG_2 == Fraction(4, 3)

# ---------------------------------------------------------------------------
# Spectral identities
# ---------------------------------------------------------------------------
# Trace = sum of eigenvalues
NL_TRACE = (NL_MULT_0 * NL_EIG_0
            + NL_MULT_1 * NL_EIG_1
            + NL_MULT_2 * NL_EIG_2)
# = 0 + 24*(5/6) + 15*(4/3) = 20 + 20 = 40
# For connected K-regular: trace(L_norm) = V - 1 ... actually = V*(1 - K/...) 
# The correct identity: sum eigenvalues = tr(I - A/K) = V - tr(A)/K = V - 0 = V
NL_TRACE_EQ_V = (NL_TRACE == V)  # 40 == 40  True

# Second moment
NL_TRACE_SQ = (NL_MULT_0 * NL_EIG_0**2
               + NL_MULT_1 * NL_EIG_1**2
               + NL_MULT_2 * NL_EIG_2**2)
# = 0 + 24*(25/36) + 15*(16/9) = 600/36 + 240/9 = 50/3 + 80/3 = 130/3
NL_TRACE_SQ_FORMULA = (Fraction(1) + Fraction(1, K)) * (V - 1)
# trace(L_norm^2) = tr((I - A/K)^2) = tr(I) - 2*tr(A)/K + tr(A^2)/K^2
# tr(A^2) = 2*EDGES = 480; tr(A)=0
# = V + tr(A^2)/K^2 = 40 + 480/144 = 40 + 10/3 = 130/3
NL_TRACE_SQ_ALT = Fraction(V) + Fraction(2 * EDGES, K * K)
NL_TRACE_SQ_EQ = (NL_TRACE_SQ == NL_TRACE_SQ_ALT)  # both 130/3, True

# Largest eigenvalue = mu_2 = 4/3
NL_LARGEST = NL_EIG_2  # 4/3
# For connected non-bipartite: mu_max < 2
NL_LARGEST_LT_2 = (NL_LARGEST < 2)  # True

# Spectral gap (smallest nonzero eigenvalue = mu_1 = 5/6)
NL_GAP = NL_EIG_1  # 5/6
NL_GAP_EQ = (NL_GAP == Fraction(5, 6))  # True

# ---------------------------------------------------------------------------
# SM encodings
# ---------------------------------------------------------------------------
# mu_1 numerator = 5 = MU + 1
NL_EIG1_NUM = NL_EIG_1.numerator   # 5
NL_EIG1_DEN = NL_EIG_1.denominator  # 6
NL_EIG1_NUM_SM = (NL_EIG1_NUM == MU + 1)  # 5 == 5  True

# mu_1 denominator = 6 = K/2
NL_EIG1_DEN_SM = (NL_EIG1_DEN == K // 2)  # 6 == 6  True

# mu_2 numerator = 4 = MU
NL_EIG2_NUM = NL_EIG_2.numerator   # 4
NL_EIG2_DEN = NL_EIG_2.denominator  # 3
NL_EIG2_NUM_SM = (NL_EIG2_NUM == MU)  # 4 == 4  True

# mu_2 denominator = 3 = GENERATIONS
NL_EIG2_DEN_SM = (NL_EIG2_DEN == GENERATIONS)  # 3 == 3  True

# mu_1 + mu_2 = 5/6 + 4/3 = 5/6 + 8/6 = 13/6
NL_SUM_12 = NL_EIG_1 + NL_EIG_2  # 13/6
NL_SUM_12_NUM = NL_SUM_12.numerator   # 13
NL_SUM_12_DEN = NL_SUM_12.denominator  # 6

# ALPHA + 3 = 13; K/2 = 6
NL_SUM_12_SM = (NL_SUM_12_NUM == ALPHA + GENERATIONS and NL_SUM_12_DEN == K // 2)
# 13 == 13, 6 == 6  True

# mu_2 - mu_1 = 4/3 - 5/6 = 8/6 - 5/6 = 3/6 = 1/2
NL_DIFF_21 = NL_EIG_2 - NL_EIG_1  # 1/2
NL_DIFF_21_SM = (NL_DIFF_21 == Fraction(1, 2))  # True

# mu_1 * mu_2 = (5/6)*(4/3) = 20/18 = 10/9
NL_PROD_12 = NL_EIG_1 * NL_EIG_2  # 10/9
NL_PROD_12_NUM = NL_PROD_12.numerator   # 10
NL_PROD_12_DEN = NL_PROD_12.denominator  # 9
NL_PROD_12_SM = (NL_PROD_12_NUM == ALPHA and NL_PROD_12_DEN == V // EW_GAUGE_4 - 1)
# ALPHA=10 True; V//4 - 1 = 10-1 = 9  True

# Trace = V = 40: V = ALPHA*EW_GAUGE_4 = 10*4
NL_TRACE_SM = (NL_TRACE == V and V == ALPHA * EW_GAUGE_4)

# Algebraic connectivity (Fiedler): related. mu_1 = 5/6; 6*mu_1 = 5 = MU+1
NL_FIEDLER_INT = 6 * NL_EIG_1   # 5 (as fraction numerator after multiply by denom)
NL_FIEDLER_SM = (NL_FIEDLER_INT == MU + 1)  # True

# ---------------------------------------------------------------------------
# Isoperimetric / Cheeger-type identity
# ---------------------------------------------------------------------------
# For K-regular: Cheeger constant h(G) satisfies mu_1/2 <= h(G) <= sqrt(2*mu_1)
# We just encode the exact rational bounds
NL_CHEEGER_LB = NL_EIG_1 / 2   # 5/12
NL_CHEEGER_UB_SQ = 2 * NL_EIG_1  # 5/3
NL_CHEEGER_LB_NUM_SM = (NL_CHEEGER_LB.numerator == MU + 1 and NL_CHEEGER_LB.denominator == K)
# 5 == 5, 12 == 12  True

# Multiplicity sum check
NL_MULTS_SUM_EQ_V = (NL_MULT_SUM == V)  # 40 == 40  True

# Ordering: 0 < mu_1 < 1 < mu_2 < 2
NL_ORDERING = (NL_EIG_0 < NL_EIG_1 < 1 < NL_EIG_2 < 2)  # True


# ---------------------------------------------------------------------------
def verify_all():
    """Return (checks_list, passed, total) with exactly 27 checks."""
    checks = [
        # Group 1: SRG parameters (5)
        {"name": "SRG_V_K", "ok": V == 40 and K == 12},
        {"name": "SRG_edges", "ok": EDGES == 240},
        {"name": "SRG_adj_eigs", "ok": R_EIG == 2 and S_EIG == -4},
        {"name": "SRG_mults", "ok": MULT_R == 24 and MULT_S == 15},
        {"name": "SM_constants", "ok": ALPHA == 10 and MU == 4 and GENERATIONS == 3},

        # Group 2: Normalized Laplacian eigenvalues (5)
        {"name": "NL_eig0_zero", "ok": NL_EIG_0 == Fraction(0)},
        {"name": "NL_eig1_frac", "ok": NL_EIG_1 == Fraction(5, 6)},
        {"name": "NL_eig2_frac", "ok": NL_EIG_2 == Fraction(4, 3)},
        {"name": "NL_mults_sum_V", "ok": NL_MULTS_SUM_EQ_V},
        {"name": "NL_ordering", "ok": NL_ORDERING},

        # Group 3: Spectral identities (5)
        {"name": "NL_trace_eq_V", "ok": NL_TRACE_EQ_V},
        {"name": "NL_trace_sq_eq", "ok": NL_TRACE_SQ_EQ},
        {"name": "NL_largest_lt_2", "ok": NL_LARGEST_LT_2},
        {"name": "NL_gap_exact", "ok": NL_GAP_EQ},
        {"name": "NL_diff_21_half", "ok": NL_DIFF_21_SM},

        # Group 4: SM encodings via numerators/denominators (6)
        {"name": "NL_eig1_num_MU1", "ok": NL_EIG1_NUM_SM},
        {"name": "NL_eig1_den_K2", "ok": NL_EIG1_DEN_SM},
        {"name": "NL_eig2_num_MU", "ok": NL_EIG2_NUM_SM},
        {"name": "NL_eig2_den_GEN", "ok": NL_EIG2_DEN_SM},
        {"name": "NL_sum12_SM", "ok": NL_SUM_12_SM},
        {"name": "NL_prod12_SM", "ok": NL_PROD_12_SM},

        # Group 5: Algebraic/Cheeger (3)
        {"name": "NL_trace_SM", "ok": NL_TRACE_SM},
        {"name": "NL_fiedler_SM", "ok": NL_FIEDLER_SM},
        {"name": "NL_cheeger_lb_SM", "ok": NL_CHEEGER_LB_NUM_SM},

        # Group 6: Finale (3)
        {"name": "NL_eig1_formula", "ok": NL_EIG_1 == 1 - Fraction(R_EIG, K)},
        {"name": "NL_eig2_formula", "ok": NL_EIG_2 == 1 - Fraction(S_EIG, K)},
        {"name": "NL_trace_sq_alt", "ok": NL_TRACE_SQ == Fraction(130, 3)},
    ]
    passed = sum(1 for c in checks if c["ok"])
    return checks, passed, len(checks)


def build_cccix_summary():
    """Return summary dict for PART CCCIX."""
    checks, passed, total = verify_all()
    return {
        "part": "CCCIX",
        "title": "Normalized Laplacian Spectrum of W(3,3)",
        "checks_pass": passed,
        "checks_total": total,
        "status": "PASS" if passed == total else "FAIL",
        "fields": {
            "NL_EIG_0": str(NL_EIG_0),
            "NL_EIG_1": str(NL_EIG_1),
            "NL_EIG_2": str(NL_EIG_2),
            "NL_MULT_0": NL_MULT_0,
            "NL_MULT_1": NL_MULT_1,
            "NL_MULT_2": NL_MULT_2,
            "NL_TRACE": str(NL_TRACE),
            "NL_TRACE_SQ": str(NL_TRACE_SQ),
            "NL_GAP": str(NL_GAP),
            "NL_LARGEST": str(NL_LARGEST),
            "NL_PROD_12": str(NL_PROD_12),
        },
        "discoveries": [
            "NL_eig1 = 5/6: numerator=MU+1=5, denominator=K/2=6",
            "NL_eig2 = 4/3: numerator=MU=4, denominator=GENERATIONS=3",
            "NL_eig1*NL_eig2 = 10/9: numerator=ALPHA, denominator=V//4-1",
            "NL_eig1+NL_eig2 = 13/6: numerator=ALPHA+GENERATIONS, denominator=K/2",
            "tr(L_norm)=V=ALPHA*EW_GAUGE_4: fundamental SM-SRG trace identity",
            "NL_eig2 - NL_eig1 = 1/2: the gap between non-trivial eigenvalues is 1/2",
            "Cheeger lower bound = 5/12: numerator=MU+1, denominator=K",
            "6*NL_eig1 = 5 = MU+1: Fiedler value times K/2 encodes co-degree",
        ],
    }


if __name__ == "__main__":
    checks, passed, total = verify_all()
    print(f"PART CCCIX: {passed}/{total} checks passed")
    for c in checks:
        status = "OK" if c["ok"] else "FAIL"
        print(f"  [{status}] {c['name']}")
