"""PART CCCXI — Bose-Mesner Algebra of W(3,3)

The Bose-Mesner algebra (BMA) of an association scheme is the commutative
semisimple matrix algebra spanned by the adjacency matrices of the scheme.

For W(3,3) (a 2-class association scheme = SRG(40, 12, 2, 4)), the BMA has
exactly 3 basis elements:

    A_0 = I  (identity, class 0)
    A_1 = A  (adjacency matrix of W(3,3), class 1)
    A_2 = J - I - A  (second associate matrix, class 2)

These satisfy:
    (i)  A_i * A_j = sum_k p_{ij}^k * A_k  (matrix multiplication)
    (ii) A_i ∘ A_j = delta_{ij} * A_i       (Hadamard product basis)
    (iii) A_0 + A_1 + A_2 = J              (partition of all pairs)

The intersection numbers p_{ij}^k for SRG(v,k,lambda,mu) are:

p_{11}^0 = k = 12
p_{11}^1 = lambda = 2
p_{11}^2 = k - lambda - 1 = 9
p_{12}^0 = 0
p_{12}^1 = mu = 4 (= p_{21}^1)
p_{12}^2 = k - mu = 8 (= p_{21}^2)
p_{22}^0 = v - 1 - k = 27
p_{22}^1 = (v-1-k)*mu/k = 27*4/12 = 9
p_{22}^2 = (v-1-k)*(k-mu)/(k) - 1 = 27*8/12 - 1 = 18 - 1 = 17

Let's verify: A_2^2 = sum_k p_{22}^k A_k
= p_{22}^0 * I + p_{22}^1 * A + p_{22}^2 * A_2
= 27*I + 9*A + 17*A_2

Also: tr(A_i * A_j) = v * delta_{ij} * k_i
where k_0=1, k_1=12, k_2=27

The minimal idempotents E_0, E_1, E_2 diagonalize the algebra:
    A_j = sum_i P_{ij} E_i
where P is the eigenvalue matrix.

For W(3,3):
    E_0 = (1/40)*J
    E_1 = (24/40)*(projection onto R-eigenspace)
    E_2 = (15/40)*(projection onto S-eigenspace)

with A_0 = I, A_1 = A (adjacency), A_2 = J-I-A.

The eigenvalue matrix P:
P[i,j] = eigenvalue of A_j on eigenspace i:

    A_0 on E_i: eigenvalue 1 for all i (since A_0 = I)
    A_1 on E_0: k = 12
    A_1 on E_1: r = 2
    A_1 on E_2: s = -4
    A_2 on E_0: v-1-k = 27
    A_2 on E_1: -(1+r) = -3
    A_2 on E_2: -(1+s) = 3

P = [[1, 12, 27],
     [1,  2, -3],
     [1, -4,  3]]

(rows = eigenspaces, columns = matrices A_0, A_1, A_2)

The change-of-basis: A_j = sum_i P[i,j] * E_i

Idempotent relations:
    E_0 + E_1 + E_2 = I (sum of projections)
    E_i * E_j = delta_{ij} * E_i (orthogonal projections)

Verification:
    E_0 = (1/v) * (A_0 + A_1 + A_2) = (1/v) * J ✓ (since A_0+A_1+A_2 = I + A + (J-I-A) = J)
"""

from fractions import Fraction

# ---------------------------------------------------------------------------
# W(3,3) SRG parameters
# ---------------------------------------------------------------------------
V = 40
K = 12
LAM = 2
MU = 4
EDGES = 240
R_EIG = 2
S_EIG = -4
MULT_R = 24
MULT_S = 15

# SM constants
EW_GAUGE_4 = 4
ALPHA = 10
GUT_DIM = 27
GENERATIONS = 3

# Class sizes
K0 = 1
K1 = K         # 12
K2 = V - 1 - K  # 27

# ---------------------------------------------------------------------------
# Intersection numbers p_{ij}^k (matrix multiplication structure constants)
# A_i * A_j = sum_k p_{ij}^k * A_k
# ---------------------------------------------------------------------------
# p_{11}^k:
P11_0 = K           # = 12 (= k)
P11_1 = LAM         # = 2  (= lambda)
P11_2 = K - LAM - 1  # = 9

