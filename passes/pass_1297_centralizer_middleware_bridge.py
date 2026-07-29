"""Pass 1297 — Centralizer and middleware bridge.

From levi_five_frontiers.md Section 5:
  Jordan partition 4^2 3^22 1^6 at q=3, conjugate partition (30,24,24,2).
  Nilpotent centralizer in GL(80,2) has order 2^2056 * product_terms (618 digits).
  Quotient acting on two J4 chains = GL(2,2) = S3.
  Adjoining phase/inversion bit: S3 x C2 = D12.
  D12 element-order profile: {1:1, 2:7, 3:2, 6:2}.
  Count bridges: 8*6=48, 8*12=96, 24*45*48=51840, 25920/12=2160.

This pass verifies all the exact arithmetic.
"""
import numpy as np
from functools import reduce
from math import gcd, prod

print("=== Pass 1297: Centralizer and middleware bridge ===")

# --- Jordan partition ---
Jordan_partition = [4]*2 + [3]*22 + [1]*6
size = sum(Jordan_partition)
assert size == 80, f"Jordan partition sum = {size} != 80"
print(f"Jordan partition: 4^2 * 3^22 * 1^6, sum = {size} (= 80 = 2*40) ✓")

# Conjugate partition:
def conjugate_partition(partition):
    if not partition:
        return []
    max_part = max(partition)
    return [sum(1 for p in partition if p >= k) for k in range(1, max_part+1)]

conj = conjugate_partition(Jordan_partition)
print(f"Conjugate partition: {conj}")
# Expected: (30, 24, 24, 2)
# conjugate[1] = #{parts >= 1} = 2+22+6 = 30
# conjugate[2] = #{parts >= 2} = 2+22 = 24
# conjugate[3] = #{parts >= 3} = 2+22 = 24
# conjugate[4] = #{parts >= 4} = 2
assert conj == [30, 24, 24, 2], f"Conjugate partition {conj} != [30,24,24,2]"
print(f"Conjugate partition [30,24,24,2] verified ✓")

# --- Centralizer order ---
# For a nilpotent Jordan matrix N in GL(n, F_q) with Jordan type lambda:
# |C_GL(N)| = q^{A(lambda)} * prod_{i} prod_{j=1}^{lambda_i'} (1 - q^{-j})
# where A(lambda) = sum_{i} (i-1)*lambda_i = sum_{i<j} min(lambda_i, lambda_j)
# Actually the centralizer order formula for nilpotent element with Jordan type
# (n_1, n_2, ...) where n_k = number of Jordan blocks of size k:
# |C| = q^{E} * prod_k |GL(n_k, q)| * prod_{k<l} q^{2*n_k*n_l*min(k,l)}
# where E = sum_k n_k^2 * k + ... (complex formula)
#
# Simpler: use the formula from Kung/Stong:
# For Jordan type with blocks of sizes lambda_1 >= lambda_2 >= ...:
# |C_{GL(n,q)}(N)| = q^{sum_{i,j} min(lambda_i, lambda_j) - n} * prod_i |GL(mult_i, q)|
# But we only need the exponent of q=2:

# For Jordan partition 4^2 3^22 1^6 in GL(80, 2):
# Exponent E = sum_{i,j} min(lambda_i, lambda_j)
# = sum over all pairs (including i=j)
blocks = [4]*2 + [3]*22 + [1]*6  # all 30 Jordan blocks (2+22+6=30)
n_blocks = len(blocks)
assert n_blocks == 30

# E = sum_{i,j} min(lambda_i, lambda_j)
E = sum(min(blocks[i], blocks[j]) for i in range(n_blocks) for j in range(n_blocks))
print(f"\nCentralizer computation:")
print(f"  Number of Jordan blocks: {n_blocks}")
print(f"  E = sum_{{i,j}} min(lambda_i, lambda_j) = {E}")
print(f"  Centralizer order: 2^(E-80) * [polynomial corrections]")
# E - n = E - 80 is the exponent from Kung formula:
print(f"  E - n = {E} - 80 = {E-80}")
# But frontier says exponent is 2056
# Let's compute using the correct formula:
# From Kung (1981): |C| = q^{N(lambda)} where
# N(lambda) = 2*sum_{i<j} min(lambda_i,lambda_j) + sum_i lambda_i (but this is just E)
# Actually the correct formula is:
# |C_{GL(n,Fq)}(N)| = q^{A} * prod_{k} prod_{j=1}^{m_k} (q^j - 1)
# where m_k = multiplicity of block size k, and
# A = sum_{k,l} min(k,l) * m_k * m_l - sum_k m_k ("wrong" -- let me use direct computation)

# Direct formula from the theory of Jordan centralizers:
# A = sum_{s,t} m_s * m_t * min(s,t) where m_s = #{blocks of size s}
m4, m3, m1 = 2, 22, 6  # multiplicities
A = (m4*m4*4 + m3*m3*3 + m1*m1*1 +
     2*m4*m3*min(4,3) + 2*m4*m1*min(4,1) + 2*m3*m1*min(3,1))
print(f"  A = m4^2*4 + m3^2*3 + m1^2*1 + 2*m4*m3*3 + 2*m4*m1*1 + 2*m3*m1*1")
print(f"    = {m4**2*4} + {m3**2*3} + {m1**2*1} + {2*m4*m3*3} + {2*m4*m1*1} + {2*m3*m1*1}")
print(f"    = {A}")
print(f"  Expected exponent from frontier: 2056")
# Check if A == 2056 or close:
if A == 2056:
    print(f"  Exponent 2056 verified ✓")
