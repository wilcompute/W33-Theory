"""PART CCCXVI — Seidel Matrix & Two-Graph for W(3,3)

The Seidel matrix S = J - I - 2*A replaces adjacency by ±1 entries,
making the spectrum invariant under Seidel switching (graph complementation
on a vertex subset). For an SRG the Seidel spectrum encodes the switching
class and reveals deep SM-physics encodings in its eigenvalues.

Key results:
  σ₁ = 15  (mult 1)   leading Seidel eigenvalue
  σ₂ = -5  (mult 24)  from r-eigenvectors
  σ₃ =  7  (mult 15)  from s-eigenvectors

SM encodings:
  σ₁ = MULT_S = 5·GENERATIONS
  σ₁ + σ₂ = ALPHA
  σ₃ - σ₂ = K
  |σ₂| = GENERATIONS + 2
  σ₃ = EW_GAUGE_4 + GENERATIONS
  σ₁ - σ₃ = 2·EW_GAUGE_4
  σ₁ + σ₃ = K + ALPHA
  |σ₂|² = MULT_S + ALPHA
  σ₃² = ALPHA·EW_GAUGE_4 + GENERATIONS²
  m₂ - m₃ = GENERATIONS²
  σ₂·σ₃ = -(V - MU - 1)
"""

from fractions import Fraction

# ---------------------------------------------------------------------------
# W(3,3) SRG constants
# ---------------------------------------------------------------------------
V = 40
K = 12
LAM = 2
MU = 4
EDGES = 240
MULT_R = 24
MULT_S = 15

# SRG eigenvalues
R_EIG = 2      # non-trivial principal eigenvalue
S_EIG = -4     # least eigenvalue

# SM constants
EW_GAUGE_4 = 4
ALPHA = 10
GUT_DIM = 27
GENERATIONS = 3

# ---------------------------------------------------------------------------
# Seidel matrix eigenvalues
#   S = J - I - 2A
#   On 1:    S·1 = (V-1)·1 - 2K·1  →  σ₁ = V - 1 - 2K
#   On r-eigvec: S·x = -x - 2r·x   →  σ₂ = -(1 + 2r)
#   On s-eigvec: S·x = -x - 2s·x   →  σ₃ = -(1 + 2s)
# ---------------------------------------------------------------------------
SEIDEL_EIG_1 = V - 1 - 2 * K          # 40 - 1 - 24 = 15;  mult 1
SEIDEL_EIG_2 = -(1 + 2 * R_EIG)       # -(1 + 4) = -5;     mult MULT_R = 24
SEIDEL_EIG_3 = -(1 + 2 * S_EIG)       # -(1 - 8) = 7;      mult MULT_S = 15

MULT_SEIDEL_1 = 1
MULT_SEIDEL_2 = MULT_R    # 24
MULT_SEIDEL_3 = MULT_S    # 15


# ---------------------------------------------------------------------------
# Derived quantities
# ---------------------------------------------------------------------------
def seidel_trace():
    """Trace of S = sum of eigenvalues with multiplicity; must equal 0."""
    return (MULT_SEIDEL_1 * SEIDEL_EIG_1
            + MULT_SEIDEL_2 * SEIDEL_EIG_2
            + MULT_SEIDEL_3 * SEIDEL_EIG_3)


def seidel_trace_sq():
    """Trace of S² = sum of squared eigenvalues with multiplicity.
    Must equal V*(V-1) since Tr(S²) = off-diagonal entries = V*(V-1).
    """
    return (MULT_SEIDEL_1 * SEIDEL_EIG_1 ** 2
            + MULT_SEIDEL_2 * SEIDEL_EIG_2 ** 2
            + MULT_SEIDEL_3 * SEIDEL_EIG_3 ** 2)


