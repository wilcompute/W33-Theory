"""
PART CCCVI — Distance Matrix Spectrum of W(3,3)

For a connected graph of diameter d, the distance matrix D has entries
D_ij = shortest-path distance between vertices i and j (D_ii = 0).

W(3,3) is strongly regular with diameter 2: every non-adjacent pair of
vertices is at distance exactly 2 (guaranteed by μ = MU = 4 > 0).

    D_ij = 0  if i = j
    D_ij = 1  if i ~ j  (adjacent)
    D_ij = 2  if i ≁ j, i ≠ j  (non-adjacent)

For a strongly regular graph srg(V, K, λ, μ) the distance matrix is:

    D = A + 2·(J − I − A) = 2J − 2I − A

where J is the all-ones matrix.  The eigenvalues follow from the spectral
decompositions of J, I, and A:

    Perron eigenvalue (eigenvector = all-ones):
        d_0 = 2V − 2 − K  =  2·40 − 2 − 12  = 66   (multiplicity 1)

    Restricted eigenvalues (eigenvectors orthogonal to all-ones):
        d_1 = 0 − 2 − R  =  −2 − 2  = −4   (multiplicity MULT_R = 24)
        d_2 = 0 − 2 − S  =  −2 − (−4) = 2  (multiplicity MULT_S = 15)

Remarkable: the restricted distance eigenvalues are {−4, 2} = {S, R} —
a permutation of the restricted adjacency eigenvalues!

Spectral identities:
    tr(D) = 1·66 + 24·(−4) + 15·2 = 66 − 96 + 30 = 0  (all diagonal zeros)
    tr(D²) = 1·66² + 24·16 + 15·4 = 4356 + 384 + 60 = 4800

From the matrix structure:
    tr(D²) = (# ordered adj. pairs)·1² + (# ordered non-adj. pairs)·2²
           = 2·EDGES·1 + (V·(V−1) − 2·EDGES)·4
           = 480 + 1080·4 = 480 + 4320 = 4800

SM encoding of tr(D²):
    4800 = V · ALPHA · K = 40 · 10 · 12
    4800 = 2 · EDGES · ALPHA = 480 · 10

SM encoding of d_0 = 66:
    66 = 2 · GUT_DIM + K   =  54 + 12
    66 = (V − 1) + GUT_DIM =  39 + 27  (also: V−1 = K + K2 = 12+27 = 39 ✓)

SM encoding of d_1 = −4:
    |d_1| = 4 = EW_GAUGE_4 = MU

SM encoding of d_2 = 2:
    d_2 = 2 = R_EIG = LAM

Wiener index (sum of all pairwise distances):
    W = sum_{i<j} D_ij
      = EDGES·1 + (V·(V−1)/2 − EDGES)·2
      = 240 + 540·2 = 240 + 1080 = 1320
    Equivalently: W = V·(V−1) − EDGES = 1560 − 240 = 1320

SM identities for Wiener index:
    W = GUT_DIM · V + EDGES   = 27·40 + 240 = 1320
    W = MULT_R · MULT_S + 4 · EDGES = 360 + 960 = 1320
    W = V · (GUT_DIM + K//2)  = 40·33 = 1320

Distance spread:
    d_0 − d_1 = 66 − (−4) = 70
    70 = MULT_R + MULT_S + MU + GUT_DIM = 24 + 15 + 4 + 27

SM finale:
    d_0 − |d_1| − d_2 = 66 − 4 − 2 = 60 = 2 · ALPHA · GENERATIONS
    Diameter = 2 = LAM  (a numerical coincidence between graph diameter and λ)
"""

from fractions import Fraction

# ── W(3,3) constants ──────────────────────────────────────────────────────────
V = 40
K = 12
K2 = 27       # second subconstituent size = V - 1 - K
LAM = 2
MU = 4
EDGES = 240

R_EIG = 2
S_EIG = -4
MULT_R = 24
MULT_S = 15

EW_GAUGE_4 = 4
ALPHA = 10
GUT_DIM = 27
GENERATIONS = 3

# ── Distance matrix eigenvalues ───────────────────────────────────────────────
# D = 2J - 2I - A  (for srg with diameter 2)
# d_0 = 2V - 2 - K  (Perron, multiplicity 1)
# d_1 = -2 - R     (restricted, multiplicity MULT_R)
# d_2 = -2 - S     (restricted, multiplicity MULT_S)

D_EIG_0 = 2 * V - 2 - K          # = 66
D_EIG_1 = -2 - R_EIG              # = -4
D_EIG_2 = -2 - S_EIG              # =  2

# Verify multiplicity sum
D_MULT_SUM = 1 + MULT_R + MULT_S  # = 40 = V

# ── Remarkable coincidences ───────────────────────────────────────────────────
# d_1 = S_EIG and d_2 = R_EIG (restricted distance eigenvalues = adjacency eigenvalues swapped)
D_EIG_1_EQ_S = (D_EIG_1 == S_EIG)
D_EIG_2_EQ_R = (D_EIG_2 == R_EIG)

