"""Ramanujan's tau congruences modulo 691, 5, 7, 256, 27.

Ramanujan (1916) discovered that the coefficients tau(n) of

    Delta(q) = q prod (1 - q^n)^{24}  =  sum tau(n) q^n

obey startling congruences modulo small primes and prime powers.  The
"exceptional primes" of weight 12 (Serre / Swinnerton-Dyer, 1973) are

            l in { 2, 3, 5, 7, 23, 691 }

each carrying its own congruence.  Five are pinned here:

(I)    tau(n) ≡ sigma_{11}(n) (mod 691)        for all n ≥ 1.
       This is the *original* Ramanujan 691 congruence.  The modulus
       691 is the numerator of B_{12} = -691/2730, i.e. the prime that
       entered Layer 61 through
           zeta(-11) = -B_{12}/12 = 691/32760.

(II)   tau(n) ≡ n sigma_{1}(n) (mod 5)         for all n.

(III)  tau(n) ≡ n sigma_{3}(n) (mod 7)         for all n.

(IV)   tau(n) ≡ sigma_{11}(n) (mod 2^8 = 256)  for n odd.

(V)    tau(n) ≡ n^2 sigma_{7}(n) (mod 27)      for gcd(n, 3) = 1.

Consequence (VI): for every prime p,
    tau(p) ≡ 1 + p^{11}   (mod 691),
which follows from sigma_{11}(p) = 1 + p^{11} and Euler product.

Layer 63 -- closes the Ramanujan-Serre congruence loop on the Delta
tower and ties directly back to Layer 61 (B_12 and zeta(-11) = 691 /
32760).
"""

from __future__ import annotations

from typing import Any

from w33_L_delta import tau_table


# ----------------------------------------------------------------------
# Divisor sums.
# ----------------------------------------------------------------------
def sigma_k(n: int, k: int) -> int:
    """sigma_k(n) = sum_{d | n} d^k."""
    if n < 1:
        raise ValueError("n must be >= 1.")
    total = 0
    d = 1
    while d * d <= n:
        if n % d == 0:
            total += d ** k
            other = n // d
            if other != d:
                total += other ** k
        d += 1
    return total


# ----------------------------------------------------------------------
# Verifiers for each congruence.
# ----------------------------------------------------------------------
def verify_691_congruence(N: int = 500) -> dict[str, Any]:
    """tau(n) ≡ sigma_{11}(n) (mod 691) for 1 <= n <= N."""
    t = tau_table(N)
    failures: list[dict[str, Any]] = []
    for n in range(1, N + 1):
        lhs = t[n] % 691
        rhs = sigma_k(n, 11) % 691
        if lhs != rhs:
            failures.append({"n": n, "tau_mod_691": lhs,
                             "sigma_11_mod_691": rhs})
    return {"all_match": len(failures) == 0,
            "N": N, "failures": failures}


def verify_mod_5(N: int = 500) -> dict[str, Any]:
    """tau(n) ≡ n sigma_1(n) (mod 5) for 1 <= n <= N."""
    t = tau_table(N)
    failures = []
    for n in range(1, N + 1):
        lhs = t[n] % 5
        rhs = (n * sigma_k(n, 1)) % 5
        if lhs != rhs:
            failures.append({"n": n, "lhs": lhs, "rhs": rhs})
    return {"all_match": len(failures) == 0,
            "N": N, "failures": failures}


def verify_mod_7(N: int = 500) -> dict[str, Any]:
    """tau(n) ≡ n sigma_3(n) (mod 7) for 1 <= n <= N."""
    t = tau_table(N)
    failures = []
    for n in range(1, N + 1):
        lhs = t[n] % 7
        rhs = (n * sigma_k(n, 3)) % 7
        if lhs != rhs:
            failures.append({"n": n, "lhs": lhs, "rhs": rhs})
    return {"all_match": len(failures) == 0,
            "N": N, "failures": failures}


def verify_mod_256_odd(N: int = 500) -> dict[str, Any]:
    """tau(n) ≡ sigma_11(n) (mod 256) for odd n <= N."""
    t = tau_table(N)
    failures = []
    for n in range(1, N + 1, 2):
        lhs = t[n] % 256
        rhs = sigma_k(n, 11) % 256
        if lhs != rhs:
            failures.append({"n": n, "lhs": lhs, "rhs": rhs})
    return {"all_match": len(failures) == 0,
            "N": N, "failures": failures}


def verify_mod_27_coprime3(N: int = 500) -> dict[str, Any]:
    """tau(n) ≡ n^2 sigma_7(n) (mod 27) for gcd(n, 3) = 1, n <= N."""
    t = tau_table(N)
    failures = []
    for n in range(1, N + 1):
        if n % 3 == 0:
            continue
        lhs = t[n] % 27
        rhs = (n * n * sigma_k(n, 7)) % 27
        if lhs != rhs:
            failures.append({"n": n, "lhs": lhs, "rhs": rhs})
    return {"all_match": len(failures) == 0,
            "N": N, "failures": failures}


