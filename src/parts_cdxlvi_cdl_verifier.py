"""
Parts CDXLVI-CDL Verifier
Run: python src/parts_cdxlvi_cdl_verifier.py
"""
from sympy import factorint, isprime
from math import comb, gcd, factorial

p=3;u=6;PKT=24;SIX=6
V=27;K=16;LAM=10;MU=8;MU1=12;MU2=18;EDGES=216;TRIS=720
FLAGS_T=192;AUT_T=96;MON_T=18432;Gamma2=36864
LEECH_MIN=196560;Phi6_u=31
C_V=7;C_E=21;C_F=14
E6d=78;E7d=133;E8d=248;G2d=14;F4d=52

print("PARTS CDXLVI-CDL VERIFIER")
print("="*50)

print("[CDXLVI] Magic square")
diag=[3,16,66,248]
offdiag=[8,21,52,35,78,133]
magic_total=sum(diag)+2*sum(offdiag)
assert magic_total==987
assert 987==p*C_V*(2*PKT-1)
fib=[1,1]
while len(fib)<17: fib.append(fib[-1]+fib[-2])
assert fib[15]==987
assert diag[1]==K; assert comb(MU1,2)==66
assert sum(diag)==333==p**2*(PKT+K-p)
print("  OK")

print("[CDXLVII] E6 chain")
assert E6d==F4d+G2d+MU1
assert E6d-F4d==V-1==26
assert G2d+MU1==V-1
assert 26==SIX+2*LAM
print("  OK")

print("[CDXLVIII] E7/E8")
assert E7d==E6d+2*V+1
assert 56==V+K+LAM+p
assert E7d==E6d+56-1
assert 126==2*p**2*C_V
assert 240==126+K*C_V+2
assert 240==C_V*(2*p**2+K)+2
print("  OK")

print("[CDXLIX-CDL] Closure")
assert SIX*u**2==EDGES
assert K**2-K+1==241
assert isprime(241)
assert 241==(EDGES+PKT)+1
assert MU1==p*4; assert MU2==p*SIX
assert 8-4+2==SIX
print("  OK")

print("ALL PASSED")