# ── Trace identities ─────────────────────────────────────────────────────────
D_SPEC_SUM = 1 * D_EIG_0 + MULT_R * D_EIG_1 + MULT_S * D_EIG_2
# = 66 - 96 + 30 = 0

D_TRACE_SQ_EIG = (1 * D_EIG_0**2 + MULT_R * D_EIG_1**2 + MULT_S * D_EIG_2**2)
# = 4356 + 384 + 60 = 4800

# From matrix structure:
D_TRACE_SQ_STRUCT = (2 * EDGES * 1 + (V * (V - 1) - 2 * EDGES) * 4)
# = 480 + 4320 = 4800

# SM encodings
D_TRACE_SQ_SM1 = V * ALPHA * K          # 40*10*12 = 4800
D_TRACE_SQ_SM2 = 2 * EDGES * ALPHA      # 2*240*10 = 4800

# ── Perron eigenvalue SM encodings ───────────────────────────────────────────
D_EIG_0_EQ_2GUT_K = (D_EIG_0 == 2 * GUT_DIM + K)       # 2*27+12 = 66
D_EIG_0_EQ_VM1_GUT = (D_EIG_0 == (V - 1) + GUT_DIM)    # 39+27 = 66

# SM encoding of restricted eigenvalues
D_ABS_EIG1_EQ_EW = (abs(D_EIG_1) == EW_GAUGE_4)         # |-4| = 4 = EW_GAUGE_4
D_ABS_EIG1_EQ_MU = (abs(D_EIG_1) == MU)                 # |-4| = 4 = MU
D_EIG_2_EQ_LAM = (D_EIG_2 == LAM)                       # 2 = λ

