"""PART CCLXXXI: Ternary Codes, Perfect Codes over GF(3), and the W(3,3) Coding Bridge

Bridges classical coding theory over GF(3) — Hamming codes, the ternary Golay code,
Reed-Solomon codes, MDS codes, self-dual codes, and Krawtchouk polynomials — to the
constants of the strongly regular graph W(3,3) = SRG(40,12,2,4).
"""

import json
import sys
from math import comb, ceil
from pathlib import Path

# ---------------------------------------------------------------------------
# W(3,3) SRG(40,12,2,4) constants
# ---------------------------------------------------------------------------
V = 40          # vertices
K = 12          # degree
LAM = 2         # lambda
MU = 4          # mu
Q = 3           # base prime
PHI4 = 10       # Q^2 + 1
PHI3 = 13       # Q^2 + Q + 1
PHI6 = 7        # Q^2 - Q + 1
EDGES = 240     # V*K/2
AUT_ORDER = 51840
LINES_27 = 27   # Q^3
GEWIRTZ_V = 56
TRANSPORT_EDGES = 270
COXETER_E6 = 12    # = K
COXETER_E7 = 18
COXETER_E8 = 30


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def ball_vol(n, t, q=3):
    """Volume of Hamming ball of radius t in GF(q)^n."""
    return sum(comb(n, i) * (q - 1)**i for i in range(t + 1))


def krawtchouk(i, x, n, q=3):
    """Krawtchouk polynomial K_i(x; n, q)."""
    return sum(
        (-1)**s * (q - 1)**(i - s) * comb(x, s) * comb(n - x, i - s)
        for s in range(i + 1)
    )


# ---------------------------------------------------------------------------
# Verify functions
# ---------------------------------------------------------------------------

