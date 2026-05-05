"""
PART CCCVIII — Seidel Matrix Spectrum of W(3,3)

The Seidel matrix of a graph G on V vertices is S = J - I - 2A,
where J is the all-ones matrix and A is the adjacency matrix.
Entries are 0 on the diagonal, -1 for adjacent pairs, +1 for non-adjacent pairs.

For W(3,3) — srg(40, 12, 2, 4) — the Seidel eigenvalues are:
  sigma_0 = V - 1 - 2*K   (from K-eigenvector of A)
  sigma_1 = -(1 + 2*R)    (from R-eigenvectors of A, orthogonal to 1)
  sigma_2 = -(1 + 2*S)    (from S-eigenvectors of A, orthogonal to 1)

Because J acts as (V-1) on the all-ones eigenvector and 0 on orthogonal vectors.

W(3,3) SRG parameters: (V, K, lambda, mu) = (40, 12, 2, 4)
Restricted eigenvalues:  R = 2 (mult 24), S = -4 (mult 15)
SM constants: ALPHA=10, EW_GAUGE_4=4, GUT_DIM=27, GENERATIONS=3, LAM=2, MU=4
"""
from fractions import Fraction

# ---------------------------------------------------------------------------
# SRG parameters
# ---------------------------------------------------------------------------
V = 40
K = 12
K2 = 27
LAM = 2
MU = 4
EDGES = V * K // 2          # = 240
R_EIG = 2
S_EIG = -4
MULT_R = 24
MULT_S = 15

# SM proxy constants
EW_GAUGE_4 = 4
ALPHA = 10
GUT_DIM = 27
GENERATIONS = 3

# ---------------------------------------------------------------------------
# Seidel matrix eigenvalue formulae
# J acts as (V-1) on all-ones vector, 0 on its orthogonal complement.
# (J - I - 2A) v_K = (V-1)*1 - 1 - 2*K  = V - 1 - 2K   for all-ones eigenvector
# (J - I - 2A) v_R = 0 - 1 - 2*R         = -(1 + 2R)    for R-eigenvectors
# (J - I - 2A) v_S = 0 - 1 - 2*S         = -(1 + 2S)    for S-eigenvectors
# ---------------------------------------------------------------------------
SEI_EIG_0 = V - 1 - 2 * K          # = 39 - 24 = 15, multiplicity 1
SEI_EIG_1 = -(1 + 2 * R_EIG)       # = -(1+4) = -5, multiplicity MULT_R = 24
SEI_EIG_2 = -(1 + 2 * S_EIG)       # = -(1-8) = 7,  multiplicity MULT_S = 15

SEI_MULT_0 = 1
SEI_MULT_1 = MULT_R   # = 24
SEI_MULT_2 = MULT_S   # = 15

SEI_MULT_SUM = SEI_MULT_0 + SEI_MULT_1 + SEI_MULT_2   # = 40 = V

# ---------------------------------------------------------------------------
# Spectral identities
# ---------------------------------------------------------------------------
# Trace = sum of eigenvalues (Seidel is traceless: diagonal is 0)
SEI_SPEC_SUM = (SEI_MULT_0 * SEI_EIG_0
                + SEI_MULT_1 * SEI_EIG_1
                + SEI_MULT_2 * SEI_EIG_2)
# = 1*15 + 24*(-5) + 15*7 = 15 - 120 + 105 = 0

# tr(S^2): each off-diagonal entry is ±1, so tr(S^2) = sum_{i≠j} s_ij^2 = V*(V-1)
SEI_TRACE_SQ_EIG = (SEI_MULT_0 * SEI_EIG_0 ** 2
                    + SEI_MULT_1 * SEI_EIG_1 ** 2
                    + SEI_MULT_2 * SEI_EIG_2 ** 2)
# = 1*225 + 24*25 + 15*49 = 225 + 600 + 735 = 1560

SEI_TRACE_SQ_VM = V * (V - 1)      # = 40 * 39 = 1560  (all off-diagonal ±1)

# ---------------------------------------------------------------------------
# Symmetry: eigenvalue-multiplicity reflection
# SEI_EIG_0 = 15 = MULT_S  (Seidel Perron eigenvalue equals MULT_S of A)
# ---------------------------------------------------------------------------
SEI_EIG0_EQ_MULTS = SEI_EIG_0 == MULT_S