# ── Wiener index ─────────────────────────────────────────────────────────────
WIENER = EDGES * 1 + (V * (V - 1) // 2 - EDGES) * 2
# = 240 + 540*2 = 1320

WIENER_ALT = V * (V - 1) - EDGES    # = 1560 - 240 = 1320

WIENER_SM1 = GUT_DIM * V + EDGES            # 27*40+240 = 1320
WIENER_SM2 = MULT_R * MULT_S + 4 * EDGES   # 360+960 = 1320
WIENER_SM3 = V * (GUT_DIM + K // 2)        # 40*33 = 1320

# ── Distance spread and SM finale ────────────────────────────────────────────
D_SPREAD = D_EIG_0 - D_EIG_1          # = 66 - (-4) = 70
D_SPREAD_SM = (D_SPREAD == MULT_R + MULT_S + MU + GUT_DIM)
# 70 = 24 + 15 + 4 + 27

D_FINALE = D_EIG_0 - abs(D_EIG_1) - D_EIG_2   # = 66-4-2 = 60
D_FINALE_SM = (D_FINALE == 2 * ALPHA * GENERATIONS)  # 2*10*3 = 60

# Diameter = 2 (srg with μ > 0 has diameter exactly 2)
DIAMETER = 2
DIAMETER_EQ_LAM = (DIAMETER == LAM)   # diameter = λ = 2 (coincidence)


def verify_all():
    """Return (checks, passed, total) with exactly 27 checks."""
    checks = []

    def chk(name, ok, lhs=None, rhs=None):
        checks.append({"name": name, "ok": bool(ok), "lhs": str(lhs), "rhs": str(rhs)})

    # Group 1 — SRG parameters (5)
    chk("V = 40", V == 40, V, 40)
    chk("K = 12", K == 12, K, 12)
    chk("EDGES = 240", EDGES == 240, EDGES, 240)
    chk("R_EIG = 2, S_EIG = -4",
        R_EIG == 2 and S_EIG == -4, (R_EIG, S_EIG), (2, -4))
    chk("MULT_R = 24, MULT_S = 15",
        MULT_R == 24 and MULT_S == 15, (MULT_R, MULT_S), (24, 15))

    # Group 2 — Distance eigenvalue formulae (5)
    chk("d_0 = 2V-2-K = 66", D_EIG_0 == 66, D_EIG_0, 66)
    chk("d_1 = -2-R = -4", D_EIG_1 == -4, D_EIG_1, -4)
    chk("d_2 = -2-S = 2", D_EIG_2 == 2, D_EIG_2, 2)
    chk("d_1 = S_EIG (restricted distance = adj S eigenvalue)",
        D_EIG_1_EQ_S, D_EIG_1, S_EIG)
    chk("d_2 = R_EIG (restricted distance = adj R eigenvalue)",
        D_EIG_2_EQ_R, D_EIG_2, R_EIG)

    # Group 3 — Spectral identities (5)
    chk("tr(D) = 0 (weighted eigenvalue sum)",
        D_SPEC_SUM == 0, D_SPEC_SUM, 0)
    chk("tr(D^2) = 4800 (from eigenvalues)",
        D_TRACE_SQ_EIG == 4800, D_TRACE_SQ_EIG, 4800)
    chk("tr(D^2) = 4800 (from matrix structure)",
        D_TRACE_SQ_STRUCT == 4800, D_TRACE_SQ_STRUCT, 4800)
    chk("tr(D^2) = V*ALPHA*K = 4800",
        D_TRACE_SQ_SM1 == 4800, D_TRACE_SQ_SM1, 4800)
    chk("tr(D^2) = 2*EDGES*ALPHA = 4800",
        D_TRACE_SQ_SM2 == 4800, D_TRACE_SQ_SM2, 4800)

    # Group 4 — Spectral radius SM encodings (4)
    chk("d_0 = 2*GUT_DIM + K = 66",
        D_EIG_0_EQ_2GUT_K, D_EIG_0, 2 * GUT_DIM + K)
    chk("d_0 = (V-1) + GUT_DIM = 66",
        D_EIG_0_EQ_VM1_GUT, D_EIG_0, (V - 1) + GUT_DIM)
    chk("|d_1| = EW_GAUGE_4 = MU = 4",
        D_ABS_EIG1_EQ_EW and D_ABS_EIG1_EQ_MU, abs(D_EIG_1), EW_GAUGE_4)
    chk("d_2 = LAM = 2",
        D_EIG_2_EQ_LAM, D_EIG_2, LAM)

    # Group 5 — Wiener index (4)
    chk("WIENER = V*(V-1) - EDGES = 1320",
        WIENER == 1320 and WIENER_ALT == 1320, WIENER, 1320)
    chk("WIENER = GUT_DIM*V + EDGES = 1320",
        WIENER_SM1 == 1320, WIENER_SM1, 1320)
    chk("WIENER = MULT_R*MULT_S + 4*EDGES = 1320",
        WIENER_SM2 == 1320, WIENER_SM2, 1320)
    chk("WIENER = V*(GUT_DIM + K//2) = 1320",
        WIENER_SM3 == 1320, WIENER_SM3, 1320)

    # Group 6 — SM finale (4)
    chk("d_0 - |d_1| - d_2 = 2*ALPHA*GENERATIONS = 60",
        D_FINALE_SM, D_FINALE, 2 * ALPHA * GENERATIONS)
    chk("1 + MULT_R + MULT_S = V (multiplicity partition)",
        D_MULT_SUM == V, D_MULT_SUM, V)
    chk("D_SPREAD = d_0-d_1 = MULT_R+MULT_S+MU+GUT_DIM = 70",
        D_SPREAD_SM, D_SPREAD, MULT_R + MULT_S + MU + GUT_DIM)
    chk("DIAMETER = 2 = LAM (diameter coincides with lambda)",
        DIAMETER_EQ_LAM, DIAMETER, LAM)

    passed = sum(1 for c in checks if c["ok"])
    return checks, passed, len(checks)


def build_cccvi_summary():
    checks, passed, total = verify_all()
    return {
        "part": "CCCVI",
        "title": "Distance Matrix Spectrum of W(3,3)",
        "checks_pass": passed,
        "checks_total": total,
        "status": "PASS" if passed == total else "FAIL",
        "fields": {
            "V": V,
            "K": K,
            "D_EIG_0": D_EIG_0,
            "D_EIG_1": D_EIG_1,
            "D_EIG_2": D_EIG_2,
            "D_SPEC_SUM": D_SPEC_SUM,
            "D_TRACE_SQ": D_TRACE_SQ_EIG,
            "WIENER": WIENER,
            "D_SPREAD": D_SPREAD,
            "DIAMETER": DIAMETER,
        },
        "discoveries": [
            "d_0=66=2*GUT_DIM+K: Perron distance eigenvalue encodes GUT dimension and valency",
            "d_0=66=(V-1)+GUT_DIM: V-1=K+K2 vertex gap plus GUT dimension",
            "d_1=-4=S_EIG: restricted distance eigenvalue equals adjacency S eigenvalue",
            "d_2=2=R_EIG=LAM: restricted distance eigenvalue equals adjacency R eigenvalue",
            "|d_1|=EW_GAUGE_4=MU: absolute value of second distance eigenvalue = EW factor = codegree",
            "tr(D^2)=4800=V*ALPHA*K=2*EDGES*ALPHA: second moment has dual SM encoding",
            "WIENER=1320=GUT_DIM*V+EDGES=MULT_R*MULT_S+4*EDGES: Wiener index has triple SM encoding",
            "D_SPREAD=70=MULT_R+MULT_S+MU+GUT_DIM: spectral spread is sum of four SM constants",
            "d_0-|d_1|-d_2=60=2*ALPHA*GENERATIONS: SM-weighted eigenvalue combination",
            "DIAMETER=2=LAM: graph diameter numerically coincides with first subconstituent parameter",
        ],
    }
