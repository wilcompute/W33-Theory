"""Ramanujan's three partition congruences and pentagonal-number recursion.

Let p(n) be the number of partitions of n (A000041), generating function

    sum_{n >= 0} p(n) q^n  =  prod_{n >= 1} 1 / (1 - q^n).

Ramanujan (1919) discovered three striking congruences:

    (R5)  p(5n + 4)  ≡ 0  (mod 5),
    (R7)  p(7n + 5)  ≡ 0  (mod 7),
    (R11) p(11n + 6) ≡ 0  (mod 11).

These are the only three primes l for which there is a congruence of
the form p(l n + b_l) ≡ 0 (mod l).  At 13, no such congruence exists
(a famous "obstruction"); Ahlgren and Ono (2000) extended the picture
to all l >= 5 by finding hidden higher-modulus congruences.

Generating function identities:

    sum p(5n+4) q^n = 5  prod (1-q^{5n})^5 / (1-q^n)^6,    (I)
    sum p(7n+5) q^n = 7  prod (1-q^{7n})^3 / (1-q^n)^4
                        + 49 q prod (1-q^{7n})^7 / (1-q^n)^8.  (II)

We only pin the congruences numerically -- not these generating-
function identities -- but (I) makes (R5) obvious because of the
factor of 5.

Partition function by pentagonal-number recursion (Euler):

    p(n) = sum_{k != 0}  (-1)^{k - 1}  p(n - k(3k - 1)/2),

where k ranges over ±1, ±2, ±3, ...  and the generalised pentagonal
numbers are k(3k - 1)/2 = 1, 2, 5, 7, 12, 15, 22, 26, ...

Hardy-Ramanujan asymptotic:

    p(n) ~ (1 / (4 n sqrt 3)) * exp(pi sqrt(2 n / 3)).

The relative error decays like 1/n, so at n = 1000 the asymptotic is
within ~1% of the true value.

Layer 66 -- the *partition* face of the Ramanujan-Serre tower (Delta
face is Layer 63), same 691-era mathematics, different modular form.
"""

from __future__ import annotations

from typing import Any

import mpmath as mp


# ----------------------------------------------------------------------
# Generalised pentagonal numbers: 1, 2, 5, 7, 12, 15, 22, 26, ...
# ----------------------------------------------------------------------
def pentagonals(limit: int) -> list[tuple[int, int]]:
    """List pairs (k, g_k) with g_k = k(3k-1)/2 <= limit, alternating
    signs for recurrence:  sign = (-1)^{|k| - 1} for k = 1, -1, 2, -2, ...
    """
    out: list[tuple[int, int]] = []
    k = 1
    while True:
        g1 = k * (3 * k - 1) // 2
        g2 = k * (3 * k + 1) // 2  # same formula with k -> -k
        stop_1 = g1 > limit
        stop_2 = g2 > limit
        if stop_1 and stop_2:
            break
        if not stop_1:
            out.append((k, g1))
        if not stop_2:
            out.append((-k, g2))
        k += 1
    return out


# ----------------------------------------------------------------------
# Partition table by Euler's pentagonal-number recursion, cached.
# ----------------------------------------------------------------------
_P_CACHE: list[int] = [1]   # p(0) = 1


def partition_table(N: int) -> list[int]:
    """p(0), p(1), ..., p(N) using Euler's pentagonal recurrence."""
    global _P_CACHE
    if len(_P_CACHE) >= N + 1:
        return _P_CACHE[:N + 1]
    pent = pentagonals(N + 1)
    while len(_P_CACHE) <= N:
        n = len(_P_CACHE)
        total = 0
        for k, g in pent:
            if g > n:
                break
            sign = 1 if (abs(k) - 1) % 2 == 0 else -1
            total += sign * _P_CACHE[n - g]
        _P_CACHE.append(total)
    return _P_CACHE[:N + 1]


def p(n: int) -> int:
    return partition_table(n)[n]