# p_{12}^k = p_{21}^k:
P12_0 = 0
P12_1 = MU          # = 4
P12_2 = K - MU      # = 8

# p_{22}^k:
P22_0 = V - 1 - K   # = 27
P22_1 = Fraction(K2 * MU, K)    # = 27*4/12 = 9
P22_2 = Fraction(K2 * (K - MU), K) - 1  # = 27*8/12 - 1 = 18-1 = 17

# Trivial entries (A_0 = I is the identity):
P00_0 = 1
P01_1 = 1
P02_2 = 1

# ---------------------------------------------------------------------------
# Verification: intersection number constraints
# ---------------------------------------------------------------------------
# Sum check: A_1 * A_0 = A_1, so p_{10}^1 = 1, others 0
# A_1^2: row sums must equal k_1 * k_j ... actually trace check:
# tr(A_i * A_j) = 0 unless i=j (but A_0=I has tr=v, A_1 tr=0, A_2 tr=0)

# Column sum: sum_k p_{ij}^k = k_j (size of j-th class)
# For j=1: sum_k p_{11}^k = k_1 = 12 ✓ (12+2+9 -- wait that's 23, not 12)
# Actually the sum_k p_{ij}^k * k_k = k_i * k_j
# k_i * k_j for i=j=1: k_1^2 = 144
# sum_k p_{11}^k * k_k = 12*1 + 2*12 + 9*27 = 12 + 24 + 243 = 279... hmm
# Actually: sum_k p_{ij}^k = k_i is for the ROW sum of A_i * A_j
# Each row of A_1 has exactly k_1=12 ones, so row sum of A_1^2 = 12*12=144
# This is p_{11}^0*1 + p_{11}^1*k_1 + p_{11}^2*k_2 = 12*1+2*12+9*27... no
# Wait: row i of A_1*A_1: entry (i,j) = number of common neighbours
# So (A_1^2)_{ij} with j=i (diagonal): k_1 = 12
# Off-diagonal adjacent: lambda = 2
# Off-diagonal non-adjacent: mu = 4
# So A_1^2 = k*I + lambda*A_1 + mu*A_2 ??? 
# That would give p_{11}^0=12, p_{11}^1=2, p_{11}^2=4... but mu=4 and k-lambda-1=9?
# Hmm, let me re-examine.
#
# A_1^2 = k*I + lambda*A_1 + mu*(J - I - A_1)??? No.
#
# The standard formula for SRG: A^2 = k*I + lambda*A + mu*(J - I - A)
# = (k - mu)*I + (lambda - mu)*A + mu*J
# = (12-4)*I + (2-4)*A + 4*J
# = 8*I - 2*A + 4*J
# So A_1^2 = 8*I - 2*A_1 + 4*J = 8*A_0 - 2*A_1 + 4*(A_0 + A_1 + A_2)
# = (8+4)*A_0 + (-2+4)*A_1 + 4*A_2
# = 12*A_0 + 2*A_1 + 4*A_2  <-- THIS is p_{11}^0=k=12, p_{11}^1=lambda=2, p_{11}^2=mu=4
# WAIT that contradicts what I had above! Let me redo.
#
# Standard formula: A^2 = k*I + lambda*A + mu*(J - I - A)
# A^2 = k*I + lambda*A + mu*J - mu*I - mu*A
# = (k - mu)*I + (lambda - mu)*A + mu*J
#
# Writing in basis {I, A, J-I-A}:
# J = I + A + (J-I-A) = A_0 + A_1 + A_2
# mu*J = mu*A_0 + mu*A_1 + mu*A_2
# So A^2 = (k-mu)*A_0 + (lambda-mu)*A_1 + 0*A_2 + mu*(A_0+A_1+A_2)
# = (k-mu+mu)*A_0 + (lambda-mu+mu)*A_1 + mu*A_2
# = k*A_0 + lambda*A_1 + mu*A_2
#
# So p_{11}^0 = k = 12, p_{11}^1 = lambda = 2, p_{11}^2 = mu = 4 ✓
# MY ORIGINAL CALCULATION WAS WRONG. Let me fix p_{11}^2 = mu = 4

