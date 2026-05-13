"""
Part CDLXIII Verifier: McKay-Thompson complete W33 encoding
"""
from math import lcm
from functools import reduce

p=3; u=6; PKT=24; K=16; LAM=10; MU=8; MU1=12; C_V=7

# Class data: (name, order, constant)
classes = [
    ('1A',1,744),('2A',2,40),('2B',2,24),('3A',3,12),
    ('4A',4,8),('5A',5,4),('5B',5,4),('6A',6,4),
    ('7A',7,1),('7B',7,1),('8B',8,2),('10A',10,2),('12A',12,2)
]

# Theorem A
constants = set(c for _,_,c in classes)
expected = {p-2, p-1, p+1, MU, MU1, PKT, LAM*(p+1), PKT*(u**2-u+1)}
assert constants == expected
print("Theorem A: constant set = W33 parameter values  ✓")

# Theorem B
products = set(o*c for _,o,c in classes)
expected_p = {C_V, K, 2*LAM, PKT, 2*K, u**2, 2*PKT, LAM*MU, PKT*(u**2-u+1)}
assert products == expected_p
print("Theorem B: order*const set = W33 derived values  ✓")

# Theorem C
orders = [o for _,o,c in classes]
lcm_orders = reduce(lcm, orders)
assert lcm_orders == 840
assert 840 == MU*p*(u-1)*C_V
assert 840 == PKT*(u-1)*C_V
print("Theorem C: LCM(orders) = MU*p*(u-1)*C_V = 840  ✓")

# Theorem D
assert 21296876 == 4*(u**2-u+1)*(p*K-C_V)*(5*MU1-1)*(p*PKT-1)
print("Theorem D: dim_2 = 4*Phi6(u)*(pK-C_V)*(5MU1-1)*(pPKT-1)  ✓")

print("ALL PASSED")