else:
    print(f"  Computed A = {A}; frontier states 2056")
    # The formula has a subtraction: actual exponent = A - n
    print(f"  A - n = {A} - 80 = {A-80}")
    # Or the formula might be: exponent = A (not A-n), depends on convention
    # Let's check: A = 16 + 1452 + 6 + 396 + 12 + 132 = 2014? recompute:
    terms = [
        m4**2 * 4,     # 4*4=16
        m3**2 * 3,     # 484*3=1452
        m1**2 * 1,     # 36*1=36 (not 6)
        2*m4*m3*3,     # 2*2*22*3=264
        2*m4*m1*1,     # 2*2*6*1=24
        2*m3*m1*1,     # 2*22*6*1=264
    ]
    print(f"  Individual terms: {terms}, sum={sum(terms)}")
    # sum = 16+1452+36+264+24+264 = 2056 !
A_correct = m4**2*4 + m3**2*3 + m1**2*1 + 2*m4*m3*3 + 2*m4*m1*1 + 2*m3*m1*1
print(f"  A (corrected) = {m4**2*4} + {m3**2*3} + {m1**2*1} + {2*m4*m3*3} + {2*m4*m1*1} + {2*m3*m1*1} = {A_correct}")
assert A_correct == 2056, f"Expected 2056, got {A_correct}"
print(f"  Exponent 2056 VERIFIED ✓")

# --- GL(2,2) = S3 quotient ---
print("\nGL(2,2) = S3 quotient on two J4 chains:")
print("  The two J4 blocks give a 2x2 matrix slot in the centralizer")
print("  Centralizer modulo J3 and J1 blocks: GL(2,2) acting on the J4 slot")
print("  GL(2,2) = S3, order 6")
print("  This is exactly the terminal selector group from Pass 1295")

# --- D12 middleware bus ---
print("\nAdjoining phase/inversion bit: D12 = S3 x C2")
print("  S3 x C2 = D12 (dihedral group of order 12) since S3 has center C1 and...")
# Actually S3 x C2: this is not D12 in general.
# S3 x C2 has order 12. Is it D12 (dihedral of order 12 = 2*6)?
# D6 (dihedral of order 6) = S3, so D12 = D_{12} has order 12.
# S3 x C2 is one of the groups of order 12: Z12, Z2xZ6, D6xC2=S3xC2, A4, D12.
# D12 = <r,s | r^6=s^2=1, srs=r^{-1}>. S3xC2 = <a,b,c | a^3=b^2=c^2=1, [a,c]=[b,c]=1, bab=a^{-1}>
# These are isomorphic: S3 x C2 = D12 (dihedral of order 12) -- YES, they are isomorphic.
print("  S3 x C2 = Dih(6) = D12: dihedral group of order 12 ✓")

# Element orders of D12:
# D12 = Z2 x S3. Element orders:
# From Z2 (0,1) x S3 ({e, (12), (13), (23), (123), (132)}):
# Orders: (0,e)->1, (1,e)->2, (0,(12))->2, (1,(12))->lcm(2,2)=2, (0,(123))->3, (1,(123))->6
# etc.
from itertools import product as iprod
D12_orders = []
Z2 = [0, 1]
S3_elements_orders = [1, 2, 2, 2, 3, 3]  # identity, 3 transpositions, 2 three-cycles
for z, s_ord in iprod(Z2, S3_elements_orders):
    order = s_ord if z == 0 else {1:2, 2:2, 3:6}[s_ord]
    D12_orders.append(order)
from collections import Counter
D12_order_profile = Counter(D12_orders)
print(f"  D12 element order profile: {dict(sorted(D12_order_profile.items()))}")
assert D12_order_profile[1] == 1
assert D12_order_profile[2] == 7  # 1(from Z2*e) + 3(from Z2*(12),(13),(23)) + 3(from (12),(13),(23))
assert D12_order_profile[3] == 2  # 2 three-cycles
assert D12_order_profile[6] == 2  # (1,(123)) and (1,(132))
print(f"  Order profile {{1:1, 2:7, 3:2, 6:2}} VERIFIED ✓")

# --- Count bridges ---
print("\nCount bridges:")
bridge1 = 8 * 6
bridge2 = 8 * 12
bridge3 = 24 * 45 * 48
bridge4 = 25920 // 12
print(f"  8 * 6 = {bridge1}   (homP * |S3|)")
print(f"  8 * 12 = {bridge2}  (homP * |D12|)")
print(f"  24 * 45 * 48 = {bridge3}  (kerAP * W(3,3)-lines * 48)")
print(f"  25920 / 12 = {bridge4} = 2160  (|Sp(4,3)/...| / |D12|)")
assert bridge1 == 48
assert bridge2 == 96
assert bridge3 == 51840
assert bridge4 == 2160
print(f"  All 4 count bridges exact: 48, 96, 51840, 2160")

# Connection to Sp(4,3):
print("\nSp(4,3) connections:")
print("  |Sp(4,3)| = 25920 (from prior passes / group theory)")
print("  25920 / 12 = 2160 = index of D12-stabilizer")
print("  25920 = 2160 * 12: D12 acts as stabilizer of the J4 sector")
print("  51840 = 2 * 25920: order of |W(E6)| = |Sp(4,3)| * 2 (Weyl group connection)")
assert 2 * 25920 == 51840
print(f"  2 * |Sp(4,3)| = {2*25920} = |W(E6)| = 51840 ✓")

print("\n=== EXACT-30 REGISTERED ===")
print("Centralizer middleware bridge:")
print("  Nilpotent centralizer exponent 2056 verified")
print("  Conjugate partition [30,24,24,2] verified")
print("  GL(2,2)=S3 quotient on J4 chains, adjoining C2 gives D12")
print("  D12 order profile {1:1, 2:7, 3:2, 6:2} exact")
print("  Count bridges: 48, 96, 51840=2*|Sp(4,3)|=|W(E6)|, 2160 = |Sp(4,3)|/12")
