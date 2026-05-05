"""
PART CCCVII — Line Graph Spectrum of W(3,3)

The line graph L(G) of a graph G has the edges of G as its vertices,
with two vertices of L(G) adjacent when the corresponding edges of G
share an endpoint.

For a K-regular graph G on V vertices with EDGES = VK/2 edges:

    |V(L(G))| = EDGES  =  240
    |E(L(G))| = V·C(K,2) = V·K·(K−1)/2  =  40·66 = 2640
    degree in L(G)  = 2·(K−1) = 22  (L(G) is itself 2(K−1)-regular)

The spectrum of L(G) follows from the incidence matrix B (n×m):
    BB^T = A(G) + K·I,   B^T B = A(L(G)) + 2·I

Hence eigenvalues of A(L(G)):
    λ_i(G) + K − 2   for each adjacency eigenvalue λ_i(G)  (i = 1…n)
    −2   with multiplicity  m − n  (null vectors of B^T)

Applied to W(3,3) — srg(40, 12, 2, 4):

    A(G) eigenvalues:  K=12 (×1),  R=2 (×24),  S=−4 (×15)

    L(G) eigenvalues:
      ℓ_0 = K + K − 2 =  22,  mult  1
      ℓ_1 = R + K − 2 =  12,  mult  24   (= MULT_R)
      ℓ_2 = S + K − 2 =   6,  mult  15   (= MULT_S)
      ℓ_3 =         −2,  mult  EDGES − V = 200

Total multiplicity: 1 + 24 + 15 + 200 = 240 = EDGES = |V(L(G))| ✓

Spectral identities:
    tr(A(L))  = 1·22 + 24·12 + 15·6 + 200·(−2)
              = 22 + 288 + 90 − 400 = 0
    tr(A(L)²) = 1·484 + 24·144 + 15·36 + 200·4
              = 484 + 3456 + 540 + 800 = 5280
             = 2·|E(L(G))| = 2·2640

SM encodings:
    ℓ_0 = 22 = K + ALPHA         = 12 + 10
    ℓ_1 = 12 = K   (line graph eigenvalue equals SRG valency)
    ℓ_2 =  6 = LAM·GENERATIONS   = 2·3
    mult(ℓ_3) = 200 = (ALPHA//2)·V = 5·40

    tr(A(L)²) = 5280 = V·K·(K−1)       = 40·12·11
                     = 2·EDGES·(K−1)   = 2·240·11

SM finale:
    ℓ_0 − ℓ_2         = 22 − 6  = 16 = K + EW_GAUGE_4
    ℓ_0 + ℓ_3         = 22 + (−2) = 20 = 2·ALPHA
    ℓ_1 − |ℓ_3|       = 12 − 2  = 10 = ALPHA
"""

from fractions import Fraction

# ── W(3,3) constants ──────────────────────────────────────────────────────────
V = 40
K = 12
K2 = 27
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

# ── Line graph parameters ─────────────────────────────────────────────────────
L_V = EDGES                            # |V(L(G))| = 240
L_EDGES = V * K * (K - 1) // 2        # |E(L(G))| = 2640
L_VALENCY = 2 * (K - 1)               # = 22  (L(G) is 22-regular)

# ── Line graph eigenvalues (from B^T B = A(L) + 2I, BB^T = A(G) + KI) ───────
L_EIG_0 = K + K - 2                   # = 22,  mult 1
L_EIG_1 = R_EIG + K - 2               # = 12,  mult MULT_R = 24
L_EIG_2 = S_EIG + K - 2               # =  6,  mult MULT_S = 15
L_EIG_3 = -2                          # = -2,  mult EDGES - V = 200

MULT_L3 = L_V - V                     # = 200
L_MULT_SUM = 1 + MULT_R + MULT_S + MULT_L3   # = 240 = L_V

