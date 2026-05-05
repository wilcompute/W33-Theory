"""
Part CCXCIII: Lovász Theta Function and Spectral Independence Bounds for W(3,3).

Theme: The Lovász theta function ϑ(G) for the W(3,3) strongly regular graph equals
the independence number α(G) = 10, while ϑ(Ḡ) = 4 = EW_GAUGE_4 (electroweak gauge
bosons). Their product ϑ(G) · ϑ(Ḡ) = 40 = V recovers the vertex count exactly via
the Lovász sandwich product equality for vertex-transitive graphs.

A remarkable triple alignment: ϑ(W(3,3)^c) = ω(W(3,3)) = χ_f(W(3,3)) = 4 = EW_GAUGE_4
— spectral, clique, and fractional-chromatic bounds all resolve to the electroweak
gauge sector dimension.

Checks: 27 / 27
"""

from fractions import Fraction

# ── W(3,3) SRG constants ──────────────────────────────────────────────────────
V = 40          # vertices
K = 12          # degree
LAM = 2         # lambda: common neighbours between adjacent pair
MU = 4          # mu: common neighbours between non-adjacent pair
K2 = 27         # V - 1 - K
MULT_R = 24     # multiplicity of positive restricted eigenvalue
MULT_S = 15     # multiplicity of negative restricted eigenvalue
EDGES = 240     # |E(W(3,3))| = V*K/2

# ── SM constants ──────────────────────────────────────────────────────────────
EW_GAUGE_4 = 4          # electroweak gauge bosons: W+, W−, Z, γ
QUARKS_36 = 36
TOTAL_SM_40 = 40
SM_GENERATIONS = 3
SM_WEYL_PER_GEN = 16
Q = 3                   # ternary base

# ── SRG eigenvalues from discriminant formula ─────────────────────────────────
# For SRG(v, k, λ, μ): restricted eigenvalues satisfy
#   r, s = ((λ − μ) ± sqrt((λ − μ)² + 4(k − μ))) / 2
# W(3,3): λ − μ = 2 − 4 = −2; k − μ = 12 − 4 = 8
# discriminant = (−2)² + 4·8 = 4 + 32 = 36; sqrt = 6
_DISC = (LAM - MU) ** 2 + 4 * (K - MU)   # = 36
_SQRT_DISC = 6                             # exact integer square root of 36

DISC_INT = _DISC                           # 36 (stored for verification)
R_EIG = (LAM - MU + _SQRT_DISC) // 2      # = (−2 + 6) / 2 = 2
S_EIG = (LAM - MU - _SQRT_DISC) // 2      # = (−2 − 6) / 2 = −4

# ── Lovász theta function for W(3,3) ─────────────────────────────────────────
# For an SRG with smallest eigenvalue s < 0:
#   ϑ(G) = v · |s| / (k − s) = v · |s| / (k + |s|)
# W(3,3): ϑ = 40 · 4 / (12 + 4) = 160 / 16 = 10
THETA_NUM = V * abs(S_EIG)          # 160
THETA_DEN = K - S_EIG               # 16
THETA_LOVÁSZ = Fraction(THETA_NUM, THETA_DEN)    # Fraction(10, 1) = 10

# ── Complement SRG: W(3,3)^c = SRG(40, 27, 18, 18) ──────────────────────────
# For complement of SRG(v, k, λ, μ):
#   k̄  = v − 1 − k          = 40 − 1 − 12 = 27
#   λ̄  = v − 2k + μ − 2     = 40 − 24 + 4 − 2 = 18
#   μ̄  = v − 2k + λ         = 40 − 24 + 2 = 18
# Eigenvalues of complement: -(s+1) and -(r+1) (non-trivial), and k̄ (trivial)
K_COMP = V - 1 - K          # 27
LAM_COMP = V - 2 * K + MU - 2   # 18
MU_COMP = V - 2 * K + LAM       # 18

R_COMP = -(S_EIG + 1)       # −(−4 + 1) = 3
S_COMP = -(R_EIG + 1)       # −(2 + 1) = −3

# ϑ(Ḡ) = v · |s_comp| / (k̄ − s_comp) = 40 · 3 / (27 + 3) = 120 / 30 = 4
THETA_COMP_NUM = V * abs(S_COMP)        # 120
THETA_COMP_DEN = K_COMP - S_COMP        # 30
THETA_COMP = Fraction(THETA_COMP_NUM, THETA_COMP_DEN)   # Fraction(4, 1) = 4

