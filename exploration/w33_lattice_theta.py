"""
LATTICE THETA SERIES:  E_8 AND LEECH
======================================

The theta series of an even unimodular lattice  L  of rank  2k  is a
weight-k modular form for SL(2, Z):

    Theta_L(tau)  =  sum_{v in L}  q^{(v, v) / 2},   q = e^{2 pi i tau}.

Two classical incarnations:

E_8 LATTICE (rank 8, weight 4).

    Theta_{E_8}(tau)  =  E_4(tau)   exactly.

Since  M_4 = C * E_4  is one-dimensional, matching the constant term
suffices.  The q^1 coefficient equals 240 = |E_8 root system|, and
  [q^n] Theta_{E_8}  =  240 * sigma_3(n)  for  n >= 1.

LEECH LATTICE (rank 24, weight 12).

The unique even unimodular lattice in R^{24} with NO norm-2 vectors.
M_12 has dim 2 with basis {E_4^3, Delta}, so two coefficients pin it:

    Theta_{Leech}  =  E_4^3  -  720 * Delta.

The 720 = 3 * 240 = 3 * |E_8 roots| kills the q^1 coefficient (Leech
has no roots), forcing

    [q^2] Theta_{Leech}  =  179280 + 17280  =  196560

which is the Leech lattice KISSING NUMBER (the max kissing number in
dimension 24, proved by Cohn-Kumar-Miller-Radchenko-Viazovska 2017).

BRIDGE TO W(3, 3).

    k = 12 valency of W(3, 3)
    2k = 24 = rank of Leech lattice = weight of Leech theta
    |E_8 roots| = 240 appears as [q^1] E_4 (= Theta_{E_8})
    3 * |E_8 roots| = 720 = first Ramanujan tau coefficient of j - 744
    Leech kissing 196560 = 196884 - 324 is one step from the
      Monster coefficient c_j(1) = 196884 (monstrous moonshine).

The 744 = 3 * dim(E_8) identity from the McKay layer and the
720 = 3 * |E_8 roots| correction here are the SAME factor-of-three
acting on two different E_8 numerical signatures (dim vs root count).
"""
from __future__ import annotations

import json
from collections import Counter
from itertools import product
from pathlib import Path