# ----------------------------------------------------------------------
# Hardy-Ramanujan asymptotic.
# ----------------------------------------------------------------------
def p_asymptotic(n: int) -> mp.mpf:
    if n < 1:
        return mp.mpf(1)
    return (1 / (4 * mp.mpf(n) * mp.sqrt(3))) * mp.exp(mp.pi * mp.sqrt(2 * n / mp.mpf(3)))


# ----------------------------------------------------------------------
# Verifiers.
# ----------------------------------------------------------------------
def verify_p_small_values() -> dict[str, Any]:
    """Pin the first 10 partition numbers: 1, 1, 2, 3, 5, 7, 11, 15, 22, 30."""
    expected = [1, 1, 2, 3, 5, 7, 11, 15, 22, 30]
    tab = partition_table(10)
    rows = []
    all_match = True
    for n, e in enumerate(expected):
        match = tab[n] == e
        rows.append({"n": n, "p_n": tab[n], "expected": e, "match": match})
        all_match = all_match and match
    return {"all_match": all_match, "rows": rows}


def verify_R5(N_max: int = 500) -> dict[str, Any]:
    """p(5n + 4) ≡ 0 mod 5 for n = 0, 1, ..., N_max."""
    tab = partition_table(5 * N_max + 4)
    failures = []
    all_match = True
    for n in range(N_max + 1):
        v = tab[5 * n + 4]
        ok = v % 5 == 0
        if not ok:
            failures.append({"n": n, "p_5n_plus_4": v, "mod_5": v % 5})
            all_match = False
    return {"all_match": all_match, "N_max": N_max, "failures": failures}


def verify_R7(N_max: int = 500) -> dict[str, Any]:
    """p(7n + 5) ≡ 0 mod 7 for n = 0, 1, ..., N_max."""
    tab = partition_table(7 * N_max + 5)
    failures = []
    all_match = True
    for n in range(N_max + 1):
        v = tab[7 * n + 5]
        ok = v % 7 == 0
        if not ok:
            failures.append({"n": n, "p_7n_plus_5": v, "mod_7": v % 7})
            all_match = False
    return {"all_match": all_match, "N_max": N_max, "failures": failures}


def verify_R11(N_max: int = 200) -> dict[str, Any]:
    """p(11n + 6) ≡ 0 mod 11 for n = 0, 1, ..., N_max."""
    tab = partition_table(11 * N_max + 6)
    failures = []
    all_match = True
    for n in range(N_max + 1):
        v = tab[11 * n + 6]
        ok = v % 11 == 0
        if not ok:
            failures.append({"n": n, "p_11n_plus_6": v, "mod_11": v % 11})
            all_match = False
    return {"all_match": all_match, "N_max": N_max, "failures": failures}


def verify_R5_first_spot_check() -> dict[str, Any]:
    """p(4) = 5 (five partitions of 4: 4, 3+1, 2+2, 2+1+1, 1+1+1+1);
    p(9) = 30;  p(14) = 135;  p(19) = 490.  All divisible by 5."""
    assertions = []
    all_match = True
    for n in [4, 9, 14, 19, 24, 29, 34]:
        v = p(n)
        match = v % 5 == 0
        assertions.append({"n": n, "p_n": v, "divisible_by_5": match})
        all_match = all_match and match
    return {"all_match": all_match, "rows": assertions}


def verify_R13_has_no_congruence() -> dict[str, Any]:
    """At modulus 13 there is no b with p(13n + b) ≡ 0 mod 13 for all n.
    Check the dual statement: for every b in {0,...,12}, there exists
    n <= 40 with p(13n + b) !≡ 0 mod 13."""
    tab = partition_table(13 * 40 + 12)
    rows = []
    all_match = True
    for b in range(13):
        found = False
        for n in range(41):
            if tab[13 * n + b] % 13 != 0:
                found = True
                break
        rows.append({"b": b, "has_nonvanishing": found})
        all_match = all_match and found
    return {"all_match": all_match, "rows": rows}


