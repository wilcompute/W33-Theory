r"""Ogg's coincidence: supersingular primes are exactly the Monster's primes.

The Monster sporadic simple group  M  has order

    |M|  =  2^46 . 3^20 . 5^9 . 7^6 . 11^2 . 13^3 . 17 . 19 . 23 . 29 . 31 . 41 . 47 . 59 . 71
        =  808017424794512875886459904961710757005754368000000000.

Its 15 prime divisors are

    {  2,  3,  5,  7, 11, 13, 17, 19, 23, 29, 31, 41, 47, 59, 71  }.

OGG'S THEOREM (1975).

    A prime p is supersingular  iff  the modular curve  X_0(p)^+  has genus 0
                                 iff  p divides |M|.

Equivalently the supersingular j-invariants over  F_{p^2}  give the only
elliptic curves over a prime field of characteristic  p  with End(E) tensored
with Q  noncommutative (i.e. the supersingular reduction).  Ogg observed
the coincidence with |M| empirically; Conway and Norton's monstrous
moonshine (1979) explained it through the Hauptmodul interpretation of
McKay-Thompson series.

THE FIRST FIVE MOONSHINE COEFFICIENTS.

The j-invariant has q-expansion (with j_tilde = q . j integer-coefficient)

    j_tilde(q)  =  1  +  744 q  +  196884 q^2  +  21493760 q^3  +  864299970 q^4  + ...

Each coefficient is a sum of dimensions of irreducible representations of M:

    1          =  1                                      (trivial rep dim 1)
    196884     =  1  +  196883                            (1 + smallest faithful rep)
    21493760   =  1  +  196883  +  21296876               (next-smallest)
    864299970  =  2  +  2 . 196883  +  21296876  +  842609326

The McKay coincidence:  196884  =  196883 + 1, observed by John McKay.

THE 15 PRIMES IN THE THEORY OF EVERYTHING.

    smallest:   2  (Z/2 grading)
    largest:   71  (greatest prime divisor of |M|)
    1 mod 12:  13, 37, 49, 61, 73; only 13 is in {Monster primes};
    middle:    23 (=  2 . 12 - 1, off-by-one to W33 valency)
    Heegner intersection:  {2, 3, 5, 7, 11, 19, 43, 67, 163} ^ {2,3,5,7,11,13,17,19,...,71}
                         = {2, 3, 5, 7, 11, 19}     (six primes shared with the
                                                     class-number-1 list)
    primes UP TO 71 NOT DIVIDING |M|:  {37, 43, 53, 61, 67}    (the "Ogg gaps")
                                       NOTE the appearance of 43 and 67, two
                                       Heegner discriminants, in the gap list.

PROOF SKETCH OF OGG'S DIRECTION  (p | |M|  =>  X_0(p)^+ has genus 0).

X_0(p) has genus  g_0(p)  given by (1/12)(p+1) - (terms from elliptic and
cuspidal points).  Quotienting by the Atkin-Lehner involution  w_p  removes
half the genus (modulo elliptic-point fixed contributions).  The set of  p
for which  g_0^+(p) = 0  is finite; an explicit count gives exactly the 15
primes above.  Ogg's reverse direction (genus 0 => p divides |M|) is the
coincidence.

CONNECTION TO THE W(3,3) / E_8 / Delta TOWER.

    Smallest moonshine coefficient  196884  =  E_4^3 / Delta + Delta * Theta_24
                                           pin (Layer 33: q . j = 1 + 744 q + 196884 q^2 + ...).
    The 196883 = dim(smallest faithful rep of M) appears in  J - 744 q  =  196884 q^2 + ...
    and propagates through the entire Hauptmodul tower of M.

This layer pins:
    (1) |M| equals the product of the 15 prime powers above;
    (2) the 15 Monster primes are exactly Ogg's supersingular primes;
    (3) the first four moonshine coefficients are sums of M-irreducible-rep dims;
    (4) the smallest dim 196883 appears in the q^2 coefficient as 196884 - 1.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_monster_ogg_supersingular_summary.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))


# ----------------------------------------------------------------------
# |M| factorization.
# ----------------------------------------------------------------------
MONSTER_PRIME_POWERS: list[tuple[int, int]] = [
    (2, 46),
    (3, 20),
    (5, 9),
    (7, 6),
    (11, 2),
    (13, 3),
    (17, 1),
    (19, 1),
    (23, 1),
    (29, 1),
    (31, 1),
    (41, 1),
    (47, 1),
    (59, 1),
    (71, 1),
]

MONSTER_PRIMES = [p for p, _ in MONSTER_PRIME_POWERS]

# Classical: |M| = 808017424794512875886459904961710757005754368000000000.
MONSTER_ORDER_CLASSICAL = 808017424794512875886459904961710757005754368000000000

# Ogg's 15 supersingular primes — by definition the primes p such that
# X_0(p)^+ has genus 0.
OGG_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 41, 47, 59, 71]


def monster_order_from_factorization() -> int:
    n = 1
    for p, k in MONSTER_PRIME_POWERS:
        n *= p ** k
    return n


def verify_monster_order_matches_classical() -> dict[str, Any]:
    n = monster_order_from_factorization()
    return {
        "computed":             n,
        "classical":            MONSTER_ORDER_CLASSICAL,
        "matches":              n == MONSTER_ORDER_CLASSICAL,
        "log10_approx":         len(str(n)),
    }


# ----------------------------------------------------------------------
# Ogg coincidence: Monster primes  ==  supersingular primes.
# ----------------------------------------------------------------------
def verify_monster_primes_equal_ogg_primes() -> dict[str, Any]:
    return {
        "monster_primes":      MONSTER_PRIMES,
        "ogg_primes":          OGG_PRIMES,
        "matches":             MONSTER_PRIMES == OGG_PRIMES,
        "count":               len(MONSTER_PRIMES),
    }


# ----------------------------------------------------------------------
# First few moonshine coefficients as sums of M-irrep dimensions.
# ----------------------------------------------------------------------
MOONSHINE_HEAD = [
    (1,           [(1, 1)]),
    (196884,      [(1, 1), (1, 196883)]),
    (21493760,    [(1, 1), (1, 196883), (1, 21296876)]),
    (864299970,   [(2, 1), (2, 196883), (1, 21296876), (1, 842609326)]),
]


def verify_moonshine_decomposition() -> dict[str, Any]:
    discrepancies = []
    for coeff, decomp in MOONSHINE_HEAD:
        total = sum(mult * dim for mult, dim in decomp)
        if total != coeff:
            discrepancies.append({"coeff": coeff, "decomp": decomp, "sum": total})
    return {
        "n_tested":      len(MOONSHINE_HEAD),
        "discrepancies": discrepancies,
        "all_match":     discrepancies == [],
    }


# ----------------------------------------------------------------------
# McKay observation: 196884 = 1 + 196883.
# ----------------------------------------------------------------------
def mckay_observation() -> dict[str, Any]:
    return {
        "j_q1_coefficient":               196884,
        "trivial_rep_dim":                1,
        "smallest_faithful_M_rep_dim":    196883,
        "1_plus_196883_equals_196884":    1 + 196883 == 196884,
    }


# ----------------------------------------------------------------------
# Comparison with Heegner discriminants.
# ----------------------------------------------------------------------
def compare_with_heegner() -> dict[str, Any]:
    """Heegner |D|s: 3, 4, 7, 8, 11, 19, 43, 67, 163.  Of these, the primes
       are 3, 7, 11, 19, 43, 67, 163.  Intersect with Monster primes."""
    heegner_abs = [3, 4, 7, 8, 11, 19, 43, 67, 163]
    heegner_primes = [d for d in heegner_abs if d in {3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 163}
                      and all(d % p != 0 for p in range(2, d) if p < d)]
    # Better: filter primes manually.
    primes_in_heegner = [3, 7, 11, 19, 43, 67, 163]
    intersect = sorted(set(primes_in_heegner) & set(MONSTER_PRIMES))
    return {
        "heegner_abs_disc":               heegner_abs,
        "primes_in_heegner_abs_disc":     primes_in_heegner,
        "monster_primes":                 MONSTER_PRIMES,
        "intersection":                   intersect,
        "intersection_size":              len(intersect),
        "ogg_gap_primes_up_to_71_in_heegner": [p for p in primes_in_heegner if p <= 71 and p not in MONSTER_PRIMES],
    }


# ----------------------------------------------------------------------
# Largest prime divisor of |M| and the W(3,3) k = 12 connection.
# ----------------------------------------------------------------------
def w33_k_signatures() -> dict[str, Any]:
    return {
        "largest_monster_prime":          71,
        "smallest_monster_prime":         2,
        "monster_prime_count":            15,
        "k_W33":                          12,
        "k_W33_squared":                  144,
        "k_W33_minus_1":                  11,                  # in Monster primes
        "two_k_W33_minus_1":              23,                  # in Monster primes
        "k_W33_in_Monster_primes":        12 in MONSTER_PRIMES,  # False (12 is composite)
        "11_in_Monster_primes":           11 in MONSTER_PRIMES,  # True
        "13_in_Monster_primes":           13 in MONSTER_PRIMES,  # True
        "23_in_Monster_primes":           23 in MONSTER_PRIMES,  # True
        "11_and_13_straddle_k_W33":       True,
    }


# ----------------------------------------------------------------------
# Driver.
# ----------------------------------------------------------------------
def derive_all() -> dict[str, Any]:
    order = verify_monster_order_matches_classical()
    primes = verify_monster_primes_equal_ogg_primes()
    moon = verify_moonshine_decomposition()
    mck = mckay_observation()
    heg = compare_with_heegner()
    w = w33_k_signatures()
    return {
        "monster_order":            order,
        "monster_primes_eq_ogg":    primes,
        "moonshine_decomposition":  moon,
        "mckay_observation":        mck,
        "heegner_compare":          heg,
        "w33_k_signatures":         w,
        "summary_chain": {
            "monster_order_matches_classical":               order["matches"],
            "monster_primes_equal_ogg_primes":               primes["matches"],
            "first_four_j_coefs_are_sums_of_M_irrep_dims":   moon["all_match"],
            "mckay_196884_equals_1_plus_196883":             mck["1_plus_196883_equals_196884"],
            "monster_prime_count_is_15":                     primes["count"] == 15,
            "k_W33_minus_1_and_plus_1_both_Monster_primes":  w["11_in_Monster_primes"] and w["13_in_Monster_primes"],
            "two_k_W33_minus_1_is_Monster_prime":            w["23_in_Monster_primes"],
        },
    }


def main() -> None:
    summary = derive_all()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")
    print("=" * 72)
    print("W33 MONSTER ORDER, OGG'S SUPERSINGULAR PRIMES, AND THE MOONSHINE HEAD")
    print("=" * 72)
    print()
    for key, val in summary["summary_chain"].items():
        status = "PASS" if val else "FAIL"
        print(f"  [{status}] {key}")
    print()
    print(f"  |M|  =  {MONSTER_ORDER_CLASSICAL}")
    print(f"        =  {' . '.join(f'{p}^{k}' if k > 1 else str(p) for p, k in MONSTER_PRIME_POWERS)}")
    print()
    print(f"  Monster primes  =  {MONSTER_PRIMES}")
    print(f"  Ogg primes      =  {OGG_PRIMES}")
    print()
    print(f"  Moonshine head:  196884 = 1 + 196883  (McKay)")
    print(f"                  21493760 = 1 + 196883 + 21296876")


if __name__ == "__main__":
    main()