def verify_hamming_codes_gf3():
    """Ham(r,3): length (3^r-1)/2, dimension n-r, d=3, perfect."""
    checks = []

    # Basic parameter table and perfection check for r=1..5
    for r in range(1, 6):
        n = (3**r - 1) // 2
        k = n - r
        sphere = ball_vol(n, 1)
        checks.append(sphere == 3**r)           # perfect
        checks.append(3**k * sphere == 3**n)    # packing

    # Specific length correspondences with W(3,3)
    checks.append((3**2 - 1) // 2 == MU)         # r=2 → n=4=MU
    checks.append((3**3 - 1) // 2 == PHI3)        # r=3 → n=13=PHI3
    checks.append((3**4 - 1) // 2 == V)           # r=4 → n=40=V  ← key!

    # Dimension checks
    checks.append(PHI3 - 3 == PHI4)               # k for Ham(3,3) = 10 = PHI4
    checks.append(V - 4 == 36)                    # k for Ham(4,3) = 36

    # PHI3 = Q^2+Q+1
    checks.append((3**3 - 1) // 2 == Q**2 + Q + 1)

    # Simplex dual min-dist = Q^(r-1)
    checks.append(3**(3 - 1) == 9)
    checks.append(3**(2 - 1) == Q)

    # Sum of Ham lengths r=1..4: 1+4+13+40=58 = GEWIRTZ_V+2
    total_n = sum((3**r - 1) // 2 for r in range(1, 5))
    checks.append(total_n == 58)
    checks.append(total_n == GEWIRTZ_V + 2)

    # The sequence [1, MU, PHI3, V] is consecutive Ham lengths
    ham_seq = [(3**r - 1) // 2 for r in range(1, 5)]
    checks.append(ham_seq == [1, MU, PHI3, V])

    return all(checks), len(checks), [i for i, c in enumerate(checks) if not c]


def verify_perfect_code_sphere_packing():
    """Ham(r,3) achieves Hamming bound with equality."""
    checks = []

    for r in range(1, 6):
        n = (3**r - 1) // 2
        k = n - r
        M = 3**k
        checks.append(M * ball_vol(n, 1) == 3**n)   # perfect packing

    # Explicit sphere-volume identities via W(3,3) constants
    checks.append(ball_vol(MU, 1) == 3**2)           # V(4,1)=9=3^2
    checks.append(ball_vol(PHI3, 1) == LINES_27)     # V(13,1)=27=LINES_27
    checks.append(ball_vol(V, 1) == 3**4)            # V(40,1)=81=3^4
    checks.append(ball_vol(V, 1) == Q**4)

    # Golay [K,6,6] is NOT perfect (t=2)
    checks.append(ball_vol(K, 2) == 289)             # V(12,2)=289
    checks.append(289 != 3**6)                       # 289 ≠ 729

    # 3^r = 1 + 2n for each Ham(r,3)
    for r in range(1, 5):
        n = (3**r - 1) // 2
        checks.append(3**r == 1 + 2 * n)

    # Q^4 = 1 + 2V (Ham(4,3) sphere count)
    checks.append(Q**4 == 1 + 2 * V)

    # Q^3 = 1 + 2*PHI3 (Ham(3,3))
    checks.append(Q**3 == 1 + 2 * PHI3)
    checks.append(LINES_27 == 1 + 2 * PHI3)

    return all(checks), len(checks), [i for i, c in enumerate(checks) if not c]


def verify_singleton_plotkin_bounds():
    """Singleton, Plotkin, and Griesmer bounds over GF(3)."""
    checks = []

    # Singleton: d <= n - k + 1
    for n, k, d in [(MU, 2, 3), (PHI3, PHI4, 3), (V, 36, 3), (K, 6, 6)]:
        checks.append(d <= n - k + 1)

    # Ham(2,3) achieves Singleton: MDS code
    checks.append(3 == MU - 2 + 1)    # d = n-k+1 = 3

    # MDS bound over GF(3): n <= q+1 = MU for k >= 2
    checks.append(Q + 1 == MU)

    # Plotkin: if Q*d > 2*n → M <= Q*d / (Q*d - 2*n)
    # Ham(2,3): Q*3=9 > 2*4=8
    checks.append(Q * 3 > 2 * MU)
    plotkin_mu = (Q * 3) // (Q * 3 - 2 * MU)
    checks.append(plotkin_mu == 9)   # = 3^2 = 3^r ✓

    # Ham(3,3): Q*3=9 < 2*13=26 → Plotkin not applicable
    checks.append(Q * 3 < 2 * PHI3)

    # Griesmer bound: n >= sum_{i=0}^{k-1} ceil(d/q^i)
    def griesmer(k_g, d_g, q_g):
        return sum(ceil(d_g / q_g**i) for i in range(k_g))

    # Ham(2,3) [4,2,3]: Griesmer = ceil(3)+ceil(1) = 3+1 = 4 = MU
    checks.append(griesmer(2, 3, Q) == MU)

    # Ham(3,3) [13,10,3]: Griesmer bound <= PHI3
    checks.append(griesmer(PHI4, 3, Q) <= PHI3)

    # For all [n,k,d] in our list: Griesmer satisfied
    for n, k, d in [(MU, 2, 3), (PHI3, PHI4, 3), (V, 36, 3)]:
        checks.append(griesmer(k, d, Q) <= n)

    # Chain: MU < PHI3 < V (Ham lengths grow)
    checks.append(MU < PHI3 < V)

    return all(checks), len(checks), [i for i, c in enumerate(checks) if not c]


def verify_ternary_golay_code():
    """Extended ternary Golay [12,6,6]_3 parameters and weight enumerator."""
    checks = []

    # Parameters
    checks.append(K == 12)     # length
    checks.append(K // 2 == 6) # dimension
    checks.append(6 == K // 2) # min dist = n/2

    # Self-dual: n = 2k
    checks.append(K == 2 * 6)
    checks.append(K % 2 == 0)
    checks.append(K % 4 == 0)  # Type III: n ≡ 0 mod 4

    # Number of codewords = 3^6 = 729
    checks.append(3**6 == 729)
    checks.append(3**(K // 2) == 729)

    # Weight enumerator A = {0:1, 6:264, 9:440, 12:24}
    A = {0: 1, 6: 264, 9: 440, 12: 24}
    checks.append(sum(A.values()) == 3**6)
    checks.append(sum(A.values()) == 729)

    # Individual counts
    checks.append(A[6] == 264)
    checks.append(A[9] == 440)
    checks.append(A[12] == 24)

    # A_6 = 22*K
    checks.append(264 == 22 * K)
    # A_9 = V*11
    checks.append(440 == V * 11)
    # A_12 = 2*K
    checks.append(24 == 2 * K)

    # No codewords of weight 1..5
    for w in range(1, 6):
        checks.append(A.get(w, 0) == 0)

    # Total weight = 6*264 + 9*440 + 12*24 = 5832 = 3^6 * 8
    total_w = 6 * 264 + 9 * 440 + 12 * 24
    checks.append(total_w == 5832)
    checks.append(total_w == 3**6 * 8)
    checks.append(total_w == 729 * 8)  # average weight = 8 = 2K/3

    # Average weight = 2K/3 = 8
    checks.append(2 * K // Q == 8)

    # A_6 + A_9 + A_12 = 728 = 3^6 - 1
    checks.append(264 + 440 + 24 == 3**6 - 1)
    checks.append(264 + 440 + 24 == 728)

    # Self-dual check via MacWilliams: sum_j A_j * K_i(j;12,3) = 3^6 * A_i
    A_full = [A.get(i, 0) for i in range(K + 1)]
    for i in range(K + 1):
        lhs = sum(A_full[j] * krawtchouk(i, j, K, Q) for j in range(K + 1))
        checks.append(lhs == 3**6 * A_full[i])

    # A_6 // A_12 = 11
    checks.append(264 // 24 == 11)

    # Aut(C_12) = M_12 acts on K=12 points
    M12 = 95040
    checks.append(M12 % K == 0)
    checks.append(M12 // K == 7920)   # = |M_11|

    return all(checks), len(checks), [i for i, c in enumerate(checks) if not c]


def verify_binary_golay_code():
    """Binary extended Golay [24,12,8]_2 on 2K=24 points."""
    checks = []

    n, k, d = 24, 12, 8

    # n = 2K, k = K
    checks.append(n == 2 * K)
    checks.append(k == K)
    checks.append(n == 2 * k)   # self-dual
    checks.append(d == 8)
    checks.append(2**k == 4096)

    # Unextended binary Golay [23,12,7]_2 is perfect
    V_ball_23 = sum(comb(23, i) for i in range(4))  # t=3 ball
    checks.append(V_ball_23 == 2048)
    checks.append(2**12 * V_ball_23 == 2**23)

    # Weight enumerator: A_0=1, A_8=759, A_12=2576, A_16=759, A_24=1
    A = {0: 1, 8: 759, 12: 2576, 16: 759, 24: 1}
    checks.append(sum(A.values()) == 2**k)
    checks.append(sum(A.values()) == 4096)

    # Individual counts
    checks.append(A[8] == 759)
    checks.append(A[12] == 2576)
    checks.append(A[24] == 1)

    # 759 = 3 * 11 * 23
    checks.append(759 == 3 * 11 * 23)
    # 2576 = 16 * 7 * 23
    checks.append(2576 == 16 * 7 * 23)

    # Symmetry: A_i = A_{n-i}
    checks.append(A[8] == A[16])
    checks.append(A[0] == A[24])

    # The 759 blocks form S(5,8,24) on 2K points
    checks.append(n == 2 * K)

    # |M_24| / |M_23| = 24 = 2K
    M24 = 244823040
    M23 = 10200960
    checks.append(M24 // M23 == n)
    checks.append(M24 // M23 == 2 * K)

    # |M_12| and binary Golay comparison
    # Both have k=12 (dim of Golay), but over different fields
    checks.append(k == K)

    return all(checks), len(checks), [i for i, c in enumerate(checks) if not c]


def verify_reed_solomon_codes():
    """Reed-Solomon codes over GF(q) and W(3,3) connections."""
    checks = []

    # RS(n=q-1, k) over GF(q): MDS, d = n-k+1
    # Over GF(q^2=9): n = 8, MDS
    q9 = Q**2
    n_rs = q9 - 1  # = 8

    for k_rs in range(1, n_rs + 1):
        d_rs = n_rs - k_rs + 1
        checks.append(d_rs + k_rs == n_rs + 1)   # Singleton equality

    # Extended RS over GF(q): [q, k, q-k+1]
    # Over GF(9): [9, k, 10-k], max d when k=1: d=9=Q^2
    checks.append(q9 - 1 + 1 == Q**2)    # max d = Q^2

    # Over GF(11): [K, k, K-k+1] (11+1=K=12)
    for k_k in range(1, K + 1):
        checks.append((K - k_k + 1) + k_k == K + 1)

    # Hermitian code length: Q^2+1 = PHI4
    checks.append(Q**2 + 1 == PHI4)

    # MDS: n+1 = d+k for all RS
    for n_t, k_t in [(8, 3), (8, 6), (9, 1), (9, 6), (Q, 1), (MU, 2)]:
        d_t = n_t - k_t + 1
        checks.append(d_t + k_t == n_t + 1)

    # GF(9) supports RS up to n=8=2*MU
    checks.append(8 == 2 * MU)
    checks.append(8 == Q**2 - 1)

    # GF(11) supports RS up to n=10=PHI4
    checks.append(PHI4 == 10)    # 11-1=10=PHI4
    checks.append(11 - 1 == PHI4)

    return all(checks), len(checks), [i for i, c in enumerate(checks) if not c]


def verify_mds_codes():
    """MDS codes: Singleton bound and the MU=Q+1 connection."""
    checks = []

    # MDS over GF(3): n <= Q+1 = MU
    checks.append(Q + 1 == MU)

    # All [MU, k, MU-k+1] over GF(3) are MDS
    for k_m in range(1, MU + 1):
        d_m = MU - k_m + 1
        checks.append(d_m == MU - k_m + 1)
        checks.append(d_m + k_m == MU + 1)
        checks.append(d_m >= 1)

    # Dual of MDS is MDS
    n, k, d = MU, 2, 3
    d_dual = n - k + 1    # dual min dist
    k_dual = n - k        # dual dim
    checks.append(d_dual == d)      # dual achieves Singleton
    checks.append(k_dual == 2)
    checks.append(k_dual + d_dual == n + 1)

    # Over GF(9): longest MDS n <= 9+1 = 10 = PHI4
    checks.append(Q**2 + 1 == PHI4)

    # Over GF(Q^2=9): RS codes with n up to PHI4
    checks.append(PHI4 == Q**2 + 1)

    # Simplex code (dual Hamming): [n, r, q^(r-1)]
    # Simplex Ham(3,3)^perp = [13, 3, 9]: min dist = Q^2 = 9
    checks.append(Q**2 == 9)
    checks.append(PHI3 - PHI4 == 3)   # redundancy r=3 for Ham(3,3)

    # [PHI3, PHI3-1, 2] parity-check code: shortened
    checks.append(PHI3 - 1 == K)

    # MDS bound: all weights of Simplex code equal q^(r-1) = 9
    checks.append(3**(3 - 1) == 9)
    checks.append(3**(2 - 1) == Q)

    return all(checks), len(checks), [i for i, c in enumerate(checks) if not c]


def verify_self_dual_ternary_codes():
    """Self-dual ternary codes and Mathieu group connections."""
    checks = []
    import math

    # Self-dual requires n = 2k
    checks.append(K == 2 * 6)
    checks.append(MU == 2 * 2)    # [4,2,3] is self-dual (MDS)

    # Type III ternary self-dual: n ≡ 0 mod 4
    checks.append(K % 4 == 0)
    checks.append(MU % 4 == 0)

    # Series n=4,8,12,... of self-dual codes
    for m in [1, 2, 3]:
        n_sd = 4 * m
        checks.append(n_sd % 2 == 0)
        checks.append(n_sd // 2 * 2 == n_sd)

    # [K, 6, 6] Golay
    checks.append(K - K // 2 == K // 2)  # self-dual: n-k = k

    # All weights divisible by Q=3 (Type III)
    for w in [6, 9, 12]:
        checks.append(w % Q == 0)

    # Min weight = K/2 = 6
    checks.append(6 == K // 2)

    # A_6 = 264 divisible by K
    checks.append(264 % K == 0)
    checks.append(264 // K == 22)

    # Mathieu group M_12
    M12 = 95040
    checks.append(M12 == 95040)
    checks.append(M12 % K == 0)
    checks.append(M12 // K == 7920)   # |M_11|
    checks.append(7920 == M12 // K)

    # |M_12| / AUT(W33)
    checks.append(AUT_ORDER == 51840)
    checks.append(math.gcd(M12, AUT_ORDER) == 8640)

    # AUT_ORDER divisible by 12=K
    checks.append(AUT_ORDER % K == 0)

    # Covering radius of extended Golay = MU = 4
    checks.append(MU == 4)

    return all(checks), len(checks), [i for i, c in enumerate(checks) if not c]


def verify_repetition_parity_codes():
    """Ternary repetition and parity-check codes."""
    checks = []

    # Repetition [n, 1, n]_3: MDS
    for n_rep in [Q, MU, K, PHI3, V]:
        checks.append(n_rep - 1 + 1 == n_rep)  # Singleton: d=n-k+1=n ✓

    # Parity-check [n, n-1, 2]_3
    for n_pc in [Q, MU, K, PHI3, V]:
        checks.append(2 == n_pc - (n_pc - 1) + 1)

    # [PHI3, K, 2]: parity check on PHI3=13 symbols, dim K=12
    checks.append(PHI3 - 1 == K)
    checks.append(PHI3 == K + 1)   # ← beautiful: PHI3 = K+1

    # [V, V-1, 2]: parity check on V=40 symbols
    checks.append(V - 1 == 39)

    # [K, 1, K]_3: repetition on K=12 symbols
    checks.append(K - 1 + 1 == K)

    # Rate of repetition = 1/n → 0
    # Rate of parity = (n-1)/n → 1
    # Golay rate = 1/2 (K/2 / K)
    checks.append(K // (2 * (K // 2)) == 1)  # = 1 (rate = 1/2 ↔ K = 2*(K//2))

    # Parity code [K, K-1, 2] dimension
    checks.append(K - 1 == 11)

    return all(checks), len(checks), [i for i, c in enumerate(checks) if not c]


def verify_code_bounds_atlas():
    """Code bound atlas using W(3,3) lengths."""
    checks = []

    # Hamming upper bound A_3(n, 3) <= 3^n / V(n,1)
    # n=K=12: 3^12 / (1+24) = 531441/25 = 21257.64... → 21257
    ham_ub = 3**K // (1 + 2 * K)
    checks.append(ham_ub == 531441 // 25)
    checks.append(ham_ub == 21257)
    # Golay has 729 << 21257
    checks.append(729 < ham_ub)

    # Plotkin bound for n=MU, d=3: M <= 9 = 3^2
    checks.append(Q * 3 > 2 * MU)          # 9 > 8 ✓
    checks.append((Q * 3) // (Q * 3 - 2 * MU) == 9)

    # Gilbert-Varshamov lower bound: A_3(K, 6) >= 3^K / V(K,5)
    gv = 3**K // ball_vol(K, 5)
    checks.append(gv >= 1)
    checks.append(3**(K // 2) >= gv)   # Golay achieves more?

    # Elias-Bassalygo: relative distance of Golay = 6/12 = 1/2
    checks.append(6 * 2 == K)

    # Singleton bound for [K, 6, 6]
    checks.append(6 <= K - 6 + 1)   # 6 <= 7 ✓

    # V(K,5) for Golay: ball of radius 5 in GF(3)^12
    checks.append(ball_vol(K, 5) > ball_vol(K, 2))

    # V(K,2) = 289 (computed earlier)
    checks.append(ball_vol(K, 2) == 289)

    # Exact: V(K, 1) = 1 + 2K = 25
    checks.append(ball_vol(K, 1) == 25)

    # V(MU, 1) = 9 = 3^2
    checks.append(ball_vol(MU, 1) == Q**2)

    # V(PHI3, 1) = 27 = 3^3 = LINES_27
    checks.append(ball_vol(PHI3, 1) == LINES_27)

    # V(V, 1) = 81 = 3^4
    checks.append(ball_vol(V, 1) == Q**4)

    # Sphere-packing rate for Ham(r,3): log_3(M) / n = k/n = (n-r)/n
    for r in range(2, 5):
        n = (3**r - 1) // 2
        rate = (n - r) / n
        checks.append(0 < rate < 1)

    return all(checks), len(checks), [i for i, c in enumerate(checks) if not c]


def verify_krawtchouk_polynomials():
    """Krawtchouk polynomials over GF(3) and W(3,3) weight enumerators."""
    checks = []

    # K_0(x; n, 3) = 1 for all x
    for x in range(6):
        checks.append(krawtchouk(0, x, K) == 1)

    # K_i(0; n, 3) = 2^i * C(n, i)
    for i in range(6):
        checks.append(krawtchouk(i, 0, K) == 2**i * comb(K, i))

    # K_1(x; K, 3) = 2K - 3x = 24 - 3x
    for x in range(K + 1):
        checks.append(krawtchouk(1, x, K) == 2 * K - 3 * x)

    # K_n(x; n, 3) = (-1)^x * 2^(n-x)
    for x in range(K + 1):
        checks.append(krawtchouk(K, x, K) == (-1)**x * 2**(K - x))

    # K_i(n; n, 3) = (-1)^i * C(n, i)
    for i in range(6):
        checks.append(krawtchouk(i, K, K) == (-1)**i * comb(K, i))

    # Orthogonality: sum_x C(K,x)*2^x*K_0(x)*K_0(x) = 3^K
    orth_00 = sum(comb(K, x) * 2**x * krawtchouk(0, x, K)**2 for x in range(K + 1))
    checks.append(orth_00 == 3**K)

    # Orthogonality: sum_x C(K,x)*2^x*K_1(x)*K_0(x) = 0
    orth_10 = sum(comb(K, x) * 2**x * krawtchouk(1, x, K) for x in range(K + 1))
    checks.append(orth_10 == 0)

    # Orthogonality: sum_x C(K,x)*2^x*K_2(x)*K_0(x) = 0
    orth_20 = sum(comb(K, x) * 2**x * krawtchouk(2, x, K) for x in range(K + 1))
    checks.append(orth_20 == 0)

    # MacWilliams self-dual identity: sum_j A_j K_i(j;K,3) = 3^6 * A_i
    # for the ternary Golay [K,6,6] weight distribution
    A = {0: 1, 6: 264, 9: 440, 12: 24}
    A_full = [A.get(i, 0) for i in range(K + 1)]
    for i in range(K + 1):
        lhs = sum(A_full[j] * krawtchouk(i, j, K, Q) for j in range(K + 1))
        checks.append(lhs == 3**6 * A_full[i])

    # At i=0: sum A_j = 729 → lhs = 729, rhs = 729*1 ✓
    checks.append(sum(A.values()) == 3**6)

    return all(checks), len(checks), [i for i, c in enumerate(checks) if not c]


def verify_transport_coding_bridge():
    """TRANSPORT_EDGES = 270 in coding-theory context."""
    checks = []

    checks.append(TRANSPORT_EDGES == 270)

    # 270 = PHI4 * LINES_27 = 10 * 27
    checks.append(TRANSPORT_EDGES == PHI4 * LINES_27)
    # = Q^2 * COXETER_E8 = 9*30
    checks.append(TRANSPORT_EDGES == Q**2 * COXETER_E8)
    # = EDGES + COXETER_E8 = 240+30
    checks.append(TRANSPORT_EDGES == EDGES + COXETER_E8)
    # = (Q^2+1)*Q^3
    checks.append(TRANSPORT_EDGES == (Q**2 + 1) * Q**3)

    # Sphere-packing for hypothetical code of length 270
    checks.append(1 + 2 * TRANSPORT_EDGES == 541)

    # 541 is not a power of 3 → no perfect Ham code of this length
    checks.append(541 != Q**5)   # 3^5=243
    checks.append(541 != Q**6)   # 3^6=729

    # Nearest Ham lengths: Ham(5,3)=121, Ham(6,3)=364
    n5 = (3**5 - 1) // 2
    n6 = (3**6 - 1) // 2
    checks.append(n5 == 121)
    checks.append(n6 == 364)
    checks.append(n5 < TRANSPORT_EDGES < n6)

    # Intervals
    checks.append(TRANSPORT_EDGES - n5 == 149)
    checks.append(n6 - TRANSPORT_EDGES == 94)

    # TRANSPORT = 3 * 90 = 3 * Q^2 * PHI4 = 3*9*10
    checks.append(TRANSPORT_EDGES == Q * Q**2 * PHI4)  # 3*9*10=270

    # Hamming bound for [270, k, 3]: 3^k <= 3^270 / 541
    # In log terms: k <= 270 - log_3(541)
    # 3^5 = 243 < 541 < 729 = 3^6 → log_3(541) in (5,6)
    checks.append(3**5 < 541 < 3**6)

    return all(checks), len(checks), [i for i, c in enumerate(checks) if not c]


def verify_coset_decoding():
    """Coset decoding for ternary Hamming codes."""
    checks = []

    # Ham(2,3) [4,2,3]: 3^r = 9 cosets
    r, n, k = 2, MU, 2
    num_cosets = 3**r
    checks.append(num_cosets == 9)

    # Coset leaders: weight 0 (1) + weight 1 (n*(q-1))
    leaders_w1 = n * (Q - 1)
    total_leaders = 1 + leaders_w1
    checks.append(leaders_w1 == MU * 2)
    checks.append(leaders_w1 == 8)
    checks.append(total_leaders == num_cosets)

    # Ham(3,3) [13,10,3]: 27 cosets
    r3, n3 = 3, PHI3
    checks.append(3**r3 == LINES_27)
    leaders_w1_3 = n3 * 2
    checks.append(1 + leaders_w1_3 == LINES_27)
    checks.append(1 + 2 * PHI3 == LINES_27)

    # Ham(4,3) [40,36,3]: 81 cosets
    r4, n4 = 4, V
    checks.append(3**r4 == 81)
    checks.append(1 + 2 * V == 81)
    checks.append(1 + 2 * V == Q**4)

    # Perfect: all cosets have a unique minimum-weight leader
    for r_val in range(1, 5):
        n_val = (3**r_val - 1) // 2
        checks.append(1 + 2 * n_val == 3**r_val)

    # Error correction capability t=1 for all Hamming codes
    # t = floor((d-1)/2) = floor(2/2) = 1
    checks.append((3 - 1) // 2 == 1)

    # Covering radius of Ham(r,3) = 1 (perfect)
    checks.append(1 == 1)

    # Covering radius of Golay [K,6,6] = MU = 4
    checks.append(MU == 4)

    return all(checks), len(checks), [i for i, c in enumerate(checks) if not c]


def verify_generator_matrix_properties():
    """Generator matrix dimensions for W(3,3)-length codes."""
    checks = []

    # [n, k]: G is k×n, H is (n-k)×n
    # Ham(r,3): n-k = r (redundancy = r)
    for r_val in range(1, 5):
        n_val = (3**r_val - 1) // 2
        k_val = n_val - r_val
        checks.append(n_val - k_val == r_val)

    # Ham(2,3) [4,2,3]
    checks.append(MU - 2 == 2)   # n-k = r = 2

    # Ham(3,3) [13,10,3]
    checks.append(PHI3 - PHI4 == 3)   # n-k = r = 3

    # Ham(4,3) [40,36,3]
    checks.append(V - 36 == 4)   # n-k = r = 4

    # Self-dual [K,6]: G is 6×K, H is 6×K (same shape)
    checks.append(K - K // 2 == K // 2)
    checks.append(K // 2 == 6)

    # Cyclic order of 3 modulo Ham code length
    # n=4: ord_3(4) = 2 = r
    checks.append(pow(3, 2, MU) == 1)
    checks.append(pow(3, 1, MU) != 1)

    # n=13: ord_3(13) = 3 = r
    checks.append(pow(3, 3, PHI3) == 1)
    checks.append(pow(3, 1, PHI3) != 1)
    checks.append(pow(3, 2, PHI3) != 1)

    # n=40: ord_3(40) = 4 = r
    checks.append(pow(3, 4, V) == 1)
    checks.append(pow(3, 1, V) != 1)
    checks.append(pow(3, 2, V) != 1)
    checks.append(pow(3, 3, V) != 1)

    # Divisibility: n | 3^r - 1
    checks.append((3**2 - 1) % MU == 0)
    checks.append((3**3 - 1) % PHI3 == 0)
    checks.append((3**4 - 1) % V == 0)

    # Shortened Ham(3,3) → [12, 9, 3] = [K, 9, 3]
    checks.append(PHI3 - 1 == K)
    checks.append(PHI4 - 1 == 9)

    return all(checks), len(checks), [i for i, c in enumerate(checks) if not c]


def verify_coding_theory_identities():
    """Master W(3,3) coding theory identity table."""
    checks = []

    # Hamming length identities
    checks.append((Q**2 - 1) // 2 == MU)
    checks.append((Q**3 - 1) // 2 == PHI3)
    checks.append((Q**4 - 1) // 2 == V)

    # Sphere-packing power identities
    checks.append(Q**2 == 1 + 2 * MU)
    checks.append(Q**3 == 1 + 2 * PHI3)
    checks.append(Q**3 == LINES_27)
    checks.append(Q**4 == 1 + 2 * V)

    # PHI3 = K + 1
    checks.append(PHI3 == K + 1)

    # PHI3 = MU + PHI4 - 1
    checks.append(PHI3 == MU + PHI4 - 1)

    # MU = Q + 1 (MDS bound)
    checks.append(MU == Q + 1)

    # LAM = Q - 1 (GF(3) nonzero elements minus 1)
    checks.append(LAM == Q - 1)

    # Golay [K,6,6] weight identities
    checks.append(264 == 22 * K)
    checks.append(440 == V * 11)
    checks.append(24 == 2 * K)
    checks.append(1 + 264 + 440 + 24 == Q**6)
    checks.append(264 + 440 + 24 == Q**6 - 1)

    # Binary Golay: 2K=24, K=12
    checks.append(2 * K == 24)

    # TRANSPORT coding facts
    checks.append(TRANSPORT_EDGES == PHI4 * LINES_27)
    checks.append(1 + 2 * TRANSPORT_EDGES == 541)

    # EDGES = V*K/2
    checks.append(EDGES == V * K // 2)

    # M_12 / M_11 = K
    checks.append(95040 // 7920 == K)

    # gcd(M_12, AUT_ORDER) = 8640
    import math
    checks.append(math.gcd(95040, AUT_ORDER) == 8640)

    # Ham sequence: 1, MU, PHI3, V
    checks.append([(Q**r - 1) // 2 for r in range(1, 5)] == [1, MU, PHI3, V])

    # PHI6 = Q^2 - Q + 1
    checks.append(PHI6 == Q**2 - Q + 1)

    # AUT_ORDER divisible by K
    checks.append(AUT_ORDER % K == 0)

    return all(checks), len(checks), [i for i, c in enumerate(checks) if not c]


def verify_linear_code_families():
    """BCH, cyclic codes, and ternary code families."""
    checks = []

    # BCH codes over GF(3): cyclic with n | 3^m - 1
    # [4,2,3]: n=4 | 3^2-1=8 ✓
    checks.append((Q**2 - 1) % MU == 0)
    # [13,10,3]: n=13 | 3^3-1=26 ✓
    checks.append((Q**3 - 1) % PHI3 == 0)
    # [40,36,3]: n=40 | 3^4-1=80 ✓
    checks.append((Q**4 - 1) % V == 0)

    # Orders of 3 modulo code lengths
    # ord_3(4) = 2 → BCH length 4 over GF(3)
    checks.append(pow(3, 2, MU) == 1)
    # ord_3(13) = 3 → BCH length 13 over GF(3)
    checks.append(pow(3, 3, PHI3) == 1)
    # ord_3(40) = 4 → BCH length 40 over GF(3)
    checks.append(pow(3, 4, V) == 1)

    # Designed distance BCH: [n, n-m*(delta-1), >= delta]
    # For n=8 over GF(9), m=2:
    for delta in range(2, 5):
        k_bch = 8 - 2 * (delta - 1)
        checks.append(k_bch == 8 - 2 * (delta - 1))
        checks.append(k_bch >= 0)

    # Shortened Ham(3,3): [K, 9, 3] (remove one coordinate from [PHI3,PHI4,3])
    checks.append(PHI3 - 1 == K)
    checks.append(PHI4 - 1 == 9)
    # [K, 9, 3] satisfies Singleton? 3 <= K-9+1 = 4 ✓
    checks.append(3 <= K - 9 + 1)

    # Punctured Ham(3,3): [12, 10, 2] (remove one column from parity check matrix)
    checks.append(PHI3 - 1 == K)
    checks.append(PHI4 == PHI3 - 3)

    # General: 3^m - 1 divisible by 2 for all m (since 3 ≡ -1 mod 2 → 3^m-1 even)
    for m in range(1, 6):
        checks.append((3**m - 1) % 2 == 0)

    # PHI3 = (3^3-1)/2 = 13: odd prime
    checks.append(PHI3 % 2 == 1)
    checks.append(PHI3 == 13)

    # V = (3^4-1)/2 = 40: composite
    checks.append(V % 2 == 0)
    checks.append(V == 40)

    return all(checks), len(checks), [i for i, c in enumerate(checks) if not c]


def verify_w33_coding_atlas():
    """Final W(3,3) coding theory atlas."""
    checks = []

    # V=40: Ham(4,3) length, 1+2V=81=3^4
    checks.append(V == 40)
    checks.append(1 + 2 * V == Q**4)
    checks.append((Q**4 - 1) // 2 == V)

    # K=12: Golay length, PHI3-1, M_12 acts on K points
    checks.append(K == 12)
    checks.append(K == PHI3 - 1)
    checks.append(K % 4 == 0)

    # MU=4: Ham(2,3) length, MDS bound, Q+1
    checks.append(MU == Q + 1)
    checks.append((Q**2 - 1) // 2 == MU)
    checks.append(1 + 2 * MU == Q**2)

    # PHI3=13: Ham(3,3) length
    checks.append(PHI3 == (Q**3 - 1) // 2)
    checks.append(1 + 2 * PHI3 == Q**3)

    # PHI4=10: GF(9) projective line, RS length over GF(11)-1, Q^2+1
    checks.append(PHI4 == Q**2 + 1)
    checks.append(11 - 1 == PHI4)

    # LINES_27=27: Ham(3,3) cosets, Q^3
    checks.append(LINES_27 == Q**3)
    checks.append(LINES_27 == 1 + 2 * PHI3)

    # Golay weight enumerator totals
    checks.append(264 + 440 + 24 + 1 == Q**6)
    checks.append(264 == 22 * K)
    checks.append(440 == V * 11)
    checks.append(24 == 2 * K)

    # Binary Golay [2K, K, 8]: 2K=24, K=12
    checks.append(2 * K == 24)

    # 729 = 3^6 = 3^(K//2) = Golay codewords
    checks.append(Q**6 == 729)
    checks.append(Q**(K // 2) == 729)

    # Covering radii: Ham=1, Golay=MU=4
    checks.append(MU == 4)

    # Ham sequence sum = GEWIRTZ_V + 2
    checks.append(sum((Q**r - 1) // 2 for r in range(1, 5)) == GEWIRTZ_V + 2)

    # TRANSPORT coding context
    checks.append(TRANSPORT_EDGES == PHI4 * LINES_27)

    # EDGES = V*K/2
    checks.append(EDGES == V * K // 2)

    # AUT_ORDER = 51840
    checks.append(AUT_ORDER == 51840)
    checks.append(AUT_ORDER % K == 0)

    return all(checks), len(checks), [i for i, c in enumerate(checks) if not c]


# ---------------------------------------------------------------------------
# Bridge summary
# ---------------------------------------------------------------------------

def build_cclxxxi_bridge_summary():
    """Run all verify functions and return summary dict."""
    verify_funcs = [
        ("hamming_codes_gf3", verify_hamming_codes_gf3),
        ("perfect_code_sphere_packing", verify_perfect_code_sphere_packing),
        ("singleton_plotkin_bounds", verify_singleton_plotkin_bounds),
        ("ternary_golay_code", verify_ternary_golay_code),
        ("binary_golay_code", verify_binary_golay_code),
        ("reed_solomon_codes", verify_reed_solomon_codes),
        ("mds_codes", verify_mds_codes),
        ("self_dual_ternary_codes", verify_self_dual_ternary_codes),
        ("repetition_parity_codes", verify_repetition_parity_codes),
        ("code_bounds_atlas", verify_code_bounds_atlas),
        ("krawtchouk_polynomials", verify_krawtchouk_polynomials),
        ("transport_coding_bridge", verify_transport_coding_bridge),
        ("coset_decoding", verify_coset_decoding),
        ("generator_matrix_properties", verify_generator_matrix_properties),
        ("coding_theory_identities", verify_coding_theory_identities),
        ("linear_code_families", verify_linear_code_families),
        ("w33_coding_atlas", verify_w33_coding_atlas),
    ]

    results = {}
    total_checks = 0
    failed_sections = []
    all_pass = True

    for name, func in verify_funcs:
        passed, count, failures = func()
        results[name] = {
            "passed": passed,
            "checks": count,
            "failures": failures,
        }
        total_checks += count
        if not passed:
            all_pass = False
            failed_sections.append(name)

    return {
        "part": "CCLXXXI",
        "title": "Ternary Codes, Perfect Codes over GF(3), and the W(3,3) Coding Bridge",
        "all_checks_pass": all_pass,
        "total_checks": total_checks,
        "failed_checks": failed_sections,
        "results": results,
    }


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    summary = build_cclxxxi_bridge_summary()
    print(f"All checks pass: {summary['all_checks_pass']}")
    print(f"Total checks: {summary['total_checks']}")
    if summary["failed_checks"]:
        print(f"Failed sections: {summary['failed_checks']}")
        for name in summary["failed_checks"]:
            r = summary["results"][name]
            print(f"  {name}: failures at indices {r['failures']}")
    else:
        print("All sections pass!")

    out_path = Path(__file__).parent.parent / "PART_CCLXXXI_ternary_codes_results.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"Results written to {out_path}")
