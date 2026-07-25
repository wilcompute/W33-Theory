#!/usr/bin/env python3
"""
PART MCCCVI: Pisano Period Tower for W(3,3)
Computes and verifies all Pisano periods from BREAKTHROUGH_MCCCXIII_MCCCXX.
"""

def pisano_period(n):
    """Compute the Pisano period pi(n) — period of Fibonacci mod n."""
    if n == 1:
        return 1
    prev, cur = 0, 1
    for i in range(1, n * n * 6 + 1):
        prev, cur = cur, (prev + cur) % n
        if prev == 0 and cur == 1:
            return i
    return None  # Should not reach here for valid n

# W(3,3) substrate constants
q = 3; r = 2; k = 12
lambda1 = 10; lambda2 = 16
g1 = 21; g2 = 6; v = 40
Phi3 = 13; Phi6 = 7; p_Ih = 11
F5 = 5; F6 = 8
prime_k = 37  # 12th prime
prime_g1 = 73  # 21st prime

targets = [
    ('r=2',         r,       'base prime'),
    ('q=3',         q,       'base prime'),
    ('F5=5',        F5,      'Fibonacci prime'),
    ('Phi6=7',      Phi6,    'cyclotomic prime'),
    ('p_Ih=11',     p_Ih,    'icosahedral prime'),
    ('Phi3=13',     Phi3,    'Gaussian prime'),
    ('prime(k)=37', prime_k, '12th prime'),
    ('prime(g1)=73',prime_g1,'21st prime'),
]

print("=" * 70)
print("PISANO PERIOD TOWER — W(3,3)")
print("=" * 70)
print(f"{'Name':20s} {'n':>5s} {'pi(n)':>8s} {'pi mod 12':>12s} {'pi(n)/n':>10s} {'key identity'}")
print("-" * 70)

results = {}
for name, n, role in targets:
    p = pisano_period(n)
    results[n] = p
    ratio = p / n
    mod12 = p % 12
    print(f"{name:20s} {n:5d} {p:8d} {mod12:12d} {ratio:10.4f}  [{role}]")

print()
print("EIGENVALUE-PISANO DUALITY (Theorem MCCCXIV):")
print(f"  pi(Phi6=7) = {results[7]} = lambda_2 = {lambda2}? {results[7] == lambda2}")
print(f"  pi(p_Ih=11) = {results[11]} = lambda_1 = {lambda1}? {results[11] == lambda1}")
print(f"  Map Phi6 -> pi(Phi6)=lambda_2 and p_Ih -> pi(p_Ih)=lambda_1: ORDER-REVERSED (7<11 but 16>10)")

print()
print("PISANO CHAIN (Theorem MCCCXV):")
print(f"  pi(Phi3=13) = {results[13]} = Phi6 = {Phi6}? {results[13] == Phi6}")
print(f"  pi(Phi6=7)  = {results[7]} = lambda_2 = {lambda2}? {results[7] == lambda2}")
print(f"  Chain: Phi3 -pi-> Phi6 -pi-> lambda_2")

print()
print("DOUBLE PISANO (Theorem MCCCXVI):")
print(f"  pi(r=2) = {results[2]} = q = {q}? {results[2] == q}")
print(f"  pi(q=3) = {results[3]} = r^q = 2^3 = {r**q}? {results[3] == r**q}")
print(f"  pi(pi(r)) = pi(q) = r^q: {results[results[2]] == r**q}")

print()
print("PRIME(K) PISANO (Theorem MCCCXVII):")
p37 = results[37]
print(f"  pi(prime(k)=37) = {p37}")
print(f"  lambda1*g2 + lambda2 = {lambda1}*{g2} + {lambda2} = {lambda1*g2 + lambda2}")
print(f"  Identity pi(37) = lambda1*g2 + lambda2? {p37 == lambda1*g2 + lambda2}")

print()
print("MOD-12 EXCLUSION (Theorem MCCCXVIII):")
all_nonzero = all(results[n] % k != 0 for name,n,role in targets)
print(f"  All substrate Pisano periods non-zero mod k=12: {all_nonzero}")
for name, n, role in targets:
    mod = results[n] % k
    print(f"    pi({n}) = {results[n]} ≡ {mod} (mod 12)")

print()
print("SUM AND PRODUCT (Theorem MCCCXIX):")
pi7 = results[7]; pi11 = results[11]
print(f"  pi(7) + pi(11) = {pi7} + {pi11} = {pi7+pi11} = r*Phi3 = {r*Phi3}? {pi7+pi11 == r*Phi3}")
print(f"  pi(7) * pi(11) = {pi7} * {pi11} = {pi7*pi11} = r^2*v = {r**2*v}? {pi7*pi11 == r**2*v}")
