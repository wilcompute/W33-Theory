"""
SOLVING THE MOONSHINE 324:  WHY  196884 = 196560 + 324
=======================================================

OPEN PROBLEM.  The previous Leech layer (w33_leech_lattice.py) noted that
the j-invariant coefficient at q^1, namely 196884, exceeds the Leech minimum
vector count 196560 by exactly 324, but only sketched why.  This module
proves the identity completely, deriving 324 mechanically and then upgrading
to a closed formula for EVERY j-coefficient as a sum of Leech vector counts
weighted by 24-color partition numbers.

THE LATTICE-CFT IDENTITY.

For an even unimodular lattice L of rank r, the vertex algebra V_L has
graded character

    chi_{V_L}(tau)  =  theta_L(tau)  /  eta(tau)^r.

For Leech (rank 24) this is

    chi_{V_Lambda}(tau)
        =  theta_Lambda(tau) / eta(tau)^{24}
        =  (E_4^3 - 720 Delta) / Delta
        =  E_4^3 / Delta  -  720
        =  j(tau)  -  720.

So the modular-form identity

    j(tau)  =  720  +  theta_Lambda(tau) * Delta(tau)^{-1}

becomes a coefficient identity for every n >= -1:

    [q^n] j(tau)  =  720 * delta_{n, 0}  +  sum_{k} N_{2k}(Lambda) * p_{24}(n - k + 1)

where  N_{2k}(Lambda)  is the number of Leech vectors of squared norm 2k and
p_{24}(m)  is the number of partitions of m into parts of 24 colors -- the
graded dimensions of the 24 free bosons that make up the lattice CFT.

THE 324.

    1 / Delta(tau)  =  q^{-1}  +  24  +  324 q  +  3200 q^2  +  25650 q^3  + ...

The constant 24 = p_{24}(1), the Leech rank.
The 324 = p_{24}(2):

    p_{24}(2)
       =  (one part of size 2, any of 24 colors)            =  24
       +  (two parts of size 1, repetitions allowed)         =  C(24 + 1, 2) = 300
       =  324.

Computing  [q^1] j  via the convolution:

    [q^1] j  =  720 * 0  +  sum_k  N_{2k} * p_{24}(1 - k + 1)
            =  N_0 * p_{24}(2)  +  N_2 * p_{24}(1)  +  N_4 * p_{24}(0)
            =    1   *   324    +    0  *   24      +  196560 *   1
            =  324  +  0  +  196560
            =  196884.

DECOMPOSITION:  196884 = 196560 + 324.  The 196560 is the geometric
contribution (one Leech minimum vector creating a primary state), and the
324 is the oscillator contribution (two free bosons exciting the vacuum).

W(3, 3) BRIDGE.

    324  =  18^2                                            (perfect square)
    324  =  24 * Phi_3(3)  +  k                            (= 312 + 12)
    324  =  p_24(2)        =  24 + C(25, 2) = 24 + 300

The decomposition  324 = 24 + 300  matches  rank(Leech) + (2-oscillator BE
states), and  300 = 12 * 25 = k * (k + 13) = k * (k + Phi_3(q))  on the W(3,3)
side, threading the SRG valency into the Monster module.
"""
from __future__ import annotations

import json
from fractions import Fraction
from math import comb
from pathlib import Path

from w33_eisenstein import (
    delta_qseries,
    eisenstein_qseries,
    j_invariant_qseries,
    qinv,
    qmul,
    qpow,
)
from w33_leech_lattice import theta_leech


