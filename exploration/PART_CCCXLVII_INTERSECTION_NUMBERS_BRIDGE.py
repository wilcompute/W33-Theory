"""
PART CCCXLVII -- Intersection Numbers as Primal Propagators of W(3,3)
=======================================================================

The Bose-Mesner algebra of W(3,3) supports TWO product structures:

  Hadamard (entry-wise) product:  structure constants = Krein parameters q[i][j][l]
                                   (Part CCCXLV)

  Ordinary matrix product:        structure constants = intersection numbers p[i][j][l]
                                   (THIS PART)

The intersection numbers are defined by:

    A_i * A_j  =  sum_l  p[i][j][l]  A_l

They encode the "propagator structure" of the graph: p[i][j][l] counts the
number of vertices z at relation-distance i from x AND relation-distance j from y
when (x,y) is in relation l.

For the 3-class association scheme of W(3,3) (classes A_0=I, A_1=adj, A_2=compl):

    p[1][1][0] = K = 12        (degree of adjacency graph)
    p[1][1][1] = LAM = 2       (triangles -- equals R eigenvalue!)
    p[1][1][2] = MU  = 4       (quads    -- equals |S eigenvalue|! = EW_GAUGE_4)
    p[1][2][2] = 8             (= K - MU = 8 = SU(3)_C gluon octet count!)
    p[2][2][0] = L  = 27       (complement valency = GUT_DIM)
    p[2][2][1] = p[2][2][2] = 18  (complement is conference-type: LAM_c = MU_c)

All computations use exact integer arithmetic.  No numpy.  27 checks pass.
"""

from fractions import Fraction
import json
from pathlib import Path

# ── W(3,3) SRG constants ─────────────────────────────────────────────────────
V       = 40
K       = 12
LAM     = 2           # lambda: triangles (common nbrs of adjacent pair)
MU      = 4           # mu: quads (common nbrs of non-adjacent pair)
R_EIG   = 2           # positive non-trivial eigenvalue
S_EIG   = -4
ABS_S   = 4
MULT_R  = 24          # multiplicity of R eigenvalue
MULT_S  = 15          # multiplicity of S eigenvalue
L       = V - K - 1  # = 27: complement valency

# ── SU(5) / Standard Model constants ─────────────────────────────────────────
SU5_DIM            = 5
SU5_ADJ            = SU5_DIM ** 2 - 1   # 24
SU5_MATTER_PER_GEN = 15
GENERATIONS        = 3
GUT_DIM            = 27
EW_GAUGE_4         = 4     # W+, W-, Z, gamma
GLUON_COUNT        = 8     # SU(3)_C octet

# ── Relation valencies ────────────────────────────────────────────────────────
K_VAL = [1, K, L]   # k_0=1, k_1=12, k_2=27


# ── Compute intersection numbers ──────────────────────────────────────────────
def compute_intersection_numbers():
    """Return p[i][j][l] for 0 <= i,j,l <= 2 as exact Fractions (integers here).

    The SRG recurrences give:
      A_1^2  = K*A_0 + LAM*A_1 + MU*A_2
      A_1*A_2 = (K-LAM-1)*A_1 + (K-MU)*A_2     (using A_1*J = K*J)
      A_2^2  = L*A_0 + (L-K+MU-1)*A_1 + (L-K+LAM-1)*A_2
    """
    p = [[[Fraction(0)] * 3 for _ in range(3)] for _ in range(3)]

    # A_0 acts as multiplicative identity
    for j in range(3):
        p[0][j][j] = Fraction(1)
        p[j][0][j] = Fraction(1)

    # A_1^2 = K*A_0 + LAM*A_1 + MU*A_2
    p[1][1][0] = Fraction(K)
    p[1][1][1] = Fraction(LAM)
    p[1][1][2] = Fraction(MU)

    # A_1*A_2:  derived from A_1*J = K*J and J = A_0+A_1+A_2
    # A_1*A_2 = K*J - A_1 - A_1^2
    #          = K*(A_0+A_1+A_2) - A_1 - (K*A_0+LAM*A_1+MU*A_2)
    #          = 0*A_0 + (K-1-LAM)*A_1 + (K-MU)*A_2
    p[1][2][0] = Fraction(0)
    p[1][2][1] = Fraction(K - 1 - LAM)   # = 9
    p[1][2][2] = Fraction(K - MU)         # = 8
    p[2][1][0] = p[1][2][0]
    p[2][1][1] = p[1][2][1]
    p[2][1][2] = p[1][2][2]

    # A_2^2:  derived from A_2*J = L*J
    # A_2*J = A_2*(A_0+A_1+A_2) = A_2 + A_2*A_1 + A_2^2
    #       = L*(A_0+A_1+A_2)
    # => A_2^2 = L*J - A_2 - A_1*A_2
    #          = L*(A_0+A_1+A_2) - A_2 - (0*A_0 + 9*A_1 + 8*A_2)
    #          = L*A_0 + (L-9)*A_1 + (L-1-8)*A_2
    #          = 27*A_0 + 18*A_1 + 18*A_2
    p[2][2][0] = Fraction(L)
    p[2][2][1] = Fraction(L - (K - 1 - LAM))   # = 27 - 9 = 18
    p[2][2][2] = Fraction(L - 1 - (K - MU))    # = 27 - 1 - 8 = 18

    return p


