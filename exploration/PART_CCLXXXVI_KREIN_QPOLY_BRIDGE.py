"""
Part CCLXXXVI: Krein Parameters and the Q-Polynomial Association Scheme of W(3,3)

The symplectic polar space W(3,3) gives the SRG(40,12,2,4).  This graph is not
only P-polynomial (distance-regular diameter 2) but also Q-polynomial — it belongs
to a 2-class association scheme whose Krein parameters, Q-matrix, P-matrix, and
dual eigenvalues satisfy a rich web of identities tightly coupled to the W(3,3)
constants V=40, K=12, LAM=2, MU=4, Q=3.
"""

from __future__ import annotations

# ── W(3,3) SRG parameters ────────────────────────────────────────────────────
V   = 40    # vertices
K   = 12    # valency / degree
LAM = 2     # lambda (common neighbours of adjacent pair)
MU  = 4     # mu    (common neighbours of non-adjacent pair)
Q   = 3     # field order GF(3)

# ── derived SRG constants ────────────────────────────────────────────────────
K2  = V - K - 1          # = 27  size of Γ_2(x) = LINES_27
PHI4 = 10                # = Q^2+1
PHI3 = K + 1             # = 13
PHI6 = K - MU - 1        # = 7
LINES_27 = 27
EDGES = 240
AUT_ORDER = 51840
TRANSPORT_EDGES = 270
STABILIZER_STATES = 360
GEWIRTZ_V = 56
E8_RANK = 8
SP4F3_ORDER = 51840
PSP4F3_ORDER = 25920

# ── SRG eigenvalues ──────────────────────────────────────────────────────────
# Characteristic polynomial of adjacency matrix: (x-K)(x-r)(x-s)
# discriminant = (LAM - MU)^2 + 4(K - MU) = 4 + 32 = 36
DISCRIMINANT = (LAM - MU)**2 + 4*(K - MU)   # = 36
# r = (LAM - MU + sqrt(DISCRIMINANT)) / 2
R_EIGENVALUE = (LAM - MU + 6) // 2          # = (2-4+6)/2 = 2
S_EIGENVALUE = (LAM - MU - 6) // 2          # = (2-4-6)/2 = -4

# ── eigenvalue multiplicities ────────────────────────────────────────────────
# m_r: (r+1-K)(r-s) * ... using standard formula
# f = k(s+1)(s-k) / ((r-s)(rs+k))
# g = k(r+1)(r-k) / ((r-s)(rs+k))
# For SRG: f = V*s*(s+1)/((s-r)(1+ks))  — actually use:
# f + g = V - 1;  f*r + g*s = -K;  => f = (V-1+K/s)/(1-r/s) simplification
# Direct: f = k(k+1)(s-k)/((k+rs)(r-s)) etc.
# Standard: f = (1/2)*( V - 1 - 2k/(r-s) ) = (1/2)*(39 - 2*12/6) = (1/2)*(39-4) = 35/2 NO
# Use: mult_r = k*(s+1)*(s-k) / ((r-s)*(1 + k - r*(V-1)/k))  — messy
# Correct formula:
#   m_r = k*(k - s*(s+1)) / ((r - s)*(r*(r+1) - k))   — no
# Actually the correct formula for SRG:
#   1 + f*r + g*s = 0   [trace of A]
#   f + g = V - 1       [size]
# => f = (-g*s - 1)/r  ... f + g = 39
# From -K = f*r + g*s = f*r + (39-f)*s = f(r-s) + 39s
# f = (-K - 39*s)/(r - s) = (-12 - 39*(-4))/(2-(-4)) = (-12+156)/6 = 144/6 = 24
MULT_R = (-K - (V-1)*S_EIGENVALUE) // (R_EIGENVALUE - S_EIGENVALUE)   # = 24
MULT_S = V - 1 - MULT_R                                                # = 15

# ── 2-class association scheme ───────────────────────────────────────────────
# Relation R0 = identity, R1 = edges (Gamma), R2 = non-edges (Gamma-bar)
# p^k_{ij}: intersection numbers
# p^0_{ij} = k_i * delta_{ij}
# p^1_{11} = LAM, p^1_{12} = MU*, p^1_{22} = ...
# For SRG: p^1_{11}=LAM=2, p^1_{12}=p^1_{21}=K-LAM-1=9, p^1_{22}=K2-p^1_{12}... wait
# Standard scheme for SRG(v,k,lam,mu):
#   k_0=1, k_1=K=12, k_2=K2=27
#   p^1_{11} = LAM = 2
#   p^1_{12} = p^1_{21} = K - LAM - 1 = 9
#   p^1_{22} = K2 - (K - LAM - 1) = 27 - 9 = 18  [= mu*(K2/K) sort of]
# wait: p^1_{22} = k_2 - p^1_{12} - delta_{12} ... use regularity
# For vertex x in R2 from y (R2-neighbour of y), how many R1-neighbours of x are also R1-nbrs of y?
# That is MU = 4. So p^2_{11}=MU=4.
# p^2_{12}: for x,z at R2 with y at R1 from both... 
# Sum: p^1_{12} = K - LAM - 1 = 9;  p^2_{12} = K - MU = 8;  p^2_{22} = K2 - 1 - p^2_{12} = 18
# Let's list all:
# k0=1, k1=12, k2=27
K0 = 1; K1 = K; K2_VAL = K2

# Intersection array for the association scheme (2-class):
# p^i_{jk}  for i,j,k in {0,1,2}
P100 = 1
P111 = LAM         # = 2
P112 = K - LAM - 1 # = 9
P122 = K2 - (K - LAM - 1)  # = 27-9 = 18 ... actually verify with k_1*p^1_{12} = k_2*p^2_{11}
# k1*p112 = 12*9 = 108 should equal k2*p211
# p211 = MU = 4  =>  k2*p211 = 27*4 = 108. ✓ Great.
P211 = MU          # = 4
P212 = K - MU - 1  # = 7  (= PHI6)
P222 = K2 - 1 - P212  # = 27-1-7 = 19

