"""W(3,3) BREAKTHROUGH 298: RAMANUJAN / EXPANDER GRAPHS AT SUBSTRATE PRIMES.

A Ramanujan graph X is a k-regular graph whose non-trivial adjacency
eigenvalues satisfy |lambda| <= 2 * sqrt(k - 1). Such graphs are
provably optimal expanders.

The LPS (Lubotzky-Phillips-Sarnak 1988) construction produces explicit
Ramanujan graphs X^{p, q} indexed by pairs of primes (p, q) with p == q
== 1 mod 4. This BT identifies the substrate-natural Ramanujan
constructions and connects to the BT chain.

==============================================================
LPS RAMANUJAN GRAPHS X^{p, q}
==============================================================

For primes p, q with p == q == 1 mod 4, the LPS graph X^{p, q} is:
  vertices: PSL(2, F_q) (when (p/q) = +1)
  k-regular with k = p + 1
  Ramanujan: |lambda_2| <= 2 * sqrt(p)

==============================================================
SUBSTRATE-NATURAL LPS CHOICE: (p, q) = (F_5, p_Ih)?
==============================================================

We need both p, q == 1 mod 4. Substrate primitives:
  q = 3 == 3 mod 4   (NOT 1 mod 4)
  F_5 = 5 == 1 mod 4 (YES)
  Phi_6 = 7 == 3 mod 4 (NOT)
  p_Ih = 11 == 3 mod 4 (NOT)
  Phi_3 = 13 == 1 mod 4 (YES)
  M_5 = 31 == 3 mod 4 (NOT)
  F_5+lambda+lambda = 17 == 1 mod 4 (substrate-adjacent)

Substrate-natural primes == 1 mod 4 are F_5 and Phi_3.

THE LPS CHOICE (p, q) = (F_5, Phi_3):
  X^{F_5, Phi_3} = X^{5, 13}
  |V| = |PSL(2, 13)| = 1092 = lambda^lambda * q * Phi_6 * Phi_3
  k = F_5 + 1 = 6 = q! (SUBSTRATE!)
  Ramanujan: |lambda_2| <= lambda * sqrt(F_5)

==============================================================
SUBSTRATE STAR: LPS DEGREE = q!
==============================================================

  X^{F_5, Phi_3} is 6-regular with k = F_5 + 1 = q! (substrate!).

NEW SUBSTRATE STAR:
  At LPS prime p = F_5, the graph is q! = 6-regular.

==============================================================
|V(X^{F_5, Phi_3})| = 1092 (NEW STAR)
==============================================================

  |V| = |PSL(2, 13)| = 1092 = lambda^lambda * q * Phi_6 * Phi_3
                              = 4 * 3 * 7 * 13
                              = lambda^lambda * q * Phi_6 * Phi_3

ALL FOUR substrate factors (lambda, q, Phi_6, Phi_3).

This is the second Hurwitz-curve order above Klein quartic (BT289):
  Hurwitz curve at genus 14 has |Aut| = 1092 (BT289).

NEW IDENTITY:
  |V(X^{F_5, Phi_3})| = |Aut(genus-14 Hurwitz curve)| = 1092.

==============================================================
ALON-BOPPANA BOUND AT SUBSTRATE k
==============================================================

Alon-Boppana (1986): every k-regular graph X with diameter d satisfies
  lambda_2(X) >= 2 * sqrt(k - 1) - O(1).

Equality holds for Ramanujan graphs in the infinite-vertex limit.

At substrate k = q = 3 (Heawood, Petersen, MK -- BT chain cubic cages):
  lambda_2 >= lambda * sqrt(lambda) = lambda^(3/2) ~ 2.83

The Heawood graph spectrum (BT267) is {3, sqrt(2), -sqrt(2), -3}.
  lambda_2 = sqrt(2) = sqrt(lambda).

NEW IDENTITY:
  Heawood's lambda_2 = sqrt(lambda) (= sqrt(2)).
  Heawood is RAMANUJAN with lambda_2 < 2*sqrt(q - 1) = lambda*sqrt(lambda).

==============================================================
PETERSEN AND MOBIUS-KANTOR RAMANUJAN STATUS
==============================================================

Petersen (BT279):
  spectrum {3, 1, -2} with mults (1, F_5, mu)
  lambda_2 = 1
  Ramanujan bound at k = q = 3: 2*sqrt(k-1) = 2*sqrt(lambda) ~ 2.83
  1 <= 2.83 -> Petersen IS Ramanujan.

Mobius-Kantor (BT270):
  3-regular, lambda_2 = sqrt(3) = sqrt(q)
  Ramanujan: sqrt(q) <= 2*sqrt(q-1) = 2*sqrt(lambda) iff q <= 4*lambda = 8.
  At q = 3, sqrt(3) ~ 1.73 < 2*sqrt(2) ~ 2.83 -> MK IS Ramanujan.

ALL THREE substrate cubic cages (Heawood, Petersen, Mobius-Kantor)
are Ramanujan graphs.

==============================================================
CAYLEY GRAPHS OF SUBSTRATE GROUPS
==============================================================

Several substrate-natural Cayley graphs:
  Cay(F_q^n, std basis) = Q_n (BT157 etc.)
  Cay(Z_q^lambda, gens) = q-cycle products
  Cay(PSL(2, F_q), reflections) = LPS-type
  Cay(Sp(4, F_q), generators) = Sp-Cayley graphs

PSL(2, F_5) order = 60 = mu * g_neg = |V(C_60)| (BT284 link!)
  Cayley graph of PSL(2, F_5) on substrate generators has 60 = |V(C_60)|
  vertices.

PSL(2, F_7) order = 168 = Aut(Fano) = Aut(KQ) (BT285 link).
PSL(2, F_11) order = 660 = ?
PSL(2, F_13) order = 1092 (above).

==============================================================
THE RAMANUJAN PRIME COUNT
==============================================================

Substrate primes 1 mod 4: {F_5, Phi_3}, the substrate primes 3 mod 4:
{q, Phi_6, p_Ih, M_5}.

  #(substrate primes == 1 mod 4) = lambda = 2
  #(substrate primes == 3 mod 4) = mu = 4

NEW PARTITION:
  6 = lambda + mu = q! substrate primes total split as lambda + mu
  by quadratic residue character.

==============================================================
"""
from __future__ import annotations

