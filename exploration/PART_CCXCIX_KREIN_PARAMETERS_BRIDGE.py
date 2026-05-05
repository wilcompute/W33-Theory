"""
PART CCXCIX — Krein Parameters of the W(3,3) Bose-Mesner Algebra
==================================================================
The association scheme {A_0=I, A_1=W(3,3), A_2=complement} has first
eigenmatrix P built from the SRG(40,12,2,4) spectrum.  Its second
eigenmatrix Q = v·P⁻¹ encodes the *Krein parameters* q^k_{ij}, which
are the dual intersection numbers that must be non-negative by the
Delsarte–Krein conditions.

Builds on:
  CCXCVIII — Equitable partitions / quotient matrices  (69/69 ✓)
  CCXCVII  — Cauchy–Interlacing theorem                (78/78 ✓)
  CCXCVI   — Hoffman ratio bound = 10 = α              (70/70 ✓)
  CCXCV    — Seidel matrix spectral decomposition      (✓)

Central result:
  Every Krein parameter q^k_{ij} ≥ 0 (Krein conditions hold).
  The parameters encode the graph constants V, K, ALPHA, MULT_R,
  MULT_S, MU, and EW_GAUGE_4 in exact rational form:

      3·q²₁₁  = V   = 40
      3·q²₂₂  = α   = 10    (Hoffman bound from CCXCVI)
      3·q¹₁₂  = α + MULT_S = 25
      3·q²₁₂  = MULT_R + 2·MU = 32
      3·(q¹₁₁ + q¹₂₂) = EW³ = 64
      q¹₁₁ + q²₁₁  = V − K = 28
      q¹₂₂ + q²₂₂  = α     = 10
      q⁰₁₁  = MULT_R = 24
      q⁰₂₂  = MULT_S = 15

Test suite: 27 checks in verify_all().
"""

from fractions import Fraction

# ── W(3,3) SRG constants ────────────────────────────────────────────────────
V         = 40          # vertices
K         = 12          # valency (adjacency eigenvalue k)
K2        = 27          # complement valency = V − 1 − K
LAM       = 2           # λ  (common neighbours of adjacent pair)
MU        = 4           # μ  (common neighbours of non-adjacent pair)
EDGES     = 240         # |E| = V·K/2
R_EIG     = 2           # restricted eigenvalue r  (multiplicity f)
S_EIG     = -4          # restricted eigenvalue s  (multiplicity g)
MULT_R    = 24          # f — multiplicity of r
MULT_S    = 15          # g — multiplicity of s
EW_GAUGE_4 = 4          # |λ_min| = 4 — electroweak gauge-boson count
ALPHA     = 10          # Hoffman independence number (CCXCVI)

# ── First eigenmatrix P ─────────────────────────────────────────────────────
# P[i][j] = eigenvalue of A_j on the i-th eigenspace.
# Classes: A_0=I (valency 1), A_1=W (valency K=12), A_2=complement (valency K2=27)
# Eigenspaces: E_0 (trivial, mult 1), E_1 (r-space, mult MULT_R), E_2 (s-space, mult MULT_S)
#
#        A_0  A_1   A_2
# E_0  [  1,  12,   27 ]     ← trivial eigenvalue on each class
# E_1  [  1,   2,   -3 ]     ← A_2 eigenvalue = -1 - R_EIG = -3
# E_2  [  1,  -4,    3 ]     ← A_2 eigenvalue = -1 - S_EIG =  3

_P = [
    [Fraction(1), Fraction(K),     Fraction(K2)        ],
    [Fraction(1), Fraction(R_EIG), Fraction(-1-R_EIG)  ],
    [Fraction(1), Fraction(S_EIG), Fraction(-1-S_EIG)  ],
]

# ── Helpers ─────────────────────────────────────────────────────────────────

def _det3(M):
    """Determinant of a 3×3 matrix of Fractions."""
    a, b, c = M[0]
    d, e, f = M[1]
    g, h, i = M[2]
    return a*(e*i - f*h) - b*(d*i - f*g) + c*(d*h - e*g)


def _inv3(M):
    """
    Exact inverse of a 3×3 matrix of Fractions.
    Returns P_inv[i][j] = (P^{-1})_{ij}.
    """
    det = _det3(M)
    if det == 0:
        raise ValueError("Matrix is singular")
    a, b, c = M[0]
    d, e, f = M[1]
    g, h, i = M[2]
    # cofactor matrix (transposed → adjugate)
    C = [
        [ e*i - f*h,  -(b*i - c*h),   b*f - c*e ],
        [-(d*i - f*g),  a*i - c*g,  -(a*f - c*d)],
        [ d*h - e*g,  -(a*h - b*g),   a*e - b*d  ],
    ]
    return [[C[i][j] / det for j in range(3)] for i in range(3)]