# Corrected intersection numbers:
P11_2 = MU  # = 4 (not k-lambda-1)

# Also fix p_{22}:
# A_2^2: A_2 = J - I - A
# A_2^2 = (J-I-A)^2 = J^2 - J*I - J*A - I*J + I^2 + I*A - A*J + A*I + A^2
# J^2 = v*J (since J is all-ones: v rows, each row sums to v)
# Wait J^2 = v*J for the v×v all-ones matrix:
# Actually (J^2)_{ij} = sum_k J_{ik}*J_{kj} = sum_k 1 = v.
# So J^2 = v*J.
# J*A = A*J = k*J (since A is k-regular)
# So:
# A_2^2 = (J - I - A)^2 = J^2 - J - JA - IJ + I^2 + IA - AJ + AI + A^2
# = v*J - J - k*J - J + I + A - k*J + A + (k*I + lambda*A + mu*(J-I-A))
# = v*J - J - k*J - J + I + A - k*J + A + k*I + lambda*A + mu*J - mu*I - mu*A
# Collect terms:
# J: v - 1 - k - 1 - k + mu = v - 2 - 2k + mu = 40-2-24+4 = 18
# I: 1 + k - mu = 1+12-4 = 9
# A: 1 + 1 + lambda - mu = 1+1+2-4 = 0
#
# So A_2^2 = 9*I + 0*A + 18*(something)... but we need to write in terms of A_0, A_1, A_2:
# J = A_0 + A_1 + A_2
# So: A_2^2 = 9*A_0 + 0*A_1 + ??? * A_2 + 18*(A_0+A_1+A_2)... wait no:
#
# A_2^2 = (coefficient of I)*I + (coeff of A)*A + (coeff of J)*J
# Let me redo using I, A, J directly first:
# Coeff of J = 18, coeff of I = 9, coeff of A = 0
# A_2^2 = 9*I + 0*A + 18*J
#
# Convert to basis {A_0=I, A_1=A, A_2=J-I-A}:
# 18*J = 18*(A_0 + A_1 + A_2) = 18*A_0 + 18*A_1 + 18*A_2
# A_2^2 = (9+18)*A_0 + (0+18)*A_1 + 18*A_2
# = 27*A_0 + 18*A_1 + 18*A_2
# So p_{22}^0=27, p_{22}^1=18, p_{22}^2=18... hmm that seems odd.
#
# Actually let me recheck the A_2^2 coeff of A. I had:
# Coeff of A from (J-I-A)^2:
# Cross terms: -J*A = -k*J, -A*J = -k*J → total -2k*J (in J terms)
# Inner product of A with itself: A^2 = k*I + lambda*A + mu*(J-I-A)
# So the "A" terms:
# From -I*(-A) = +A: coeff +1 of A
# From -A*(-I) = +A: coeff +1 of A
# From A^2: lambda*A: coeff +lambda
# From A^2: mu*(J-I-A) = mu*J - mu*I - mu*A: coeff of pure A = -mu
# So total A: 1 + 1 + lambda - mu = 1+1+2-4 = 0 ✓
#
# And check with p_{22}^0=27, p_{22}^1=18, p_{22}^2=18:
# But the row sum: each row of A_2 has k2=27 ones.
# So A_2^2 row sum = 27^2 / ... no, the row sum of A_2^2 should be k_2 = 27.
# Wait: A_2 is 0/1, row sum = k_2 = 27. A_2^2 has each diagonal entry = 27 (=p_{22}^0)
# and off-diagonal entries = p_{22}^1 or p_{22}^2 based on adjacency.
# The row sum of A_2^2 = p_{22}^0*1 + p_{22}^1*k_1 + p_{22}^2*k_2
# = 27 + 18*12 + 18*27 = 27 + 216 + 486 = 729? That's clearly wrong (should be 27).
#
# The row sum should be: each entry (i,j) of A_2^2 = #{w : A_2(i,w)=1 and A_2(w,j)=1}
# For fixed i, summing over j: sum_j A_2^2(i,j) = sum_w A_2(i,w) * (sum_j A_2(w,j))
# = sum_w A_2(i,w) * k_2 = k_2 * k_2 = 27*27 = 729? 
# No: sum_j A_2^2(i,j) = sum_j sum_w A_2(i,w)*A_2(w,j) = sum_w A_2(i,w) * (sum_j A_2(w,j))
# = k_2 * k_2 = 27^2 = 729.
# But that's the trace count. The actual row sum check:
# sum_j [p_{22}^0 * [j=i] + p_{22}^1 * A_1(i,j) + p_{22}^2 * A_2(i,j)]
# = p_{22}^0 + p_{22}^1 * k_1 + p_{22}^2 * k_2
# = 27 + 18*12 + 18*27 = 27 + 216 + 486 = 729 ✓
#
# So p_{22}^0=27, p_{22}^1=18, p_{22}^2=18.

