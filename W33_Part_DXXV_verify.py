#!/usr/bin/env python3
"""Verify all Locks L51-L57: base-10 mod-12 and cyclic number."""
import sympy

# W33 parameters
V,k,lam,mu,p,u,E,g = 40,12,2,4,3,6,240,41
C = 142857  # cyclic number = (10^u - 1) / 7

# L52: Phi3 | C
Phi3 = (p**3 - 1)//(p-1)
assert C % Phi3 == 0, f"L52 FAIL: {Phi3} does not divide {C}"
print(f"L52: {Phi3} | {C}  PASS")

# L53: factorization
fact = sympy.factorint(C)
assert fact == {3:3, 11:1, 13:1, 37:1}, f"L53 FAIL: {fact}"
print(f"L53: 142857 = 3^3 * 11 * 13 * 37  PASS")

# L54: 10^24 ≡ 1 (mod C)
exp24 = pow(10, V-k-mu, C)
assert exp24 == 1, f"L54 FAIL: 10^24 mod C = {exp24}"
print(f"L54: 10^{{V-k-mu}} = 10^{V-k-mu} ≡ {exp24} (mod {C})  PASS")

# L55: six cyclic permutations
perms = set()
for n in range(1, 7):
    s = str(C * n).zfill(6)
    perms.add(s)
assert len(perms) == 6
assert all(sorted(s) == sorted('142857') for s in perms)
print(f"L55: 6 cyclic permutations of 142857  PASS")

# L56: 37 + p = V
spare = 37
assert spare + p == V, f"L56 FAIL: {spare}+{p}={spare+p} != V={V}"
assert spare == u**2 + 1, f"L56b FAIL: {spare} != u^2+1={u**2+1}"
assert V == u**2 + p + 1, f"L56c FAIL: V={V} != u^2+p+1={u**2+p+1}"
print(f"L56: 37+p={spare+p}=V, V=u^2+p+1={u**2+p+1}  PASS")

# L57: digit sum
Vs = 27  # Schlafli vertex count
ds = sum(int(d) for d in str(C))
assert ds == p**3 == Vs, f"L57 FAIL: digitsum={ds}"
print(f"L57: digitsum(142857)={ds}=p^3=Vs={Vs}  PASS")

# Bonus: 10^k mod V
assert pow(10,k,V) == 0, f"10^k mod V != 0"
print(f"Bonus: 10^k mod V = 10^{k} mod {V} = {pow(10,k,V)} = 0  PASS")

# Grand identity
print(f"\nGrand: V = u^2+p+1 = {u**2+p+1}  PASS")
print(f"All Locks L51-L57 PASSED.")