# MULT_R + MULT_S = V - 1  (total non-Perron multiplicities)
SEI_MULTS_SUM_VM1 = (MULT_R + MULT_S == V - 1)

# ---------------------------------------------------------------------------
# SM encodings
# ---------------------------------------------------------------------------
# SEI_EIG_0 = 15 = ALPHA + GENERATIONS + LAM  (10+3+2)
SEI_EIG0_SM = SEI_EIG_0 == ALPHA + GENERATIONS + LAM

# SEI_EIG_1 = -5 = -(MU + 1)
SEI_EIG1_SM = SEI_EIG_1 == -(MU + 1)

# SEI_EIG_2 = 7 = LAM + MU + 1  (2+4+1)
SEI_EIG2_SM_A = SEI_EIG_2 == LAM + MU + 1

# SEI_EIG_2 = 7 = K//2 + 1
SEI_EIG2_SM_B = SEI_EIG_2 == K // 2 + 1

# tr(S^2) = 1560 = ALPHA * (V-1) * MU  (10*39*4)
SEI_TRACE_SQ_SM1 = ALPHA * (V - 1) * MU    # = 1560
SEI_TRACE_SQ_SM2 = V * (V - 1)             # = 1560

# ---------------------------------------------------------------------------
# Key relationships between Seidel and SRG structure
# ---------------------------------------------------------------------------
# Difference: SEI_EIG_0 - |SEI_EIG_1| = ALPHA
SEI_DIFF_01 = SEI_EIG_0 - abs(SEI_EIG_1)       # = 15-5 = 10
SEI_DIFF_01_SM = SEI_DIFF_01 == ALPHA

# Sum: SEI_EIG_0 + SEI_EIG_2 = 22 = 2*(K-1)  (= line graph valency from CCCVII)
SEI_SUM_02 = SEI_EIG_0 + SEI_EIG_2             # = 15+7 = 22
SEI_SUM_02_SM = SEI_SUM_02 == 2 * (K - 1)

# Sum: SEI_EIG_0 + |SEI_EIG_1| = 2*ALPHA
SEI_SUM_0ABS1 = SEI_EIG_0 + abs(SEI_EIG_1)     # = 15+5 = 20
SEI_SUM_0ABS1_SM = SEI_SUM_0ABS1 == 2 * ALPHA

# Difference: SEI_EIG_2 - |SEI_EIG_1| = LAM
SEI_DIFF_21 = SEI_EIG_2 - abs(SEI_EIG_1)       # = 7-5 = 2
SEI_DIFF_21_SM = SEI_DIFF_21 == LAM


# ---------------------------------------------------------------------------
# Verification engine
# ---------------------------------------------------------------------------
def _chk(name: str, cond: bool) -> dict:
    return {"name": name, "ok": bool(cond)}


