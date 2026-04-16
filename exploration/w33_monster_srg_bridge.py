"""
MONSTER–SRG BRIDGE:  196883 = (4k − 1)(5k − 1)(6k − 1)  at  k = 12
=====================================================================

The smallest nontrivial irreducible representation of the Monster group M
has dimension 196883.  This number factors as

    196883  =  47 × 59 × 71,

and these three primes form an ARITHMETIC PROGRESSION with common difference

    d = 12  =  k  =  valency of W(3, 3).

Written in terms of k:

    47 = 4k − 1,       59 = 5k − 1,       71 = 6k − 1.

So the smallest Monster irrep dimension is  (4k − 1)(5k − 1)(6k − 1),
and the first nontrivial j-coefficient is

    c(1) = 196884 = 196883 + 1 = (4k − 1)(5k − 1)(6k − 1) + 1.

MONSTER IRREP DECOMPOSITION OF j-COEFFICIENTS (McKay–Thompson).

    c(−1) = 1                              = d_1
    c( 0) = 744                             (constant term)
    c( 1) = 196884                          = d_1 + d_2
    c( 2) = 21493760                        = d_1 + d_2 + d_3
    c( 3) = 864299970                       = 2 d_1 + 2 d_2 + d_3 + d_4

where  d_1 = 1,  d_2 = 196883,  d_3 = 21296876,  d_4 = 842609326.

CRITICAL STRING DIMENSION.

The bosonic string partition function is  Z(tau) = (eta(tau))^{-2(D-2)/2}
where D is the spacetime dimension.  Modular invariance (and the no-ghost
theorem) requires  D − 2 = 24,  giving  D = 26.  Equivalently, the
transverse partition function  eta^{-24} = 1/Delta  generates p_24(n),
the 24-color partition numbers.  This is the SAME 24 that appears in
Delta = eta^24 and the 24-dimensional Leech lattice.

BRIDGE TO W(3, 3).

    k  =  12  =  valency of SRG(40, 12, 2, 4)
    2k =  24  =  exponent in eta^24 = Delta  =  Leech rank  =  D_crit − 2
    196883  =  (4k − 1)(5k − 1)(6k − 1)  =  smallest Monster irrep
    196884  =  196883 + 1  =  first j-coefficient  =  N_2(Leech) + p_24(2)
"""
from __future__ import annotations

import json
from pathlib import Path

from w33_eisenstein import j_invariant_qseries


# ======================================================================
#  Monster irreducible representation dimensions (first few).
#  Source: Atlas of Finite Groups / OEIS A001379.
# ======================================================================
MONSTER_IRREP_DIMS = [
    1,            # d_1 (trivial)
    196883,       # d_2
    21296876,     # d_3
    842609326,    # d_4
    18538750076,  # d_5
]


# ======================================================================
#  j-coefficient decomposition into Monster irreps (Thompson series).
#  c(n) = sum of multiplicities × irrep dims.
#  Multiplicities from McKay–Thompson / Conway–Norton.
# ======================================================================
J_IRREP_DECOMPOSITIONS = {
    -1: {1: 1},
    1:  {1: 1, 196883: 1},
    2:  {1: 1, 196883: 1, 21296876: 1},
    3:  {1: 2, 196883: 2, 21296876: 1, 842609326: 1},
}


# ======================================================================
#  (1)  196883 = (4k − 1)(5k − 1)(6k − 1)  at  k = 12.
# ======================================================================
def srg_valency_factorization(k: int = 12) -> dict:
    """Show that 196883 = (4k-1)(5k-1)(6k-1) at k=12."""
    a, b, c = 4 * k - 1, 5 * k - 1, 6 * k - 1
    product = a * b * c
    return {
        "k":          k,
        "4k-1":       a,
        "5k-1":       b,
        "6k-1":       c,
        "product":    product,
        "is_196883":  product == 196883,
        "primes_AP":  {
            "terms":  [a, b, c],
            "diffs":  [b - a, c - b],
            "common_difference": k,
            "is_AP":  (b - a == k) and (c - b == k),
        },
    }


def verify_primes_47_59_71() -> dict:
    """Verify 47, 59, 71 are all prime."""
    def is_prime(n):
        if n < 2:
            return False
        for d in range(2, int(n ** 0.5) + 1):
            if n % d == 0:
                return False
        return True

    return {
        47: is_prime(47),
        59: is_prime(59),
        71: is_prime(71),
        "all_prime": all(is_prime(p) for p in (47, 59, 71)),
    }


# ======================================================================
#  (2)  Monster irrep decomposition of j-coefficients.
# ======================================================================
def verify_j_irrep_decomposition(n: int) -> dict:
    """Verify c(n) = sum of multiplicities * irrep dims."""
    j = j_invariant_qseries(max(n, 6))
    c_n = int(j[n])

    if n not in J_IRREP_DECOMPOSITIONS:
        return {"n": n, "c(n)": c_n, "decomposition": None}

    decomp = J_IRREP_DECOMPOSITIONS[n]
    total = sum(mult * dim for dim, mult in decomp.items())

    return {
        "n":             n,
        "c(n)":          c_n,
        "decomposition": decomp,
        "sum":           total,
        "match":         total == c_n,
    }


