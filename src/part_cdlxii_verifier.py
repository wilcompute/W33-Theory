"""
Part CDLXII Verifier: W33-Moonshine bridge
Run: python src/part_cdlxii_verifier.py
"""
from sympy import factorint

p=3; u=6; PKT=24; K=16; LAM=10; MU=8; MU1=12; C_V=7

# Theorem A
assert 744 == PKT*(u**2-u+1)
print("744 = PKT*(u^2-u+1) [Theorem A]")

# Theorem B
assert 196883 == 47*59*71
assert 196883 == (2*PKT-1)*(5*MU1-1)*(p*PKT-1)
print("196883 = (2PKT-1)(5MU1-1)(pPKT-1) [Theorem B]")

# Theorem C
assert 196884 == 196883 + (p-2)
print("c(1) = dim(Griess) + (p-2) [Theorem C]")

# Theorem D
assert 21296876 == 4*(u**2-u+1)*(p*K-C_V)*(5*MU1-1)*(p*PKT-1)
print("dim_2 = 4*(u^2-u+1)*(pK-C_V)*(5MU1-1)*(pPKT-1) [Theorem D]")

# Monster primes closure
monster_primes = {2,3,5,7,11,13,17,19,23,29,31,41,47,59,71}
for name, val in [
    ('744', 744), ('196884', 196884), ('21296876', 21296876)
]:
    primes_here = set(factorint(val).keys())
    assert primes_here.issubset(monster_primes), f"{name} has non-Monster prime"
    print(f"{name} primes subset of Monster primes: OK")

print("ALL PASSED")
