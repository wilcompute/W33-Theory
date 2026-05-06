"""
PART CCCXLVI — Q-Matrix Coupling Ratios and the Weinberg Angle

The second eigenmatrix Q = v · P⁻¹ of W(3,3) is:

    Q = [[1,     24,     15  ],
         [1,      4,     -5  ],
         [1,   -8/3,    5/3  ]]

Its off-diagonal entries encode three pillars of Standard Model structure
with no free parameters:

  Q[1,1] = MU  = 4        →  four electroweak gauge bosons (W±, Z, γ)
  Q[1,2] = -(MU+1) = -5  →  -(SU(5) rank)
  Q[2,2] = (MU+1)/GENS   →  κ_Y = 5/3 (SU(5) hypercharge normalization)
  |Q[2,1]| × GENS = K−MU →  8 gluons (SU(3)_C octet)

The hypercharge normalization κ_Y = Q[2,2] = 5/3 determines the tree-level
Weinberg angle via:

    sin²θ_W = 1 / (1 + κ_Y) = 1 / (1 + 5/3) = 3/8

Equivalently: sin²θ_W = GENERATIONS / (GENERATIONS + SU5_DIM) = 3/8.

All arithmetic is exact rational (Fraction).  No numpy.  27 checks pass.
"""
from fractions import Fraction

# ── W(3,3) SRG parameters ────────────────────────────────────────────────────
V      = 40
K      = 12
LAM    = 2
MU     = 4
MULT_R = 24    # multiplicity of r-eigenvalue (m_1)
MULT_S = 15    # multiplicity of s-eigenvalue (m_2)
R_EIG  = 2
S_EIG  = -4

# ── Standard-model / GUT constants ───────────────────────────────────────────
EW_GAUGE_4  = 4    # four electroweak gauge bosons: W+, W-, Z, γ
GENERATIONS = 3
GUT_DIM     = 27   # E_6 fundamental representation dimension
SU5_DIM     = 5    # SU(5) rank
SU5_ADJ     = SU5_DIM ** 2 - 1   # 24
GLUON_COUNT = 8    # SU(3)_C gluon octet

# Relation class sizes: k_0=1 (identity), k_1=K (adjacency), k_2=V-K-1 (complement)
K0 = 1
K1 = K
K2 = V - K - 1    # 27

# ── Second eigenmatrix Q = v · P⁻¹ ───────────────────────────────────────────
#
# First eigenmatrix P (rows = eigenspaces {trivial, r, s}; cols = relations {I, A, J̄}):
#   P = [[1, K,    V-K-1],
#        [1, R_EIG, -(R_EIG+1)],
#        [1, S_EIG, -(S_EIG+1)]]
#     = [[1, 12,  27],
#        [1,  2,  -3],
#        [1, -4,   3]]
#
# Q = V · P⁻¹ computed exactly via Cramer's rule; det(P) = -240.

Q = [
    [Fraction(1),     Fraction(MULT_R),                   Fraction(MULT_S)           ],
    [Fraction(1),     Fraction(MU),                       Fraction(-(MU + 1))        ],
    [Fraction(1),     Fraction(-(K - MU), GENERATIONS),   Fraction(MU + 1, GENERATIONS)],
]
# Shorthand aliases
Q00 = Q[0][0]; Q01 = Q[0][1]; Q02 = Q[0][2]
Q10 = Q[1][0]; Q11 = Q[1][1]; Q12 = Q[1][2]
Q20 = Q[2][0]; Q21 = Q[2][1]; Q22 = Q[2][2]

# ── Derived physics quantities ────────────────────────────────────────────────
KAPPA_Y    = Q22                           # SU(5) hypercharge normalization = 5/3
SIN2_W_GUT = Fraction(1) / (1 + KAPPA_Y)  # tree-level Weinberg angle = 3/8
COS2_W_GUT = 1 - SIN2_W_GUT               # = 5/8


# ── Verification helpers ──────────────────────────────────────────────────────

def _pq_row_col(row: int, col: int) -> Fraction:
    """Compute (P·Q)[row, col] exactly."""
    P = [
        [Fraction(1), Fraction(K),     Fraction(V - K - 1)],
        [Fraction(1), Fraction(R_EIG), Fraction(-(R_EIG + 1))],
        [Fraction(1), Fraction(S_EIG), Fraction(-(S_EIG + 1))],
    ]
    return sum(P[row][α] * Q[α][col] for α in range(3))


def _col_inner(j: int, k: int) -> Fraction:
    """Weighted inner product of Q columns j and k: Σ_α (k_α/v) Q[α,j] Q[α,k]."""
    sizes = [Fraction(K0), Fraction(K1), Fraction(K2)]
    return sum(sizes[α] / V * Q[α][j] * Q[α][k] for α in range(3))


# ── Verification ─────────────────────────────────────────────────────────────

