"""
Parts CDXXXI–CDXXXV Verifier
31=Phi_6(u), Monster classes, 196884, Phi_6 chain, E-tower.

Run: python src/parts_cdxxxi_cdxxxv_verifier.py
"""
from sympy import factorint, isprime
from math import comb

print("=" * 60)
print("PARTS CDXXXI-CDXXXV VERIFIER")
print("=" * 60)

p=3;u=6;PKT=24;V=27;K=16;LAM=10;MU=8;MU1=12;MU2=18
EDGES=216;FLAGS_T=192;E6r=72;E8r=240
LEECH_MIN=196560;c1=196884;c0=744

print("\n[CDXXXI] Prime 31 = Phi_6(u)")
assert u**2-u+1 == 31
assert isprime(31)
assert 31%3 == 1
assert 6**2 - 6*1 + 1**2 == 31
assert LAM+MU2+p == 31
assert PKT+MU-1 == 31
assert V+K-MU1 == 31
assert c0 == PKT*31
assert 248 == MU*31
assert 496 == K*31
assert MU+K == PKT
print("  All 31/Phi_6 identities  OK")

print("\n[CDXXXII] Monster classes")
assert FLAGS_T+2 == 194
assert 8*PKT+2 == 194
assert 194 == 2*(4*PKT+1)
assert isprime(97) and 4*PKT+1==97
print("  Monster classes  OK")

print("\n[CDXXXIII] 196884")
assert isprime(1823)
assert c1 == 4*V*1823
assert 1823 == 4*(V-MU)*PKT-1
assert c1 == 4*V*(4*(V-MU)*PKT-1)
assert c1-LEECH_MIN == MU2**2
print("  196884 decomposition  OK")

print("\n[CDXXXIV-CDXXXV] Phi_6 chain and E-tower")
assert 2**2-2+1 == p
assert p**2-p+1 == 7 == MU-1
assert u**2-u+1 == 31
assert 7**2-7+1 == 43
assert isprime(43)
E6d=78; E7d=133; E8d=248
assert E8d+E6d == 326 == 2*163
assert isprime(163)
assert E8d-E6d == LAM*17
assert E8d-E7d == 5*(PKT-1)
assert E8d == 2**8-MU
assert E8d == MU*(u**2-u+1)
print("  Phi_6 chain and E-tower  OK")

print("\nALL VERIFICATIONS PASSED  checkmark")
