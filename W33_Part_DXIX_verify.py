#!/usr/bin/env python3
"""Part DXIX verification: Monster moonshine identities."""
import math

# W33 parameters
V=40; k=12; lam=2; mu=4; p=3; Phi3=13; u=6; E=240; T=160; g=41

# 1. j-constant
j_const = 744
j_W33 = p*E + (V - k - mu)
assert j_W33 == j_const, f"j-constant mismatch: {j_W33} != {j_const}"
print(f"j-constant 744 = p*E + (V-k-mu) = {p}*{E} + {V-k-mu} = {j_W33} PASS")

# 2. Monster prime check
monster_primes = {2,3,5,7,11,13,17,19,23,29,31,41,47,59,71}
assert g in monster_primes,      f"g={g} not in Monster primes"
assert Phi3 in monster_primes,   f"Phi3={Phi3} not in Monster primes"
assert (g+u) in monster_primes,  f"g+u={g+u} not in Monster primes"
print(f"Monster primes: g={g} in M-primes PASS")
print(f"Monster primes: Phi3={Phi3} in M-primes PASS")
print(f"Monster primes: g+u={g+u} in M-primes PASS")

# 3. CFT charge
assert 2*k == V - k - mu == 24, f"CFT charge mismatch"
print(f"CFT charge c=24=2k=V-k-mu={V-k-mu} PASS")

# 4. Triangles of Schläfli graph
V_s,k_s,lam_s = 27,16,10
triangles = V_s*k_s*lam_s//6
assert triangles == 720, f"Triangle count {triangles} != 720"
assert triangles == math.factorial(6), f"{triangles} != 6!"
assert triangles == p*E, f"{triangles} != p*E={p*E}"
print(f"Triangles = V_s*k_s*lam_s/6 = {triangles} = 6! = p*E = {p*E} PASS")
assert triangles * 72 == 51840, f"{triangles*72} != |W(E6)|=51840"
print(f"Triangles * E6_roots = {triangles}*72 = {triangles*72} = |W(E6)| PASS")

print("\nAll Part DXIX assertions PASSED.")