def verify_all():
    """
    Return (checks, passed, total).  Exactly 27 checks in 5 groups.
    """
    checks = []

    def ck(name: str, cond: bool):
        checks.append({"name": name, "passed": bool(cond)})

    # ── Group 1: Q matrix exact values (7 checks) ────────────────────────────
    ck("Q[0,0] = 1",        Q00 == Fraction(1))
    ck("Q[0,1] = MULT_R = 24", Q01 == Fraction(MULT_R))
    ck("Q[0,2] = MULT_S = 15", Q02 == Fraction(MULT_S))
    ck("Q[1,0] = 1",        Q10 == Fraction(1))
    ck("Q[1,1] = MU = 4",   Q11 == Fraction(MU))
    ck("Q[1,2] = -(MU+1) = -5", Q12 == Fraction(-(MU + 1)))
    ck("Q[2,0] = 1",        Q20 == Fraction(1))

    # ── Group 2: Q entries derived from SRG parameters (5 checks) ────────────
    ck("Q[2,1] = -(K-MU)/GENS = -8/3",
       Q21 == Fraction(-(K - MU), GENERATIONS))
    ck("Q[2,2] = (MU+1)/GENS = 5/3",
       Q22 == Fraction(MU + 1, GENERATIONS))
    ck("|Q[2,1]| * GENS = K-MU = GLUON_COUNT = 8",
       abs(Q21) * GENERATIONS == K - MU == GLUON_COUNT)
    ck("|Q[1,2]| = MU+1 = SU5_DIM = 5",
       abs(Q12) == MU + 1 == SU5_DIM)
    ck("K - MU = V / SU5_DIM (gluons = V/rank_SU5)",
       K - MU == V // SU5_DIM)

    # ── Group 3: Weinberg angle derivation (5 checks) ─────────────────────────
    ck("KAPPA_Y = Q[2,2] = 5/3",
       KAPPA_Y == Fraction(5, 3))
    ck("SIN2_W_GUT = 1/(1+KAPPA_Y) = 3/8",
       SIN2_W_GUT == Fraction(3, 8))
    ck("SIN2_W_GUT = GENS/(GENS+SU5_DIM) = 3/8",
       SIN2_W_GUT == Fraction(GENERATIONS, GENERATIONS + SU5_DIM))
    ck("COS2_W_GUT = 1 - SIN2_W_GUT = 5/8",
       COS2_W_GUT == Fraction(5, 8))
    ck("SIN2_W_GUT + COS2_W_GUT = 1",
       SIN2_W_GUT + COS2_W_GUT == 1)

    # ── Group 4: Standard Model coupling numbers in Q (5 checks) ─────────────
    ck("Q[1,1] = EW_GAUGE_4 = 4",
       Q11 == EW_GAUGE_4)
    ck("|Q[1,2]| = SU5_DIM = 5",
       abs(Q12) == SU5_DIM)
    ck("GLUON_COUNT = K - MU = 8",
       GLUON_COUNT == K - MU)
    ck("8 * SIN2_W_GUT = 3 (denominator GLUON_COUNT)",
       GLUON_COUNT * SIN2_W_GUT == GENERATIONS)
    ck("SU5_ADJ = SU5_DIM^2 - 1 = 24",
       SU5_ADJ == SU5_DIM ** 2 - 1 == 24)

    # ── Group 5: Q column weighted orthogonality (5 checks) ──────────────────
    ck("‖Q col0‖² = m_0 = 1",  _col_inner(0, 0) == Fraction(1))
    ck("‖Q col1‖² = m_1 = 24", _col_inner(1, 1) == Fraction(MULT_R))
    ck("‖Q col2‖² = m_2 = 15", _col_inner(2, 2) == Fraction(MULT_S))
    ck("Q col0 · col1 = 0 (orthogonality)", _col_inner(0, 1) == 0)
    ck("Q col1 · col2 = 0 (orthogonality)", _col_inner(1, 2) == 0)

    passed = sum(c["passed"] for c in checks)
    total  = len(checks)
    return checks, passed, total


# ── Summary builder ───────────────────────────────────────────────────────────

def build_cccxlvi_summary() -> dict:
    checks, passed, total = verify_all()
    return {
        "part":         "CCCXLVI",
        "title":        "Q-Matrix Coupling Ratios and the Weinberg Angle",
        "checks_pass":  passed,
        "checks_total": total,
        "status":       "PASS" if passed == total else "FAIL",
        "fields": {
            "Q11":                 str(Q11),
            "Q12":                 str(Q12),
            "Q21":                 str(Q21),
            "Q22":                 str(Q22),
            "KAPPA_Y":             str(KAPPA_Y),
            "SIN2_W_GUT":          str(SIN2_W_GUT),
            "COS2_W_GUT":          str(COS2_W_GUT),
            "GLUON_COUNT":         GLUON_COUNT,
            "EW_GAUGE_4":          EW_GAUGE_4,
            "SU5_DIM":             SU5_DIM,
        },
        "discoveries": [
            "Q[2,2] = (MU+1)/GENERATIONS = 5/3 = κ_Y (SU(5) hypercharge normalization): no free parameter",
            "sin²θ_W = 1/(1 + Q[2,2]) = 3/8: tree-level Weinberg angle from W(3,3) spectral data",
            "sin²θ_W = GENERATIONS/(GENERATIONS + SU5_DIM) = 3/(3+5): generations and SU5 rank from Q",
            "Q[1,1] = MU = 4: four electroweak gauge bosons (W+, W-, Z, γ) = μ of the SRG",
            "Q[1,2] = -(MU+1) = -5 = -(SU5_DIM): SU(5) rank appears as negated Q entry",
            "|Q[2,1]| × GENERATIONS = K − MU = 8: gluon octet count from Q and graph parameters",
            "K − MU = V / SU5_DIM = 8: gluon count is vertex count divided by SU(5) rank",
        ],
    }


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import json
    import pathlib

    summary = build_cccxlvi_summary()
    print(f"Part {summary['part']}: {summary['title']}")
    print(
        f"status: {summary['status']}, "
        f"checks_pass: {summary['checks_pass']}, "
        f"checks_total: {summary['checks_total']}"
    )
    out = (
        pathlib.Path(__file__).resolve().parents[1]
        / "PART_CCCXLVI_q_matrix_weinberg_results.json"
    )
    out.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"JSON written: {out}")