# ======================================================================
#  24-color partition numbers.
#
#      sum_{n >= 0}  p_{24}(n)  q^n   =   prod_{n >= 1}  (1 - q^n)^{-24}.
# ======================================================================
def p24_partitions(order: int) -> list:
    """Return [p_24(0), p_24(1), ..., p_24(order)] as integers."""
    # Compute prod (1 - q^n) truncated, then invert as power series.
    # 1/Delta = q^{-1} prod(1-q^n)^{-24}; here we want just the product part.
    # Build prod(1 - q^n) up to order.
    prod = [Fraction(0)] * (order + 1)
    prod[0] = Fraction(1)
    n = 1
    while n <= order:
        # multiply prod by (1 - q^n)
        new = list(prod)
        for k in range(order - n + 1):
            new[k + n] -= prod[k]
        prod = new
        n += 1
    # Now invert and raise to 24th power.
    prod_inv = qinv(prod, order)
    # raise to 24th power
    p24 = qpow(prod_inv, 24, order)
    out = []
    for c in p24:
        assert c.denominator == 1, f"p_24 not integer: {c}"
        out.append(int(c))
    return out


def p24_combinatorial(n: int) -> int:
    """Direct combinatorial formula for p_24(2):   24 + C(24+1, 2) = 24 + 300 = 324."""
    if n == 0:
        return 1
    if n == 1:
        return 24                          # one box of color in 24 ways
    if n == 2:
        # one part of size 2 (24 ways)  +  two parts of size 1 with repetition
        return 24 + comb(24 + 1, 2)
    raise NotImplementedError("only small n hard-coded")


# ======================================================================
#  Inverse of Delta as a power series.
#
#      1 / Delta(tau)  =  q^{-1}  +  24  +  324 q  +  3200 q^2  +  ...
#
#  We compute  Delta_tilde  =  Delta / q  =  prod (1 - q^n)^{24},
#  then invert  Delta_tilde  to get  q / Delta.
# ======================================================================
def inv_delta_qseries(order_above_pole: int) -> dict:
    """Return  {-1: 1, 0: 24, 1: 324, 2: 3200, ...}  for  1/Delta(tau)
    up to coefficient at q^{order_above_pole}.
    """
    # Delta truncated to enough terms.  qinv needs D_tilde[0..order+1] to compute inv[order+1].
    D = delta_qseries(order_above_pole + 2)
    D_tilde = D[1:]                                # = prod (1 - q^n)^{24},  length order+2
    inv = qinv(D_tilde, order_above_pole + 1)      # q / Delta = inverse of D_tilde
    # 1/Delta = (1/q) * (q/Delta) so coefficient at q^n in 1/Delta = inv[n+1]
    out = {-1: int(inv[0])}
    for n in range(0, order_above_pole + 1):
        c = inv[n + 1]
        assert c.denominator == 1, f"1/Delta coef not integer: {c}"
        out[n] = int(c)
    return out


# ======================================================================
#  Verify  1/Delta  matches 24-color partition generating function.
# ======================================================================
def verify_inv_delta_equals_q_inv_times_p24(order: int = 6) -> dict:
    """Verify  1 / Delta(tau)  =  (1/q)  *  prod (1 - q^n)^{-24}."""
    inv_d = inv_delta_qseries(order)
    p24 = p24_partitions(order + 1)        # need p_24(0), p_24(1), ..., p_24(order+1)
    # Identity:  [q^n] (1/Delta)  =  p_24(n + 1).
    matches = {}
    for n in range(-1, order + 1):
        matches[n] = (inv_d[n] == p24[n + 1])
    return {
        "order":          order,
        "inv_delta":      inv_d,
        "p_24":           p24,
        "all_match":      all(matches.values()),
        "per_coeff":      matches,
    }


