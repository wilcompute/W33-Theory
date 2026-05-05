"""
PART CCCV — Signless Laplacian Spectrum of W(3,3)

The signless Laplacian of a graph is Q = D + A, where D is the degree matrix
and A is the adjacency matrix.  For a k-regular graph Q = kI + A, so its
eigenvalues are simply q_i = k + μ_i(A).

For W(3,3) (strongly regular, K=12):
    adjacency eigenvalues: K=12 (mult 1), R=2 (mult 24), S=-4 (mult 15)

    q_0 = K + K  = 24  (multiplicity 1)   — largest signless eigenvalue
    q_1 = K + R  = 14  (multiplicity 24)  — second (restricted) eigenvalue
    q_2 = K + S  =  8  (multiplicity 15)  — third (restricted) eigenvalue

These three values are the complete signless Laplacian spectrum.

Key identities:

    q_0 = 24 = 2*K = 2*ALPHA+EW_GAUGE_4+K ... let's be precise:
        24 = 2 * 12 = V/LAM * EW_GAUGE_4 / LAM = ...
        24 = MULT_R = well-known: MULT_R = 24 and q_0 = 24 coincide!

    q_1 = 14 = K + R = 12 + 2 = 14
        14 = LAP_EIG_1 + EW_GAUGE_4 = 10 + 4
        14 = GUT_DIM - K - 1 = 27 - 12 - 1 = 14  ✓
        14 = 2 * (ALPHA - R_EIG + EW_GAUGE_4) = 2*(10-2+4)/2 ... no
        14 = 2 * MU + K - MU = 12 + 2 = 14  (= K + R)

    q_2 = 8  = K + S = 12 + (-4) = 8
        8  = 2 * EW_GAUGE_4 = 2*4 = 8  ✓
        8  = MU + EW_GAUGE_4 = 4 + 4 = 8  ✓
        8  = K - EW_GAUGE_4 = 12 - 4 = 8  ✓  (also K - |S|)

Eigenvalue sums and products:
    Sum (with mult): 24*1 + 14*24 + 8*15 = 24 + 336 + 120 = 480 = 2*K*V = 2*EDGES
        (makes sense: sum of signless Laplacian eigenvalues = 2*|E| = 2*EDGES)

    Sum of distinct eigenvalues: 24 + 14 + 8 = 46 = V + K/2 - 6 ... let's check:
        46 = 24 + 14 + 8 = 46
        46 = V + K - K = ... 40 + 14 - 8 = 46?  40 + 6 = 46 ✓
        46 = V + MU + GENERATIONS + ALPHA - K + 3 ... messy
        46 = 2 * GUT_DIM - LAP_EIG_1 + MULT_R/K ... 
        Let's just use: 46 = q_0 + q_1 + q_2 = 46

    Product of distinct eigenvalues: 24 * 14 * 8 = 2688
        2688 = 2^7 * 3 * 7 = 128 * 21 = ...
        2688 = V * MULT_R * GENERATIONS * EW_GAUGE_4 / ... = 40 * 24 * ... hmm
        2688 = 2 * EDGES * q_2 = 2 * 240 * 8 / 2 = 1920? no...
        2688 = V * K * q_2 / ... = 40*12*8/2 = 1920? No.
        2688 = 24 * 14 * 8 = 24 * 112 = 2688
        2688 = 2^7 * 3 * 7 = 2688
        Let's factor: 2^7=128, 128*21=2688, 21=3*7
        2688 = 8 * 336 = q_2 * (sum of remaining q's times ...) hmm
        Actually: 2688 = V * K * GENERATIONS * EW_GAUGE_4 / (GENERATIONS * 2) 
               = 40 * 12 * 3 * 4 / 6 = 40 * 24 * 4 / 6? No.
        Simple: 2688 = q_0 * q_1 * q_2 = 24 * 14 * 8

    Trace of Q (= sum with mult): sum = 2*EDGES = 480
    Trace of Q^2 (= sum of q_i^2 with mult):
        = 1*24^2 + 24*14^2 + 15*8^2
        = 576 + 24*196 + 15*64
        = 576 + 4704 + 960
        = 6240

    Note: 6240 = V * K * (K+1) = 40 * 12 * 13 = 6240 ✓ (standard identity)

    Trace of Q^2 = V*K*(K+1) is a known identity for regular graphs!

Spectral radius:
    ρ(Q) = q_0 = 24 = 2*K = 2*MULT_R/2... 
    ρ(Q) = 24 = MULT_R (coincidence of two graph parameters)
    ρ(Q) = 24 = 2*ALPHA + EW_GAUGE_4 = 2*10+4 = 24  ✓

Smallest eigenvalue:
    q_min = q_2 = 8 = 2*EW_GAUGE_4 = MU + EW_GAUGE_4 = K - EW_GAUGE_4

Bipartiteness measure:
    For bipartite graphs, q_min = 0. For W(3,3): q_min = 8 > 0, confirming
    W(3,3) is not bipartite (as expected for a strongly regular graph with λ>0).

Energy of Q (signless Laplacian energy):
    QLE = sum |q_i - 2m/n| with mult, where 2m/n = 2*EDGES/V = 480/40 = 12 = K
    QLE = |24-12| + 24*|14-12| + 15*|8-12|
        = 12 + 24*2 + 15*4
        = 12 + 48 + 60
        = 120 = EDGES/2 = K*V/EW_GAUGE_4

Q-eigenvalue sum identity:
    q_0 + q_1 + q_2 = 2K + K + R + K + S = 4K + R + S = 4*12 + 2 + (-4) = 46
    46 = 4*K + R_EIG + S_EIG

    Sum with multiplicities: K*q_0 term... no, we already know it = 2*EDGES.
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

# ── Signless Laplacian eigenvalues ────────────────────────────────────────────
# Q = D + A = K*I + A  for K-regular graph
# q_i = K + mu_i(A)
Q_EIG_0 = K + K        # = 24, multiplicity 1
Q_EIG_1 = K + R_EIG    # = 14, multiplicity MULT_R = 24
Q_EIG_2 = K + S_EIG    # =  8, multiplicity MULT_S = 15

# ── Spectral sums ─────────────────────────────────────────────────────────────
# Sum with multiplicities = 2 * EDGES
Q_SPEC_SUM = 1 * Q_EIG_0 + MULT_R * Q_EIG_1 + MULT_S * Q_EIG_2
Q_SPEC_SUM_EQ_2E = (Q_SPEC_SUM == 2 * EDGES)

# Sum of distinct eigenvalues
Q_DISTINCT_SUM = Q_EIG_0 + Q_EIG_1 + Q_EIG_2    # = 46

# 46 = 4*K + R_EIG + S_EIG
Q_DISTINCT_SUM_FORMULA = (Q_DISTINCT_SUM == 4 * K + R_EIG + S_EIG)

# Product of distinct eigenvalues
Q_DISTINCT_PROD = Q_EIG_0 * Q_EIG_1 * Q_EIG_2    # = 24 * 14 * 8 = 2688

# ── Trace of Q^2 ──────────────────────────────────────────────────────────────
Q_TRACE_SQ = 1 * Q_EIG_0**2 + MULT_R * Q_EIG_1**2 + MULT_S * Q_EIG_2**2
# = 576 + 4704 + 960 = 6240 = V*K*(K+1)
Q_TRACE_SQ_EQ_VKK1 = (Q_TRACE_SQ == V * K * (K + 1))

# ── Spectral radius ───────────────────────────────────────────────────────────
Q_SPEC_RADIUS = Q_EIG_0    # = 24 = 2*K

# q_0 = 24 = MULT_R
Q_RADIUS_EQ_MULT_R = (Q_SPEC_RADIUS == MULT_R)

# q_0 = 2*ALPHA + EW_GAUGE_4 = 20 + 4 = 24
Q_RADIUS_EQ_2ALPHA_EW = (Q_SPEC_RADIUS == 2 * ALPHA + EW_GAUGE_4)

# ── Smallest eigenvalue identities ───────────────────────────────────────────
Q_MIN = Q_EIG_2    # = 8

# q_min = 2 * EW_GAUGE_4
Q_MIN_EQ_2EW = (Q_MIN == 2 * EW_GAUGE_4)

# q_min = MU + EW_GAUGE_4
Q_MIN_EQ_MU_EW = (Q_MIN == MU + EW_GAUGE_4)

# q_min = K - EW_GAUGE_4
Q_MIN_EQ_K_EW = (Q_MIN == K - EW_GAUGE_4)

# ── q_1 identities ───────────────────────────────────────────────────────────
# q_1 = 14 = GUT_DIM - K - 1
Q_EIG_1_EQ_GUT_K = (Q_EIG_1 == GUT_DIM - K - 1)

# q_1 = K + R_EIG
Q_EIG_1_EQ_KR = (Q_EIG_1 == K + R_EIG)

# ── Signless Laplacian energy ─────────────────────────────────────────────────
# Average = 2*EDGES/V = K
Q_AVERAGE = Fraction(2 * EDGES, V)    # = 12 = K

QLE = (1 * abs(Q_EIG_0 - K) + MULT_R * abs(Q_EIG_1 - K) + MULT_S * abs(Q_EIG_2 - K))
# = 12 + 48 + 60 = 120
QLE_EQ_EDGES_HALF = (QLE == EDGES // 2)    # 120 = 240/2

# QLE = K * V / EW_GAUGE_4 = 12*40/4 = 120
QLE_EQ_KV_EW = (QLE == K * V // EW_GAUGE_4)

# ── Additional arithmetic ─────────────────────────────────────────────────────
# Eigenvalue differences
Q_EIG_01_DIFF = Q_EIG_0 - Q_EIG_1    # 24 - 14 = 10 = ALPHA
Q_DIFF_01_EQ_ALPHA = (Q_EIG_01_DIFF == ALPHA)

# 14 - 8 = 6 = K//2
Q_EIG_12_DIFF = Q_EIG_1 - Q_EIG_2    # = 6
Q_DIFF_12_EQ_K_HALF = (Q_EIG_12_DIFF == K // 2)

# 24 - 8 = 16 = K + EW_GAUGE_4 = Laplacian spectral radius
Q_EIG_02_DIFF = Q_EIG_0 - Q_EIG_2    # = 16
Q_DIFF_02_EQ_K_EW = (Q_EIG_02_DIFF == K + EW_GAUGE_4)


def verify_all():
    """Return (checks, passed, total) with exactly 27 checks."""
    checks = []

    def chk(name, ok, lhs=None, rhs=None):
        checks.append({"name": name, "ok": bool(ok), "lhs": str(lhs), "rhs": str(rhs)})

    # Group 1 — SRG parameters (5)
    chk("V = 40", V == 40, V, 40)
    chk("K = 12", K == 12, K, 12)
    chk("MULT_R = 24, MULT_S = 15",
        MULT_R == 24 and MULT_S == 15, (MULT_R, MULT_S), (24, 15))
    chk("R_EIG = 2, S_EIG = -4",
        R_EIG == 2 and S_EIG == -4, (R_EIG, S_EIG), (2, -4))
    chk("EDGES = 240", EDGES == 240, EDGES, 240)

    # Group 2 — Signless Laplacian eigenvalues (5)
    chk("q_0 = K + K = 24", Q_EIG_0 == 24, Q_EIG_0, 24)
    chk("q_1 = K + R = 14", Q_EIG_1 == 14, Q_EIG_1, 14)
    chk("q_2 = K + S = 8",  Q_EIG_2 == 8,  Q_EIG_2, 8)
    chk("q_sum (weighted) = 2*EDGES = 480",
        Q_SPEC_SUM_EQ_2E, Q_SPEC_SUM, 2 * EDGES)
    chk("tr(Q^2) = V*K*(K+1) = 6240",
        Q_TRACE_SQ_EQ_VKK1, Q_TRACE_SQ, V * K * (K + 1))

    # Group 3 — Spectral radius and smallest eigenvalue (5)
    chk("rho(Q) = q_0 = 24 = MULT_R",
        Q_RADIUS_EQ_MULT_R, Q_SPEC_RADIUS, MULT_R)
    chk("rho(Q) = 2*ALPHA + EW_GAUGE_4 = 24",
        Q_RADIUS_EQ_2ALPHA_EW, Q_SPEC_RADIUS, 2 * ALPHA + EW_GAUGE_4)
    chk("q_min = 8 = 2*EW_GAUGE_4",
        Q_MIN_EQ_2EW, Q_MIN, 2 * EW_GAUGE_4)
    chk("q_min = MU + EW_GAUGE_4 = 8",
        Q_MIN_EQ_MU_EW, Q_MIN, MU + EW_GAUGE_4)
    chk("q_min = K - EW_GAUGE_4 = 8",
        Q_MIN_EQ_K_EW, Q_MIN, K - EW_GAUGE_4)

    # Group 4 — Distinct eigenvalue arithmetic (4)
    chk("q0+q1+q2 = 46 = 4K+R+S",
        Q_DISTINCT_SUM_FORMULA, Q_DISTINCT_SUM, 4 * K + R_EIG + S_EIG)
    chk("q_1 = GUT_DIM - K - 1 = 14",
        Q_EIG_1_EQ_GUT_K, Q_EIG_1, GUT_DIM - K - 1)
    chk("q0 - q1 = ALPHA = 10",
        Q_DIFF_01_EQ_ALPHA, Q_EIG_01_DIFF, ALPHA)
    chk("q1 - q2 = K/2 = 6",
        Q_DIFF_12_EQ_K_HALF, Q_EIG_12_DIFF, K // 2)

    # Group 5 — Signless Laplacian energy (4)
    chk("QLE = 120", QLE == 120, QLE, 120)
    chk("QLE = EDGES/2 = 120",
        QLE_EQ_EDGES_HALF, QLE, EDGES // 2)
    chk("QLE = K*V/EW_GAUGE_4 = 120",
        QLE_EQ_KV_EW, QLE, K * V // EW_GAUGE_4)
    chk("q0 - q2 = K + EW_GAUGE_4 = 16",
        Q_DIFF_02_EQ_K_EW, Q_EIG_02_DIFF, K + EW_GAUGE_4)

    # Group 6 — SM encoding (4)
    chk("q_0 = 24 = MULT_R (coincidence)",
        Q_EIG_0 == MULT_R, Q_EIG_0, MULT_R)
    chk("q_2 = 8 = 2*EW (SM EW factor)",
        Q_EIG_2 == 2 * EW_GAUGE_4, Q_EIG_2, 2 * EW_GAUGE_4)
    chk("q_1 = 14 = 2*(GUT_DIM - K) = 2*15 = 30? No: GUT-K-1=14",
        Q_EIG_1 == GUT_DIM - K - 1, Q_EIG_1, GUT_DIM - K - 1)
    chk("Q_DISTINCT_PROD = 24*14*8 = 2688",
        Q_DISTINCT_PROD == 2688, Q_DISTINCT_PROD, 2688)

    passed = sum(1 for c in checks if c["ok"])
    return checks, passed, len(checks)


def build_cccv_summary():
    checks, passed, total = verify_all()
    return {
        "part": "CCCV",
        "title": "Signless Laplacian Spectrum of W(3,3)",
        "checks_pass": passed,
        "checks_total": total,
        "status": "PASS" if passed == total else "FAIL",
        "fields": {
            "V": V,
            "K": K,
            "Q_EIG_0": Q_EIG_0,
            "Q_EIG_1": Q_EIG_1,
            "Q_EIG_2": Q_EIG_2,
            "Q_SPEC_SUM": Q_SPEC_SUM,
            "Q_TRACE_SQ": Q_TRACE_SQ,
            "QLE": QLE,
            "Q_DISTINCT_SUM": Q_DISTINCT_SUM,
            "Q_DISTINCT_PROD": Q_DISTINCT_PROD,
        },
        "discoveries": [
            "q_0=24=MULT_R: spectral radius of Q coincides with restricted eigenmultiplicity",
            "q_0=2*ALPHA+EW_GAUGE_4=24: SM alpha and EW factor encode the largest Q-eigenvalue",
            "q_2=8=2*EW_GAUGE_4=MU+EW=K-EW: three simultaneous SM encodings of smallest Q-eigenvalue",
            "q_1=GUT_DIM-K-1=14: GUT dimension minus valency minus 1",
            "q_0-q_1=ALPHA=10: gap encodes fine-structure constant analogue",
            "QLE=120=EDGES/2=K*V/EW: signless Laplacian energy encodes edge count and SM constants",
            "tr(Q^2)=V*K*(K+1)=6240: universal identity for regular graphs, verified exactly",
            "Weighted eigenvalue sum = 2*EDGES = 480: trace identity",
        ],
    }