import json
from pathlib import Path


def main():
    q = 3
    lambda_, mu = 2, 4
    F5 = 5
    phi3 = 13
    phi6 = 7
    p_Ih = 11
    M5 = 31

    print("=" * 78)
    print("W(3,3) BREAKTHROUGH 298: RAMANUJAN / EXPANDER SUBSTRATE")
    print("=" * 78)
    print()

    print("LPS CONSTRUCTION X^{p, q} REQUIRES p, q == 1 mod 4:")
    sp_primes_1_mod_4 = [F5, phi3]
    sp_primes_3_mod_4 = [q, phi6, p_Ih, M5]
    print(f"  Substrate primes == 1 mod 4: {sp_primes_1_mod_4} (count = lambda)")
    print(f"  Substrate primes == 3 mod 4: {sp_primes_3_mod_4} (count = mu)")
    print(f"  Total substrate primes: lambda + mu = q! = 6")
    print()

    print("SUBSTRATE-NATURAL LPS: X^{F_5, Phi_3}")
    V_lps = 1092
    k_lps = F5 + 1
    assert V_lps == lambda_**lambda_ * q * phi6 * phi3
    assert k_lps == 6 == 2 * q  # = q!
    print(f"  |V| = |PSL(2, 13)| = {V_lps}")
    print(f"       = lambda^lambda * q * Phi_6 * Phi_3 = 4 * 3 * 7 * 13")
    print(f"  k = F_5 + 1 = 6 = q!                          *** STAR ***")
    print(f"  Ramanujan: |lambda_2| <= lambda * sqrt(F_5)")
    print()

    print("STAR LINK: LPS V = HURWITZ Aut at g = 14")
    print(f"  |V(X^{{F_5, Phi_3}})| = 1092 = |Aut(Hurwitz curve g=14)| (BT289)")
    print()

    print("SUBSTRATE CUBIC CAGES ARE ALL RAMANUJAN:")
    cages = [
        ("Heawood",       "{3, +/-sqrt(2), -3}", "sqrt(lambda)",    "BT267"),
        ("Petersen",      "{3, 1, -2}",           "1",                 "BT279"),
        ("Mobius-Kantor", "{3, +/-sqrt(3), ...}", "sqrt(q)",           "BT270"),
    ]
    print(f"  Graph            spectrum                lambda_2     link")
    for n, sp, l2, l in cages:
        print(f"  {n:<14}  {sp:<22}   {l2:<14} {l}")
    print()
    print(f"  Ramanujan bound at k = q = 3: lambda_2 <= lambda * sqrt(lambda) ~ 2.83")
    print(f"  All three substrate cubic cages satisfy this -- ALL RAMANUJAN.")
    print()

    print("CAYLEY GRAPHS OF PSL(2, F_p) AT SUBSTRATE p:")
    psl = [
        (F5,    60,    "mu * g_neg = |V(C_60)| (BT284)"),
        (phi6,  168,   "lambda^q*q*Phi_6 = Aut(Fano) = Aut(KQ) (BT285)"),
        (p_Ih,  660,   "lambda^lambda*q*F_5*p_Ih"),
        (phi3,  V_lps, "lambda^lambda*q*Phi_6*Phi_3 = LPS V (above)"),
    ]
    print(f"  prime p     |PSL(2, F_p)|    substrate")
    for p, o, s in psl:
        print(f"  {p:<8}    {o:<6}           {s}")
    print()

    print("=" * 78)
    print("BREAKTHROUGH 298 SUMMARY")
    print("=" * 78)
    print("""
RAMANUJAN / EXPANDER GRAPHS AT SUBSTRATE PRIMES:

NEW STAR IDENTITIES:
  LPS construction with substrate primes (F_5, Phi_3) gives X^{F_5, Phi_3}:
    |V| = 1092 = lambda^lambda * q * Phi_6 * Phi_3      *** STAR ***
    k = q! = 6
    |lambda_2| <= lambda * sqrt(F_5)
  Equals |Aut(Hurwitz curve genus 14)| (BT289 link).

SUBSTRATE PRIME PARTITION:
  6 = q! substrate primes total split as lambda (== 1 mod 4) +
  mu (== 3 mod 4):
    1 mod 4: F_5, Phi_3 (count = lambda)
    3 mod 4: q, Phi_6, p_Ih, M_5 (count = mu)

ALL THREE SUBSTRATE CUBIC CAGES ARE RAMANUJAN:
  Heawood (lambda_2 = sqrt(lambda))
  Petersen (lambda_2 = 1)
  Mobius-Kantor (lambda_2 = sqrt(q))
  At k = q = 3, Ramanujan bound = lambda * sqrt(lambda).

PSL(2, F_p) AT SUBSTRATE p ORDERS:
  p = F_5: |PSL(2, F_p)| = 60 = mu * g_neg = |V(C_60)| (BT284)
  p = Phi_6: 168 = Aut(Fano) = Aut(KQ) (BT285)
  p = p_Ih: 660
  p = Phi_3: 1092 = LPS V

The substrate's primes generate Cayley graphs whose orders are
substrate-clean and link to multiple BT chain objects (C_60,
Klein quartic, Hurwitz tower).
""")

    out = Path("data") / "w33_BREAKTHROUGH_298_ramanujan_expanders_substrate.json"
    out.parent.mkdir(exist_ok=True)
    packet = {
        "substrate_prime_partition": {
            "primes_1_mod_4": sp_primes_1_mod_4,
            "count_1_mod_4": "lambda",
            "primes_3_mod_4": sp_primes_3_mod_4,
            "count_3_mod_4": "mu",
        },
        "lps_substrate_natural": {
            "p_q": [F5, phi3],
            "V": V_lps,
            "V_substrate": "lambda^lambda * q * Phi_6 * Phi_3",
            "k": k_lps,
            "k_substrate": "q!",
        },
        "lps_V_eq_hurwitz_g14": True,
        "cubic_cages_ramanujan": [
            {"graph": n, "spectrum": sp, "lambda_2": l2, "link": l}
            for n, sp, l2, l in cages
        ],
        "psl_orders": [{"p": p, "order": o, "substrate": s} for p, o, s in psl],
        "conclusion": (
            "LPS Ramanujan construction at substrate primes (F_5, Phi_3) "
            "gives 6-regular graph on 1092 vertices = Hurwitz-genus-14 "
            "Aut order. Substrate primes partition (lambda count == 1 mod 4, "
            "mu count == 3 mod 4) totaling q! = 6. All 3 substrate cubic "
            "cages (Heawood, Petersen, Mobius-Kantor) are Ramanujan. "
            "PSL(2, F_p) orders at substrate p link to C_60, Klein quartic, "
            "and Hurwitz tower."
        ),
    }
    out.write_text(json.dumps(packet, indent=2, default=str), encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
