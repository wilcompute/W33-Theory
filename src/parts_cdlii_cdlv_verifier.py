"""
Parts CDLII-CDLV Verifier
Run: python src/parts_cdlii_cdlv_verifier.py
"""
from sympy import isprime
from math import comb

p=3;u=6;PKT=24;SIX=6;V=27;K=16;LAM=10;MU=8;MU1=12
FLAGS_T=192;MON_T=18432;Gamma2=36864
LEECH_MIN=196560;c1=196884;c0=744;Phi6_u=31
C_V=7;E6d=78;E8d=248;E6_roots=72;E8_roots=240

print("PARTS CDLII-CDLV VERIFIER")
print("="*50)

print("[CDLII] Golay WE")
assert 11==LAM+1
assert 759==p*(LAM+1)*(PKT-1)
assert 2576==K*C_V*(PKT-1)
print("  OK")

print("[CDLIII] Mathieu groups")
assert 244823040==2**10*p**3*5*C_V*(LAM+1)*(PKT-1)
assert 95040==2**6*p**3*5*(LAM+1)
assert 7920==2**4*p**2*5*(LAM+1)
print("  OK")

print("[CDLIV] Heterotic")
assert 496==2*E8d==K*(2*K-1)==K*Phi6_u==2*MU*Phi6_u
assert 2*K-1==Phi6_u
print("  OK")

print("[CDLV] Tower")
assert V-1==26; assert LAM==10; assert LAM+1==11; assert MU1==12
assert V-1-LAM==K
assert V-K==LAM+1
assert K-MU==MU
assert V-PKT==p
assert MU1-MU==p+1
assert MU1==p+LAM-1
assert 4==p+1
assert PKT==24; assert isprime(PKT-1)
print("  OK")

print("ALL PASSED")
