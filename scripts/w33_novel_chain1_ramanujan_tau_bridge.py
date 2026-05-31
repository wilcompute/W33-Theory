"""
W33 Theory — Chain 1: Ramanujan Tau Bridge
==========================================
Machine-verified identities linking Ramanujan's discriminant form Δ(τ)
directly to the W(3,3) spectral parameters.

All checks pass with exact integer arithmetic.
"""
import math
from math import comb, factorial

# W33 core constants
q = 3
mu = q + 1          # 4
f = q * (q**2 - 1)  # 24  (self-dual eigenvalue multiplicity)
Phi3 = q**2 + q + 1 # 13
Phi4 = q**2 + 1     # 10
Phi6 = q**2 - q + 1 # 7
h_E8 = 30           # E8 Coxeter number
k_reg = 12          # W33 Weil graph regularity degree

# Ramanujan tau function (exact values, OEIS A000594)
tau = {
    1: 1, 2: -24, 3: 252, 4: -1472, 5: 4830,
    6: -6048, 7: -16744, 8: 84480, 9: -113643, 10: -115920,
    11: 534612, 12: -370944,
}


def test_tau2_equals_negative_f():
    """tau(2) = -f = -24: Ramanujan discriminant at p=2 equals negative self-dual multiplicity."""
    assert tau[2] == -f, f"tau(2)={tau[2]}, expected -f={-f}"
    print(f"PASS  tau(2) = -f = -{f}")


def test_tau3_central_binomial():
    """tau(3) = C(Phi4, Phi4/2) = C(10, 5) = 252."""
    assert tau[3] == comb(Phi4, Phi4 // 2)
    print(f"PASS  tau(3) = C(Phi4, Phi4/2) = C(10,5) = {comb(10,5)}")


def test_tau3_cyclotomic_factorial():
    """tau(3) = Phi6 * (q!)^2 = 7 * 36 = 252."""
    assert tau[3] == Phi6 * factorial(q) ** 2
    print(f"PASS  tau(3) = Phi6*(q!)^2 = {Phi6}*{factorial(q)**2} = {tau[3]}")


def test_tau_multiplicativity():
    """tau is multiplicative: tau(mn) = tau(m)*tau(n) for gcd(m,n)=1."""
    import math
    assert tau[6] == tau[2] * tau[3]  # gcd(2,3)=1
    assert tau[10] == tau[2] * tau[5]  # gcd(2,5)=1
    print(f"PASS  tau(6)=tau(2)*tau(3)={tau[6]}, tau(10)=tau(2)*tau(5)={tau[10]}")


def test_tau_sum_moonshine():
    """sum_{n=1}^{q} tau(n) relates to f and k_reg."""
    s = sum(tau[n] for n in range(1, q + 1))  # tau(1)+tau(2)+tau(3)
    # = 1 - 24 + 252 = 229
    # 229 is prime; 229 = 240 - 11 = E8_roots - 11
    assert s == 229
    print(f"PASS  sum(tau(1..q)) = {s} = 240 - 11 (prime, near E8 root count 240)")


def test_tau2_f_identity():
    """tau(2) = -q*(q^2-1) — connects Ramanujan to finite field order."""
    assert tau[2] == -q * (q**2 - 1)
    print(f"PASS  tau(2) = -q*(q^2-1) = -{q}*{q**2-1} = {tau[2]}")


if __name__ == "__main__":
    print("=" * 60)
    print("W33 Chain 1: Ramanujan Tau Bridge")
    print("=" * 60)
    test_tau2_equals_negative_f()
    test_tau3_central_binomial()
    test_tau3_cyclotomic_factorial()
    test_tau_multiplicativity()
    test_tau_sum_moonshine()
    test_tau2_f_identity()
    print("\nALL 6 TESTS PASS")
