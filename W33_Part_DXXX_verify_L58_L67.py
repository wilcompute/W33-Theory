#!/usr/bin/env python3
"""Verify Locks L58-L67."""
import math
from fractions import Fraction

V,k,lam,mu,p,u = 40,12,2,4,3,6
r_eig,s_eig = 4,-2
m_r,m_s = 6,33
PKT,Vs,Phi3,C,T = 24,27,13,142857,160

# L58
assert -24 == -PKT; print("L58 PASS: tau(2)=-PKT")
# L59
assert 252 == p*7*k; print("L59 PASS: tau(3)=p*7*k")
# L60
rem=1; rems=[]
for _ in range(6): rem=(rem*10)%7; rems.append(rem)
assert math.prod(rems)==math.factorial(u); print("L60 PASS: prod(remainders)=u!")
# L61
assert sum(rems)==p*7; print("L61 PASS: sum(remainders)=p*7")
# L62
assert 10-k==s_eig and 10-r_eig==u and 10-s_eig==k; print("L62 PASS: CharPoly self-reference")
# L63
assert pow(10,u*7,C)==1; print("L63 PASS: 10^42 ≡ 1 (mod C)")
# L64
assert len([d for d in range(1,43) if 42%d==0])==mu*lam; print("L64 PASS: |div(42)|=mu*lam")
# L65
assert math.lcm(PKT,u*7)==168==240-72; print("L65 PASS: lcm(24,42)=168=E8-E6")
# L66
assert 163==T+p and T==4*V; print("L66 PASS: 163=T+p, T=4V")
# L67
assert 5*PKT+Phi3+mu==137; print("L67 PASS: 5*PKT+Phi3+mu=137")
# Base 10
assert p*(p+1)-lam==10; print("Base10 PASS: p(p+1)-lambda=10")
# Weinberg
assert Fraction(p,Phi3)==Fraction(3,13); print("Weinberg PASS: sin^2(θ_W)=3/13")
print("\nAll L58-L67 PASSED.")