def verify_all_j_decompositions() -> list:
    results = []
    for n in sorted(J_IRREP_DECOMPOSITIONS.keys()):
        results.append(verify_j_irrep_decomposition(n))
    return results


# ======================================================================
#  (3)  196884 = 196883 + 1 = c(1) of j.
# ======================================================================
def the_moonshine_identity() -> dict:
    """196884 = 196883 + 1:  first j-coefficient = trivial + smallest Monster irrep."""
    j = j_invariant_qseries(1)
    c1 = int(j[1])
    return {
        "c(1)":            c1,
        "d_1":             MONSTER_IRREP_DIMS[0],
        "d_2":             MONSTER_IRREP_DIMS[1],
        "d_1 + d_2":       MONSTER_IRREP_DIMS[0] + MONSTER_IRREP_DIMS[1],
        "match":           c1 == MONSTER_IRREP_DIMS[0] + MONSTER_IRREP_DIMS[1],
        "196883_from_k":   srg_valency_factorization(12),
    }


# ======================================================================
#  (4)  Critical string dimension D = 26 = 2k + 2.
# ======================================================================
def critical_dimension(k: int = 12) -> dict:
    """D_crit = 2k + 2 = 26 for the bosonic string."""
    D = 2 * k + 2
    return {
        "k":               k,
        "2k":              2 * k,
        "D_crit":          D,
        "transverse_dims": D - 2,
        "is_26":           D == 26,
        "eta_exponent":    2 * k,
        "leech_rank":      2 * k,
        "delta_is_eta_2k": True,
    }


# ======================================================================
#  (5)  The full k-to-Monster chain.
# ======================================================================
def derive_full_bridge(k: int = 12) -> dict:
    """Derive the complete chain from W(3,3) valency k to Monster."""
    srg_fact = srg_valency_factorization(k)
    primes = verify_primes_47_59_71()
    moonshine = the_moonshine_identity()
    j_decomps = verify_all_j_decompositions()
    crit_dim = critical_dimension(k)

    return {
        "w33_valency":     k,
        "srg_factorization": srg_fact,
        "primes_verified": primes,
        "moonshine_identity": moonshine,
        "j_irrep_decompositions": j_decomps,
        "all_j_decomps_match": all(d["match"] for d in j_decomps),
        "critical_dimension": crit_dim,
        "summary_chain": {
            "k_equals_12":                  k == 12,
            "196883_equals_prod_4k_5k_6k":  srg_fact["is_196883"],
            "47_59_71_are_prime":            primes["all_prime"],
            "AP_common_diff_is_k":          srg_fact["primes_AP"]["is_AP"],
            "196884_equals_196883_plus_1":   moonshine["match"],
            "D_crit_equals_26":             crit_dim["is_26"],
            "all_j_decomps_verified":       all(d["match"] for d in j_decomps),
        },
    }


def main() -> None:
    print("=" * 72)
    print("  MONSTER–SRG BRIDGE:  k = 12 -> Monster")
    print("=" * 72)
    print()

    k = 12
    print(f"  W(3,3) valency k = {k}")
    print()

    print("  (1)  196883 = (4k-1)(5k-1)(6k-1):")
    f = srg_valency_factorization(k)
    print(f"       4k-1 = {f['4k-1']},  5k-1 = {f['5k-1']},  6k-1 = {f['6k-1']}")
    print(f"       product = {f['product']}  ==  196883:  {f['is_196883']}")
    p = verify_primes_47_59_71()
    print(f"       47 prime: {p[47]},  59 prime: {p[59]},  71 prime: {p[71]}")
    print(f"       AP with common difference = {k}")
    print()

    print("  (2)  j-coefficient Monster irrep decompositions:")
    for d in verify_all_j_decompositions():
        print(f"       c({d['n']:>2d}) = {d['c(n)']:>15d}  =  sum{d['decomposition']}  =  {d['sum']}"
              f"  match={d['match']}")
    print()

    print("  (3)  196884 = 196883 + 1 = d_1 + d_2:")
    m = the_moonshine_identity()
    print(f"       c(1) = {m['c(1)']},  d_1 + d_2 = {m['d_1 + d_2']},  match = {m['match']}")
    print()

    print("  (4)  Critical string dimension:")
    cd = critical_dimension(k)
    print(f"       D_crit = 2k + 2 = {cd['D_crit']}")
    print(f"       Transverse dimensions = 2k = {cd['2k']} = Leech rank = eta exponent")
    print()

    chain = derive_full_bridge(k)
    print("  SUMMARY CHAIN:")
    for key, val in chain["summary_chain"].items():
        print(f"       {key}: {val}")
    print()

    out = Path(__file__).resolve().parent.parent / "data" / "w33_monster_srg_bridge.json"
    out.write_text(json.dumps(chain, indent=2, default=str))
    print(f"  wrote {out}")


if __name__ == "__main__":
    main()
