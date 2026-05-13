"""
Parts CDXXXVI-CDXL Verifier
Run: python src/parts_cdxxxvi_cdxl_verifier.py
"""
from sympy import factorint, isprime
from math import comb, gcd, factorial

p=3;u=6;PKT=24;SIX=6
V=27;K=16;LAM=10;MU=8;MU1=12;MU2=18;EDGES=216;TRIS=720
FLAGS_T=192;AUT_T=96;MON_T=18432;Gamma2=36864
LEECH_MIN=196560;c1=196884;c0=744;Phi6_u=31
C_V=7;C_E=21;C_F=14

print("PARTS CDXXXVI-CDXL VERIFIER")
print("="*50)

print("[CDXXXVI] Mon(T) anatomy")
assert MON_T == AUT_T * FLAGS_T
assert factorint(MON_T) == {2:11, 3:2}
assert MON_T == PKT**2 * 2*K
assert MON_T == u**2 * 2**9
assert MON_T == 2**8 * 72
assert 2**8 == 248+MU
assert Gamma2 == FLAGS_T**2
print("  OK")

print("[CDXXXVII] EDGES+PKT=E8, TRIS=6!")
assert EDGES+PKT == 240
assert TRIS == (EDGES+PKT)*p
assert TRIS == factorial(SIX)
print("  OK")

print("[CDXXXVIII] Csaszar-G2")
assert C_V-C_E+C_F == 0
assert C_V == MU-1
assert C_E == comb(C_V,2)
assert C_F == SIX+MU == K-2
assert gcd(42, MON_T) == SIX
print("  OK")

print("[CDXXXIX] Sporadic split")
assert V == C_V + 2*LAM
assert SIX + 2*LAM == V-1 == 26
assert C_E*72 == C_V*EDGES
print("  OK")

print("\nALL PASSED")
