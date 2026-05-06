"""
PART CCCXLIV — Three-Idempotent GUT Projector Decomposition

The Bose-Mesner algebra of W(3,3) has exactly three primitive idempotents
E_0, E_1, E_2 corresponding to its three distinct adjacency eigenvalues
k=12, r=2, s=-4.  Their ranks are 1, 24, 15 respectively.

These ranks encode the SU(5) GUT spectrum exactly:
  rank(E_1) = 24 = SU(5) adjoint dimension (gauge boson count: 8g+3W+1γ+12XY)
  rank(E_2) = 15 = SU(5) matter content per generation (5̄+10 Weyl fermions)
  rank(E_2) = GUT_DIM − K = 27 − 12 = 15

The idempotents are expressed exactly as linear combinations of {I, A, J}:
  E_0 = J/V
  E_1 = (A + 4I − (2/5)J) / 6
  E_2 = (−A + 2I + J/4)  / 6

All arithmetic is exact rational (Fraction).  No numpy.  27 checks pass.
"""
from fractions import Fraction

# ── W(3,3) SRG parameters ────────────────────────────────────────────────────
V      = 40
K      = 12
LAM    = 2
MU     = 4
MULT_R = 24    # multiplicity of r-eigenvalue  →  rank(E_1)
MULT_S = 15    # multiplicity of s-eigenvalue  →  rank(E_2)
R_EIG  = 2
S_EIG  = -4
ABS_S  = 4

# ── Standard-model / GUT constants ───────────────────────────────────────────
EW_GAUGE_4         = 4    # SM EW gauge-field count used elsewhere
GENERATIONS        = 3
GUT_DIM            = 27   # E_6 fundamental representation dimension
ALPHA              = 10
SU5_DIM            = 5
SU5_ADJ            = SU5_DIM ** 2 - 1      # 24  SU(5) adjoint (gauge bosons)
SU5_MATTER_PER_GEN = 15                    # 5̄ (5) + 10 Weyl fermions per generation
SU5_TOTAL_MATTER   = GENERATIONS * SU5_MATTER_PER_GEN   # 45

# ── Primitive idempotent coefficients in basis {I, A, J} ─────────────────────
# Derived from the two linear equations:
#   E_0 + E_1 + E_2 = I          (completeness)
#   k·E_0 + r·E_1 + s·E_2 = A   (spectral reconstruction)
# together with E_0 = J/V (trivial idempotent).
#
# Solving with k=12, r=2, s=−4:
#   (r−s) = 6
#   E_1 = (A − s·I + (−3/10 + s/40)·J) / (r−s)
#        = (A + 4·I − (2/5)·J) / 6
#   E_2 = (−A + r·I + (−3/10 + r/40)·J) / (−(r−s))   [sign flips]
#        = (−A + 2·I + (1/4)·J) / 6
#
# Coefficient layout: each idempotent = I_c·I + A_c·A + J_c·J

E0_I = Fraction(0);    E0_A = Fraction(0);     E0_J = Fraction(1, V)
E1_I = Fraction(2, 3); E1_A = Fraction(1, 6);  E1_J = Fraction(-1, 15)
E2_I = Fraction(1, 3); E2_A = Fraction(-1, 6); E2_J = Fraction(1, 24)


# ── Core algebraic helpers ────────────────────────────────────────────────────

def _trace(I_c: Fraction, A_c: Fraction, J_c: Fraction) -> Fraction:
    """
    Tr(I_c·I + A_c·A + J_c·J).

    Tr(I) = V = 40   (identity matrix)
    Tr(A) = 0        (adjacency matrix has zero diagonal)
    Tr(J) = V = 40   (all-ones matrix: diagonal entries are all 1)
    """
    return Fraction(V) * I_c + Fraction(0) * A_c + Fraction(V) * J_c


def rank_E0() -> int:
    return int(_trace(E0_I, E0_A, E0_J))


def rank_E1() -> int:
    return int(_trace(E1_I, E1_A, E1_J))


def rank_E2() -> int:
    return int(_trace(E2_I, E2_A, E2_J))


def eigenval_on(I_c: Fraction, A_c: Fraction, J_c: Fraction, lam: int) -> Fraction:
    """
    Compute the scalar eigenvalue of (I_c·I + A_c·A + J_c·J)
    restricted to the eigenspace of A where A·f = lam·f.

    For lam == K (trivial sector, all-ones eigenvector):
        I·f = f,  A·f = K·f,  J·f = V·f
        → eigenvalue = I_c + A_c·K + J_c·V

    For lam in {R_EIG, S_EIG} (non-trivial sectors):
        J·f = 0  (f is orthogonal to the all-ones vector)
        → eigenvalue = I_c + A_c·lam
    """
    if lam == K:
        return I_c + A_c * Fraction(K) + J_c * Fraction(V)
    return I_c + A_c * Fraction(lam)


# ── Verification ─────────────────────────────────────────────────────────────

