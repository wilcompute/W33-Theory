"""
Part CDLXI Verifier: Monster order as closed-form in {p, u, PKT}
Run: python src/part_cdlxi_verifier.py
"""
from sympy import factorint

p=3; u=6; PKT=24

# Derived
K=2**(p+1); LAM=K-u; C_V=u+1; MU=2**p; MU1=p+K-u-1

# Verify derivations
assert K==16; assert LAM==10; assert C_V==7; assert MU==8; assert MU1==12

# Monster order
M = 2**46*3**20*5**9*7**6*11**2*13**3*17*19*23*29*31*41*47*59*71

# 3-variable closed form
M_formula = (
    2**(2*(PKT-1)) *
    p**(2*(2**(p+1)-u)) *
    (u-1)**(p**2) *
    (u+1)**u *
    (2**(p+1)-u+1)**(p-1) *
    (2**(p+1)-p)**p *
    (2**(p+1)+1) *
    (PKT-u+1) *
    (PKT-1) *
    (PKT+u-1) *
    (u**2-u+1) *
    (p*2**(p+1)-u-1) *
    (2*PKT-1) *
    ((u-1)*(p+2**(p+1)-u-1)-1) *
    (p*PKT-1)
)

assert M_formula == M, f"MISMATCH: {M_formula} != {M}"

# Verify factorization
fact = factorint(M_formula)
assert fact == {2:46,3:20,5:9,7:6,11:2,13:3,17:1,19:1,23:1,29:1,31:1,41:1,47:1,59:1,71:1}

print("Monster order closed-form in {p,u,PKT}: VERIFIED")
print(f"|M| = {M_formula}")
print("ALL PASSED")