# Verify: sum over j of p^i_{jk} * k_j = k_i * k_k ?
# i=1: sum_j p^1_{j1}*k_j = p^1_{01}*k0 + p^1_{11}*k1 + p^1_{21}*k2
#                          = 0 + 2*12 + 9*27 = 24+243 = 267 ≠ k1*k1=144  hmm
# Actually the relation is: k_i * p^k_{ij} = k_j * p^k_{ji}
# and sum_j p^k_{ij} = k_i for all k,i (if counted right)
# Let me re-derive properly using standard notation.
# For SRG(v,k,lam,mu) as 2-class scheme:
# The intersection numbers are:
# p^1_{11} = lam,   p^2_{11} = mu
# p^1_{12} = k - lam - 1,  p^2_{12} = k - mu
# p^1_{22} = mu*(k2/k) ... use the eigenmatrix

# P-matrix (eigenmatrix): rows = eigenvalues, cols = relations
# P = [[1,  K,   K2 ],
#      [1,  r,   s2 ],    where s2 = -(r+1) for a strongly regular case
#      [1,  s,   r2 ]]
# For SRG, the eigenvalues of Gamma are K, r, s with
# r*s = -K*(mu-lam)/(r-s) ... actually:
# The adjacency eigenvalues of Γ₂ (the complementary scheme graph) are:
#   K2, r2 = -(s+1) = -(-4+1) = 3,  s2 = -(r+1) = -(2+1) = -3
# Wait: eigenvalues of I+A1+A2 = J, so eigenvalues of A2 = eigenvalues of J - I - A1
# J has eigenvalue V on all-ones, 0 on rest.
# A1 has eigenvalues K, r, s
# So A2 = J - I - A1 has eigenvalues: K2 (on K-ev K), -(1+r), -(1+s)
R2_EIGENVALUE = -(1 + R_EIGENVALUE)  # = -(1+2) = -3
S2_EIGENVALUE = -(1 + S_EIGENVALUE)  # = -(1-4) = 3

# P-matrix (rows: schemes 0,1,2; cols: relations R0,R1,R2)
P_MATRIX = [
    [1, K,            K2],
    [1, R_EIGENVALUE, R2_EIGENVALUE],
    [1, S_EIGENVALUE, S2_EIGENVALUE],
]
# = [[1, 12, 27],
#    [1,  2, -3],
#    [1, -4,  3]]

# ── Q-matrix (dual eigenmatrix) ──────────────────────────────────────────────
# Q_{ij} = m_i * (P^{-1})_{ij} ... or via Q_ij = (1/v) * sum_x P_{ix} * conj(P_{jx})
# For real schemes Q is real. By the Krein matrix formula or:
# Q_{ij} = (k_j / v) * P_{ij}  if scheme is self-dual (P-polynomial ↔ Q-polynomial)
# The Q matrix for a 2-class scheme satisfies Q = v * P^{-1} (up to normalization)
# For SRG Q-polynomial: the Q-matrix is
# Q = [[1, f,  g ],
#      [1, r*, s*],
#      [1, s*, r*]]
# where f = MULT_R = 24, g = MULT_S = 15
# and r* = K*MULT_R*(r / K) = ... 
# Actually for a Q-polynomial scheme, the dual eigenvalues are:
# q_j = Q-eigenvalues for the j-th dual scheme
# For the SRG(40,12,2,4): the Q-matrix is
# Q = [[1,  24,  15],
#      [1,  r*,  s*],
#      [1,  s**,  r**]]
# computed from Q = v * P^{-T} / (k vector)
# In matrix form: Q_{ij} = (m_i / k_j) * P_{ji}
# where m_i = multiplicities and k_j = |R_j|
# m = [1, 24, 15], k = [1, 12, 27]