def _solve3(A_coeff, b_rhs):
    """
    Solve A_coeff · x = b_rhs for x using Cramer's rule (exact Fractions).
    A_coeff is a 3×3 list-of-lists, b_rhs is a length-3 list.
    """
    det = _det3(A_coeff)
    results = []
    for col in range(3):
        M = [[A_coeff[r][c] if c != col else b_rhs[r]
              for c in range(3)] for r in range(3)]
        results.append(_det3(M) / det)
    return results

# ── Compute P inverse and second eigenmatrix Q = v·P⁻¹ ─────────────────────

P_INV = _inv3(_P)
_v = Fraction(V)

# Q[i][j] = v · P_inv[i][j]   (Q = v · P⁻¹)
Q_MAT = [[_v * P_INV[i][j] for j in range(3)] for i in range(3)]

P_DET = _det3(_P)

# ── Idempotent coefficients ─────────────────────────────────────────────────
# E_l = sum_j (P^{-1})_{j,l} A_j   →   E_l[A_0, A_1, A_2] = col l of P_inv
E0_COEFF = [P_INV[j][0] for j in range(3)]  # coefficients of I, A, A2 in E_0
E1_COEFF = [P_INV[j][1] for j in range(3)]  # coefficients of I, A, A2 in E_1
E2_COEFF = [P_INV[j][2] for j in range(3)]  # coefficients of I, A, A2 in E_2

# ── Krein parameters via Hadamard products ──────────────────────────────────
# E_i has entries on diag/adj/non-adj rows given by E_i_COEFF[0]*1 / [1]*K / [1]*K2.
# The Hadamard product E_i ∘ E_j is a matrix whose entry at position (u,v)
# equals E_i(u,v) · E_j(u,v). Since E_i is a matrix with three distinct
# entry values (diagonal, adjacent, non-adjacent), E_i ∘ E_j also has three
# distinct values, and those can be expressed as aI + bA + cA₂.
#
# Concretely:
#   (E_i ∘ E_j)[diag]     = E_i_COEFF[0] · E_j_COEFF[0]       (coeff of A_0)
#   (E_i ∘ E_j)[adj]      = E_i_COEFF[1] · E_j_COEFF[1]       (coeff of A_1)
#   (E_i ∘ E_j)[non-adj]  = E_i_COEFF[2] · E_j_COEFF[2]       (coeff of A_2)
#
# Krein equation: E_i ∘ E_j = (1/v) Σ_k q^k_{ij} E_k
# → for each "class coefficient" we get a linear system in (q^0,q^1,q^2).

def _krein_params(ei_coeff, ej_coeff):
    """
    Compute (q0, q1, q2) = (q^0_{ij}, q^1_{ij}, q^2_{ij}).

    The three equations (one per class A_0, A_1, A_2):
      sum_k q^k * E_k_COEFF[m] = v * ei_coeff[m] * ej_coeff[m]   (m=0,1,2)

    Written as a 3×3 linear system A·q = b, where
      A[m][k] = E_k_COEFF[m]
      b[m]    = v * ei_coeff[m] * ej_coeff[m]
    """
    _ec = [E0_COEFF, E1_COEFF, E2_COEFF]
    A = [[_ec[k][m] for k in range(3)] for m in range(3)]
    b = [_v * ei_coeff[m] * ej_coeff[m] for m in range(3)]
    return _solve3(A, b)


# All six (i,j) pairs with i ≤ j (scheme has 3 classes 0,1,2)
_Q00 = _krein_params(E0_COEFF, E0_COEFF)
_Q11 = _krein_params(E1_COEFF, E1_COEFF)
_Q12 = _krein_params(E1_COEFF, E2_COEFF)
_Q22 = _krein_params(E2_COEFF, E2_COEFF)

# q^k_{00}   →  should give (1, 0, 0) — E0 is "trivial" idempotent
KREIN_Q00 = tuple(_Q00)   # (q^0_{00}, q^1_{00}, q^2_{00})

# q^k_{11}
KREIN_Q11 = tuple(_Q11)   # (q^0_{11}, q^1_{11}, q^2_{11})
Q0_11 = _Q11[0]           # = MULT_R = 24
Q1_11 = _Q11[1]           # = 44/3
Q2_11 = _Q11[2]           # = 40/3