# ======================================================================
#  THE KEY DECOMPOSITION.
#
#      [q^n] j(tau)  =  720 * delta_{n,0}  +  sum_k  N_{2k}(Lambda) * p_{24}(n - k + 1).
# ======================================================================
def decompose_j_via_leech(n: int) -> dict:
    """Decompose [q^n] j(tau) as Leech * partition convolution + 720 * delta_{n,0}."""
    # Need theta_Lambda up to enough order, and p_24 up to enough.
    # For [q^n] j, contributions come from k <= n + 1 (since p_24 needs n-k+1 >= 0).
    K = n + 1
    leech = theta_leech(K)         # [N_0, N_2, N_4, ...]  i.e., N_{2k} at index k
    p24 = p24_partitions(n + 2)    # p_24(0), ..., p_24(n+1)

    contributions = []
    total_lattice = 0
    for k in range(K + 1):
        Nk = int(leech[k])
        m = n - k + 1
        if m < 0:
            continue
        pm = p24[m]
        contrib = Nk * pm
        contributions.append({
            "k":               k,
            "squared_norm":    2 * k,
            "N_{2k}":          Nk,
            "p_24(n-k+1)":     pm,
            "n-k+1":           m,
            "contribution":    contrib,
        })
        total_lattice += contrib

    constant = 720 if n == 0 else 0
    j_via_decomp = total_lattice - constant            # j = chi_Lambda + 720 = (theta_Lambda/Delta) + 720,
                                                       # but theta_Lambda/Delta is what equals j-720, so:
    # Re-derive carefully:
    #   chi_Lambda = j - 720
    #   chi_Lambda = theta_Lambda * (1/Delta)
    # So  [q^n] j  =  [q^n] chi_Lambda  +  720 * delta_{n, 0}
    #              =  sum_k N_{2k} * p_{24}(n - k + 1)  +  720 * delta_{n, 0}
    j_predicted = total_lattice + constant

    j_actual = j_invariant_qseries(max(n, 1))[n]

    return {
        "n":                       n,
        "contributions":           contributions,
        "lattice_sum":             total_lattice,
        "constant_720_at_n_eq_0":  constant,
        "j_via_decomposition":     j_predicted,
        "j_actual":                j_actual,
        "match":                   j_predicted == j_actual,
    }


# ======================================================================
#  Special case proven: 196884 = 196560 + 324.
# ======================================================================
def the_324_solution() -> dict:
    """Mechanically prove  196884 = 196560 + 324."""
    decomp = decompose_j_via_leech(1)
    # The two non-zero contributions at n=1:
    #   k=0:  N_0 = 1    *  p_24(2) = 324    =>  324       (oscillator)
    #   k=2:  N_4 = 196560 * p_24(0) = 1     =>  196560    (Leech minimum vectors)
    p24_2 = p24_combinatorial(2)
    return {
        "j_q_coef":                  196884,
        "leech_minimum_count":       196560,
        "oscillator_contribution":   324,
        "p_24_of_2_combinatorial":   {
            "one_part_of_2_in_24_colors":   24,
            "two_parts_of_1_with_reps":     comb(25, 2),
            "total":                         24 + comb(25, 2),
        },
        "p_24_of_2_value":           p24_2,
        "p_24_matches":              p24_2 == 324,
        "convolution_explained":     decomp,
        "moonshine_relation":        "196884 = 196883 + 1 (Monster)",
        "lattice_relation":          "196884 = 196560 + 324 (Leech CFT)",
        "bridge":                    "Both are TRUE; they are different reductions of the same number.",
    }


# ======================================================================
#  Higher-order extension: solve for [q^2] j = 21493760.
# ======================================================================
def the_21493760_solution() -> dict:
    """Decompose  [q^2] j = 21493760  via Leech and 24-color oscillators.

    Contributions:
      k=0: 1       * p_24(3) = 1 * 3200  =       3200
      k=2: 196560  * p_24(1) = 196560 * 24 =  4717440
      k=3: N_6     * p_24(0) = N_6 * 1    =   N_6 = 16773120
      total:                                 21493760  =  3200 + 4717440 + 16773120.
    """
    decomp = decompose_j_via_leech(2)
    return {
        "j_q2_coef":   21493760,
        "monster_decomposition":
            "21493760 = 1 + 196883 + 21296876   (sum of three smallest Monster irreps)",
        "leech_decomposition_via_CFT": decomp,
    }