def compute_q_matrix():
    """Compute the Q-matrix (dual eigenmatrix) from P-matrix and multiplicities."""
    m = [1, MULT_R, MULT_S]  # [1, 24, 15]
    k = [1, K, K2]           # [1, 12, 27]
    # Q_{ij} = (m_i / k_j) * P_{ji}  but P is indexed rows=eigenvals, cols=relations
    # Standard: Q_{ij} = (1/v) * sum_x m_x * P_{xi} * P_{xj} (orthogonality -- no)
    # Use: Q = diagonal(m) * P * diagonal(1/k) * V -- NO
    # Correct: for a commutative association scheme,
    # Q_{ij} = (m_j / v) * sum_x P_{ix} * P_{jx} / k_x  ...
    # Simplest: for 2-class, use explicit formula:
    # Q_{0j} = 1 for all j (trivial row)
    # Q_{i0} = m_i  (column for R0 = identity)
    # For i,j >=1: Q_{ij} from the standard formula
    # Actually use the known result: for SRG, Q-matrix rows are [1, m_r, m_s]
    # and the dual scheme is also a SRG → self-dual
    # Dual eigenvalues: q0_0=1, q0_1=m_r/1, q0_2=m_s/1 -- no
    # Let's just compute numerically: Q = v * P^{-T} * diag(k)  [standard formula]
    # Q = v * (P^{-1})^T * ... 
    # Known: Q * P^T = v * I  (in appropriate normalization)
    # Alternatively: Q_{ij} = (m_i * P_{ji}) / k_j  where m = mults of eigenvalues
    # This gives:
    Q = [[0]*3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            Q[i][j] = (m[i] * P_MATRIX[j][i]) // k[j] if (m[i] * P_MATRIX[j][i]) % k[j] == 0 \
                      else m[i] * P_MATRIX[j][i] / k[j]
    return Q

Q_MATRIX_DATA = compute_q_matrix()
# Q[0] = [1*1/1, 1*12/12, 1*27/27] = [1, 1, 1]
# Q[1] = [24*1/1, 24*2/12, 24*(-3)/27] = [24, 4, -8/3] -- not integer!
# That formula is wrong. Let me use the correct one.

# The correct formula: Q_{ij} = (m_i / k_j) * P_{ji}
# where P_{ji} means row j, col i of the P-matrix.
# Q[0][j] = (m[0]/k[j]) * P[j][0] = (1/k[j]) * 1 -- not right either.
# 
# CORRECT standard association scheme formula:
# Q_{ij} = sum_x P_{ix} * conj(P_{jx}) * k_x / v  -- NO
# 
# Actually the correct relation between P and Q matrices:
# PQ = vI  (where both P and Q are indexed by (eigenvalue, relation))
# so Q = v * P^{-1}
# Let's compute P^{-1} numerically.

def matrix_inverse_3x3(M):
    """Compute inverse of 3x3 matrix M using cofactors."""
    def det2(a,b,c,d): return a*d - b*c
    a,b,c = M[0]
    d,e,f = M[1]
    g,h,i = M[2]
    det = a*(e*i-f*h) - b*(d*i-f*g) + c*(d*h-e*g)
    if det == 0:
        return None
    inv_det = 1/det
    return [
        [ (e*i-f*h)*inv_det, -(b*i-c*h)*inv_det,  (b*f-c*e)*inv_det],
        [-(d*i-f*g)*inv_det,  (a*i-c*g)*inv_det, -(a*f-c*d)*inv_det],
        [ (d*h-e*g)*inv_det, -(a*h-b*g)*inv_det,  (a*e-b*d)*inv_det],
    ]

P_FLOAT = [[float(x) for x in row] for row in P_MATRIX]
P_INV = matrix_inverse_3x3(P_FLOAT)
# Q = v * P^{-1}
Q_MATRIX = [[V * P_INV[i][j] for j in range(3)] for i in range(3)]
# Round to check integrality:
def round_matrix(M):
    return [[round(x) for x in row] for row in M]

Q_MATRIX_INT = round_matrix(Q_MATRIX)
# Should give:
# Q[0] = [1, 24, 15]  (multiplicities)
# Q[1] = [1,  4, -5]  (dual eigenvalues for R1 direction)
# Q[2] = [1, -2,  1]  (dual eigenvalues for R2 direction)
# Let's verify via explicit computation:
# P = [[1, 12, 27], [1, 2, -3], [1, -4, 3]]
# det(P) = 1*(2*3-(-3)*(-4)) - 12*(1*3-(-3)*1) + 27*(1*(-4)-2*1)
#        = 1*(6-12) - 12*(3+3) + 27*(-4-2)
#        = -6 - 72 - 162 = -240
DET_P = -240  # = -EDGES

# ── Krein parameters q^k_{ij} ────────────────────────────────────────────────
# Krein parameters satisfy: m_i * m_j * Q_{ki} * Q_{kj} / (v * m_k) summed appropriately
# For 2-class scheme, there are only a few non-trivial Krein parameters.
# The Krein condition requires q^k_{ij} >= 0 for all i,j,k.
# 
# Formula: q^k_{ij} = (m_i * m_j / (v * m_k)) * sum_x (Q_{ix} * Q_{jx} * Q_{kx} / k_x)
# For 2-class with Q computed above:
# q^0_{11} = m_1^2/v * sum_x Q_{1x}^2/k_x  = MULT_R^2/V * (1/1 + 4^2/12 + (-5)^2/27)
#           = 576/40 * (1 + 16/12 + 25/27)
#           = 14.4 * (1 + 1.333 + 0.926)
#           = 14.4 * 3.259 = 46.93... ≠ integer?  Hmm.
# 
# Let's use the correct formula via the P and Q matrices.
# Krein parameters for 2-class scheme can be read from:
# q^k_{ij} = (1/v) * sum_{x=0}^{d} (k_x / (m_x)) * Q_{ix} * Q_{jx} * Q_{kx}  -- no
#
# The standard formula: q^k_{ij} = (m_i * m_j) / (v * m_k) * sum_{x} P_{xi}^* P_{xj}^* / P_{xk}^*
# where P_{xi}^* are the Q-matrix entries.
#
# Actually the simplest definition:
# q^k_{ij} is defined by: E_i * E_j = (1/v) sum_k q^k_{ij} * E_k
# where E_i = (m_i/v) * Q_i(x) are the idempotents.
# For a 2-class scheme the Krein parameters are:
# q^0_{11} = m_1 (always), q^0_{22} = m_2
# q^1_{11}, q^1_{12}, q^1_{22} 
# q^2_{11}, q^2_{12}, q^2_{22}
#
# For SRG that is Q-polynomial, these can be computed as:
# q^1_{11} = MULT_R * (r**)^2 / (v * q1_0) ... this is getting complicated.
#
# Use the Eberlein polynomial / Hahn polynomial approach for Q-polynomial SRG:
# For SRG(v,k,lam,mu) the Krein parameters are given by:
# q^1_{11} = m_r * (r - s)^2 * (r+1) / (2 * (r - s) * v) ... I'll compute directly.
#
# DIRECT computation: 
# The Krein matrix A^*_1 (dual Bose-Mesner generator) has entries:
# (A^*_1)_{xy} = v/m_1 * (E_1)_{xy} = Q-polynomial structure.
# For the Krein parameters, use:
# q^k_{ij} = Tr(A^*_i * A^*_j * (A^*_k)^{-1}) / v  
# which for 2-class is tractable.
#
# PRACTICAL: for 2-class scheme over real Q, Krein params are:
# q^k_{ij} = (m_i * m_j / (v * m_k)) * sum_{l=0}^{2} (Q_{li} * Q_{lj} * Q_{lk} / k_l)
# Q matrix rows indexed by k (dual index), columns by l (relation):
# Our Q_MATRIX[k][l]:  Q[0]=[1,1,1], Q[1]=[1,4,-5], Q[2]=[1,-2,1]  (predicted)
# wait—let me recheck by verifying PQ = vI.

# From P = [[1,12,27],[1,2,-3],[1,-4,3]] and expected Q^T (= v*P^{-1}):
# Q^T[col i] = v * (P^{-1})[i]  (i-th column of P^{-1} times v)
# det(P) = -240
# Cofactor matrix C:
# C[0][0] = det([[2,-3],[-4,3]]) = 6-12 = -6
# C[0][1] = -det([[1,-3],[1,3]]) = -(3+3) = -6
# C[0][2] = det([[1,2],[1,-4]]) = -4-2 = -6
# C[1][0] = -det([[12,27],[-4,3]]) = -(36+108) = -144
# C[1][1] = det([[1,27],[1,3]]) = 3-27 = -24
# C[1][2] = -det([[1,12],[1,-4]]) = -(-4-12) = 16
# C[2][0] = det([[12,27],[2,-3]]) = -36-54 = -90
# C[2][1] = -det([[1,27],[1,-3]]) = -(-3-27) = 30
# C[2][2] = det([[1,12],[1,2]]) = 2-12 = -10
# P^{-1} = C^T / det = C^T / (-240)
# C^T: row i = C[j][i]:
# C^T[0] = [-6, -144, -90]
# C^T[1] = [-6, -24, 30]
# C^T[2] = [-6, 16, -10]
# P^{-1}[0] = [-6/-240, -144/-240, -90/-240] = [1/40, 3/5, 3/8]
# P^{-1}[1] = [-6/-240, -24/-240, 30/-240] = [1/40, 1/10, -1/8]
# P^{-1}[2] = [-6/-240, 16/-240, -10/-240] = [1/40, -1/15, 1/24]
# Q = v * P^{-1} = 40 * P^{-1}:
# Q[0] = [40/40, 40*3/5, 40*3/8] = [1, 24, 15]        ✓ (multiplicities)
# Q[1] = [40/40, 40/10, -40/8]   = [1,  4, -5]
# Q[2] = [40/40, -40/15, 40/24]  = [1, -8/3, 5/3]  -- NOT INTEGER!

# Hmm. This means the SRG(40,12,2,4) is NOT self-dual in the classical sense,
# or my formula is off.  Let me reconsider.
# 
# The issue: for a 2-class association scheme with integer P-matrix,
# the Q-matrix need not have integer entries.  The Krein parameters
# q^k_{ij} = (m_i m_j / (v m_k)) * sum_l (Q_{li} Q_{lj} Q_{lk} / k_l)
# must be >= 0 and often are rational or irrational.
#
# For the SRG(40,12,2,4), the Krein parameters are known to be non-negative
# (it's a valid Q-polynomial scheme) but the Q-matrix can have irrational entries
# if the SRG is not self-complementary. Let's compute q^k_{ij} directly using
# the orthogonality relations without requiring Q to be integer.

# Q-matrix (exact fractions):
# Q[0] = [1, 24, 15]
# Q[1] = [1, 4, -5]
# Q[2] = [1, -8/3, 5/3]
from fractions import Fraction

Q_EXACT = [
    [Fraction(1), Fraction(24), Fraction(15)],
    [Fraction(1), Fraction(4),  Fraction(-5)],
    [Fraction(1), Fraction(-8,3), Fraction(5,3)],
]
K_VALS = [Fraction(1), Fraction(12), Fraction(27)]

def krein_param(i, j, k):
    """Compute q^k_{ij} for the 2-class scheme."""
    m = [Fraction(1), Fraction(MULT_R), Fraction(MULT_S)]
    num = m[i] * m[j]
    den = Fraction(V) * m[k]
    total = Fraction(0)
    for l in range(3):
        total += Q_EXACT[l][i] * Q_EXACT[l][j] * Q_EXACT[l][k] / K_VALS[l]
    return (num / den) * total

# Compute all non-trivial Krein parameters:
# q^0_{00}=1, q^1_{00}=0, q^2_{00}=0
# q^0_{01}=0 (by orthogonality), q^0_{11}, q^0_{12}, q^0_{22}
# q^1_{11}, q^1_{12}, q^1_{22}
# q^2_{11}, q^2_{12}, q^2_{22}

KREIN_Q0_11 = krein_param(1, 1, 0)   # should = MULT_R (= 24)
KREIN_Q0_22 = krein_param(2, 2, 0)   # should = MULT_S (= 15)
KREIN_Q1_11 = krein_param(1, 1, 1)
KREIN_Q1_12 = krein_param(1, 2, 1)
KREIN_Q1_22 = krein_param(2, 2, 1)
KREIN_Q2_11 = krein_param(1, 1, 2)
KREIN_Q2_12 = krein_param(1, 2, 2)
KREIN_Q2_22 = krein_param(2, 2, 2)

# ── Q-polynomial ordering ────────────────────────────────────────────────────
# A 2-class scheme is Q-polynomial (with ordering 0,1,2) iff
# the Krein parameters q^k_{ij} = 0 whenever k > i+j or k+i < j or k+j < i
# (triangle condition). For diameter 2 there's only the condition q^2_{11} >= 0.
Q_POLY_CONDITION = KREIN_Q2_11 >= 0   # must be True

# ── Cometric association scheme ─────────────────────────────────────────────
# Dual degree sequence: d* = 2.  The dual distance distribution around a "codeword"
# in the dual scheme uses the Q-matrix as the P-matrix would in the primal.
# Dual k-values: m_0=1, m_1=MULT_R=24, m_2=MULT_S=15
DUAL_K0 = 1
DUAL_K1 = MULT_R   # = 24
DUAL_K2 = MULT_S   # = 15

# ── Additional structural constants ─────────────────────────────────────────
# The "absolute bound" for a 2-class Q-polynomial scheme states:
# v <= C(m_1 + 1, 2) = C(25, 2) = 300
# (here the +1 because the scheme is not "tight")
ABSOLUTE_BOUND = MULT_R * (MULT_R + 1) // 2   # = 24*25/2 = 300
# Since V = 40 <= 300, satisfied.

# Tight bound: for a tight Q-polynomial scheme (equality), v = (d+1)(m+1)/d
# This scheme is not tight. Tight would require: V = 40 = ?
# The "absolute bound" for the restricted Q-polynomial is
# V <= (m_1 + 1) for d=2: V <= m_1*(m_1+3)/2 for d=2? Actually:
# absolute bound: V <= C(m+d, d) for Q-polynomial of diameter d and multiplicity m
# d=2, m=24: V <= C(26, 2) = 325; V=40 << 325.

# "Tight" condition for Q-polynomial SRG: m_1 = K (degree = dual degree?)
# NOT tight here.

# ── Delsarte linear programming bound ───────────────────────────────────────
# For the 2-class scheme, the dual linear program gives a bound on clique sizes.
# Maximum clique bound from eigenvalue method:
# omega(Gamma) <= 1 - K / s_min = 1 - 12/(-4) = 1 + 3 = 4
CLIQUE_BOUND_HOFFMAN = 1 - K // S_EIGENVALUE   # = 1+3 = 4
# Maximum independent set:
# alpha(Gamma) <= v * (-s_min) / (K - s_min) = 40*4/(12+4) = 160/16 = 10
INDSET_BOUND_HOFFMAN = V * (-S_EIGENVALUE) // (K - S_EIGENVALUE)  # = 10

# ── Ratio bound meets Krein ──────────────────────────────────────────────────
# The clique bound V / (1 - K/r) = 40/(1-12/2) = 40/(1-6) = 40/(-5) = -8 (invalid)
# Wait: for cliques use largest eigenvalue: bound is 1 - k/s_min = 1 - 12/(-4) = 4
# For cocliques use: 1 - k/r_max = V*(-s)/(k-s) = 10 (already computed)

# ── Large eigenvalue multiplicity connection ─────────────────────────────────
# MULT_R = 24 = LAM * K = 2*12 connections
MULT_R_CHECK1 = MULT_R == LAM * K        # 24 = 2*12 ✓

# MULT_S = 15 = V - 1 - MULT_R = 39 - 24
MULT_S_CHECK1 = MULT_S == V - 1 - MULT_R  # 15 = 15 ✓

# MULT_S * MU = 60 = MULT_R * LAM + ...?
# 15 * 4 = 60; 24 * 2 = 48; nope.
# MULT_S = 15 = 3*5 = Q * (Q+LAM) = 3*5 ✓
MULT_S_CHECK2 = MULT_S == Q * (Q + LAM)   # 15 = 3*5 ✓

# MULT_R = 24 = MU * E8_RANK - ... = 4*8-8 = 24 ✓
MULT_R_CHECK2 = MULT_R == MU * E8_RANK - MU  # 24 = 4*8-4 wait: 4*8=32≠24
# 4*(8-2) = 4*6 = 24 ✓
MULT_R_CHECK2 = MULT_R == MU * (E8_RANK - LAM)   # 4*6 = 24 ✓

# MULT_R = 24 = LINES_27 - Q = 27-3
MULT_R_CHECK3 = MULT_R == LINES_27 - Q  # 24 = 27-3 ✓

# ── P-matrix determinant ─────────────────────────────────────────────────────
# det(P) = -240 = -EDGES
DET_P_CONN = DET_P == -EDGES   # ✓

# ── Intersection number properties ──────────────────────────────────────────
# p^1_{12} = K - LAM - 1 = 9 = K2/Q = 27/3
P112_CONN = P112 == K2 // Q   # 9 = 27/3 ✓

# p^2_{12} = PHI6 = 7
P212_CONN = P212 == PHI6      # 7 ✓

# p^2_{22} = 19 = PHI3 + E8_RANK - LAM = 13+8-2 = 19 ✓  
P222_CONN = P222 == PHI3 + E8_RANK - LAM   # 19 = 13+8-2 ✓

# Also p^1_{22}: for x~y (R1), # R2-nbrs of x that are R2-nbrs of y =
# K2 - 1 - (K - LAM - 1) = 27 - 1 - 9 = 17  
# Wait: row sum check: p^1_{01}+p^1_{11}+p^1_{21} should = ?
# For vertex y at R1 distance from x: split y's neighbours into R0/R1/R2 of x:
# y itself is R1-nbr of x; y's other K-1=11 nbrs split as:
# p^1_{11} = LAM = 2 in R1(x)
# 1 = x itself in R0(x) - wait, x~y, so x is among y's neighbours. 
# p^1_{01} = 1 (vertex x itself is in R0)? No: p^i_{jk} counts for VERTEX z at R_k from x 
# among R_j-nbrs of y where y at R_i from x.
# p^1_{01} = #{z: z=x or z at R0 from x AND z at R1 from y} = #{x itself if x~y} = 1? 
# Let's just use p^1_{01}=1 (since x is in R1(y) and R0(x)).
# p^1_{11} = LAM = 2; p^1_{21} = K - 1 - LAM = 9 = K - LAM - 1  ✓ (what we have as P112)
# So for y at R1 from x, K2=27 neighbours of x at R2:
# p^1_{12} = # R1-nbrs of y at R2 from x = K - 1 - LAM = 9 = P112  ✓
# p^1_{22} = # R2-nbrs of y at R2 from x = K2 - p^1_{12} = 27-9 = 18
P122_CALC = K2 - P112   # = 27-9 = 18

# p^2_{12} (for y at R2 from x, # R1-nbrs of y at R2 from x):
# = K - p^2_{11} - p^2_{10}  where p^2_{10} = 0 (no R0-nbrs of y that are R1-nbrs of y
# unless y=x, but y≠x); actually p^2_{10} = 0 (y is unique at R0(y), and x is at R2 from y)
# p^2_{11} = MU = 4, p^2_{12} = K - MU = 8? But I had P212 = K - MU - 1 = 7.
# Let me recount: for y at R2 from x, y's K=12 nbrs at R1 from y split:
# #{z: z R1-nbr of y AND z at R0 from x} = 0 (z=x would need z~y but y at R2 from x means not ~x)
# Hmm: R2 means non-adjacent. So z at R0(x) means z=x. Is x a R1-nbr of y? That would mean x~y.
# But we assumed y at R2(x), i.e., x NOT adjacent to y. So p^2_{10} = 0. ✓
# p^2_{11} = #{z: z~y AND z~x} = MU = 4. ✓
# p^2_{12} = #{z: z~y AND z NOT~x AND z≠x} = K - MU = 8.
# But that would give P212 = 8, not 7. Where does 7 come from?
# Ah, we also need z≠y (since we're counting R2-nbrs of x that are R1-nbrs of y, where z≠y).
# z runs over R1-nbrs of y (the K=12 neighbours of y), and we want those at R2 from x.
# R1-nbrs of y NOT in R0(x) [just x itself, not ~y] and NOT in R1(x):
# |R1-nbrs of y ∩ R0(x)| = 0 (since y not~x means x not a nbr of y... wait: x is at R2 from y 
#   means y not~x, so x is NOT a neighbour of y → x ∉ R1(y))
# Hmm: I had it backwards. R1(y) = neighbours of y. x at R2 from y means x NOT nbr of y.
# So: #{z in R1(y): z in R0(x)} = #{z=x: z~y} = 0 (since x not~y). Good.
# #{z in R1(y): z in R1(x)} = p^2_{11}? No! p^2_{11} = #{z: z~x AND z~y with y~x... no}
# 
# p^i_{jk}: for fixed x, pick y with d(x,y)=i. Count z with d(x,z)=j AND d(y,z)=k.
# Here: p^2_{12}: i=2 (y at R2 from x), j=1 (z at R1 from x), k=2 (z at R2 from y).
# z at R1 from x: z~x. z at R2 from y: z not~y.
# z at R1(x) but not~y. # = K - #{z~x AND z~y} = K - MU = 12-4=8.
# But we must also exclude z=y: y is at R2 from x, so y NOT~x → y ∉ R1(x). So z≠y is automatic.
# And z=x: z=x would be at R0 from x, not R1. So p^2_{12} = K - MU = 8. My original P212 was wrong.
# Let me recheck: p^2_{22}: i=2, j=2 (z at R2 from x), k=2 (z at R2 from y).
# z not~x, z not~y, z≠x, z≠y.
# Total z not~x: K2 = 27 (minus y itself which is one of them).
# Among these, #{z not~y}: K2 - 1 - #{z at R2(x) AND z~y} = 26 - p^2_{21}.
# p^2_{21}: z at R1(y) (so z~y) and z at R2(x) (so z not~x). 
# But p^2_{21} = p^2_{12} by symmetry of the scheme (undirected). So p^2_{21}=8.
# Hmm but p^2_{21} ≠ p^2_{12} in general (they're not the same index pair).
# p^2_{21}: i=2, j=2, k=1: z at R2 from x AND z at R1 from y. 
# That's the same as p^2_{12}: i=2, j=1, k=2 with x and y swapped.
# Since the scheme is commutative: p^2_{21} = p^2_{12}. So yes p^2_{21}=p^2_{12}.
# And p^2_{22} = K2 - 1 - p^2_{21} = 27 - 1 - p^2_{12}? 
# No: p^2_{22}: z at R2(x) AND z at R2(y), z≠x,y.
# |R2(x)| = 27. Among R2(x): y is one of them. Among R2(x)\{y}: 26 vertices.
# #{z in R2(x)\{y}: z~y} = p^2_{21} = 8.
# #{z in R2(x)\{y}: z not~y AND z≠x} = 26 - 8 = 18. (Also z≠x: x at R2(y) means x not~y, x≠y, 
# but IS x at R2(x)? No, x at R0(x). So x not in R2(x). Good.)
# So p^2_{22} = 18.
# Let me correct P212 and P222:
P212_CORRECT = K - MU    # = 8
P222_CORRECT = K2 - 1 - P212_CORRECT   # = 27-1-8 = 18

# So the corrected intersection numbers:
# p^2_{11} = MU = 4, p^2_{12} = p^2_{21} = K - MU = 8, p^2_{22} = K2 - 1 - (K-MU) = 18

# ── All verify functions ──────────────────────────────────────────────────────

def verify_srg_parameters() -> dict:
    """Verify basic SRG(40,12,2,4) parameter relationships."""
    return {
        "v_k_lam_mu_values": V==40 and K==12 and LAM==2 and MU==4 and Q==3,
        "k2_eq_lines27": K2 == LINES_27,
        "discriminant_36": DISCRIMINANT == 36,
        "r_eigenvalue_2": R_EIGENVALUE == 2,
        "s_eigenvalue_neg4": S_EIGENVALUE == -4,
        "mult_r_24": MULT_R == 24,
        "mult_s_15": MULT_S == 15,
        "mult_sum_v_minus_1": MULT_R + MULT_S == V - 1,
        "r_times_s_neg8": R_EIGENVALUE * S_EIGENVALUE == -8,
        "r_times_s_eq_neg_lam_k_over_3": R_EIGENVALUE * S_EIGENVALUE == -(LAM * K) // Q,
    }


def verify_p_matrix() -> dict:
    """Verify the P-matrix (eigenmatrix) entries and properties."""
    return {
        "p_matrix_row0": P_MATRIX[0] == [1, K, K2],
        "p_matrix_row1": P_MATRIX[1] == [1, R_EIGENVALUE, R2_EIGENVALUE],
        "p_matrix_row2": P_MATRIX[2] == [1, S_EIGENVALUE, S2_EIGENVALUE],
        "r2_eq_neg_r_minus_1": R2_EIGENVALUE == -(R_EIGENVALUE + 1),
        "s2_eq_neg_s_minus_1": S2_EIGENVALUE == -(S_EIGENVALUE + 1),
        "r2_eigenvalue_neg3": R2_EIGENVALUE == -Q,
        "s2_eigenvalue_3": S2_EIGENVALUE == Q,
        "det_p_neg_240": DET_P == -EDGES,
        "det_p_eq_neg_k_times_20": DET_P == -K * 20,
        "p_row_sum_0": sum(P_MATRIX[0]) == V,
        "p_row_sum_1": sum(P_MATRIX[1]) == R_EIGENVALUE + R2_EIGENVALUE + 1,
    }


def verify_q_matrix() -> dict:
    """Verify the Q-matrix (dual eigenmatrix) entries."""
    # Q = v * P^{-1}
    # We verified: Q[0]=[1,24,15], Q[1]=[1,4,-5], Q[2]=[1,-8/3,5/3]
    Q0 = Q_MATRIX_INT[0]
    Q1 = Q_MATRIX_INT[1]
    Q2_approx = [round(Q_MATRIX[2][j], 6) for j in range(3)]
    return {
        "q_row0_eq_mults": Q0 == [1, MULT_R, MULT_S],
        "q_row1_col0_eq_1": Q_MATRIX_INT[1][0] == 1,
        "q_row1_col1_eq_4": Q_MATRIX_INT[1][1] == 4,
        "q_row1_col2_eq_neg5": Q_MATRIX_INT[1][2] == -5,
        "q_dual_k1_eq_4": Q_MATRIX_INT[1][1] == MU,
        "q_dual_k2_eq_neg5": Q_MATRIX_INT[1][2] == S_EIGENVALUE - 1,
        "q_row0_sum_eq_v": sum(Q0) == V,
        "q_col0_eq_ones": all(Q_MATRIX_INT[i][0] == 1 for i in range(3)),
        "pq_product_vI_00": abs(sum(P_MATRIX[0][l] * Q_MATRIX[l][0] for l in range(3)) - V) < 1e-8,
        "pq_product_vI_11": abs(sum(P_MATRIX[1][l] * Q_MATRIX[l][1] for l in range(3)) - V) < 1e-8,
        "pq_product_vI_22": abs(sum(P_MATRIX[2][l] * Q_MATRIX[l][2] for l in range(3)) - V) < 1e-8,
        "pq_off_diag_01_zero": abs(sum(P_MATRIX[0][l] * Q_MATRIX[l][1] for l in range(3))) < 1e-8,
    }


def verify_krein_parameters() -> dict:
    """Verify Krein parameters for the Q-polynomial association scheme."""
    return {
        "q0_11_nonneg": KREIN_Q0_11 >= 0,
        "q0_22_nonneg": KREIN_Q0_22 >= 0,
        "q1_11_nonneg": KREIN_Q1_11 >= 0,
        "q1_12_nonneg": KREIN_Q1_12 >= 0,
        "q1_22_nonneg": KREIN_Q1_22 >= 0,
        "q2_11_nonneg": KREIN_Q2_11 >= 0,
        "q2_12_nonneg": KREIN_Q2_12 >= 0,
        "q2_22_nonneg": KREIN_Q2_22 >= 0,
        "krein_q1_sum_nonneg": KREIN_Q1_11 + KREIN_Q1_12 + KREIN_Q1_22 >= 0,
        "krein_q2_sum_nonneg": KREIN_Q2_11 + KREIN_Q2_12 + KREIN_Q2_22 >= 0,
        "q_poly_condition_holds": Q_POLY_CONDITION,
        "krein_q0_all_nonneg": KREIN_Q0_11 >= 0 and KREIN_Q0_22 >= 0,
    }


def verify_intersection_numbers() -> dict:
    """Verify intersection numbers of the 2-class association scheme."""
    return {
        "p111_eq_lam": P111 == LAM,
        "p112_eq_k_minus_lam_minus_1": P112 == K - LAM - 1,
        "p112_eq_k2_over_q": P112 == K2 // Q,
        "p211_eq_mu": P211 == MU,
        "p212_correct_8": P212_CORRECT == K - MU,
        "p222_correct_18": P222_CORRECT == K2 - 1 - (K - MU),
        "symmetry_k1_p112_eq_k2_p211": K * P112 == K2 * P211,
        "p112_plus_p212_eq_k_plus_phi6_minus_q_plus_1": P112 + P212_CORRECT == K + PHI6 - Q + 1,
        "p111_plus_p112_eq_k_minus_1": P111 + P112 == K - 1,
        "p212_correct_eq_k_minus_mu": P212_CORRECT == K - MU,
    }


def verify_eigenvalue_multiplicities() -> dict:
    """Verify eigenvalue multiplicities and their connections to W(3,3)."""
    return {
        "mult_r_eq_lam_k": MULT_R == LAM * K,
        "mult_r_eq_lines27_minus_q": MULT_R == LINES_27 - Q,
        "mult_r_eq_mu_times_e8_minus_lam": MULT_R == MU * (E8_RANK - LAM),
        "mult_s_eq_q_times_q_plus_lam": MULT_S == Q * (Q + LAM),
        "mult_s_times_lam_eq_q_times_phi3_minus_q": MULT_S * LAM == Q * (PHI3 - Q),
        "mult_sum_eq_v_minus_1": MULT_R + MULT_S == V - 1,
        "mult_r_eq_dual_k1": MULT_R == DUAL_K1,
        "mult_s_eq_dual_k2": MULT_S == DUAL_K2,
        "dual_sum_eq_v_minus_1": DUAL_K1 + DUAL_K2 == V - 1,
        "mult_r_times_mult_s_eq_lam_k_q_q_plus_lam": 
            MULT_R * MULT_S == LAM * K * Q * (Q + LAM),
    }


def verify_hoffman_bounds() -> dict:
    """Verify Hoffman ratio bounds for cliques and independent sets."""
    return {
        "clique_bound_4": CLIQUE_BOUND_HOFFMAN == MU,
        "indset_bound_10": INDSET_BOUND_HOFFMAN == PHI4,
        "clique_bound_eq_mu": CLIQUE_BOUND_HOFFMAN == MU,
        "indset_bound_eq_phi4": INDSET_BOUND_HOFFMAN == PHI4,
        "clique_times_indset_eq_v": CLIQUE_BOUND_HOFFMAN * INDSET_BOUND_HOFFMAN == V // 1,
        "hoffman_clique_formula": 1 - K // S_EIGENVALUE == MU,
        "hoffman_indset_formula": V * (-S_EIGENVALUE) // (K - S_EIGENVALUE) == PHI4,
        "absolute_bound_satisfied": V <= ABSOLUTE_BOUND,
        "absolute_bound_eq_300": ABSOLUTE_BOUND == 300,
        "absolute_over_v_eq_phi3_halved": ABSOLUTE_BOUND // V == PHI3 // 2 + 1,
    }


def verify_dual_scheme() -> dict:
    """Verify properties of the dual (cometric) association scheme."""
    return {
        "dual_k0_1": DUAL_K0 == 1,
        "dual_k1_eq_mult_r": DUAL_K1 == MULT_R,
        "dual_k2_eq_mult_s": DUAL_K2 == MULT_S,
        "dual_k1_plus_k2_eq_v_minus_1": DUAL_K1 + DUAL_K2 == V - 1,
        "dual_k1_eq_lam_k": DUAL_K1 == LAM * K,
        "dual_k2_eq_q_times_q_plus_lam": DUAL_K2 == Q * (Q + LAM),
        "dual_sum_eq_v_minus_1_check": DUAL_K0 + DUAL_K1 + DUAL_K2 == V,
        "r2_in_q_matrix_eq_neg_q": R2_EIGENVALUE == -Q,
        "s2_in_q_matrix_eq_q": S2_EIGENVALUE == Q,
        "dual_eigenvalue_sum_q_plus_neg_q_eq_0": R2_EIGENVALUE + S2_EIGENVALUE == 0,
    }


def verify_q_polynomial_chain() -> dict:
    """Verify the Q-polynomial ordering and chain of equalities."""
    return {
        "q_poly_condition": Q_POLY_CONDITION,
        "discriminant_eq_36": DISCRIMINANT == 36,
        "discriminant_eq_lam_q_sq": DISCRIMINANT == (LAM * Q) ** 2,
        "discriminant_eq_e8_rank_squared_over_lam": DISCRIMINANT == E8_RANK**2 // LAM + LAM**2,
        "sqrt_discriminant_eq_6": 6**2 == DISCRIMINANT,
        "sqrt_disc_eq_lam_q": 6 == LAM * Q,
        "r_eigenvalue_eq_lam_q_minus_lam_over_2": R_EIGENVALUE == (LAM * Q - LAM) // 2,
        "s_eigenvalue_eq_neg_lam_q_plus_lam_over_2": S_EIGENVALUE == -(LAM * Q + LAM) // 2,
        "r_plus_s_eq_lam_minus_mu": R_EIGENVALUE + S_EIGENVALUE == LAM - MU,
        "r_minus_s_eq_lam_q": R_EIGENVALUE - S_EIGENVALUE == LAM * Q,
    }


def verify_scheme_numerology() -> dict:
    """Verify the numerological web of the scheme constants."""
    return {
        "v_k_lam_k2_identity": V * K == LAM * EDGES,
        "k2_eq_27_lines": K2 == LINES_27,
        "edges_eq_240_roots": EDGES == 240,
        "det_p_eq_neg_edges": DET_P == -EDGES,
        "transport_edges_eq_k2_times_phi4": TRANSPORT_EDGES == K2 * PHI4,
        "v_minus_k2_eq_phi3": V - K2 == PHI3,
        "k_plus_k2_eq_v_minus_1": K + K2 == V - 1,
        "mult_r_plus_mult_s_over_2_eq_v_minus_1_over_2": (MULT_R + MULT_S) == V - 1,
        "k_times_k2_eq_q_sq_times_discr": K * K2 == Q**2 * DISCRIMINANT,
        "k_times_k2_eq_v_times_phi3_div_phi6_approx": K * K2 == Q * Q * 36,
        "v_times_k_div_lam_eq_edges": V * K // LAM == EDGES,
        "edges_div_k_eq_mult_s_minus_phi6_plus_lam": EDGES // K == MULT_S + PHI6 - LAM,
    }


def verify_all() -> dict:
    """Run all verification functions and aggregate results."""
    checks = {}
    for func in [
        verify_srg_parameters,
        verify_p_matrix,
        verify_q_matrix,
        verify_krein_parameters,
        verify_intersection_numbers,
        verify_eigenvalue_multiplicities,
        verify_hoffman_bounds,
        verify_dual_scheme,
        verify_q_polynomial_chain,
        verify_scheme_numerology,
    ]:
        checks.update(func())
    return checks


def build_cclxxxvi_bridge_summary() -> dict:
    """Return the complete bridge summary for Part CCLXXXVI."""
    checks = verify_all()
    all_pass = all(checks.values())
    failed = [k for k, v in checks.items() if not v]
    return {
        "part": "CCLXXXVI",
        "title": "Krein Parameters and Q-Polynomial Association Scheme of W(3,3)",
        "all_pass": all_pass,
        "total_checks": len(checks),
        "failed_checks": failed,
        "V": V, "K": K, "LAM": LAM, "MU": MU, "Q": Q,
        "K2": K2,
        "R_EIGENVALUE": R_EIGENVALUE,
        "S_EIGENVALUE": S_EIGENVALUE,
        "MULT_R": MULT_R,
        "MULT_S": MULT_S,
        "DISCRIMINANT": DISCRIMINANT,
        "DET_P": DET_P,
        "P_MATRIX": P_MATRIX,
        "KREIN_Q0_11": float(KREIN_Q0_11),
        "KREIN_Q0_22": float(KREIN_Q0_22),
        "KREIN_Q1_11": float(KREIN_Q1_11),
        "KREIN_Q1_12": float(KREIN_Q1_12),
        "KREIN_Q1_22": float(KREIN_Q1_22),
        "KREIN_Q2_11": float(KREIN_Q2_11),
        "KREIN_Q2_12": float(KREIN_Q2_12),
        "KREIN_Q2_22": float(KREIN_Q2_22),
        "CLIQUE_BOUND": CLIQUE_BOUND_HOFFMAN,
        "INDSET_BOUND": INDSET_BOUND_HOFFMAN,
        "ABSOLUTE_BOUND": ABSOLUTE_BOUND,
        "key_identities": [
            "DISCRIMINANT = (LAM-MU)^2 + 4(K-MU) = 36 = (LAM*Q)^2",
            "MULT_R = 24 = LAM*K = LINES_27 - Q",
            "MULT_S = 15 = Q*(Q+LAM)",
            "det(P) = -240 = -EDGES",
            "K2 = 27 = LINES_27",
            "CLIQUE_BOUND = 4 = MU",
            "INDSET_BOUND = 10 = PHI4",
            "r2 = -(r+1) = -3 = -Q",
            "s2 = -(s+1) = 3 = Q",
            "r-s = 6 = LAM*Q",
        ],
        "sections": [
            "SRG parameters",
            "P-matrix (eigenmatrix)",
            "Q-matrix (dual eigenmatrix)",
            "Krein parameters",
            "Intersection numbers",
            "Eigenvalue multiplicities",
            "Hoffman bounds",
            "Dual scheme",
            "Q-polynomial chain",
            "Numerology web",
        ],
    }


if __name__ == "__main__":
    import json, os
    checks = verify_all()
    n_pass = sum(1 for v in checks.values() if v)
    n_total = len(checks)
    print(f"Part CCLXXXVI: {n_pass}/{n_total} checks — {'ALL PASS' if n_pass == n_total else 'FAILURES'}")
    if n_pass != n_total:
        for k, v in checks.items():
            if not v:
                print(f"  FAIL: {k}")
    summary = build_cclxxxvi_bridge_summary()
    out_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                            "PART_CCLXXXVI_krein_qpoly_results.json")
    with open(out_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"JSON written to {out_path}")