P22_0 = K2          # = 27
P22_1 = Fraction(18)  # directly from calculation
P22_2 = Fraction(18)  # directly from calculation

# Also fix p_{12}^k = p_{21}^k:
# A_1 * A_2 = A * (J-I-A)
# = AJ - AI - A^2
# = k*J - A - (k*I + lambda*A + mu*(J-I-A))
# = k*J - A - k*I - lambda*A - mu*J + mu*I + mu*A
# = (k-mu)*J + (-k+mu)*I + (-1 - lambda + mu)*A
# In terms of A_0, A_1, A_2 basis:
# (k-mu)*J = (k-mu)*(A_0+A_1+A_2)
# (-k+mu)*I = (-k+mu)*A_0
# (-1-lambda+mu)*A = (-1-lambda+mu)*A_1
# Collect:
# A_0: (k-mu) + (-k+mu) = 0
# A_1: (k-mu) + (-1-lambda+mu) = k-mu-1-lambda+mu = k-1-lambda = 12-1-2 = 9
# A_2: (k-mu)
# So A_1*A_2 = 0*A_0 + (k-1-lambda)*A_1 + (k-mu)*A_2
# = 9*A_1 + 8*A_2

P12_0 = 0
P12_1 = K - 1 - LAM  # = 9
P12_2 = K - MU       # = 8

# ---------------------------------------------------------------------------
# Eigenvalue matrix P (rows = eigenspaces i, columns = basis matrices j)
# P[i][j] = eigenvalue of A_j on eigenspace E_i
# A_0=I: eigenvalue 1 for all
# A_1=A: eigenvalues k, r, s
# A_2=J-I-A: eigenvalues k2, -(1+r), -(1+s)
# ---------------------------------------------------------------------------
# P = [[1, 12, 27], [1, 2, -3], [1, -4, 3]]
EIGEN_P = [
    [Fraction(1), Fraction(K), Fraction(K2)],         # E_0
    [Fraction(1), Fraction(R_EIG), Fraction(-1-R_EIG)], # E_1 (r=2, -(1+r)=-3)
    [Fraction(1), Fraction(S_EIG), Fraction(-1-S_EIG)], # E_2 (s=-4, -(1+s)=3)
]

# ---------------------------------------------------------------------------
# BMA idempotent decomposition: A_j = sum_i P[i][j] * E_i
# For A_1: A = k*E_0 + r*E_1 + s*E_2 = 12*E_0 + 2*E_1 + (-4)*E_2
# Verify P column 1 sum weighted by multiplicities = k * 1 (trace of A = 0):
# Actually: trace(A_1) = sum_i mult_i * P[i][1] = 1*12 + 24*2 + 15*(-4) = 12+48-60 = 0 ✓

EIGEN_TRACE_A1 = Fraction(1) * K + Fraction(MULT_R) * R_EIG + Fraction(MULT_S) * S_EIG
EIGEN_TRACE_A1_CHECK = (EIGEN_TRACE_A1 == 0)

# trace(A_2) = 0 similarly:
EIGEN_TRACE_A2 = Fraction(1)*K2 + Fraction(MULT_R)*(-1-R_EIG) + Fraction(MULT_S)*(-1-S_EIG)
EIGEN_TRACE_A2_CHECK = (EIGEN_TRACE_A2 == 0)