# q^k_{12}   (q^k_{21} = q^k_{12} by symmetry)
KREIN_Q12 = tuple(_Q12)
Q0_12 = _Q12[0]           # = 0
Q1_12 = _Q12[1]           # = 25/3
Q2_12 = _Q12[2]           # = 32/3

# q^k_{22}
KREIN_Q22 = tuple(_Q22)
Q0_22 = _Q22[0]           # = MULT_S = 15
Q1_22 = _Q22[1]           # = 20/3
Q2_22 = _Q22[2]           # = 10/3

# Collect all non-trivial Krein parameters for non-negativity check
_ALL_KREIN = list(KREIN_Q11) + list(KREIN_Q12) + list(KREIN_Q22)
ALL_KREIN_NONNEG = all(q >= 0 for q in _ALL_KREIN)

# ── Summary dictionary ───────────────────────────────────────────────────────

def build_ccxcix_summary():
    """
    Returns a dict summarising Part CCXCIX (Krein Parameters).
    """
    _, passed, total = verify_all()
    return {
        "part":          "CCXCIX",
        "title":         "Krein Parameters of the W(3,3) Bose-Mesner Algebra",
        "checks_pass":   passed,
        "checks_total":  total,
        "status":        "PASS" if passed == total else "FAIL",
        "fields": {
            "V":            V,
            "K":            K,
            "K2":           K2,
            "R_EIG":        R_EIG,
            "S_EIG":        S_EIG,
            "MULT_R":       MULT_R,
            "MULT_S":       MULT_S,
            "ALPHA":        ALPHA,
            "P_DET":        int(P_DET),
            "E1_COEFF":     [str(c) for c in E1_COEFF],
            "E2_COEFF":     [str(c) for c in E2_COEFF],
            "Q0_11":        str(Q0_11),
            "Q1_11":        str(Q1_11),
            "Q2_11":        str(Q2_11),
            "Q0_12":        str(Q0_12),
            "Q1_12":        str(Q1_12),
            "Q2_12":        str(Q2_12),
            "Q0_22":        str(Q0_22),
            "Q1_22":        str(Q1_22),
            "Q2_22":        str(Q2_22),
            "ALL_KREIN_NONNEG": ALL_KREIN_NONNEG,
        },
        "discoveries": [
            "3·q²₁₁ = V = 40  (Krein parameter encodes vertex count)",
            "3·q²₂₂ = α = 10  (Krein parameter = Hoffman bound from CCXCVI)",
            "q⁰₁₁ = MULT_R = 24  (trivial Krein parameter = eigenvalue multiplicity)",
            "q⁰₂₂ = MULT_S = 15  (trivial Krein parameter = eigenvalue multiplicity)",
            "3·q¹₁₂ = α + MULT_S = 25",
            "3·q²₁₂ = MULT_R + 2·MU = 32",
            "3·(q¹₁₁ + q¹₂₂) = EW³ = 64  (cube of electroweak gauge count)",
            "q¹₁₁ + q²₁₁ = V − K = 28  (complement valency + 1)",
            "q¹₂₂ + q²₂₂ = α = 10  (cross-pair sum = Hoffman bound)",
            "All Krein parameters ≥ 0: Delsarte–Krein conditions hold",
        ],
    }


# ── Verification suite: exactly 27 checks ───────────────────────────────────

