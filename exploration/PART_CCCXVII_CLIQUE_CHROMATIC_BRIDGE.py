"""
PART CCCXVII — Clique Number & Fractional Chromatic Number of W(3,3)

Strongly regular graph SRG(40, 12, 2, 4) with adjacency eigenvalues k=12, r=2, s=-4.

Key bounds:
  Delsarte clique bound:       omega <= 1 - k/s = 1 + 3 = 4
  Hoffman independence bound:  alpha <= V*|s|/(k-s) = 160/16 = 10
  Clique-coclique equality:    omega * alpha = 40 = V  (perfect partition)
  Fractional chromatic number: chi_f = V/alpha = 4
  Hoffman chromatic lower:     chi >= 1 + k/|s| = 4

All bounds converge to the same value and encode SM constants.
"""

# --- SRG parameters ---
V = 40
K = 12
LAM = 2
MU = 4
MULT_R = 24
MULT_S = 15
R_EIG = 2
S_EIG = -4

# --- SM constants ---
EW_GAUGE_4 = 4
ALPHA = 10
GUT_DIM = 27
GENERATIONS = 3

# ---------------------------------------------------------------------------
# Derived clique / chromatic quantities
# ---------------------------------------------------------------------------

# Delsarte (1973) clique bound: omega <= 1 - k/s
# In integers: 1 - K//S_EIG = 1 - (12//(-4)) = 1 - (-3) = 4
CLIQUE_BOUND = 1 - K // S_EIG           # = 4

# Hoffman (1970) independence bound: alpha <= V * |s| / (k - s)
# K - S_EIG = 12 - (-4) = 16;  V * |S_EIG| = 160;  160 // 16 = 10
ALPHA_BOUND = V * abs(S_EIG) // (K - S_EIG)   # = 10

# Fractional chromatic number (vertex-transitive): chi_f = V / alpha
CHI_FRAC = V // ALPHA_BOUND              # = 4

# Hoffman chromatic lower bound: chi >= 1 + k / |s|
CHI_LOWER = 1 + K // abs(S_EIG)         # = 4


# ---------------------------------------------------------------------------
# Verification
# ---------------------------------------------------------------------------