# ======================================================================
#  Driver.
# ======================================================================
def derive_all_moonshine_decomposed(max_n: int = 5) -> dict:
    inv_d = inv_delta_qseries(max_n)
    p24 = p24_partitions(max_n + 1)
    inv_check = verify_inv_delta_equals_q_inv_times_p24(max_n)

    decompositions = {}
    for n in range(-1, max_n + 1):
        try:
            decompositions[f"q^{n}"] = decompose_j_via_leech(n)
        except Exception as e:
            decompositions[f"q^{n}"] = {"error": str(e)}

    return {
        "inv_delta":                 inv_d,
        "p_24_partitions":           p24,
        "inv_delta_equals_q_inv_p24":  inv_check,
        "the_324_solution":          the_324_solution(),
        "the_21493760_solution":     the_21493760_solution(),
        "all_decompositions":        decompositions,
        "master_identity":
            "j(tau) - 720  =  theta_Lambda(tau) / Delta(tau)  =  chi_{V_Lambda}(tau)",
        "consequence":
            "Every j-coefficient is a finite sum of Leech vector counts weighted "
            "by 24-color partition numbers; the Monster is the natural symmetry "
            "of this sum.",
    }


def main() -> None:
    print("=" * 72)
    print("  SOLVING THE MOONSHINE 324 PROBLEM")
    print("=" * 72)
    print()

    print("  STEP 1 -- 1/Delta(tau) coefficients are 24-color partition numbers.")
    inv_d = inv_delta_qseries(5)
    p24 = p24_partitions(6)
    print(f"    [q^n] (1/Delta) for n = -1..5 :  {[inv_d[n] for n in range(-1, 6)]}")
    print(f"    p_24(n) for       n =  0..6 :  {p24}")
    print(f"    These agree by  [q^n](1/Delta) = p_24(n+1).")
    print()

    print("  STEP 2 -- Show p_24(2) = 324 combinatorially.")
    print(f"    one part of size 2 in any of 24 colors :   24")
    print(f"    two parts of size 1, repetitions allowed :  C(25, 2) = 300")
    print(f"    total                                  :  324")
    print()

    print("  STEP 3 -- The KEY IDENTITY:  196884 = 196560 + 324.")
    sol = the_324_solution()
    decomp = sol["convolution_explained"]
    print(f"    Contributions to [q^1] j(tau):")
    for c in decomp["contributions"]:
        if c["contribution"] != 0:
            print(f"      k={c['k']}  |v|^2={c['squared_norm']:2d}  "
                  f"N_{{2k}}={c['N_{2k}']:7d}  *  p_24({c['n-k+1']})={c['p_24(n-k+1)']:5d}  "
                  f"=  {c['contribution']:7d}")
    print(f"    sum                                               =  {decomp['lattice_sum']}")
    print(f"    [q^1] j (actual)                                  =  {decomp['j_actual']}")
    print(f"    match                                             =  {decomp['match']}")
    print()

    print("  STEP 4 -- Generalize to next coefficient:  [q^2] j = 21493760.")
    sol2 = the_21493760_solution()
    decomp2 = sol2["leech_decomposition_via_CFT"]
    print(f"    Contributions to [q^2] j(tau):")
    for c in decomp2["contributions"]:
        if c["contribution"] != 0:
            print(f"      k={c['k']}  |v|^2={c['squared_norm']:2d}  "
                  f"N_{{2k}}={c['N_{2k}']:8d}  *  p_24({c['n-k+1']})={c['p_24(n-k+1)']:5d}  "
                  f"=  {c['contribution']:9d}")
    print(f"    sum                                               =  {decomp2['lattice_sum']}")
    print(f"    [q^2] j (actual)                                  =  {decomp2['j_actual']}")
    print(f"    match                                             =  {decomp2['match']}")
    print()

    print("  CONCLUSION.")
    print("    j(tau) - 720  =  theta_Lambda(tau) / Delta(tau)  =  chi_{V_Lambda}(tau)")
    print("    Every j-coefficient is a finite Z-linear combination")
    print("    of Leech vector counts weighted by 24-color partition numbers.")
    print("    The Monster is the symmetry of THIS decomposition;")
    print("    196884 = 196560 + 324 is its mechanical proof at level 1.")
    print()

    chain = derive_all_moonshine_decomposed(max_n=4)
    out = Path(__file__).resolve().parent.parent / "data" / "w33_moonshine_decomposed.json"
    out.write_text(json.dumps(chain, indent=2, default=str))
    print(f"  wrote {out}")


if __name__ == "__main__":
    main()
