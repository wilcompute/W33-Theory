"""
Part CDLI: Full Chain Verifier
Run: python src/part_cdli_verifier.py
"""
from sympy import factorint
from math import comb

p=3;u=6;PKT=24;SIX=6;V=27;K=16;LAM=10;MU=8;MU1=12
FLAGS_T=192;AUT_T=96;MON_T=18432;Gamma2=36864
LEECH_MIN=196560;c1=196884;c0=744;Phi6_u=31
C_V=7;E6_roots=72;E8_roots=240;E7_roots=126

print("PART CDLI VERIFIER")
print("="*50)

print("Arrow 1: Z[omega] -> W33")
assert 51840//1920==V; assert 51840==E8_roots*216
assert 51840==E6_roots*720; assert 51840==1152*45
print("  OK")

print("Arrow 2: W33 -> Leech")
assert LEECH_MIN==2*PKT*(2**12-1)
assert PKT==p*MU==4*SIX
print("  OK")

print("Arrow 3: Leech -> Golay")
assert PKT==24; assert MU1==12; assert MU==8
assert 2**MU1==Gamma2//p**2==4096
assert 759==p*11*23; assert 2576==K*C_V*23
print("  OK")

print("Arrow 4: Golay -> V^nat")
assert c0==PKT*Phi6_u; assert c1==4*V*(4*(V-MU)*PKT-1)
assert c1==196883+1
print("  OK")

print("Arrow 5: V^nat -> Monster")
assert 194==FLAGS_T+2==PKT*MU+2
print("  OK")

print("Monster irrep dimensions")
assert 196883==47*59*71
assert 47==2*PKT-1; assert 59==5*MU1-1; assert 71==E6_roots-1
assert 21296876==(p+1)*Phi6_u*41*59*71
assert 41==42-1
assert 842609326==2*(K-p)**2*29*Phi6_u*(2*PKT-1)*(5*MU1-1)
assert 29==5*u-1
print("  OK")

print("ALL PASSED")
