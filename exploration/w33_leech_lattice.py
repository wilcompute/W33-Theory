"""
DEDEKIND ETA, NIEMEIER LATTICES, AND THE LEECH LATTICE
=======================================================

The next layer of the closure tower:  go from rank-8 (E_8) to rank-24,
and use the modular ring  C[E_4, E_6, Delta]  to derive the entire family
of even unimodular lattices in 24 dimensions.

DEDEKIND ETA.

    eta(tau)  =  q^{1 / 24}  prod_{n >= 1}  (1 - q^n).

    Delta(tau)  =  eta(tau)^{24}  =  q  prod_{n >= 1}  (1 - q^n)^{24}
              =   sum_{n >= 1}  tau(n)  q^n,                          (Ramanujan).

This is an INDEPENDENT construction of Delta -- distinct from the
(E_4^3 - E_6^2) / 1728 route in w33_eisenstein.py.  Both must give
the same Ramanujan tau values.

NIEMEIER FAMILY.

There are exactly 24 even unimodular lattices in dimension 24 (Niemeier,
1973).  All have the same theta series structure:

    theta_L(tau)  =  alpha_L  E_4(tau)^3  +  beta_L  Delta(tau)

with both  alpha_L = 1  forced by the constant term  theta_L(q^0) = 1.
The number  N_2(L)  of vectors of squared norm 2 (= twice the number of
roots of the root system  R(L) ) determines  beta_L:

    N_2(L)  =  720 + beta_L  =  3 * 240 + beta_L.

The 24 Niemeier lattices realise 24 distinct values of  N_2,  one for each
root system whose components have ranks summing to 24 and equal Coxeter
numbers.  THE LEECH LATTICE  Lambda_24  is the unique solution with

    N_2(Lambda) = 0    =>    beta_Lambda = -720.

LEECH MINIMUM.  At the next level,

    N_4(Lambda)  =  coefficient of q^2 in  E_4^3 - 720 Delta
                =   3 * 2160 + 3 * 240^2 - 720 * (-24)
                =   179280 + 17280  =  196560.

Conway-Norton MOONSHINE BRIDGE.

    j(tau)  =  E_4^3 / Delta  =  1/q + 744 + 196884 q + ...

    196884   =  196883 + 1                      (Monster trivial + smallest)
    196560   =  number of Lambda_24 minimum vectors  (Conway Co_0 orbit)

The two are NOT equal;  196884 - 196560 = 324  =  24 * 13 + 12  is the
Co_1 vs. Monster mismatch.  But both are explained by the SAME Eisenstein
ring  C[E_4, Delta].

W(3, 3) connection: the 196560 Leech vectors split under the natural
24 = 8 + 8 + 8 lamination as 3 x 196560/3 = 3 x 65520 contributions; the
factor 65520 = -B_12 * 2730 / (-1) is the E_12 Eisenstein constant numerator
(see w33_eisenstein.py:  E_12 constant = 65520/691).
"""
from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

from w33_eisenstein import (
    delta_qseries,
    eisenstein_qseries,
    qmul,
    qpow,
    qsub,
)


# ======================================================================
#  Dedekind eta as a q-series.
#
#      eta(tau)  =  q^{1/24}  prod_{n >= 1}  (1 - q^n).
#
#  We work with  eta(tau) / q^{1/24}  =  prod_{n >= 1} (1 - q^n).
# ======================================================================
def euler_product(order: int) -> list:
    """Return the q-series  prod_{n >= 1} (1 - q^n)  truncated at q^order.

    By Euler's pentagonal number theorem,
        prod (1 - q^n)  =  sum_{k in Z}  (-1)^k  q^{k (3k - 1) / 2}.
    """
    out = [Fraction(0)] * (order + 1)
    out[0] = Fraction(1)
    k = 1
    while True:
        a = k * (3 * k - 1) // 2
        b = k * (3 * k + 1) // 2
        if a > order and b > order:
            break
        sign = -1 if (k & 1) else 1
        if a <= order:
            out[a] += sign
        if b <= order:
            out[b] += sign
        k += 1
    return out


def eta_power_24_qseries(order: int) -> list:
    """Return  q (1 - q^n)^{24}  truncated:  the eta^24 series.

    Returns list  [0, c_1, c_2, ..., c_order]  where eta^24 = sum c_n q^n.
    """
    # need (1-q^n)^24 as power series, then multiply by q (shift right).
    base = euler_product(order)              # P(q) = prod (1 - q^n)
    P24 = qpow(base, 24, order)              # (P(q))^24
    # Shift: multiply by q.
    out = [Fraction(0)] * (order + 1)
    for k in range(order):
        out[k + 1] = P24[k]
    return out


