#!/usr/bin/env python3
"""
PART MCDLX-MCDLXII: The Alpha-Inverse Polynomial

P(x) = x^4 + 2x^3 + x^2 - 2x - 1

Verified identities:
  P(q)    = P(3)    = 137 = alpha^-1  [PRIME]
  P(phi)  = 2*phi^4 (golden identity)
  P(2)    = 31      = M5 (Mersenne prime)
  P(p_Ih) = 17401   [PRIME]
  P(Phi6) = 3121    [PRIME]
"""
import math

q, g1, g2, m_r, m_s, v = 3, 21, 6, 24, 15, 40
k, chi, p_Ih, Phi6 = 12, 4, 11, 7
alpha_inv = 137
phi = (1 + math.sqrt(5)) / 2

def P(x):
    return x**4 + 2*x**3 + x**2 - 2*x - 1

# Factored form: (x^2 + x)^2 - (2x+1) = x^2(x+1)^2 - (2x+1)
# This is why k^2 - 2q - 1 = alpha^-1:
# k = chi*q = (q+1)*q, so k^2 = q^2*(q+1)^2
# P(q) = q^2*(q+1)^2 - 2q - 1 = k^2 - 2q - 1

assert P(q) == alpha_inv
assert P(2) == 31
assert P(1) == 1
assert abs(P(phi) - 2*phi**4) < 1e-9

def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0: return False
    return True

print("P(x) = x^4 + 2x^3 + x^2 - 2x - 1")
print(f"Factored: (x*(x+1))^2 - (2x+1)")
print()
for x, label in [(q,'q=3'),(2,'2'),(1,'1'),(chi,'chi=4'),(Phi6,'Phi6=7'),(p_Ih,'p_Ih=11'),(k,'k=12')]:
    pv = P(x)
    prime_flag = '[PRIME]' if is_prime(pv) else ''
    special = '= alpha^-1' if pv == alpha_inv else ''
    print(f"  P({label}) = {pv} {prime_flag} {special}")

print()
print(f"P(phi) = 2*phi^4 = {2*phi**4:.8f}")
print(f"P(phi) = 6*phi + 4 (exact rational-phi form)")

# K3 identities
print()
print("K3 Surface Identities:")
K3_chi, K3_sigma, K3_b2 = 24, -16, 22
print(f"  chi(K3) - sigma(K3) = {K3_chi} - ({K3_sigma}) = {K3_chi - K3_sigma} = v")
print(f"  chi(K3)    = {K3_chi} = m_r")
print(f"  chi(K3)/2  = {K3_chi//2} = k")
print(f"  sigma(K3)  = {K3_sigma} = -4*chi")
print(f"  b2(K3)     = {K3_b2} = k + Phi6 + q = {k}+{Phi6}+{q}")
print()

# Mathieu moonshine
coeff_M24 = 2*q*Phi6*p_Ih
print(f"Mathieu moonshine K3 coefficient: 462 = 2*q*Phi6*p_Ih = {coeff_M24}")

# CS TQFT
import math
def fib(n):
    a, b = 1, 1
    for _ in range(n - 1): a, b = b, a + b
    return a

print()
print(f"Chern-Simons SU(2) at level k={k}:")
print(f"  Primaries = k+1 = {k+1} = F(7) = {fib(7)}")
print(f"  F(7) = Fibonacci prime at index 7 = 2*chi-1")
print()

# Master cascade
print("Master Cascade (all verified):")
print(f"  q={q}")
print(f"  chi = q+1 = {chi}")
print(f"  k   = chi*q = {k}")
print(f"  E1  = v/chi = {v//chi}")
print(f"  m_r = 2*k   = {2*k}")
print(f"  j_i = k^3   = {k**3}")
assert chi==q+1 and k==chi*q and v//chi==10 and 2*k==m_r and k**3==1728
print("  ALL VERIFIED")