def verify_691_prime_consequence(prime_limit: int = 100) -> dict[str, Any]:
    """tau(p) ≡ 1 + p^11 (mod 691) for every prime p <= prime_limit."""
    # Small prime sieve.
    def sieve(L):
        s = [True] * (L + 1)
        s[0] = s[1] = False
        for i in range(2, int(L ** 0.5) + 1):
            if s[i]:
                for j in range(i * i, L + 1, i):
                    s[j] = False
        return [i for i in range(L + 1) if s[i]]
    primes = sieve(prime_limit)
    t = tau_table(prime_limit + 1)
    rows = []
    all_match = True
    for p in primes:
        lhs = t[p] % 691
        rhs = (1 + pow(p, 11, 691)) % 691
        match = lhs == rhs
        rows.append({"p": p, "tau_p_mod_691": lhs,
                     "one_plus_p11_mod_691": rhs, "match": match})
        all_match = all_match and match
    return {"all_match": all_match, "rows": rows}


def verify_bernoulli_691_connection() -> dict[str, Any]:
    """691 is the numerator of B_12 = -691/2730 (up to sign) and shows
    up in zeta(-11) = 691 / 32760.  Here we simply pin the arithmetic
    identity 32760 = 12 * 2730."""
    return {
        "B_12_numerator_abs": 691,
        "B_12_denominator": 2730,
        "zeta_minus_11_numerator": 691,
        "zeta_minus_11_denominator": 32760,
        "identity_32760_equals_12_times_2730": 12 * 2730 == 32760,
        "match": 12 * 2730 == 32760,
    }


def verify_specific_tau_values() -> dict[str, Any]:
    """Pin the reported small tau values cross-checked with sigma_11
    residues mod 691."""
    t = tau_table(20)
    expected = {
        1: (1, 1),           # (tau(n), sigma_{11}(n) mod 691) pairs.
        2: (-24, 2049 % 691),
        3: (252, (1 + 3 ** 11) % 691),
        5: (4830, (1 + 5 ** 11) % 691),
        7: (-16744, (1 + 7 ** 11) % 691),
    }
    rows = []
    all_match = True
    for n, (tn, rn) in expected.items():
        tau_mod = t[n] % 691
        match_t = t[n] == tn
        match_cong = tau_mod == rn
        rows.append({
            "n": n, "tau": t[n], "expected_tau": tn,
            "tau_mod_691": tau_mod, "sigma_11_mod_691": rn,
            "tau_matches": match_t, "congruence_matches": match_cong,
        })
        all_match = all_match and match_t and match_cong
    return {"all_match": all_match, "rows": rows}


# ----------------------------------------------------------------------
# Driver.
# ----------------------------------------------------------------------
def derive_all() -> dict[str, Any]:
    r691 = verify_691_congruence(N=500)
    r5 = verify_mod_5(N=500)
    r7 = verify_mod_7(N=500)
    r256 = verify_mod_256_odd(N=500)
    r27 = verify_mod_27_coprime3(N=500)
    r691p = verify_691_prime_consequence(prime_limit=100)
    bern = verify_bernoulli_691_connection()
    spec = verify_specific_tau_values()
    chain = {
        "tau_n_equiv_sigma_11_mod_691_up_to_500":
            r691["all_match"],
        "tau_n_equiv_n_sigma_1_mod_5_up_to_500":
            r5["all_match"],
        "tau_n_equiv_n_sigma_3_mod_7_up_to_500":
            r7["all_match"],
        "tau_n_equiv_sigma_11_mod_256_for_odd_n_up_to_500":
            r256["all_match"],
        "tau_n_equiv_n_squared_sigma_7_mod_27_for_gcd_n_3_eq_1":
            r27["all_match"],
        "tau_p_equiv_1_plus_p_11_mod_691_for_p_up_to_100":
            r691p["all_match"],
        "bernoulli_691_connection_32760_equals_12_times_2730":
            bern["match"],
        "specific_small_tau_values_match_and_satisfy_congruence":
            spec["all_match"],
    }
    return {
        "mod_691": r691,
        "mod_5": r5,
        "mod_7": r7,
        "mod_256": r256,
        "mod_27": r27,
        "prime_691": r691p,
        "bernoulli": bern,
        "specific": spec,
        "summary_chain": chain,
    }


if __name__ == "__main__":
    s = derive_all()
    print("summary_chain:")
    for k, v in s["summary_chain"].items():
        print(f"  {k}: {v}")
    print("\ntau(p) vs 1 + p^11 mod 691 (first 10 primes):")
    for row in s["prime_691"]["rows"][:10]:
        print(f"  p={row['p']:>3}: tau(p) mod 691 = {row['tau_p_mod_691']:>3}, "
              f"1+p^11 = {row['one_plus_p11_mod_691']:>3}, "
              f"match={row['match']}")
    print(f"\nBernoulli connection: B_12 denom = "
          f"{s['bernoulli']['B_12_denominator']}, "
          f"zeta(-11) = {s['bernoulli']['zeta_minus_11_numerator']}/"
          f"{s['bernoulli']['zeta_minus_11_denominator']}, "
          f"match = {s['bernoulli']['match']}")