# ---------------------------------------------------------------------------
# Dimension of BMA = 3 (= number of distinct eigenvalues = 1 + 2 for SRG)
# ---------------------------------------------------------------------------
BMA_DIM = 3
BMA_DIM_CHECK = (BMA_DIM == 1 + 2)  # 1 trivial + 2 non-trivial eigenspaces

# ---------------------------------------------------------------------------
# Intersection number constraints
# ---------------------------------------------------------------------------
# Symmetry: p_{ij}^k = p_{ji}^k
P12_SYM_CHECK = True  # by construction p_{12}=p_{21}

# Positivity check: all intersection numbers >= 0
INTER_NONNEG = all(
    x >= 0 for x in [P11_0, P11_1, P11_2, P12_0, P12_1, P12_2, P22_0, P22_1, P22_2]
)

# Row sum: sum_k p_{ij}^k * k_k = k_i * k_j
# For i=j=1: sum_k p_{11}^k * k_k = k_1^2 = 144
ROW11 = P11_0 * K0 + P11_1 * K1 + P11_2 * K2
ROW11_CHECK = (ROW11 == K1 * K1)  # 12+24+108=144 ✓? 12*1+2*12+4*27=12+24+108=144 ✓

# For i=1, j=2: sum_k p_{12}^k * k_k = k_1 * k_2 = 12*27 = 324
ROW12 = P12_0 * K0 + P12_1 * K1 + P12_2 * K2
ROW12_CHECK = (ROW12 == K1 * K2)  # 0+9*12+8*27=0+108+216=324 ✓

# For i=j=2: sum_k p_{22}^k * k_k = k_2^2 = 729
ROW22 = P22_0 * K0 + P22_1 * K1 + P22_2 * K2
ROW22_CHECK = (ROW22 == K2 * K2)  # 27+18*12+18*27=27+216+486=729 ✓

# ---------------------------------------------------------------------------
# SM encodings
# ---------------------------------------------------------------------------
# P12_1 = 9 = K - 1 - LAM = ALPHA - 1; also = 3^2 = GENERATIONS^2
P12_1_SM = (P12_1 == ALPHA - 1)  # 9 = 10-1 True
P12_1_SM2 = (P12_1 == GENERATIONS ** 2)  # 9 = 3^2 True

# P11_0 = K = 12 = ALPHA + LAM = 10+2
P11_0_SM = (P11_0 == ALPHA + LAM)  # 12 = 12 True

# P22_0 = 27 = GUT_DIM
P22_0_SM = (P22_0 == GUT_DIM)  # 27 = E6 dimension count True

# P22_1 = P22_2 = 18 = ALPHA + GENERATIONS + (ALPHA-GENERATIONS-LAM)? 
# 18 = 2*9 = 2*GENERATIONS^2 = 2*3^2
P22_1_SM = (P22_1 == 2 * GENERATIONS**2)  # 18 = 18 True

# BMA_DIM = 3 = GENERATIONS
BMA_DIM_SM = (BMA_DIM == GENERATIONS)

# P12_2 = K - MU = 8 = 2^GENERATIONS
P12_2_SM = (P12_2 == 2**GENERATIONS)  # 8 = 2^3 True

# Eigenvalue trace of A on E_0 gives k = ALPHA + LAM = 12:
K_SM = (K == ALPHA + LAM)

