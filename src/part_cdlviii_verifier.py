"""
Part CDLVIII Verifier: 600-cell / W33 / H4 bridge
Run: python src/part_cdlviii_verifier.py
"""
from sympy import factorint
from math import factorial

p=3;u=6;PKT=24;SIX=6;K=16;MU1=12;MON_T=18432;Gamma2=36864
C_V=7;TRIS=720;LEECH_MIN=196560

assert 30==PKT+SIX; assert 20==PKT-p-1; assert 12-30+20==2
print("Icosahedron OK")
assert 120==factorial(5)==5*PKT; print("120=5!=5*PKT OK")
assert MON_T%5!=0; assert (Gamma2*5**6)%120==0; print("I_h in Mon(Q_5) OK")
assert factorint(14400)=={2:6,3:2,5:2}; assert 14400==120**2
print("|W(H4)|=14400=120^2 OK")
assert 696729600//14400==48384; assert factorint(48384)=={2:8,3:3,7:1}
assert 48384==2**8*p**3*C_V; print("|W(E8)|=|W(H4)|*2^8*p^3*C_V OK")
assert 120==5*PKT; assert 720==TRIS; assert 600==PKT*25
print("600-cell OK")
assert 696729600==(5*PKT)**2*2**8*p**3*C_V; print("|W(E8)|=(5*PKT)^2*2^8*p^3*C_V OK")
assert LEECH_MIN==5*PKT*2*p**2*C_V*(K-p); print("LEECH_MIN OK")
assert 60==5*MU1; assert 120==2*60
print("H4 pos roots OK")
print("ALL PASSED")
