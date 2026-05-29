#!/usr/bin/env python3
"""PART MCCCXII: Spectral entropy, moments, Fisher information for W(3,3)."""
from math import log, sqrt
r,q,F5,Phi3,v,k = 2,3,5,13,40,12
l1,l2 = 10,16
m1,m2 = 24,15
total = m1+m2  # = 39
p1 = m1/total  # 8/13
p2 = m2/total  # 5/13
print('SPECTRAL ENTROPY AND MOMENTS VERIFIER')
print('p1 =', p1, '= 8/13:', abs(p1-8/13)<1e-12)
print('p2 =', p2, '= 5/13:', abs(p2-5/13)<1e-12)
assert abs(p1 - r**q/Phi3) < 1e-12  # 8/13
assert abs(p2 - F5/Phi3) < 1e-12    # 5/13
print('Fibonacci decomposition of Phi3: r^q + F5 =', r**q, '+', F5, '=', r**q+F5, '== Phi3:', r**q+F5==Phi3)
# Entropy
H = -(p1*log(p1) + p2*log(p2))
H_bits = -(p1*log(p1,2) + p2*log(p2,2))
print('Shannon entropy (nats) =', H)
print('Shannon entropy (bits) =', H_bits)
print('Entropy < 1 bit:', H_bits < 1)
# Mean
mean = p1*l1 + p2*l2
print('Spectral mean =', mean, '= r^2*v/Phi3:', abs(mean - r**2*v/Phi3)<1e-10)
assert abs(mean - 160/13) < 1e-10
# Variance
var = p1*(l1-mean)**2 + p2*(l2-mean)**2
print('Variance =', var, '= 1440/169:', abs(var-1440/169)<1e-10)
assert abs(var - 1440/169) < 1e-10
assert abs(1440/169 - k*5040/169) < 1e-10  # k*Phi6!/Phi3^2
# Standard deviation
std = sqrt(var)
print('Std dev =', std, '= k*sqrt(l1)/Phi3:', abs(std - k*sqrt(l1)/Phi3)<1e-10)
assert abs(std - k*sqrt(l1)/Phi3) < 1e-10
# Fisher information
FI = 1/(p1*p2)
print('Fisher information =', FI, '= Phi3^2/v:', abs(FI - Phi3**2/v)<1e-10)
assert abs(FI - Phi3**2/v) < 1e-10
# KL from uniform
KL = p1*log(p1*2) + p2*log(p2*2)
print('KL from uniform (nats) =', KL)
print('ALL ENTROPY AND MOMENT IDENTITIES VERIFIED')
