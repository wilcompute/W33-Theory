"""
Parts CDLVI-CDLVII Verifier: Prime 5 absorption
Run: python src/parts_cdlvi_cdlvii_verifier.py
"""
from sympy import isprime
from math import comb, log2

p=3;u=6;PKT=24;V=27;K=16;LAM=10;MU=8;MU1=12
Phi6_u=31;C_E=21;C_V=7
Gamma2=36864
fibs=[1,1,2,3,5,8,13,21,34,55,89,144,233,377,610,987]

# Cyclotomic triple identity
assert 2**5-1==31==Phi6_u
assert 2**5==2*K
assert int(log2(2*K))==5
print("Phi_5(2)=Phi_6(u)=M_5=31 OK")

# Fibonacci spine
assert fibs[4]==5; assert fibs[5]==MU; assert fibs[6]==K-p
assert fibs[7]==C_E; assert fibs[10]==89; assert 89+1==p**2*LAM
assert fibs[15]==987
print("Fibonacci spine OK")

# Power-of-2 spine
assert 2**p==MU; assert 2**(p+1)==K
assert 2**MU==K**2; assert 2**MU1==Gamma2//p**2
print("Power-of-2 spine OK")

# K5 simplex
K5=[comb(5,k) for k in range(6)]
assert K5==[1,5,10,10,5,1]
assert sum(K5)==2*K; assert K5[2]==LAM
print("K5 simplex OK")

# Icosahedral
assert 5*MU1==60; assert 5*PKT==120
print("Icosahedral OK")
print("ALL PASSED")