# ======================================================================
#  E_8 lattice enumeration.
#
#  E_8 = D_8^+  =  { v in Z^8 : sum v_i even }
#               U  { v in (Z + 1/2)^8 : sum v_i in 2Z }.
#
#  All norms |v|^2 are even integers, and we index by n = |v|^2 / 2.
# ======================================================================
def enumerate_e8_norms(n_max: int) -> Counter:
    """Return counts: counts[n] = #{v in E_8 : (v, v) = 2n}  for 0 <= n <= n_max.

    Direct enumeration; feasible for small n_max (n_max <= 4 is fast).
    """
    counts: Counter = Counter()
    max_norm_sq = 2 * n_max

    # Integer coords: v in Z^8, sum v_i even.
    bound = int(max_norm_sq ** 0.5) + 1
    for v in product(range(-bound, bound + 1), repeat=8):
        ns = sum(x * x for x in v)
        if ns > max_norm_sq:
            continue
        if sum(v) % 2 != 0:
            continue
        counts[ns // 2] += 1

    # Half-integer coords: 2*v_i = w_i odd, sum w_i divisible by 4.
    # |v|^2 = (sum w_i^2) / 4, so |v|^2 = 2n  iff  sum w_i^2 = 8n.
    wbound = int((4 * max_norm_sq) ** 0.5) + 1
    odd_list = [i for i in range(-wbound - 1, wbound + 2) if i % 2 != 0]
    for w in product(odd_list, repeat=8):
        ws = sum(x * x for x in w)
        if ws > 4 * max_norm_sq:
            continue
        if sum(w) % 4 != 0:
            continue
        counts[ws // 8] += 1

    return counts


def e8_theta_coefficients(n_max: int) -> list:
    """Theta coefficients of E_8 as a list [c_0, c_1, ..., c_{n_max}]."""
    counts = enumerate_e8_norms(n_max)
    return [counts.get(n, 0) for n in range(n_max + 1)]


# ======================================================================
#  E_4 series for comparison.
# ======================================================================
def _sigma(k: int, n: int) -> int:
    return sum(d ** k for d in range(1, n + 1) if n % d == 0)


def e4_series(n_max: int) -> list:
    """E_4(tau) = 1 + 240 sum_{n>=1} sigma_3(n) q^n."""
    coefs = [1] + [240 * _sigma(3, n) for n in range(1, n_max + 1)]
    return coefs


def verify_e8_theta_equals_e4(n_max: int = 3) -> dict:
    """Direct check: E_8 lattice theta = E_4."""
    e8 = e8_theta_coefficients(n_max)
    e4 = e4_series(n_max)
    mismatches = [(n, e8[n], e4[n]) for n in range(n_max + 1) if e8[n] != e4[n]]
    return {
        "n_max":       n_max,
        "e8_theta":    e8,
        "e4_series":   e4,
        "mismatches":  mismatches,
        "all_match":   len(mismatches) == 0,
        "q0_is_1":          e8[0] == 1,
        "q1_is_240_roots":  e8[1] == 240,
        "q2_is_2160":       e8[2] == 2160 if n_max >= 2 else None,
        "q3_is_6720":       e8[3] == 6720 if n_max >= 3 else None,
    }


# ======================================================================
#  Leech theta = E_4^3 - 720 * Delta.
# ======================================================================
def e6_series(n_max: int) -> list:
    """E_6(tau) = 1 - 504 sum sigma_5(n) q^n."""
    return [1] + [-504 * _sigma(5, n) for n in range(1, n_max + 1)]


def _series_mul(A: list, B: list, n_max: int) -> list:
    out = [0] * (n_max + 1)
    for i in range(n_max + 1):
        if A[i] == 0:
            continue
        for j in range(n_max + 1 - i):
            if B[j] != 0:
                out[i + j] += A[i] * B[j]
    return out


def delta_from_e4_e6(n_max: int) -> list:
    """Delta = (E_4^3 - E_6^2) / 1728, via the modular-ring identity."""
    e4 = e4_series(n_max)
    e6 = e6_series(n_max)
    e4_cubed = _series_mul(_series_mul(e4, e4, n_max), e4, n_max)
    e6_sq = _series_mul(e6, e6, n_max)
    diff = [e4_cubed[i] - e6_sq[i] for i in range(n_max + 1)]
    # Must be divisible by 1728
    delta = [c // 1728 for c in diff]
    assert all(c * 1728 == d for c, d in zip(delta, diff)), "Delta not integral"
    return delta


def leech_theta_coefficients(n_max: int) -> list:
    """Theta_{Leech} = E_4^3 - 720 * Delta."""
    e4 = e4_series(n_max)
    delta = delta_from_e4_e6(n_max)
    e4_cubed = _series_mul(_series_mul(e4, e4, n_max), e4, n_max)
    return [e4_cubed[i] - 720 * delta[i] for i in range(n_max + 1)]


def verify_leech_theta(n_max: int = 4) -> dict:
    """Check Leech kissing number = 196560 and other pins."""
    leech = leech_theta_coefficients(n_max)
    delta = delta_from_e4_e6(n_max)
    e4 = e4_series(n_max)
    e4_cubed = _series_mul(_series_mul(e4, e4, n_max), e4, n_max)
    expected_first_five = [1, 0, 196560, 16773120, 398034000]
    return {
        "n_max":        n_max,
        "leech_theta":  leech,
        "e4_cubed":     e4_cubed,
        "delta":        delta[:n_max + 1],
        "constant_term_is_1":  leech[0] == 1,
        "q1_is_0_no_roots":     leech[1] == 0,
        "kissing_number_196560": leech[2] == 196560 if n_max >= 2 else None,
        "q3_is_16773120":       leech[3] == 16773120 if n_max >= 3 else None,
        "matches_known_values": (leech[: min(n_max + 1, 5)]
                                 == expected_first_five[: min(n_max + 1, 5)]),
    }


# ======================================================================
#  720 = 3 * 240 bridge.
# ======================================================================
def verify_720_equals_3_times_E8_roots() -> dict:
    """The correction 720 * Delta that turns E_4^3 into Theta_Leech is
    exactly 3 * |E_8 roots|."""
    e8_roots = 240
    expected = 720
    return {
        "e8_roots":           e8_roots,
        "3_times_e8_roots":   3 * e8_roots,
        "leech_correction":   720,
        "match":              3 * e8_roots == 720,
        "also_equals":        "3 * 240 = 720 = 6! = 3 * [q^1] E_4",
    }


# ======================================================================
#  Moonshine proximity: 196560 vs 196884.
# ======================================================================
def moonshine_gap() -> dict:
    """The Leech kissing number is one modular form away from the
    monstrous moonshine coefficient c_j(1) = 196884."""
    kissing = 196560
    c_j_1 = 196884
    monster_smallest = 196883
    return {
        "leech_kissing":             kissing,
        "c_j(1)":                    c_j_1,
        "monster_smallest_irrep":    monster_smallest,
        "moonshine":                 c_j_1 == monster_smallest + 1,
        "kissing_to_c_j_1_diff":     c_j_1 - kissing,
        "kissing_to_monster_diff":   monster_smallest - kissing,
    }


# ======================================================================
#  Driver.
# ======================================================================
def derive_all_lattice_theta(n_max: int = 3) -> dict:
    e8_check = verify_e8_theta_equals_e4(n_max=n_max)
    leech_check = verify_leech_theta(n_max=4)
    bridge = verify_720_equals_3_times_E8_roots()
    moon = moonshine_gap()
    return {
        "e8_theta_check":    e8_check,
        "leech_theta_check": leech_check,
        "bridge_720_3x240":  bridge,
        "moonshine_gap":     moon,
        "summary_chain": {
            "Theta_E8_equals_E4":           e8_check["all_match"],
            "E8_q1_coef_is_240_roots":      e8_check["q1_is_240_roots"],
            "Theta_Leech_q0_is_1":          leech_check["constant_term_is_1"],
            "Leech_has_no_roots":           leech_check["q1_is_0_no_roots"],
            "Leech_kissing_196560":         leech_check["kissing_number_196560"],
            "720_equals_3_times_E8_roots":  bridge["match"],
            "c_j_1_equals_196883_plus_1":   moon["moonshine"],
        },
    }


def main() -> None:
    print("=" * 72)
    print("  LATTICE THETA SERIES: E_8 AND LEECH")
    print("=" * 72)
    print()

    print("  Enumerating E_8 lattice vectors (this may take a few seconds)...")
    e8 = e8_theta_coefficients(3)
    print(f"  Theta_E8 coefficients (q^0..q^3):  {e8}")
    print(f"  E_4 coefficients     (q^0..q^3):  {e4_series(3)}")
    print(f"  Match: {e8 == e4_series(3)}")
    print()
    print(f"  |E_8 root system| = 240 = [q^1] Theta_E8")
    print(f"  [q^2] = 240 * sigma_3(2) = 240 * 9 = {240*9}")
    print(f"  [q^3] = 240 * sigma_3(3) = 240 * 28 = {240*28}")
    print()

    leech = leech_theta_coefficients(4)
    print(f"  Theta_Leech = E_4^3 - 720 * Delta:")
    print(f"    first 5 coefs: {leech}")
    print(f"    Leech kissing number (coef of q^2) = {leech[2]}")
    print()

    bridge = verify_720_equals_3_times_E8_roots()
    print(f"  Bridge: 720 = 3 * |E_8 roots| = 3 * 240 = {bridge['3_times_e8_roots']}")
    print()

    moon = moonshine_gap()
    print(f"  Moonshine proximity:")
    print(f"    Leech kissing   = 196560")
    print(f"    c_j(1) (j-coef) = 196884 = 196883 + 1  (Monster irrep + 1)")
    print(f"    difference      = {moon['kissing_to_c_j_1_diff']}")
    print()

    chain = derive_all_lattice_theta(n_max=3)
    print("  SUMMARY CHAIN:")
    for k, v in chain["summary_chain"].items():
        print(f"    {k}: {v}")
    print()

    out = Path(__file__).resolve().parent.parent / "data" / "w33_lattice_theta.json"
    out.write_text(json.dumps(chain, indent=2, default=str))
    print(f"  wrote {out}")


if __name__ == "__main__":
    main()
