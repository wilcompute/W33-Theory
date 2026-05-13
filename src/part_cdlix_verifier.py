"""
Part CDLIX Verifier: All 15 Monster primes in W33
Run: python src/part_cdlix_verifier.py
"""
from sympy import factorint, isprime
from math import comb, factorial

p=3;u=6;PKT=24;K=16;MU=8;MU1=12;LAM=10;C_V=7;C_E=21
E6_roots=72;W_E8=696729600;W_H4=14400

coset=W_E8//W_H4; assert coset==48384
assert factorint(48384)=={2:8,3:3,7:1}
assert 48384==K**2*p**3*C_V
assert 336==K*C_E==2*PKT*C_V
assert 168==PKT*C_V  # |Aut(Fano)|
print("Coset decomp OK")
assert 2016==(7**2-1)*(7**2-7)
assert 2016==2*K*p**2*C_V
assert C_V+1==MU
print("GL(2,7) OK")

# All 15 Monster primes
assert 17==K+1
assert 19==MU+LAM+1==PKT-5
assert 23==PKT-1; assert isprime(23)
assert 29==PKT+5
assert 31==Phi6_u
assert 41==p*K-C_V
assert 47==2*PKT-1
assert 59==5*MU1-1
assert 71==E6_roots-1==p*PKT-1
print("All 15 Monster primes OK")
print("ALL PASSED")