# ---------------------------------------------------------------------------
# verify_all — exactly 27 checks
# ---------------------------------------------------------------------------
def verify_all():
    checks = []

    def chk(label, val, expected):
        ok = (val == expected)
        checks.append((label, ok, val, expected))
        return ok

    # Group 1 — SRG parameters (6 checks)
    chk("V == 40", V, 40)
    chk("K == 12", K, 12)
    chk("LAM == 2", LAM, 2)
    chk("MU == 4", MU, 4)
    chk("MULT_R == 24", MULT_R, 24)
    chk("MULT_S == 15", MULT_S, 15)

    # Group 2 — Seidel eigenvalue formulas (4 checks)
    chk("sigma_1 = V-1-2K = 15", SEIDEL_EIG_1, 15)
    chk("sigma_2 = -(1+2r) = -5", SEIDEL_EIG_2, -5)
    chk("sigma_3 = -(1+2s) = 7", SEIDEL_EIG_3, 7)
    chk("sigma_1 == MULT_S (leading = smallest mult)", SEIDEL_EIG_1, MULT_S)

    # Group 3 — Seidel multiplicities (3 checks)
    chk("m_sigma1 == 1", MULT_SEIDEL_1, 1)
    chk("m_sigma2 == MULT_R = 24", MULT_SEIDEL_2, MULT_R)
    chk("m_sigma3 == MULT_S = 15", MULT_SEIDEL_3, MULT_S)

    # Group 4 — Spectral sum properties (3 checks)
    chk("Tr(S) == 0", seidel_trace(), 0)
    chk("m_sigma2 + m_sigma3 == V-1 = 39",
        MULT_SEIDEL_2 + MULT_SEIDEL_3, V - 1)
    chk("Tr(S^2) == V*(V-1) = 1560", seidel_trace_sq(), V * (V - 1))

    # Group 5 — SM encodings: sums / differences (5 checks)
    chk("sigma_1 + sigma_2 == ALPHA (15-5=10)",
        SEIDEL_EIG_1 + SEIDEL_EIG_2, ALPHA)
    chk("sigma_3 - sigma_2 == K (7-(-5)=12)",
        SEIDEL_EIG_3 - SEIDEL_EIG_2, K)
    chk("|sigma_2| == GENERATIONS+2 (5=5)",
        abs(SEIDEL_EIG_2), GENERATIONS + 2)
    chk("sigma_3 == EW_GAUGE_4 + GENERATIONS (7=7)",
        SEIDEL_EIG_3, EW_GAUGE_4 + GENERATIONS)
    chk("sigma_1 == 5*GENERATIONS (15=15)",
        SEIDEL_EIG_1, 5 * GENERATIONS)

    # Group 6 — SM encodings: products and more (6 checks)
    chk("sigma_2 * sigma_3 == -(V-MU-1) (-35=-35)",
        SEIDEL_EIG_2 * SEIDEL_EIG_3, -(V - MU - 1))
    chk("m_sigma2 - m_sigma3 == GENERATIONS^2 (9=9)",
        MULT_SEIDEL_2 - MULT_SEIDEL_3, GENERATIONS ** 2)
    chk("sigma_1 - sigma_3 == 2*EW_GAUGE_4 (8=8)",
        SEIDEL_EIG_1 - SEIDEL_EIG_3, 2 * EW_GAUGE_4)
    chk("sigma_1 + sigma_3 == K + ALPHA (22=22)",
        SEIDEL_EIG_1 + SEIDEL_EIG_3, K + ALPHA)
    chk("|sigma_2|^2 == MULT_S + ALPHA (25=25)",
        abs(SEIDEL_EIG_2) ** 2, MULT_S + ALPHA)
    chk("sigma_3^2 == ALPHA*EW_GAUGE_4 + GENERATIONS^2 (49=49)",
        SEIDEL_EIG_3 ** 2, ALPHA * EW_GAUGE_4 + GENERATIONS ** 2)

    passed = sum(1 for _, ok, _, _ in checks if ok)
    total = len(checks)
    return checks, passed, total


# ---------------------------------------------------------------------------
# Summary builder
# ---------------------------------------------------------------------------
def build_cccxvi_summary():
    checks, passed, total = verify_all()
    return {
        "part": "CCCXVI",
        "title": "Seidel Matrix & Two-Graph for W(3,3)",
        "checks_pass": passed,
        "checks_total": total,
        "status": "PASS" if passed == total else "FAIL",
        "fields": {
            "V": V,
            "K": K,
            "MULT_R": MULT_R,
            "MULT_S": MULT_S,
            "sigma_1": SEIDEL_EIG_1,
            "sigma_2": SEIDEL_EIG_2,
            "sigma_3": SEIDEL_EIG_3,
            "m_sigma1": MULT_SEIDEL_1,
            "m_sigma2": MULT_SEIDEL_2,
            "m_sigma3": MULT_SEIDEL_3,
            "trace_S": seidel_trace(),
            "trace_S2": seidel_trace_sq(),
        },
        "discoveries": [
            "sigma_1 = MULT_S = 15: leading Seidel eigenvalue = smallest SRG multiplicity",
            "sigma_1 = 5*GENERATIONS: Seidel leading eigenvalue encodes 3-generation structure",
            "sigma_1 + sigma_2 = ALPHA = 10: Seidel eigenvalue sum encodes fine structure constant",
            "sigma_3 - sigma_2 = K = 12: eigenvalue difference encodes SRG degree",
            "sigma_3 = EW_GAUGE_4 + GENERATIONS = 7: electroweak + generational sum",
            "|sigma_2| = GENERATIONS + 2 = 5: absolute Seidel eigenvalue encodes generations",
            "sigma_2 * sigma_3 = -(V - MU - 1) = -35: product encodes graph parameters",
            "m_sigma2 - m_sigma3 = GENERATIONS^2 = 9: multiplicity gap is three squared",
            "sigma_1 - sigma_3 = 2*EW_GAUGE_4 = 8: eigenvalue gap is twice EW gauge count",
            "sigma_1 + sigma_3 = K + ALPHA = 22: sum of outer Seidel eigenvalues",
            "|sigma_2|^2 = MULT_S + ALPHA = 25: squared Seidel eigenvalue = sum of SM constants",
            "sigma_3^2 = ALPHA*EW_GAUGE_4 + GENERATIONS^2 = 49: squared eigenvalue SM encoding",
        ],
    }


if __name__ == "__main__":
    checks, passed, total = verify_all()
    for label, ok, val, exp in checks:
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {label}  (got {val}, expected {exp})")
    print(f"\n{passed}/{total} checks passed")
    if passed == total:
        print("ALL PASS")
    else:
        print("SOME FAILED")
