#!/usr/bin/env python3
"""
PART MCCCVII: E6 / 27-Line Cubic Surface Verification
Verifies all identities from BREAKTHROUGH_MCCCXXI_MCCCXXVII.
"""
import math

# W(3,3) constants
q=3; r=2; k=12; v=40; g1=21; g2=6
lambda1=10; lambda2=16
Phi3=13; Phi6=7; p_Ih=11; F5=5

# E6 data
E6_exponents = [1, 4, 5, 7, 8, 11]
E6_coxeter = 12
E6_weyl_order = 51840
E6_rank = 6
cubic_lines = 27
cubic_tritangents = 45
cubic_double_sixes = 36

print("=" * 60)
print("E6 / 27-LINE CUBIC SURFACE — W(3,3) VERIFICATION")
print("=" * 60)

print("\n--- THEOREM MCCCXXI: Cubic Surface Vertex Identity ---")
print(f"  cubic_lines + Phi3(q) = {cubic_lines} + {Phi3} = {cubic_lines + Phi3} = v = {v}?")
print(f"  {cubic_lines + Phi3 == v}")
print(f"  cubic_lines = q^3 = {q}^3 = {q**3}? {cubic_lines == q**3}")

print("\n--- THEOREM MCCCXXII: Weyl Group Factorization ---")
fact_r = r**Phi6
fact_q = q**4
fact_F5 = F5
product = fact_r * fact_q * fact_F5
print(f"  r^Phi6 = {r}^{Phi6} = {fact_r}")
print(f"  q^4 = {q}^4 = {fact_q}")
print(f"  F5 = {fact_F5}")
print(f"  r^Phi6 * q^4 * F5 = {product} = |W(E6)| = {E6_weyl_order}? {product == E6_weyl_order}")

print("\n--- THEOREM MCCCXXIII: E6 Exponents ---")
exp_sum = sum(E6_exponents)
exp_prod = math.prod(E6_exponents)
print(f"  E6 exponents: {E6_exponents}")
print(f"  Sum = {exp_sum} = g2^2 = {g2}^2 = {g2**2}? {exp_sum == g2**2}")
print(f"  Product = {exp_prod}")
fact_prod = r**5 * F5 * Phi6 * p_Ih
print(f"  r^5 * F5 * Phi6 * p_Ih = {r**5}*{F5}*{Phi6}*{p_Ih} = {fact_prod}? {exp_prod == fact_prod}")

print("\n  Exponent identification:")
identities = [
    (1,  '1 = identity'),
    (4,  f'4 = r^2 = {r**2}'),
    (5,  f'5 = F5 = {F5}'),
    (7,  f'7 = Phi6 = {Phi6}'),
    (8,  f'8 = r^q = {r**q}'),
    (11, f'11 = p_Ih = {p_Ih}'),
]
for e, label in identities:
    print(f"    {e}: {label}  in E6 exponents? {e in E6_exponents}")

print("\n--- THEOREM MCCCXXIV: Coxeter Number ---")
print(f"  h(E6) = {E6_coxeter} = k = {k}? {E6_coxeter == k}")
print(f"  max_exp - min_exp = {max(E6_exponents)} - {min(E6_exponents)} = {max(E6_exponents)-min(E6_exponents)} = lambda1 = {lambda1}? {max(E6_exponents)-min(E6_exponents) == lambda1}")
print(f"  (max+min)/2 = ({max(E6_exponents)}+{min(E6_exponents)})/2 = {(max(E6_exponents)+min(E6_exponents))/2} = g2 = {g2}? {(max(E6_exponents)+min(E6_exponents))/2 == g2}")

print("\n--- THEOREM MCCCXXV: Tritangent Planes ---")
from math import comb
tritangent_via_C = comb(lambda1, 2)
print(f"  C(lambda1, 2) = C({lambda1}, 2) = {tritangent_via_C} = cubic_tritangents = {cubic_tritangents}? {tritangent_via_C == cubic_tritangents}")

print("\n--- THEOREM MCCCXXVI: Double-Sixes ---")
print(f"  g2^2 = {g2}^2 = {g2**2} = double_sixes = {cubic_double_sixes}? {g2**2 == cubic_double_sixes}")
from math import comb
print(f"  C(q^2, 2) = C({q**2}, 2) = {comb(q**2, 2)} = double_sixes = {cubic_double_sixes}? {comb(q**2,2) == cubic_double_sixes}")

print("\n--- THEOREM MCCCXXVII: E6 Rank ---")
print(f"  rank(E6) = {E6_rank} = g2 = {g2}? {E6_rank == g2}")

print("\n=" * 60)
print("ALL IDENTITIES VERIFIED" if all([
    cubic_lines + Phi3 == v,
    cubic_lines == q**3,
    product == E6_weyl_order,
    exp_sum == g2**2,
    exp_prod == fact_prod,
    E6_coxeter == k,
    max(E6_exponents)-min(E6_exponents) == lambda1,
    tritangent_via_C == cubic_tritangents,
    g2**2 == cubic_double_sixes,
    E6_rank == g2,
]) else "SOME IDENTITIES FAILED")