def verify_all():
    """
    Run all 27 checks.  Returns (checks, passed, total).
    Each check is a dict with keys 'name', 'result', 'expected', 'ok'.
    """
    checks = []

    def chk(name, got, exp):
        ok = (got == exp)
        checks.append({"name": name, "result": got, "expected": exp, "ok": ok})

    # ── Group 1: First eigenmatrix P structure (4 checks) ───────────────────
    chk("P[0][1] == K",
        _P[0][1], Fraction(K))
    chk("P[1][1] == R_EIG",
        _P[1][1], Fraction(R_EIG))
    chk("P[2][1] == S_EIG",
        _P[2][1], Fraction(S_EIG))
    chk("det(P) == -EDGES",
        P_DET, Fraction(-EDGES))

    # ── Group 2: Idempotent coefficients from P^{-1} (6 checks) ────────────
    chk("E1_coeff[A0] == 3/5",
        E1_COEFF[0], Fraction(3, 5))
    chk("E1_coeff[A1] == 1/10",
        E1_COEFF[1], Fraction(1, 10))
    chk("E1_coeff[A2] == -1/15",
        E1_COEFF[2], Fraction(-1, 15))
    chk("E2_coeff[A0] == 3/8",
        E2_COEFF[0], Fraction(3, 8))
    chk("E2_coeff[A1] == -1/8",
        E2_COEFF[1], Fraction(-1, 8))
    chk("E2_coeff[A2] == 1/24",
        E2_COEFF[2], Fraction(1, 24))

    # ── Group 3: Idempotent self-consistency (3 checks) ─────────────────────
    # E_i has eigenvalue 1 on its own eigenspace, 0 on others.
    # Check: sum_j E1_coeff[j] * P[1][j] == 1  (r-eigenspace)
    e1_on_r = sum(E1_COEFF[j] * _P[1][j] for j in range(3))
    chk("E_1 eigenvalue on r-space == 1", e1_on_r, Fraction(1))
    # Check: sum_j E2_coeff[j] * P[2][j] == 1  (s-eigenspace)
    e2_on_s = sum(E2_COEFF[j] * _P[2][j] for j in range(3))
    chk("E_2 eigenvalue on s-space == 1", e2_on_s, Fraction(1))
    # Check: sum_j E1_coeff[j] * P[2][j] == 0  (cross-eigenspace)
    e1_on_s = sum(E1_COEFF[j] * _P[2][j] for j in range(3))
    chk("E_1 eigenvalue on s-space == 0", e1_on_s, Fraction(0))

    # ── Group 4: Trivial Krein parameters (4 checks) ────────────────────────
    chk("q^0_{11} == MULT_R",
        Q0_11, Fraction(MULT_R))
    chk("q^0_{12} == 0  (orthogonality)",
        Q0_12, Fraction(0))
    chk("q^0_{22} == MULT_S",
        Q0_22, Fraction(MULT_S))

    # ── Group 5: Non-trivial Krein parameters exact values (6 checks) ───────
    chk("3·q^1_{11} == 44",
        3 * Q1_11, Fraction(44))
    chk("3·q^1_{12} == 25",
        3 * Q1_12, Fraction(25))
    chk("3·q^1_{22} == 20",
        3 * Q1_22, Fraction(20))
    chk("3·q^2_{11} == 40 == V",
        3 * Q2_11, Fraction(V))
    chk("3·q^2_{12} == 32",
        3 * Q2_12, Fraction(32))
    chk("3·q^2_{22} == 10 == ALPHA",
        3 * Q2_22, Fraction(ALPHA))

    # ── Group 6: SM / combinatorial identities (4 checks) ───────────────────
    chk("q^1_{11} + q^2_{11} == V - K  (= 28)",
        Q1_11 + Q2_11, Fraction(V - K))
    chk("q^1_{22} + q^2_{22} == ALPHA  (= 10)",
        Q1_22 + Q2_22, Fraction(ALPHA))
    chk("3·(q^1_{11} + q^1_{22}) == EW_GAUGE_4^3  (= 64)",
        3 * (Q1_11 + Q1_22), Fraction(EW_GAUGE_4 ** 3))
    chk("3·q^1_{12} == ALPHA + MULT_S  (= 25)",
        3 * Q1_12, Fraction(ALPHA + MULT_S))

    # ── All Krein params ≥ 0 (1 check) ──────────────────────────────────────
    # _ALL_KREIN has 9 entries (3 tuples × 3): Q11, Q12, Q22
    nonneg_count = sum(1 for q in _ALL_KREIN if q >= 0)
    chk("All 9 non-trivial Krein params >= 0  (Krein conditions)",
        nonneg_count, 9)

    passed = sum(1 for c in checks if c["ok"])
    return checks, passed, len(checks)


# ── Self-test ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    checks, passed, total = verify_all()
    print(f"\nPART CCXCIX — Krein Parameters of W(3,3) Bose-Mesner Algebra")
    print(f"{'='*65}")
    for c in checks:
        mark = "✓" if c["ok"] else "✗"
        print(f"  {mark}  {c['name']}")
        if not c["ok"]:
            print(f"       got={c['result']}  expected={c['expected']}")
    print(f"\n{passed}/{total} checks passed")
    if passed == total:
        print("STATUS: PASS")
    else:
        print("STATUS: FAIL")
    print()
    summary = build_ccxcix_summary()
    print("Key discoveries:")
    for d in summary["discoveries"]:
        print(f"  • {d}")
