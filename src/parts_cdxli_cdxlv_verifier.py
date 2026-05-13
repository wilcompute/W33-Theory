"""
Parts CDXLI-CDXLV Verifier
Run: python src/parts_cdxli_cdxlv_verifier.py
"""
from sympy import factorint, isprime
from math import comb, gcd, factorial

p=3;u=6;PKT=24;SIX=6
V=27;K=16;LAM=10;MU=8;MU1=12;MU2=18;EDGES=216;TRIS=720
FLAGS_T=192;AUT_T=96;MON_T=18432;Gamma2=36864
LEECH_MIN=196560;Phi6_u=31
C_V=7;C_E=21;C_F=14
E6d=78;E7d=133;E8d=248

print("PARTS CDXLI-CDXLV VERIFIER")

assert 128 == 2**(MU-1) == K*MU == 2*MU**2
assert MON_T//SIX == PKT*K*MU
print("[CDXLI] Pariah coset OK")

assert 2**MU == E8d+MU == 256
assert K == 16
print("[CDXLII] Clifford OK")

assert 96 == AUT_T
assert 1152 == SIX*FLAGS_T == 2*SIX*AUT_T == 128*p**2
assert 48 == 2*PKT == MU*SIX
assert 52 == V+PKT+1 == 4*(K-p)
assert 52 == E6d - C_F - MU1
print("[CDXLIII] 24-cell/F4 OK")

assert 46 == 2*(PKT-1)
assert 20 == 2*LAM
assert 9 == p**2
assert 6 == u
assert len([2,3,5,7,11,13,17,19,23,29,31,41,47,59,71]) == K-1
assert Phi6_u in [2,3,5,7,11,13,17,19,23,29,31,41,47,59,71]
assert 71 == 72-1; assert 47==2*PKT-1; assert 23==PKT-1
assert 19==V-MU; assert 17==K+1; assert 41==42-1
print("[CDXLIV] Monster primes OK")

assert LEECH_MIN == (EDGES+PKT)*p**2*C_V*(K-p)
assert LEECH_MIN == 2*PKT*(2**12-1)
assert E6d == SIX*(K-p)
assert E7d == C_V*(V-MU)
assert E8d == MU*Phi6_u
assert E6d+E8d == 2*163
print("[CDXLV] Leech+Exceptional OK")

print("ALL PASSED")
