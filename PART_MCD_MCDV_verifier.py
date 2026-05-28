"""MCD-MCDV: Fifth root of unity and W(3,3) — verified."""
import math, cmath
from fractions import Fraction

q, g1, g2, m_r, m_s, v = 3, 21, 6, 24, 15, 40
E1, E2, p_Ih, Phi6, chi = 10, 16, 11, 7, 4
phi = (1 + math.sqrt(5)) / 2
phi_prime = (1 - math.sqrt(5)) / 2

print("MCD-MCDV VERIFICATION")
print()

# MCD: p_Ih = sqrt(Phi_5(q))
Phi5_q = q**4 + q**3 + q**2 + q + 1
assert Phi5_q == p_Ih**2, f"{Phi5_q} != {p_Ih**2}"
print(f"MCD: Phi_5(q) = {Phi5_q} = p_Ih^2 = {p_Ih}^2  PASS")

# MCDI: cyclotomic values
assert q**2 + 1 == E1
assert q + 1 == chi
assert q**2 - q + 1 == Phi6
print(f"MCDI: Phi_4(q)=E1={E1}, Phi_2(q)=chi={chi}, Phi_6(q)=Phi6={Phi6}  PASS")

# MCDII: [Q(zeta_5):Q] = chi
assert (5-1) == chi  # phi(5) = 4 = chi
print(f"MCDII: [Q(zeta_5):Q] = phi(5) = 4 = chi  PASS")

# Norm N_{Q(sqrt5)/Q}(3-phi) = 5
norm = (3 - phi) * (3 - phi_prime)
assert abs(norm - 5) < 1e-10
print(f"MCDII: N(3-phi) = {norm:.4f} = 5  PASS")

# MCDIII: D^2 = chi + 2*phi
D2 = 1 + phi**2 + phi**2 + 1  # quantum dims: 1, phi, phi, 1
assert abs(D2 - (chi + 2*phi)) < 1e-10
print(f"MCDIII: D^2 = {D2:.6f} = chi + 2*phi = {chi+2*phi:.6f}  PASS")

# MCDIV: D^2 * sqrt(5) = E1 * phi
lhs = D2 * math.sqrt(5)
rhs = E1 * phi
assert abs(lhs - rhs) < 1e-9
print(f"MCDIV: D^2 * sqrt(5) = E1 * phi = {rhs:.6f}  PASS")

# MCDV: Fibonacci convergent chain
assert Fraction(g2, chi) == Fraction(3, 2)   # F(4)/F(3)
assert Fraction(E1, g2) == Fraction(5, 3)    # F(5)/F(4)
assert Fraction(E2, E1) == Fraction(8, 5)    # F(6)/F(5)
print(f"MCDV: g2/chi=3/2, E1/g2=5/3, E2/E1=8/5 = F(n+1)/F(n)  PASS")

# Icosahedral: order of 2I = 120 = (q+2)!
assert math.factorial(q+2) == 120
print(f"BONUS: |2I| = (q+2)! = 5! = {math.factorial(q+2)} = 120  PASS")
assert math.factorial(q+2) == 2 * 60  # 2I is double cover of I (order 60)
print(f"BONUS: |I| = 60 = chi * m_s = {chi} * {m_s} = {chi*m_s}  PASS")

print()
print("ALL MCD-MCDV CHECKS PASS")
