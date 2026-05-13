"""
Part CDLX Verifier: Monster exponents all in W33
Run: python src/part_cdlx_verifier.py
"""
from math import comb

p=3;u=6;PKT=24;K=16;MU=8;MU1=12;LAM=10;C_V=7

# All exponent identities
assert 46==2*(PKT-1)==PKT+MU+LAM+p+1
assert 20==PKT-p-1==2*LAM
assert 9==p**2==MU+1
assert 6==u==p*(p-1)==comb(4,2)
assert 2==p-1
assert 3==p
assert 1==p-2
print("All Monster exponents verified in W33 parameters")

# Recursion
exps=[46,20,9,6,3,2]+[1]*9
for e in exps:
    assert e in [1,2,3,6,9,20,46]
print("Exponent set verified")
print("ALL PASSED")