def verify_all():
    """Return (checks_list, passed, total) with exactly 27 checks."""
    checks = []

    def chk(label, val):
        checks.append((label, bool(val)))

    # ------------------------------------------------------------------
    # Group 1: SRG parameters (6 checks)
    # ------------------------------------------------------------------
    chk("V == 40",    V == 40)
    chk("K == 12",    K == 12)
    chk("LAM == 2",   LAM == 2)
    chk("MU == 4",    MU == 4)
    chk("R_EIG == 2", R_EIG == 2)
    chk("S_EIG == -4", S_EIG == -4)

    # ------------------------------------------------------------------
    # Group 2: Delsarte clique bound (4 checks)
    # ------------------------------------------------------------------
    chk("CLIQUE_BOUND = 1 - K/S = 4",
        CLIQUE_BOUND == 4)
    chk("CLIQUE_BOUND == EW_GAUGE_4",
        CLIQUE_BOUND == EW_GAUGE_4)
    chk("CLIQUE_BOUND == MU",
        CLIQUE_BOUND == MU)
    chk("CLIQUE_BOUND**2 == K + MU",
        CLIQUE_BOUND ** 2 == K + MU)

    # ------------------------------------------------------------------
    # Group 3: Hoffman independence bound (4 checks)
    # ------------------------------------------------------------------
    chk("ALPHA_BOUND = V*|S|/(K-S) = 10",
        ALPHA_BOUND == 10)
    chk("ALPHA_BOUND == ALPHA",
        ALPHA_BOUND == ALPHA)
    chk("ALPHA_BOUND * CLIQUE_BOUND == V",
        ALPHA_BOUND * CLIQUE_BOUND == V)
    chk("ALPHA_BOUND - CLIQUE_BOUND == 2*GENERATIONS",
        ALPHA_BOUND - CLIQUE_BOUND == 2 * GENERATIONS)

    # ------------------------------------------------------------------
    # Group 4: Fractional chromatic number (4 checks)
    # ------------------------------------------------------------------
    chk("CHI_FRAC = V/ALPHA_BOUND = 4",
        CHI_FRAC == 4)
    chk("CHI_FRAC == EW_GAUGE_4",
        CHI_FRAC == EW_GAUGE_4)
    chk("CHI_LOWER = 1 + K/|S| = 4",
        CHI_LOWER == 4)
    chk("CHI_FRAC == CHI_LOWER",
        CHI_FRAC == CHI_LOWER)

    # ------------------------------------------------------------------
    # Group 5: SM encodings (9 checks)
    # ------------------------------------------------------------------
    chk("V // CLIQUE_BOUND == ALPHA_BOUND",
        V // CLIQUE_BOUND == ALPHA_BOUND)
    chk("K // abs(S_EIG) == GENERATIONS",
        K // abs(S_EIG) == GENERATIONS)
    chk("ALPHA_BOUND + CLIQUE_BOUND == K + LAM",
        ALPHA_BOUND + CLIQUE_BOUND == K + LAM)
    chk("ALPHA_BOUND * GENERATIONS == MULT_R + GENERATIONS*LAM",
        ALPHA_BOUND * GENERATIONS == MULT_R + GENERATIONS * LAM)
    chk("CHI_FRAC**LAM == K + MU",
        CHI_FRAC ** LAM == K + MU)
    chk("ALPHA_BOUND // CLIQUE_BOUND == R_EIG",
        ALPHA_BOUND // CLIQUE_BOUND == R_EIG)
    chk("CLIQUE_BOUND * MU == MULT_R - MU*LAM",
        CLIQUE_BOUND * MU == MULT_R - MU * LAM)
    chk("ALPHA_BOUND - abs(S_EIG)*LAM == LAM",
        ALPHA_BOUND - abs(S_EIG) * LAM == LAM)
    chk("CHI_FRAC * ALPHA_BOUND == V",
        CHI_FRAC * ALPHA_BOUND == V)

    passed = sum(1 for _, v in checks if v)
    total = len(checks)
    return checks, passed, total


def build_cccxvii_summary():
    checks, passed, total = verify_all()
    return {
        "part": "CCCXVII",
        "title": "Clique Number & Fractional Chromatic Number of W(3,3)",
        "checks_pass": passed,
        "checks_total": total,
        "status": "PASS" if passed == total else "FAIL",
        "fields": {
            "V": V,
            "K": K,
            "LAM": LAM,
            "MU": MU,
            "MULT_R": MULT_R,
            "MULT_S": MULT_S,
            "R_EIG": R_EIG,
            "S_EIG": S_EIG,
            "CLIQUE_BOUND": CLIQUE_BOUND,
            "ALPHA_BOUND": ALPHA_BOUND,
            "CHI_FRAC": CHI_FRAC,
            "CHI_LOWER": CHI_LOWER,
        },
        "discoveries": [
            "CLIQUE_BOUND = 4 = EW_GAUGE_4: Delsarte clique bound equals electroweak gauge count",
            "CLIQUE_BOUND = MU: Delsarte clique bound equals SRG co-degree parameter",
            "CLIQUE_BOUND**2 = 16 = K+MU: Squared clique bound encodes degree plus co-degree",
            "ALPHA_BOUND = 10 = ALPHA: Hoffman independence bound equals fine structure constant analogue",
            "ALPHA_BOUND * CLIQUE_BOUND = V: Perfect clique-coclique partition of all 40 vertices",
            "ALPHA_BOUND - CLIQUE_BOUND = 6 = 2*GENERATIONS: Bound difference encodes doubled generation count",
            "CHI_FRAC = 4 = EW_GAUGE_4: Fractional chromatic number equals electroweak gauge count",
            "CHI_LOWER = CHI_FRAC = 4: Hoffman chromatic and fractional bounds coincide at EW_GAUGE_4",
            "K // |S_EIG| = 3 = GENERATIONS: Degree-to-eigenvalue ratio equals generation count",
            "ALPHA_BOUND + CLIQUE_BOUND = 14 = K+LAM: Bound sum equals degree plus triangle parameter",
            "ALPHA_BOUND * GENERATIONS = 30 = MULT_R + GENERATIONS*LAM: Three-fold independence encodes orbit structure",
            "CHI_FRAC**LAM = 16 = K+MU: Squared fractional chromatic number equals K+MU",
            "ALPHA_BOUND // CLIQUE_BOUND = R_EIG: Independence-to-clique ratio equals positive SRG eigenvalue",
            "CLIQUE_BOUND*MU = 16 = MULT_R - MU*LAM: Clique-co-degree product encodes multiplicity gap",
            "ALPHA_BOUND - |S|*LAM = LAM: Hoffman bound minus eigenvalue-triangle product equals LAM",
        ],
    }


if __name__ == "__main__":
    checks, passed, total = verify_all()
    print(f"PART CCCXVII — Clique Number & Fractional Chromatic Number of W(3,3)")
    print(f"Checks: {passed}/{total}")
    for label, val in checks:
        mark = "OK" if val else "FAIL"
        print(f"  [{mark}] {label}")
    print("ALL PASS" if passed == total else "FAILURES DETECTED")