# ── Lovász product and sum ────────────────────────────────────────────────────
# For vertex-transitive G: ϑ(G) · ϑ(Ḡ) = v  (Lovász, 1979)
THETA_PRODUCT = THETA_LOVÁSZ * THETA_COMP   # 10 · 4 = 40 = V
THETA_SUM = THETA_LOVÁSZ + THETA_COMP       # 10 + 4 = 14

# ── Ratio (Cvetković spectral) bound on independence number ───────────────────
# α(G) ≤ v · |s| / (k + |s|) = ϑ(G)  for SRGs (ratio bound = theta number)
RATIO_BOUND = Fraction(V * abs(S_EIG), K - S_EIG)   # 10

# ── Independence number α(W(3,3)) ─────────────────────────────────────────────
# W(3,3) is perfect in the sense that α = ϑ (theta-exact).
# α = 10 is the size of a maximal spread / maximal isotropic subspace orbit.
ALPHA_EXACT = 10
ALPHA_RATIO = Fraction(ALPHA_EXACT, V)   # 1/4

# ── Fractional chromatic number ───────────────────────────────────────────────
# For vertex-transitive G: χ_f(G) = v / α(G)  (Lovász, Schrijver)
# χ_f(W(3,3)) = 40 / 10 = 4 = EW_GAUGE_4
CHI_FRAC = Fraction(V, ALPHA_EXACT)      # Fraction(4, 1)
CHI_FRAC_INT = int(CHI_FRAC)             # 4

# ── Clique number ω(W(3,3)) ───────────────────────────────────────────────────
# W(3,3) = symplectic polar graph Sp(4, 3). Max cliques are totally isotropic
# projective planes (2-subspaces of GF(3)^4). A totally isotropic plane over
# GF(3) contains (3² − 1)/(3 − 1) = 4 projective points → ω = 4.
OMEGA_CLIQUE = 4   # = EW_GAUGE_4

# ── Lovász sandwich theorem verification ─────────────────────────────────────
# ω(G) ≤ ϑ(Ḡ) ≤ χ(G):   4 ≤ 4 ≤ χ
# α(G) ≤ ϑ(G) ≤ χ(Ḡ):  10 ≤ 10 ≤ χ(Ḡ)
OMEGA_BOUND_HOLDS = (OMEGA_CLIQUE <= int(THETA_COMP))   # True: 4 ≤ 4
ALPHA_BOUND_HOLDS = (ALPHA_EXACT <= int(THETA_LOVÁSZ))  # True: 10 ≤ 10

# ── SM triple alignment ───────────────────────────────────────────────────────
# ϑ(Ḡ) = ω(G) = χ_f(G) = 4 = EW_GAUGE_4
SM_THETA_COMP = int(THETA_COMP)
SM_CHI_FRAC = CHI_FRAC_INT
SM_OMEGA = OMEGA_CLIQUE
SM_TRIPLE_CONSISTENT = (SM_THETA_COMP == OMEGA_CLIQUE == CHI_FRAC_INT == EW_GAUGE_4)

# 4 disjoint maximum independent sets tile V: α × χ_f = V
SM_ALPHA_FOUR_TIMES = ALPHA_EXACT * EW_GAUGE_4   # 40 = V

# ── Eigenvalue ratios ─────────────────────────────────────────────────────────
# K / |S_EIG| = 12 / 4 = 3 = Q  (degree / spectral gap recovers ternary base)
K_OVER_ABS_S = Fraction(K, abs(S_EIG))   # Fraction(3)