def verify_all():
    """Return (checks, passed, total) with exactly 27 checks."""
    checks = [
        # Group 1 — SRG parameters (5)
        _chk("V=40",             V == 40),
        _chk("K=12",             K == 12),
        _chk("EDGES=240",        EDGES == 240),
        _chk("R_EIG=2,S_EIG=-4", R_EIG == 2 and S_EIG == -4),
        _chk("MULT_R=24,MULT_S=15", MULT_R == 24 and MULT_S == 15),

        # Group 2 — Seidel eigenvalue formulae (5)
        _chk("SEI_EIG_0=15",     SEI_EIG_0 == 15),
        _chk("SEI_EIG_1=-5",     SEI_EIG_1 == -5),
        _chk("SEI_EIG_2=7",      SEI_EIG_2 == 7),
        _chk("SEI_SPEC_SUM=0",   SEI_SPEC_SUM == 0),
        _chk("SEI_MULT_SUM=V",   SEI_MULT_SUM == V),

        # Group 3 — Spectral identities (5)
        _chk("SEI_TRACE_SQ_EIG=1560",   SEI_TRACE_SQ_EIG == 1560),
        _chk("SEI_TRACE_SQ_VM=1560",    SEI_TRACE_SQ_VM == 1560),
        _chk("trace_sq_agree",          SEI_TRACE_SQ_EIG == SEI_TRACE_SQ_VM),
        _chk("SEI_EIG0_EQ_MULTS",       SEI_EIG0_EQ_MULTS),
        _chk("MULTS_SUM_VM1",           SEI_MULTS_SUM_VM1),

        # Group 4 — SM encodings (5)
        _chk("SEI_EIG0_SM",     SEI_EIG0_SM),
        _chk("SEI_EIG1_SM",     SEI_EIG1_SM),
        _chk("SEI_EIG2_SM_A",   SEI_EIG2_SM_A),
        _chk("SEI_EIG2_SM_B",   SEI_EIG2_SM_B),
        _chk("trace_sq_SM1=1560", SEI_TRACE_SQ_SM1 == 1560),

        # Group 5 — Seidel–SRG relationships (4)
        _chk("SEI_DIFF_01=ALPHA",       SEI_DIFF_01_SM),
        _chk("SEI_SUM_02=2(K-1)",       SEI_SUM_02_SM),
        _chk("SEI_SUM_0ABS1=2*ALPHA",   SEI_SUM_0ABS1_SM),
        _chk("SEI_DIFF_21=LAM",         SEI_DIFF_21_SM),

        # Group 6 — SM finale (3)
        _chk("trace_sq_SM2=V(V-1)",     SEI_TRACE_SQ_SM2 == 1560),
        _chk("trace_sq_SM1=SM2",        SEI_TRACE_SQ_SM1 == SEI_TRACE_SQ_SM2),
        _chk("SEI_SUM_02=L_VALENCY",    SEI_SUM_02 == 22),
    ]
    passed = sum(1 for c in checks if c["ok"])
    return checks, passed, len(checks)


def build_cccviii_summary() -> dict:
    checks, passed, total = verify_all()
    return {
        "part": "CCCVIII",
        "title": "Seidel Matrix Spectrum of W(3,3)",
        "checks_pass": passed,
        "checks_total": total,
        "status": "PASS" if passed == total else "FAIL",
        "fields": {
            "SEI_EIG_0": SEI_EIG_0,
            "SEI_EIG_1": SEI_EIG_1,
            "SEI_EIG_2": SEI_EIG_2,
            "SEI_MULT_0": SEI_MULT_0,
            "SEI_MULT_1": SEI_MULT_1,
            "SEI_MULT_2": SEI_MULT_2,
            "SEI_SPEC_SUM": SEI_SPEC_SUM,
            "SEI_TRACE_SQ_EIG": SEI_TRACE_SQ_EIG,
            "SEI_TRACE_SQ_VM": SEI_TRACE_SQ_VM,
            "SEI_DIFF_01": SEI_DIFF_01,
            "SEI_SUM_02": SEI_SUM_02,
            "SEI_SUM_0ABS1": SEI_SUM_0ABS1,
            "SEI_DIFF_21": SEI_DIFF_21,
        },
        "discoveries": [
            "SEI_EIG_0=15=ALPHA+GENERATIONS+LAM: Seidel Perron eigenvalue encodes "
            "fine-structure proxy plus generation count plus triangle parameter.",
            "SEI_EIG_0=MULT_S=15: Perron Seidel eigenvalue equals the multiplicity "
            "of the smaller SRG adjacency eigenvalue.",
            "SEI_EIG_1=-5=-(MU+1): The negative Seidel eigenvalue is "
            "determined by the SRG co-degree parameter.",
            "SEI_EIG_2=7=LAM+MU+1=K//2+1: The positive off-Perron eigenvalue "
            "is encoded by the SRG lambda/mu parameters and half the valency.",
            "SEI_SUM_02=22=2(K-1): Sum of two Seidel eigenvalues equals the "
            "line graph valency from Part CCCVII.",
            "tr(S^2)=1560=ALPHA*(V-1)*MU=V*(V-1): Second Seidel moment encodes "
            "fine-structure proxy times V-1 times co-degree.",
            "SEI_DIFF_01=10=ALPHA: Perron minus |smallest| Seidel eigenvalue "
            "returns the fine-structure proxy exactly.",
            "SEI_DIFF_21=2=LAM: The two positive Seidel eigenvalues differ by "
            "exactly the SRG triangle parameter.",
        ],
    }


if __name__ == "__main__":
    checks, passed, total = verify_all()
    print("Passed: " + str(passed) + "/" + str(total))
    for c in checks:
        status = "OK" if c["ok"] else "FAIL"
        print("  [" + status + "] " + c["name"])