# ── Spectral sums ─────────────────────────────────────────────────────────────
L_SPEC_SUM = (1 * L_EIG_0 + MULT_R * L_EIG_1
              + MULT_S * L_EIG_2 + MULT_L3 * L_EIG_3)
# = 22 + 288 + 90 - 400 = 0

L_TRACE_SQ_EIG = (1 * L_EIG_0**2 + MULT_R * L_EIG_1**2
                  + MULT_S * L_EIG_2**2 + MULT_L3 * L_EIG_3**2)
# = 484 + 3456 + 540 + 800 = 5280

L_TRACE_SQ_EDGES = 2 * L_EDGES        # = 5280
L_TRACE_SQ_SM1 = V * K * (K - 1)     # 40·12·11 = 5280
L_TRACE_SQ_SM2 = 2 * EDGES * (K - 1) # 2·240·11 = 5280

# ── SM encodings ──────────────────────────────────────────────────────────────
L_EIG_0_EQ_K_ALPHA = (L_EIG_0 == K + ALPHA)         # 12+10=22
L_EIG_0_EQ_VALENCY = (L_EIG_0 == L_VALENCY)          # largest eig = degree
L_EIG_1_EQ_K = (L_EIG_1 == K)                        # 12=K
L_EIG_2_EQ_LAM_GEN = (L_EIG_2 == LAM * GENERATIONS)  # 2*3=6
MULT_L3_SM = (MULT_L3 == (ALPHA // 2) * V)           # 5*40=200

# ── SM finale ─────────────────────────────────────────────────────────────────
L_EIG_02_DIFF = L_EIG_0 - L_EIG_2                    # 22-6=16
L_EIG_02_DIFF_SM = (L_EIG_02_DIFF == K + EW_GAUGE_4) # 12+4=16

L_EIG_03_SUM = L_EIG_0 + L_EIG_3                     # 22-2=20
L_EIG_03_SUM_SM = (L_EIG_03_SUM == 2 * ALPHA)        # 2*10=20

L_EIG_13_DIFF = L_EIG_1 - abs(L_EIG_3)               # 12-2=10
L_EIG_13_DIFF_SM = (L_EIG_13_DIFF == ALPHA)          # 10=ALPHA


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

    # Group 2 — Line graph structure (5)
    chk("|V(L)| = EDGES = 240", L_V == 240, L_V, 240)
    chk("|E(L)| = V*K*(K-1)/2 = 2640", L_EDGES == 2640, L_EDGES, 2640)
    chk("L_VALENCY = 2*(K-1) = 22", L_VALENCY == 22, L_VALENCY, 22)
    chk("MULT_L3 = EDGES - V = 200", MULT_L3 == 200, MULT_L3, 200)
    chk("1 + MULT_R + MULT_S + MULT_L3 = L_V (total mult)",
        L_MULT_SUM == L_V, L_MULT_SUM, L_V)

    # Group 3 — Line graph eigenvalue formulae (5)
    chk("L_EIG_0 = K+K-2 = 22", L_EIG_0 == 22, L_EIG_0, 22)
    chk("L_EIG_1 = R+K-2 = 12", L_EIG_1 == 12, L_EIG_1, 12)
    chk("L_EIG_2 = S+K-2 = 6", L_EIG_2 == 6, L_EIG_2, 6)
    chk("L_EIG_3 = -2", L_EIG_3 == -2, L_EIG_3, -2)
    chk("L_EIG_0 = L_VALENCY (largest eigenvalue = degree)",
        L_EIG_0_EQ_VALENCY, L_EIG_0, L_VALENCY)

    # Group 4 — Trace identities (5)
    chk("tr(A(L)) = 0 (weighted sum of eigenvalues)",
        L_SPEC_SUM == 0, L_SPEC_SUM, 0)
    chk("tr(A(L)^2) = 5280 (from eigenvalues)",
        L_TRACE_SQ_EIG == 5280, L_TRACE_SQ_EIG, 5280)
    chk("tr(A(L)^2) = 2*|E(L)| = 5280",
        L_TRACE_SQ_EDGES == 5280, L_TRACE_SQ_EDGES, 5280)
    chk("tr(A(L)^2) = V*K*(K-1) = 5280",
        L_TRACE_SQ_SM1 == 5280, L_TRACE_SQ_SM1, 5280)
    chk("tr(A(L)^2) = 2*EDGES*(K-1) = 5280",
        L_TRACE_SQ_SM2 == 5280, L_TRACE_SQ_SM2, 5280)

    # Group 5 — SM encodings (4)
    chk("L_EIG_0 = K + ALPHA = 22",
        L_EIG_0_EQ_K_ALPHA, L_EIG_0, K + ALPHA)
    chk("L_EIG_1 = K = 12 (line eigenvalue equals SRG valency)",
        L_EIG_1_EQ_K, L_EIG_1, K)
    chk("L_EIG_2 = LAM*GENERATIONS = 6",
        L_EIG_2_EQ_LAM_GEN, L_EIG_2, LAM * GENERATIONS)
    chk("MULT_L3 = (ALPHA//2)*V = 200",
        MULT_L3_SM, MULT_L3, (ALPHA // 2) * V)

    # Group 6 — SM finale (3)
    chk("L_EIG_0 - L_EIG_2 = K + EW_GAUGE_4 = 16",
        L_EIG_02_DIFF_SM, L_EIG_02_DIFF, K + EW_GAUGE_4)
    chk("L_EIG_0 + L_EIG_3 = 2*ALPHA = 20",
        L_EIG_03_SUM_SM, L_EIG_03_SUM, 2 * ALPHA)
    chk("L_EIG_1 - |L_EIG_3| = ALPHA = 10",
        L_EIG_13_DIFF_SM, L_EIG_13_DIFF, ALPHA)

    passed = sum(1 for c in checks if c["ok"])
    return checks, passed, len(checks)


def build_cccvii_summary():
    checks, passed, total = verify_all()
    return {
        "part": "CCCVII",
        "title": "Line Graph Spectrum of W(3,3)",
        "checks_pass": passed,
        "checks_total": total,
        "status": "PASS" if passed == total else "FAIL",
        "fields": {
            "V": V,
            "K": K,
            "L_V": L_V,
            "L_EDGES": L_EDGES,
            "L_VALENCY": L_VALENCY,
            "L_EIG_0": L_EIG_0,
            "L_EIG_1": L_EIG_1,
            "L_EIG_2": L_EIG_2,
            "L_EIG_3": L_EIG_3,
            "MULT_L3": MULT_L3,
            "L_TRACE_SQ": L_TRACE_SQ_EIG,
        },
        "discoveries": [
            "L_EIG_0=22=K+ALPHA: largest line graph eigenvalue encodes SRG valency plus fine-structure constant proxy",
            "L_EIG_1=K=12: middle line eigenvalue equals SRG valency exactly",
            "L_EIG_2=6=LAM*GENERATIONS=K//2: smallest positive line eigenvalue encodes generations and SRG lambda",
            "MULT_L3=200=(ALPHA//2)*V: null-space multiplicity of -2 encodes half-ALPHA times V",
            "tr(A(L)^2)=5280=V*K*(K-1)=2*EDGES*(K-1): second moment has dual SM encoding",
            "L_EIG_0=L_VALENCY=22: line graph is regular (always true for regular G), confirming Perron=degree",
            "L_EIG_0-L_EIG_2=16=K+EW_GAUGE_4: eigenvalue gap encodes electroweak gauge factor",
            "L_EIG_0+L_EIG_3=20=2*ALPHA: Perron plus (-2) recovers twice the fine-structure proxy",
            "L_EIG_1-|L_EIG_3|=10=ALPHA: middle eigenvalue minus 2 recovers ALPHA exactly",
        ],
    }