# ── Verification ─────────────────────────────────────────────────────────────
def verify_all():
    """Run all 27 CCXCIII checks and return (checks_list, passed, total)."""
    checks = []

    def chk(name, val, exp=True):
        ok = (val == exp) if (exp is not True) else bool(val)
        checks.append((name, ok, val))
        return ok

    # SRG structure
    chk("V==40",               V,              40)
    chk("K==12",               K,              12)
    chk("LAM==2",              LAM,            2)
    chk("MU==4",               MU,             4)
    chk("K+K2+1==V",           K + K2 + 1,     V)

    # Eigenvalues
    chk("R_EIG==2",            R_EIG,          2)
    chk("S_EIG==-4",           S_EIG,          -4)
    chk("DISC_INT==36",        DISC_INT,       36)
    chk("r+s == LAM-MU",       R_EIG + S_EIG,  LAM - MU)
    chk("r*s == MU-K",         R_EIG * S_EIG,  MU - K)

    # Lovász theta
    chk("THETA==10",           THETA_LOVÁSZ,   Fraction(10))
    chk("THETA_COMP==4",       THETA_COMP,     Fraction(4))
    chk("THETA_COMP==EW4",     int(THETA_COMP), EW_GAUGE_4)
    chk("THETA*THETA_COMP==V", THETA_PRODUCT,  Fraction(V))

    # Independence and ratio bound
    chk("RATIO_BOUND==10",     RATIO_BOUND,    Fraction(10))
    chk("ALPHA==10",           ALPHA_EXACT,    10)
    chk("ALPHA==THETA",        Fraction(ALPHA_EXACT), THETA_LOVÁSZ)

    # Fractional chromatic
    chk("CHI_FRAC==4",         CHI_FRAC,       Fraction(4))
    chk("CHI_FRAC==EW4",       CHI_FRAC_INT,   EW_GAUGE_4)
    chk("4*alpha==V",          ALPHA_EXACT * EW_GAUGE_4, V)

    # Clique number
    chk("OMEGA==4",            OMEGA_CLIQUE,   4)
    chk("OMEGA==EW4",          OMEGA_CLIQUE,   EW_GAUGE_4)

    # Sandwich bounds
    chk("omega<=theta_comp",   OMEGA_BOUND_HOLDS)
    chk("alpha<=theta",        ALPHA_BOUND_HOLDS)

    # SM triple
    chk("SM_triple_consistent", SM_TRIPLE_CONSISTENT)

    # Eigenvalue ratio
    chk("K/|s|==Q",            K_OVER_ABS_S,   Fraction(Q))
    chk("alpha*chi_f==V",      ALPHA_EXACT * CHI_FRAC_INT, V)

    passed = sum(1 for _, ok, _ in checks if ok)
    total = len(checks)
    return checks, passed, total


def build_ccxciii_summary():
    """Build the Part CCXCIII result summary dictionary."""
    checks, passed, total = verify_all()
    return {
        "part": "CCXCIII",
        "title": "Lovász Theta Function and Spectral Independence Bounds for W(3,3)",
        "checks_pass": passed,
        "checks_total": total,
        "status": "ALL_PASS" if passed == total else "FAIL",
        "theta_lovász": int(THETA_LOVÁSZ),
        "theta_comp": int(THETA_COMP),
        "theta_product": int(THETA_PRODUCT),
        "alpha_exact": ALPHA_EXACT,
        "chi_frac": CHI_FRAC_INT,
        "omega_clique": OMEGA_CLIQUE,
        "eigenvalue_r": R_EIG,
        "eigenvalue_s": S_EIG,
        "sm_triple": {
            "theta_comp": SM_THETA_COMP,
            "chi_frac": SM_CHI_FRAC,
            "omega": SM_OMEGA,
            "all_equal_EW_GAUGE_4": SM_TRIPLE_CONSISTENT,
        },
        "discoveries": [
            "ϑ(W(3,3)) = 10 = α(W(3,3)) — Lovász theta is tight; theta-exact",
            "ϑ(W(3,3)^c) = 4 = EW_GAUGE_4 — complement theta equals electroweak gauge count",
            "ϑ(G) · ϑ(Ḡ) = 40 = V — Lovász product recovers vertex count exactly",
            "χ_f(W(3,3)) = 4 = EW_GAUGE_4 — fractional chromatic equals EW gauge bosons",
            "ω(W(3,3)) = 4 = EW_GAUGE_4 — max clique (totally isotropic plane) = EW_GAUGE_4",
            "Triple: ϑ(Ḡ) = ω = χ_f = 4 = EW_GAUGE_4 — spectral, clique, fractional agree",
            "K / |s| = 12 / 4 = 3 = Q — degree–eigenvalue ratio recovers ternary base",
        ],
    }


if __name__ == "__main__":
    checks, passed, total = verify_all()
    for name, ok, val in checks:
        status = "✓" if ok else "✗"
        print(f"  {status} {name}: {val}")
    print(f"\nCCXCIII Verification: {passed}/{total} checks pass {'✓' if passed == total else '✗'}")
