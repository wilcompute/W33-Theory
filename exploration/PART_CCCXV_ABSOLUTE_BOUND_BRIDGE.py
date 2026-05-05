"""PART CCCXV — Absolute Bound & Polynomial Method for W(3,3)

The **Absolute Bound** (Delsarte 1973) is a fundamental inequality for association
schemes derived from the polynomial method:

    v ≤ m_i * (m_i + 1) / 2    for each non-trivial multiplicity m_i

where v is the number of vertices and m_i is the i-th eigenspace multiplicity.
This bound follows from the fact that the minimal idempotents E_i satisfy
positive semi-definite Gram matrix conditions, and the rank of the Hadamard
product E_i ∘ E_i is at most m_i(m_i+1)/2.

**W(3,3) SRG(40, 12, 2, 4) — absolute bound check:**

Multiplicities:
    m_1 = 24   (eigenvalue r = 2)
    m_2 = 15   (eigenvalue s = -4)

Absolute bounds:
    v ≤ m_1(m_1+1)/2 = 24*25/2 = 300    ✓  (40 ≤ 300)
    v ≤ m_2(m_2+1)/2 = 15*16/2 = 120    ✓  (40 ≤ 120)

**SM encodings of the absolute bounds:**
    Bound_S = 120 = v * 3 = V * GENERATIONS
    Bound_R = 300 = v * 15 / 2 = V * MULT_S / LAM

The **Polynomial Method** (Delsarte LP bound) also yields sharp bounds for
cliques and cocliques. Using the Hoffman bound:

    Clique bound:   ω ≤ 1 - k/s = 1 - 12/(-4) = 1 + 3 = 4
    Coclique bound: α ≤ v·|s| / (k + |s|) = 40·4/16 = 10

For W(3,3):
    ω = 4 = GENERATIONS + 1
    α = 10 = ALPHA
    ω × α = 40 = V  (perfect duality!)

The key ratio in the Hoffman clique bound:
    k / |s| = 12 / 4 = 3 = GENERATIONS  (encodes 3-generation structure)

**Krein feasibility via polynomial method:**
The Krein conditions q_{ij}^k ≥ 0 (for all i, j, k) are a generalized polynomial
constraint on the scheme. All 9 distinct Krein parameters of W(3,3) are
non-negative, confirming that the scheme is Krein-feasible.

The vanishing Krein parameter q_{12}^0 = 0 is particularly significant:
it implies the orthogonality of the two non-trivial eigenspaces under
Hadamard product, which is the Q-polynomial analog of orthogonality.

Key Krein parameters (exact fractions):
    q_{11}^0 = 24 = MULT_R
    q_{11}^1 = 44/3    (44 = 4 * ALPHA + 4 = EW_GAUGE_4 * (ALPHA + 1))
    q_{11}^2 = 40/3    (40 = V = 4 * ALPHA)
    q_{12}^0 = 0       (Krein vanishing)
    q_{22}^0 = 15 = MULT_S
    q_{22}^2 = 10/3    (10 = ALPHA; denominator = GENERATIONS)

SM interpretations:
    KR_11_2 * GENERATIONS = V  →  (40/3) * 3 = 40
    KR_22_2 * GENERATIONS = ALPHA  →  (10/3) * 3 = 10
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

# Association scheme class sizes
K0 = 1
K1 = K        # 12
K2 = V - 1 - K  # 27

# Multiplicities
M0 = 1
M1 = MULT_R   # 24
M2 = MULT_S   # 15

# ---------------------------------------------------------------------------
# Absolute bound
# absolute bound from multiplicity m: v ≤ m*(m+1)//2
# ---------------------------------------------------------------------------
BOUND_R = Fraction(MULT_R * (MULT_R + 1), 2)   # 24*25/2 = 300
BOUND_S = Fraction(MULT_S * (MULT_S + 1), 2)   # 15*16/2 = 120

AB_V_LE_BOUND_R = (V <= BOUND_R)   # 40 ≤ 300 ✓
AB_V_LE_BOUND_S = (V <= BOUND_S)   # 40 ≤ 120 ✓

SLACK_R = BOUND_R - V   # 300 - 40 = 260
SLACK_S = BOUND_S - V   # 120 - 40 = 80

# ---------------------------------------------------------------------------
# SM encodings of absolute bounds
# ---------------------------------------------------------------------------
# Bound_S = 120 = V * GENERATIONS = 40 * 3
BOUND_S_SM = (BOUND_S == V * GENERATIONS)       # 120 = 120 ✓

# Bound_R = 300 = V * MULT_S / LAM = 40 * 15 / 2
BOUND_R_SM = (BOUND_R == Fraction(V * MULT_S, LAM))  # 300 = 300 ✓

# V / Bound_S = 1/GENERATIONS
V_OVER_BOUND_S = Fraction(V, int(BOUND_S))
V_OVER_BOUND_S_SM = (V_OVER_BOUND_S == Fraction(1, GENERATIONS))  # 1/3 = 1/3 ✓

# Slack_S = 80 = 2 * V = LAM * V
SLACK_S_SM = (SLACK_S == LAM * V)               # 80 = 80 ✓

# ---------------------------------------------------------------------------
# Krein parameters (computed from Q matrix, exact Fraction arithmetic)
# Q-matrix: Q = 40 * P^{-1}
#   Q[0] = [1, 24, 15]
#   Q[1] = [1,  4, -5]
#   Q[2] = [1, -8/3, 5/3]
# ---------------------------------------------------------------------------
_Q = [
    [Fraction(1),  Fraction(M1),        Fraction(M2)],
    [Fraction(1),  Fraction(4),          Fraction(-5)],
    [Fraction(1),  Fraction(-8, 3),      Fraction(5, 3)],
]
_Kclass = [K0, K1, K2]
_Mmult  = [M0, M1, M2]


def _krein(i, j, k):
    """Compute Krein parameter q_{ij}^k exactly."""
    total = Fraction(0)
    for alpha in range(3):
        total += Fraction(_Kclass[alpha]) * _Q[alpha][i] * _Q[alpha][j] * _Q[alpha][k]
    return total / (Fraction(_Mmult[k]) * Fraction(V))


KR_11_0 = _krein(1, 1, 0)   # 24
KR_11_1 = _krein(1, 1, 1)   # 44/3
KR_11_2 = _krein(1, 1, 2)   # 40/3
KR_12_0 = _krein(1, 2, 0)   # 0
KR_12_1 = _krein(1, 2, 1)   # 25/3
KR_12_2 = _krein(1, 2, 2)   # 32/3
KR_22_0 = _krein(2, 2, 0)   # 15
KR_22_1 = _krein(2, 2, 1)   # 20/3
KR_22_2 = _krein(2, 2, 2)   # 10/3

ALL_KREIN = [KR_11_0, KR_11_1, KR_11_2,
             KR_12_0, KR_12_1, KR_12_2,
             KR_22_0, KR_22_1, KR_22_2]

# Krein feasibility
KR_12_0_ZERO    = (KR_12_0 == Fraction(0))
KR_ALL_NONNEG   = all(q >= 0 for q in ALL_KREIN)
KR_22_2_SM      = (KR_22_2 * GENERATIONS == ALPHA)    # (10/3)*3 = 10 ✓
KR_11_2_SM      = (KR_11_2 * GENERATIONS == V)         # (40/3)*3 = 40 ✓
KR_11_0_EQ_M1   = (KR_11_0 == MULT_R)
KR_22_0_EQ_M2   = (KR_22_0 == MULT_S)

# ---------------------------------------------------------------------------
# Hoffman / Delsarte LP bounds on cliques and cocliques
# ---------------------------------------------------------------------------
# Hoffman clique bound: ω ≤ 1 - k / s_min
# s_min = S_EIG = -4
OMEGA_HOFFMAN = Fraction(1) - Fraction(K, S_EIG)   # 1 - 12/(-4) = 1 + 3 = 4

# Hoffman coclique bound: α ≤ v * |s| / (k + |s|)
ABS_S = abs(S_EIG)                                   # 4
ALPHA_HOFFMAN = Fraction(V * ABS_S, K + ABS_S)      # 40*4 / 16 = 10

OMEGA_EQ_GENERATIONS_PLUS_1 = (OMEGA_HOFFMAN == GENERATIONS + 1)   # 4 = 4 ✓
ALPHA_EQ_ALPHA_SM           = (ALPHA_HOFFMAN == ALPHA)              # 10 = 10 ✓

OMEGA_X_ALPHA = int(OMEGA_HOFFMAN) * int(ALPHA_HOFFMAN)             # 4 * 10 = 40
CLIQUE_COCLIQUE_EQ_V = (OMEGA_X_ALPHA == V)                        # 40 = 40 ✓

# Key ratio in Hoffman clique formula: k / |s| = GENERATIONS
K_OVER_ABS_S = Fraction(K, ABS_S)                   # 12/4 = 3
K_OVER_ABS_S_SM = (K_OVER_ABS_S == GENERATIONS)    # 3 = 3 ✓

# ---------------------------------------------------------------------------
def verify_all():
    """Return (checks_list, passed, total) with exactly 27 checks."""
    checks = [
        # Group 1: SRG parameters (5)
        {"name": "SRG_V_K",          "ok": V == 40 and K == 12},
        {"name": "SRG_lam_mu",        "ok": LAM == 2 and MU == 4},
        {"name": "SRG_eigs",          "ok": R_EIG == 2 and S_EIG == -4},
        {"name": "SRG_mults",         "ok": MULT_R == 24 and MULT_S == 15},
        {"name": "mults_sum_V",       "ok": 1 + MULT_R + MULT_S == V},

        # Group 2: Absolute bound values (5)
        {"name": "bound_R_300",       "ok": BOUND_R == 300},
        {"name": "bound_S_120",       "ok": BOUND_S == 120},
        {"name": "v_le_bound_R",      "ok": AB_V_LE_BOUND_R},
        {"name": "v_le_bound_S",      "ok": AB_V_LE_BOUND_S},
        {"name": "slacks_positive",   "ok": SLACK_R > 0 and SLACK_S > 0},

        # Group 3: SM encodings of bounds (4)
        {"name": "bound_S_eq_V_gen",  "ok": BOUND_S_SM},
        {"name": "bound_R_SM",        "ok": BOUND_R_SM},
        {"name": "V_over_bound_S",    "ok": V_OVER_BOUND_S_SM},
        {"name": "slack_S_eq_lam_V",  "ok": SLACK_S_SM},

        # Group 4: Krein feasibility (6)
        {"name": "kr_12_0_zero",      "ok": KR_12_0_ZERO},
        {"name": "kr_all_nonneg",     "ok": KR_ALL_NONNEG},
        {"name": "kr_22_2_SM",        "ok": KR_22_2_SM},
        {"name": "kr_11_2_SM",        "ok": KR_11_2_SM},
        {"name": "kr_11_0_eq_M1",     "ok": KR_11_0_EQ_M1},
        {"name": "kr_22_0_eq_M2",     "ok": KR_22_0_EQ_M2},

        # Group 5: Hoffman / LP bounds (5)
        {"name": "omega_hoffman_4",   "ok": OMEGA_HOFFMAN == 4},
        {"name": "omega_gen_plus_1",  "ok": OMEGA_EQ_GENERATIONS_PLUS_1},
        {"name": "alpha_hoffman_10",  "ok": ALPHA_EQ_ALPHA_SM},
        {"name": "clique_coclique_V", "ok": CLIQUE_COCLIQUE_EQ_V},
        {"name": "k_over_abs_s_gen",  "ok": K_OVER_ABS_S_SM},

        # Group 6: Slack & final SM checks (2)
        {"name": "slack_R_260",       "ok": SLACK_R == 260},
        {"name": "slack_S_80",        "ok": SLACK_S == 80},
    ]
    passed = sum(1 for c in checks if c["ok"])
    return checks, passed, len(checks)


def build_cccxv_summary():
    """Return summary dict for PART CCCXV."""
    checks, passed, total = verify_all()
    return {
        "part": "CCCXV",
        "title": "Absolute Bound & Polynomial Method for W(3,3)",
        "checks_pass": passed,
        "checks_total": total,
        "status": "PASS" if passed == total else "FAIL",
        "fields": {
            "V": V,
            "K": K,
            "MULT_R": MULT_R,
            "MULT_S": MULT_S,
            "BOUND_R": int(BOUND_R),
            "BOUND_S": int(BOUND_S),
            "SLACK_R": int(SLACK_R),
            "SLACK_S": int(SLACK_S),
            "omega_hoffman": int(OMEGA_HOFFMAN),
            "alpha_hoffman": int(ALPHA_HOFFMAN),
            "KR_12_0": float(KR_12_0),
            "KR_22_2": str(KR_22_2),
            "KR_11_2": str(KR_11_2),
            "k_over_abs_s": int(K_OVER_ABS_S),
        },
        "discoveries": [
            "Absolute bound from MULT_S: V ≤ 120 = V * GENERATIONS (tight SM encoding)",
            "Absolute bound from MULT_R: V ≤ 300 = V * MULT_S / LAM",
            "Slack_S = 80 = LAM * V (double the vertex count)",
            "V / Bound_S = 1/GENERATIONS (perfect reciprocal of generations)",
            "Hoffman clique ω = 4 = GENERATIONS + 1",
            "Hoffman coclique α = 10 = ALPHA",
            "ω × α = 40 = V (perfect clique-coclique duality)",
            "k / |s| = 3 = GENERATIONS (Hoffman ratio encodes generations)",
            "KR_22_2 × GENERATIONS = ALPHA (Krein encodes fine structure)",
            "KR_11_2 × GENERATIONS = V (Krein encodes vertex count)",
            "q_{12}^0 = 0: Krein orthogonality of the two eigenspaces",
        ],
    }


if __name__ == "__main__":
    checks, passed, total = verify_all()
    for c in checks:
        status = "PASS" if c["ok"] else "FAIL"
        print(f"  [{status}] {c['name']}")
    print(f"\nResult: {passed}/{total}")
    summary = build_cccxv_summary()
    print(f"Status: {summary['status']}")