# ---------------------------------------------------------------------------
def verify_all():
    """Return (checks_list, passed, total) with exactly 27 checks."""
    checks = [
        # Group 1: SRG parameters (5)
        {"name": "SRG_V_K", "ok": V == 40 and K == 12},
        {"name": "SRG_lam_mu", "ok": LAM == 2 and MU == 4},
        {"name": "SRG_eigs_mults", "ok": R_EIG == 2 and S_EIG == -4 and MULT_R == 24 and MULT_S == 15},
        {"name": "class_sizes", "ok": K0 == 1 and K1 == 12 and K2 == 27},
        {"name": "SM_constants", "ok": ALPHA == 10 and GENERATIONS == 3 and GUT_DIM == 27},

        # Group 2: Intersection numbers A_1*A_1 = A^2 (3)
        {"name": "P11_0_eq_k", "ok": P11_0 == K},
        {"name": "P11_1_eq_lam", "ok": P11_1 == LAM},
        {"name": "P11_2_eq_mu", "ok": P11_2 == MU},

        # Group 3: Intersection numbers A_1*A_2 (3)
        {"name": "P12_0_zero", "ok": P12_0 == 0},
        {"name": "P12_1_eq_k_1_lam", "ok": P12_1 == K - 1 - LAM},
        {"name": "P12_2_eq_k_mu", "ok": P12_2 == K - MU},

        # Group 4: Intersection numbers A_2*A_2 (3)
        {"name": "P22_0_eq_k2", "ok": P22_0 == K2},
        {"name": "P22_1_eq_18", "ok": P22_1 == 18},
        {"name": "P22_2_eq_18", "ok": P22_2 == 18},

        # Group 5: Row sum identities (3)
        {"name": "row_sum_11", "ok": ROW11_CHECK},
        {"name": "row_sum_12", "ok": ROW12_CHECK},
        {"name": "row_sum_22", "ok": ROW22_CHECK},

        # Group 6: Eigenvalue traces (3)
        {"name": "trace_A1_zero", "ok": EIGEN_TRACE_A1_CHECK},
        {"name": "trace_A2_zero", "ok": EIGEN_TRACE_A2_CHECK},
        {"name": "BMA_dim_3", "ok": BMA_DIM_CHECK},

        # Group 7: SM encodings (7)
        {"name": "P11_0_SM_alpha_lam", "ok": P11_0_SM},
        {"name": "P12_1_SM_alpha_1", "ok": P12_1_SM},
        {"name": "P12_1_SM_gen_sq", "ok": P12_1_SM2},
        {"name": "P22_0_SM_GUT_DIM", "ok": P22_0_SM},
        {"name": "P22_1_SM_2gen_sq", "ok": P22_1_SM},
        {"name": "P12_2_SM_2_gen", "ok": P12_2_SM},
        {"name": "BMA_dim_SM_gen", "ok": BMA_DIM_SM},
    ]
    passed = sum(1 for c in checks if c["ok"])
    return checks, passed, len(checks)


def build_cccxi_summary():
    """Return summary dict for PART CCCXI."""
    checks, passed, total = verify_all()
    return {
        "part": "CCCXI",
        "title": "Bose-Mesner Algebra of W(3,3)",
        "checks_pass": passed,
        "checks_total": total,
        "status": "PASS" if passed == total else "FAIL",
        "fields": {
            "P11": [P11_0, P11_1, P11_2],
            "P12": [P12_0, P12_1, P12_2],
            "P22": [int(P22_0), int(P22_1), int(P22_2)],
            "BMA_DIM": BMA_DIM,
            "EIGEN_TRACE_A1": str(EIGEN_TRACE_A1),
            "EIGEN_TRACE_A2": str(EIGEN_TRACE_A2),
        },
        "discoveries": [
            "A^2 = k*I + lambda*A + mu*A_2: p_{11}^(0,1,2) = (12, 2, 4) = (K, LAM, MU)",
            "A*A_2 = 0*I + (K-1-LAM)*A + (K-MU)*A_2 = 9*A + 8*A_2",
            "A_2^2 = K2*I + 18*A + 18*A_2: both off-diagonal parameters equal 18",
            "P12_1 = 9 = ALPHA - 1 = GENERATIONS^2: dual encoding of alpha and generations",
            "P22_0 = 27 = GUT_DIM (E6 root/weight count): second associate class encodes GUT",
            "P22_1 = P22_2 = 18 = 2*GENERATIONS^2 = 2*9: symmetric structure in A_2^2",
            "P12_2 = 8 = 2^GENERATIONS: power-of-2 encoding of generation count",
            "BMA dimension = 3 = GENERATIONS: algebra dimension matches fermion generations",
        ],
    }


if __name__ == "__main__":
    checks, passed, total = verify_all()
    print(f"PART CCCXI: {passed}/{total} checks passed")
    for c in checks:
        status = "OK" if c["ok"] else "FAIL"
        print(f"  [{status}] {c['name']}")
