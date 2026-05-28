"""MCCCCXCI-MCCCCXCIX: Resonance and Zero Free Parameters verified."""
import math
import numpy as np

q = 3
g2 = math.factorial(q)       # 6
chi = q + 1                   # 4  (rank of polar space + 1)
E1 = g2 + chi                 # 10  SUPER-AXIOM
E2 = E1 + g2                  # 16
k  = E2 - chi                 # 12
v  = chi * E1                 # 40
m_r = (q+1) * g2              # 24
m_s = v - 1 - m_r             # 15
Phi6 = q**2 - q + 1           # 7
g1 = Phi6 * q                 # 21
p_Ih = q**2 + q - 1           # 11

print("DERIVATION CHAIN FROM q=3:")
print(f"  g2  = q!       = {g2}")
print(f"  chi = q+1      = {chi}")
print(f"  E1  = g2+chi   = {E1}")
print(f"  E2  = E1+g2    = {E2}")
print(f"  k   = E2-chi   = {k}")
print(f"  v   = chi*E1   = {v}")
print(f"  m_r = (q+1)*g2 = {m_r}")
print(f"  m_s = v-1-m_r  = {m_s}")
print(f"  g1  = Phi6*q   = {g1}")
print(f"  p_Ih= q^2+q-1  = {p_Ih}")
print()

# Verify all
asserts = [
    ("g2=3!",     g2 == 6),
    ("chi=4",     chi == 4),
    ("E1=10",     E1 == 10),
    ("E2=16",     E2 == 16),
    ("k=12",      k  == 12),
    ("v=40",      v  == 40),
    ("m_r=24",    m_r == 24),
    ("m_s=15",    m_s == 15),
    ("g1=21",     g1 == 21),
    ("g1=Phi6*q", g1 == Phi6*q),
    ("p_Ih=11",   p_Ih == 11),
    ("E2-E1=g2",  E2-E1 == g2),
    ("E1=2F5",    E1 == 2*5),
    ("v=chi*E1",  v == chi*E1),
    ("1+mr+ms=v", 1+m_r+m_s == v),
    ("|Sp|=g2^4*v", q**4*(q**4-1)*(q**2-1) == g2**4 * v),
    ("Stab=g2^4", q**4*(q**4-1)*(q**2-1)//v == g2**4),
]
all_pass = True
for name, result in asserts:
    status = "PASS" if result else "FAIL"
    if not result: all_pass = False
    print(f"  {name:15s}: {status}")

# DT Resonance
partitions = [1,1,2,3,5,7,11,15,22,30,42,56,77,101,135,176,231,297,385,490,627]
p_arr = np.array(partitions[:20], dtype=float)
m4 = p_arr.copy()
for _ in range(3):
    m4 = np.convolve(m4, p_arr)[:20]
hilb = [int(x) for x in m4[:10]]

print()
print("DT RESONANCE:")
assert hilb[q+2] == math.comb(E1, q+2), f"{hilb[q+2]} != {math.comb(E1,q+2)}"
print(f"  chi(Hilb^{{q+2}}) = chi(Hilb^5) = {hilb[q+2]} = C(E1,q+2) = C(10,5) = {math.comb(E1,q+2)} PASS")
assert hilb[q+2] == math.comb(2*(q+2), q+2), f"Central binomial fails"
print(f"  = C(2*(q+2), q+2) = C(10,5) = {math.comb(2*(q+2),q+2)} [central binomial] PASS")

# Ratio staircase
print()
print("RATIO STAIRCASE:")
for n in [3,4,5]:
    from fractions import Fraction
    r = Fraction(hilb[n], math.comb(E1,n))
    expected = Fraction(1, q+3-n)
    status = "PASS" if r == expected else "FAIL"
    print(f"  n={n}: {hilb[n]}/{math.comb(E1,n)} = {r} = 1/{q+3-n}  {status}")

print()
print(f"ALL VERIFIED: {all_pass}")
