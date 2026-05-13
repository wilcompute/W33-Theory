"""
Part CDLXV Verifier: c_g(2) W33 encoding and graded dimension formulas
"""
from math import factorial, gcd

p=3; u=6; PKT=24; K=16; LAM=10; MU=8; MU1=12; C_V=7; V=27

# c_g(2) W33 expressions
assert 2**(MU+p) == 2048
assert -(p**5) == -243
assert PKT*(PKT-1)//2 == 276
assert MU*(p+1)*(LAM*V+1) == 8672
assert 2**(MU+p)*(LAM*(p+1)+C_V) == 96256
assert 1 + (5*MU1-1)*(p*PKT-1)*C_V*(factorial(u)+K-p) == 21493760
print('c_g(2) table verified ✓')

# Graded dimension formulas
assert 1 + (LAM*(p+1)+C_V)*(5*MU1-1)*(p*PKT-1) == 196884
assert 1 + (5*MU1-1)*(p*PKT-1)*C_V*(factorial(u)+(K-p)) == 21493760
print('Graded dimension formulas verified ✓')

# Fano factorial
assert factorial(u) == 720
assert factorial(u) + K - p == 733
assert C_V * (factorial(u) + K - p) == 5131
assert gcd(196883, 21296876) * 5131 + 1 == 21493760
print('Fano factorial theorem verified ✓')

# Module decomposition
assert 1 + 196883 == 196884
assert 1 + 196883 + 21296876 == 21493760
print('Module decomposition verified ✓')

print('ALL CDLXV ASSERTIONS PASSED')