# ── Cache intersection tensor ─────────────────────────────────────────────────
_P = compute_intersection_numbers()


def p_ij_l(i, j, l):
    """Return intersection number p[i][j][l] as exact Fraction."""
    return _P[i][j][l]


# ── Verification ──────────────────────────────────────────────────────────────
def verify_all():
    checks = []

    def chk(name, got, exp):
        checks.append({
            "name":     name,
            "passed":   bool(got == exp),
            "got":      str(got),
            "expected": str(exp),
        })

    # Group 1 (5): Identity relation acts as multiplicative identity
    chk("p[0][0][0] = 1",  p_ij_l(0, 0, 0), Fraction(1))
    chk("p[0][1][1] = 1",  p_ij_l(0, 1, 1), Fraction(1))
    chk("p[0][2][2] = 1",  p_ij_l(0, 2, 2), Fraction(1))
    chk("p[0][1][0] = 0",  p_ij_l(0, 1, 0), Fraction(0))
    chk("p[0][2][0] = 0",  p_ij_l(0, 2, 0), Fraction(0))

    # Group 2 (6): Adjacency self-product p[1][1][l]
    chk("p[1][1][0] = K = 12",               p_ij_l(1, 1, 0), Fraction(K))
    chk("p[1][1][1] = LAM = 2",              p_ij_l(1, 1, 1), Fraction(LAM))
    chk("p[1][1][2] = MU = 4",               p_ij_l(1, 1, 2), Fraction(MU))
    chk("p[1][1][0] = SU5_ADJ/2",            p_ij_l(1, 1, 0), Fraction(SU5_ADJ, 2))
    chk("p[1][1][1] = R_EIG (lambda=r)",     p_ij_l(1, 1, 1), Fraction(R_EIG))
    chk("p[1][1][2] = ABS_S = EW_GAUGE_4",  p_ij_l(1, 1, 2), Fraction(ABS_S))

    # Group 3 (5): Cross product p[1][2][l] and complement valency
    chk("p[1][2][0] = 0",                    p_ij_l(1, 2, 0), Fraction(0))
    chk("p[1][2][1] = K-LAM-1 = 9",         p_ij_l(1, 2, 1), Fraction(K - LAM - 1))
    chk("p[1][2][2] = K-MU = 8",            p_ij_l(1, 2, 2), Fraction(K - MU))
    chk("p[1][2][2] = GLUON_COUNT = 8",     p_ij_l(1, 2, 2), Fraction(GLUON_COUNT))
    chk("p[1][2][1]+p[1][2][2] = 2K-LAM-MU-1",
        p_ij_l(1, 2, 1) + p_ij_l(1, 2, 2),
        Fraction(2 * K - LAM - MU - 1))

    # Group 4 (5): Complement self-product p[2][2][l]
    chk("p[2][2][0] = L = 27 = GUT_DIM",    p_ij_l(2, 2, 0), Fraction(L))
    chk("p[2][2][1] = 18",                   p_ij_l(2, 2, 1), Fraction(18))
    chk("p[2][2][2] = 18",                   p_ij_l(2, 2, 2), Fraction(18))
    chk("p[2][2][1] = p[2][2][2] (conf.)",  p_ij_l(2, 2, 1), p_ij_l(2, 2, 2))
    chk("p[2][2][1] = 6*GENERATIONS",       p_ij_l(2, 2, 1), Fraction(6 * GENERATIONS))

    # Group 5 (6): Valency conservation and algebraic identities
    row11 = sum(p_ij_l(1, 1, l) * K_VAL[l] for l in range(3))
    chk("sum_l p[1][1][l]*k_l = K^2",       row11, Fraction(K ** 2))

    row12 = sum(p_ij_l(1, 2, l) * K_VAL[l] for l in range(3))
    chk("sum_l p[1][2][l]*k_l = K*L",       row12, Fraction(K * L))

    row22 = sum(p_ij_l(2, 2, l) * K_VAL[l] for l in range(3))
    chk("sum_l p[2][2][l]*k_l = L^2",       row22, Fraction(L ** 2))

    sym_ok = all(
        p_ij_l(i, j, l) == p_ij_l(j, i, l)
        for i in range(3) for j in range(3) for l in range(3)
    )
    checks.append({
        "name": "symmetry p[i][j][l] = p[j][i][l]",
        "passed": sym_ok, "got": str(sym_ok), "expected": "True",
    })

    chk("p[1][1][1]/p[1][1][2] = R_EIG/ABS_S",
        p_ij_l(1, 1, 1) / p_ij_l(1, 1, 2),
        Fraction(R_EIG, ABS_S))

    chk("p[2][2][0] = V-K-1",               p_ij_l(2, 2, 0), Fraction(V - K - 1))

    passed = sum(1 for c in checks if c["passed"])
    total  = len(checks)
    return checks, passed, total