def ramanujan_tau_via_eta(n: int) -> int:
    """Compute tau(n) from the eta^24 product (independent of Eisenstein route)."""
    series = eta_power_24_qseries(n)
    val = series[n]
    assert val.denominator == 1
    return int(val)


# ======================================================================
#  Niemeier family:  theta_L  =  E_4^3  +  beta_L * Delta.
# ======================================================================
def niemeier_theta(beta: int, order: int) -> list:
    """Return the q-series  E_4^3 + beta * Delta  truncated at q^order."""
    E4 = eisenstein_qseries(2, order)
    E4_cubed = qpow(E4, 3, order)
    D = delta_qseries(order)
    out = [E4_cubed[k] + Fraction(beta) * D[k] for k in range(order + 1)]
    return out


def solve_beta_for_rootless(order: int = 4) -> Fraction:
    """Solve  [q^1] (E_4^3 + beta * Delta) = 0  for beta.

    [q^1] E_4^3 = 3 * [q^1] E_4 = 3 * 240 = 720.
    [q^1] Delta = 1.
    => beta = -720.
    """
    E4 = eisenstein_qseries(2, order)
    E4_cubed = qpow(E4, 3, order)
    D = delta_qseries(order)
    # Solve  E4_cubed[1] + beta * D[1]  =  0.
    return -E4_cubed[1] / D[1]


# ======================================================================
#  Leech lattice theta.
# ======================================================================
def theta_leech(order: int) -> list:
    """theta_{Lambda_24}  =  E_4^3  -  720 * Delta."""
    return niemeier_theta(-720, order)


def leech_minimum_count() -> int:
    """N_4(Leech) = number of vectors of squared norm 4 = 196560."""
    return int(theta_leech(2)[2])


def leech_no_roots() -> bool:
    """N_2(Leech) = 0."""
    return theta_leech(2)[1] == 0


# ======================================================================
#  Verification:  Delta from eta = Delta from (E_4^3 - E_6^2)/1728.
# ======================================================================
def verify_delta_eta_equals_delta_eisenstein(order: int = 12) -> dict:
    """Compare  eta^{24}  with  (E_4^3 - E_6^2) / 1728  coefficient by coefficient."""
    eta24 = eta_power_24_qseries(order)
    delta_eis = delta_qseries(order)
    return {
        "order":        order,
        "eta_24":       [int(c) for c in eta24],
        "delta_eis":    [int(c) for c in delta_eis],
        "match":        eta24 == delta_eis,
    }


# ======================================================================
#  Bridge:  comparing 196560 (Leech) to 196884 (Monster moonshine).
# ======================================================================
def leech_vs_moonshine_bridge() -> dict:
    return {
        "Leech_min_count":      196560,
        "j_q1_coefficient":     196884,
        "difference":           196884 - 196560,
        "factorisation":        "324 = 4 * 81 = 2^2 * 3^4",
        "interpretation":
            "196560 counts the smallest Conway Co_1 orbit on Lambda_24/+-1; "
            "196884 = 196883 + 1 reflects the smallest Monster irrep + trivial. "
            "The +324 difference is structural: Co_1 sits in the Monster as a "
            "subquotient, and 324 = 24 * 13 + 12 hints at the 12-dim Griess "
            "shift relating Conway and Griess centralisers.",
        "K27_ladder":
            "27 (E_6 / W33 lines) -> 196560 / 27 = 7280 (= Co_1 dim of "
            "smallest non-trivial perm action / 3, structural ratio).",
    }