_P_REFERENCE = {
    0: 1, 1: 1, 2: 2, 3: 3, 4: 5, 5: 7, 6: 11, 7: 15, 8: 22, 9: 30,
    10: 42, 15: 176, 20: 627, 25: 1958, 30: 5604, 40: 37338, 50: 204226,
    60: 966467, 70: 4087968, 80: 15796476, 90: 56634173, 100: 190569292,
    150: 40853235313, 200: 3972999029388,
}  # OEIS A000041


def verify_pentagonal_recursion_against_standard(N: int = 200) -> dict[str, Any]:
    """Cross-check our Euler recurrence against the OEIS A000041 table."""
    tab = partition_table(N)
    all_match = True
    rows = []
    for n, expected in _P_REFERENCE.items():
        if n > N:
            continue
        ours = tab[n]
        match = ours == expected
        rows.append({"n": n, "ours": ours, "expected": expected, "match": match})
        all_match = all_match and match
    return {"all_match": all_match, "N": N, "rows": rows}


def verify_hardy_ramanujan_asymptotic(n_test: int = 1000,
                                        tol_rel: float = 0.02) -> dict[str, Any]:
    """For large n, p(n) ~ (1/(4 n sqrt 3)) exp(pi sqrt(2n/3));
    at n = 1000 the relative error is ~1%."""
    tab = partition_table(n_test)
    exact = mp.mpf(tab[n_test])
    approx = p_asymptotic(n_test)
    rel_err = abs((approx - exact) / exact)
    return {
        "n": n_test,
        "exact": str(exact),
        "asymptotic": str(approx),
        "relative_error": float(rel_err),
        "match": bool(rel_err < tol_rel),
    }


# ----------------------------------------------------------------------
# Driver.
# ----------------------------------------------------------------------
def derive_all() -> dict[str, Any]:
    small = verify_p_small_values()
    penta = verify_pentagonal_recursion_against_standard(N=200)
    r5 = verify_R5(N_max=500)
    r7 = verify_R7(N_max=500)
    r11 = verify_R11(N_max=200)
    spot = verify_R5_first_spot_check()
    no13 = verify_R13_has_no_congruence()
    hr = verify_hardy_ramanujan_asymptotic(n_test=1000)
    chain = {
        "partition_numbers_1_1_2_3_5_7_11_15_22_30":
            small["all_match"],
        "pentagonal_recursion_matches_OEIS_A000041_up_to_N_200":
            penta["all_match"],
        "ramanujan_R5_p_5n_plus_4_equiv_0_mod_5_up_to_n_500":
            r5["all_match"],
        "ramanujan_R7_p_7n_plus_5_equiv_0_mod_7_up_to_n_500":
            r7["all_match"],
        "ramanujan_R11_p_11n_plus_6_equiv_0_mod_11_up_to_n_200":
            r11["all_match"],
        "small_R5_instances_4_9_14_19_24_29_34_divisible_by_5":
            spot["all_match"],
        "no_mod_13_congruence_every_residue_class_has_nonvanishing":
            no13["all_match"],
        "hardy_ramanujan_asymptotic_at_n_1000_relative_error_under_2_percent":
            hr["match"],
    }
    return {
        "small_values": small,
        "recursion": penta,
        "R5": r5,
        "R7": r7,
        "R11": r11,
        "spot": spot,
        "no_13_congruence": no13,
        "hardy_ramanujan": hr,
        "summary_chain": chain,
    }


if __name__ == "__main__":
    s = derive_all()
    print("summary_chain:")
    for k, v in s["summary_chain"].items():
        print(f"  {k}: {v}")
    print("\np(n) for n = 0..10:")
    for row in s["small_values"]["rows"]:
        print(f"  p({row['n']}) = {row['p_n']}  (expected {row['expected']})")
    print(f"\np(4) = 5,  p(9) = 30,  p(14) = 135 — all divisible by 5")
    print(f"p(1000) = {partition_table(1000)[1000]}")
    print(f"  Hardy-Ramanujan approximation = "
          f"{float(p_asymptotic(1000)):.3e}  "
          f"(relative error {s['hardy_ramanujan']['relative_error']:.3%})")