# ── Summary builder ───────────────────────────────────────────────────────────
def build_cccxlvii_summary():
    checks, passed, total = verify_all()
    return {
        "part":          "CCCXLVII",
        "title":         "Intersection Numbers as Primal Propagators of W(3,3)",
        "checks_pass":   passed,
        "checks_total":  total,
        "status":        "PASS" if passed == total else "FAIL",
        "fields": {
            "p_11_0":         str(p_ij_l(1, 1, 0)),   # K = 12
            "p_11_1":         str(p_ij_l(1, 1, 1)),   # LAM = 2
            "p_11_2":         str(p_ij_l(1, 1, 2)),   # MU = 4
            "p_12_0":         str(p_ij_l(1, 2, 0)),   # 0
            "p_12_1":         str(p_ij_l(1, 2, 1)),   # 9
            "p_12_2":         str(p_ij_l(1, 2, 2)),   # 8
            "p_22_0":         str(p_ij_l(2, 2, 0)),   # 27 = GUT_DIM
            "p_22_1":         str(p_ij_l(2, 2, 1)),   # 18
            "p_22_2":         str(p_ij_l(2, 2, 2)),   # 18
            "lambda_eq_r":    str(LAM == R_EIG),
            "mu_eq_abs_s":    str(MU == ABS_S),
            "gluon_octet":    str(int(p_ij_l(1, 2, 2))),
            "gut_dim":        str(L),
        },
        "discoveries": [
            "p[1][1][1] = lambda = R_EIG = 2: triangle count equals R eigenvalue",
            "p[1][1][2] = mu = ABS_S = 4 = EW_GAUGE_4: quad count = |S eigenvalue| = EW gauge count",
            "p[1][2][2] = 8 = GLUON_COUNT: adj-complement cross-number = SU(3)_C gluon octet",
            "p[2][2][0] = L = GUT_DIM = 27: complement valency = E_6 fundamental rep dimension",
            "p[2][2][1] = p[2][2][2] = 18: complement is conference-type (lambda_c = mu_c)",
            "p[1][1][0] = K = SU5_ADJ/2 = 12: adjacency degree = half the SU(5) adjoint dimension",
            "Valency conservation: sum_l p[ij][l]*k_l = k_i*k_j for all i,j",
        ],
    }


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    summary = build_cccxlvii_summary()
    print(f"Part {summary['part']}: {summary['title']}")
    print(f"status: {summary['status']}, checks_pass: {summary['checks_pass']}, "
          f"checks_total: {summary['checks_total']}")
    checks, _, _ = verify_all()
    for c in checks:
        tag = "[PASS]" if c["passed"] else "[FAIL]"
        print(f"  {tag} {c['name']}")

    out = Path(__file__).resolve().parents[1] / "PART_CCCXLVII_intersection_numbers_results.json"
    out.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"\nJSON written: {out}")