def verify_all():
    """
    Return (checks, passed, total) where checks is a list of dicts
    {'name': str, 'passed': bool}.  Exactly 27 checks in 5 groups.
    """
    checks = []

    def ck(name: str, cond: bool):
        checks.append({"name": name, "passed": bool(cond)})

    # ── Group 1: Exact idempotent coefficients (7 checks) ────────────────────
    ck("E0_J_coeff = 1/V",   E0_J == Fraction(1, V))
    ck("E1_I_coeff = 2/3",   E1_I == Fraction(2, 3))
    ck("E1_A_coeff = 1/6",   E1_A == Fraction(1, 6))
    ck("E1_J_coeff = -1/15", E1_J == Fraction(-1, 15))
    ck("E2_I_coeff = 1/3",   E2_I == Fraction(1, 3))
    ck("E2_A_coeff = -1/6",  E2_A == Fraction(-1, 6))
    ck("E2_J_coeff = 1/24",  E2_J == Fraction(1, 24))

    # ── Group 2: Rank formulas via trace (5 checks) ───────────────────────────
    ck("rank(E0) = 1",                       rank_E0() == 1)
    ck("rank(E1) = MULT_R = 24",             rank_E1() == MULT_R)
    ck("rank(E2) = MULT_S = 15",             rank_E2() == MULT_S)
    ck("rank(E0)+rank(E1)+rank(E2) = V=40",  rank_E0() + rank_E1() + rank_E2() == V)
    ck("rank(E1)/rank(E2) = 8/5",            Fraction(rank_E1(), rank_E2()) == Fraction(8, 5))

    # ── Group 3: Eigenspace projection values (5 checks) ─────────────────────
    ck("E0 on K-eigenspace = 1", eigenval_on(E0_I, E0_A, E0_J, K)     == 1)
    ck("E1 on R-eigenspace = 1", eigenval_on(E1_I, E1_A, E1_J, R_EIG) == 1)
    ck("E1 on S-eigenspace = 0", eigenval_on(E1_I, E1_A, E1_J, S_EIG) == 0)
    ck("E2 on R-eigenspace = 0", eigenval_on(E2_I, E2_A, E2_J, R_EIG) == 0)
    ck("E2 on S-eigenspace = 1", eigenval_on(E2_I, E2_A, E2_J, S_EIG) == 1)

    # ── Group 4: GUT content encoding (5 checks) ─────────────────────────────
    ck("rank(E1) = SU5_ADJ = 24",             rank_E1() == SU5_ADJ)
    ck("rank(E2) = SU5_MATTER_PER_GEN = 15",  rank_E2() == SU5_MATTER_PER_GEN)
    ck("rank(E2) = GUT_DIM - K = 15",         rank_E2() == GUT_DIM - K)
    ck("3*rank(E2) = SU5_TOTAL_MATTER = 45",  GENERATIONS * rank_E2() == SU5_TOTAL_MATTER)
    ck("SU5_ADJ = SU5_DIM^2 - 1",            SU5_ADJ == SU5_DIM ** 2 - 1)

    # ── Group 5: Completeness identities (5 checks) ───────────────────────────
    ck("sum of I-coefficients = 1", E0_I + E1_I + E2_I == 1)
    ck("sum of A-coefficients = 0", E0_A + E1_A + E2_A == 0)
    ck("sum of J-coefficients = 0", E0_J + E1_J + E2_J == 0)
    ck("E1_I + E2_I = 1 (non-trivial I-span)", E1_I + E2_I == 1)
    ck("E1_A + E2_A = 0 (A-antisymmetry)",     E1_A + E2_A == 0)

    passed = sum(c["passed"] for c in checks)
    total  = len(checks)
    return checks, passed, total


# ── Summary builder ───────────────────────────────────────────────────────────

def build_cccxliv_summary() -> dict:
    checks, passed, total = verify_all()
    return {
        "part":         "CCCXLIV",
        "title":        "Three-Idempotent GUT Projector Decomposition",
        "checks_pass":  passed,
        "checks_total": total,
        "status":       "PASS" if passed == total else "FAIL",
        "fields": {
            "rank_E0":             rank_E0(),
            "rank_E1":             rank_E1(),
            "rank_E2":             rank_E2(),
            "SU5_ADJ":             SU5_ADJ,
            "SU5_MATTER_PER_GEN":  SU5_MATTER_PER_GEN,
            "SU5_TOTAL_MATTER":    SU5_TOTAL_MATTER,
            "GUT_DIM_minus_K":     GUT_DIM - K,
            "completeness":        rank_E0() + rank_E1() + rank_E2(),
        },
        "discoveries": [
            "W(3,3) Bose-Mesner algebra has exactly 3 primitive idempotents with ranks 1, 24, 15",
            "rank(E_1) = 24 = SU(5) adjoint: W(3,3) R-sector = SU(5) gauge-boson sector (8g+3W+1γ+12XY)",
            "rank(E_2) = 15 = SU(5) matter per generation (5̄+10): W(3,3) S-sector = SU(5) matter sector",
            "rank(E_2) = GUT_DIM − K = 27 − 12 = 15: E_6 fundamental rep dimension minus W(3,3) degree",
            "3 × rank(E_2) = 45: three SM generations of SU(5) Weyl fermions encoded in spectral rank",
            "Completeness: I-coefficients sum to 1, A-coefficients sum to 0, J-coefficients sum to 0",
            "A-coefficient antisymmetry: E_1 and E_2 are mirror images under A → −A (sector duality)",
        ],
    }


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import json
    import pathlib

    summary = build_cccxliv_summary()
    print(f"Part {summary['part']}: {summary['title']}")
    print(
        f"status: {summary['status']}, "
        f"checks_pass: {summary['checks_pass']}, "
        f"checks_total: {summary['checks_total']}"
    )
    out = (
        pathlib.Path(__file__).resolve().parents[1]
        / "PART_CCCXLIV_gut_projector_results.json"
    )
    out.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"JSON written: {out}")
