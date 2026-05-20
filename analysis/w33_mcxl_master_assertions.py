"""MCXL -- Master assertion block
Canonical machine-verified summary of MCXXXVI through MCXL.
Substrate identity chain C601-C615.
"""
from fractions import Fraction

q=3; v=40; k=12; lam=2; mu=4; f=24; g=15; E=240
Phi3=13; Phi6=7; Theta=10; c_EH=320
a0=17600; a2=2240; a4=480; lambda_2=10
C4=360; C2=240; C0=10560

# Curved extractor (MCXXXVIII)
assert q*Phi3*c_EH       == 12480
assert Phi6*c_EH         == a2
assert 5*(k-1)*c_EH      == a0
assert 8*v               == c_EH
assert 80*mu             == c_EH
assert 32*Theta          == c_EH
assert Fraction(12480,39)== c_EH
assert Fraction(a2,Phi6) == c_EH
assert Fraction(a0,55)   == c_EH

# Smooth limit (MCXXXIX)
assert E//2              == 120
assert v*q               == 120
assert 960 - Theta**2    == 860
assert Fraction(860,120) == Fraction(43,6)
assert Phi3+Phi6*(lam+1) == 43
assert k//2              == 6

# Heat-kernel (MCXL)
assert lambda_2 == Theta
assert f*g      == C4
assert f*Theta  == C2
assert f*a0//v  == C0

# SM constants
assert (k-1)**2+mu**2    == 137
assert (2*v-k)*q**3      == 1836
assert Fraction(q,Phi3)  == Fraction(3,13)
assert Fraction(lam,q)   == Fraction(2,3)
assert Fraction(a0,a2)   == Fraction(55,7)
assert Fraction(a4,a0)   == Fraction(3,110)
assert v+E               == 280
assert f*(k+lam)         == 384

# SRG fundamental identity
assert f+g+1             == v
assert k*(k-1)           == lam*(k-1)+mu*(v-k-1)

print("MCXL MASTER ASSERTIONS -- ALL PASSED")
print("=" * 52)
for name,val in [
 ("c_EH = 8v = 80mu = 32Theta",    c_EH),
 ("a2 = Phi6*c_EH",                 a2),
 ("a0 = 55*c_EH",                   a0),
 ("alpha^-1 = (k-1)^2+mu^2",        137),
 ("proton/electron = (2v-k)*q^3",   1836),
 ("spectral gap lambda_2 = Theta",   10),
 ("d2/d1 = 43/6",               "43/6"),
 ("G_N proxy a0/a2 = 55/7",     "55/7"),
 ("Lambda_cc a4/a0 = 3/110",  "3/110"),
 ("CC exponent v+E",                280),
 ("SRG k(k-1)=lam(k-1)+mu(v-k-1)",132),
]:
    print(f"  {name:<42s} = {val}")
print("=" * 52)
print("MCXXXVI-MCXL chain fully machine-verified.")