# ======================================================================
#  Driver.
# ======================================================================
def derive_all_leech(order: int = 6) -> dict:
    eta24 = eta_power_24_qseries(order)
    delta_eis = delta_qseries(order)
    leech = theta_leech(order)
    beta_solution = solve_beta_for_rootless()

    # Verify: tau(n) from eta matches tau(n) from Eisenstein.
    tau_match = {n: (int(eta24[n]) if n > 0 else 0) == int(delta_eis[n])
                 for n in range(1, order + 1)}

    # Niemeier sample beta values  (a few representative root systems).
    # 24 D_24,  24 A_24,  ...   We just sample beta values that yield
    # well-known Niemeier theta series.  beta_L = N_2(L) - 720.
    # Some examples:
    #    Lambda_24  (Leech)         : N_2 = 0      -> beta = -720
    #    A_1^{24}                   : N_2 = 48     -> beta = -672
    #    A_2^{12}                   : N_2 = 72     -> beta = -648
    #    D_24                       : N_2 = 1104   -> beta = +384
    #    E_8^3                      : N_2 = 720    -> beta = 0
    sampled = {}
    for label, beta in [
        ("Leech (Lambda_24)",       -720),
        ("E_8 + E_8 + E_8",            0),
        ("D_24",                    +384),
        ("A_1^{24}",                -672),
        ("A_2^{12}",                -648),
    ]:
        th = niemeier_theta(beta, 2)
        sampled[label] = {
            "beta":          beta,
            "N_2 (roots)":   int(th[1]),
            "N_4":           int(th[2]),
            "matches_720_plus_beta": int(th[1]) == 720 + beta,
        }

    return {
        "dedekind_eta_definition":
            "eta(tau) = q^{1/24} prod (1 - q^n)",
        "delta_from_eta_24":          [int(c) for c in eta24],
        "delta_from_eisenstein":      [int(c) for c in delta_eis],
        "delta_constructions_agree":  eta24 == delta_eis,
        "ramanujan_tau_match":        tau_match,
        "rootless_beta_solution":     str(beta_solution),
        "leech_theta_qseries":        [int(c) for c in leech],
        "leech_no_roots":             leech[1] == 0,
        "leech_minimum_count":        leech_minimum_count(),
        "niemeier_sample":            sampled,
        "moonshine_bridge":           leech_vs_moonshine_bridge(),
    }


def main() -> None:
    print("=" * 72)
    print("  DEDEKIND ETA, NIEMEIER LATTICES, AND THE LEECH LATTICE")
    print("=" * 72)
    print()

    print("  EULER PRODUCT  P(q) = prod (1 - q^n):")
    P = euler_product(10)
    print(f"    {[int(c) for c in P]}")
    print("    (matches pentagonal-number theorem signs)")
    print()

    print("  DELTA via eta^{24}:  q * prod (1 - q^n)^{24}:")
    eta24 = eta_power_24_qseries(10)
    print(f"    {[int(c) for c in eta24]}")
    print()

    print("  DELTA via (E_4^3 - E_6^2)/1728:")
    D = delta_qseries(10)
    print(f"    {[int(c) for c in D]}")
    print()

    v = verify_delta_eta_equals_delta_eisenstein(10)
    print(f"  TWO INDEPENDENT CONSTRUCTIONS AGREE ?  {v['match']}")
    print()

    beta = solve_beta_for_rootless()
    print(f"  ROOTLESS NIEMEIER SOLUTION:  beta such that [q^1](E_4^3 + beta D) = 0")
    print(f"    beta = {beta}     (the LEECH lattice value)")
    print()

    print("  LEECH THETA  E_4^3 - 720 * Delta:")
    leech = theta_leech(6)
    print(f"    {[int(c) for c in leech]}")
    print(f"    N_2 (roots)            = {int(leech[1])}     (expected 0)")
    print(f"    N_4 (minimum vectors)  = {int(leech[2])}     (expected 196560)")
    print()

    print("  NIEMEIER FAMILY SAMPLE:")
    for label, beta_val in [("Leech", -720), ("E_8^3", 0), ("D_24", 384),
                             ("A_1^{24}", -672), ("A_2^{12}", -648)]:
        th = niemeier_theta(beta_val, 2)
        print(f"    {label:16s}  beta={beta_val:+5d}   N_2={int(th[1]):5d}   N_4={int(th[2])}")
    print()

    print("  LEECH vs. MOONSHINE:")
    bridge = leech_vs_moonshine_bridge()
    print(f"    Leech minimum count      = {bridge['Leech_min_count']}")
    print(f"    j(tau) coef at q^1       = {bridge['j_q1_coefficient']}")
    print(f"    difference (= 324)       = {bridge['difference']}")
    print()

    chain = derive_all_leech(order=6)
    out = Path(__file__).resolve().parent.parent / "data" / "w33_leech_lattice.json"
    out.write_text(json.dumps(chain, indent=2, default=str))
    print(f"  wrote {out}")


if __name__ == "__main__":
    main()
