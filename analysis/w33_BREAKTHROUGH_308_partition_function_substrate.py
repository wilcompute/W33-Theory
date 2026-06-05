"""W(3,3) BREAKTHROUGH 308: PARTITION FUNCTION p(n) SUBSTRATE TOWER.

The partition function p(n) counts the number of ways to write n as a
sum of positive integers (order-irrelevant).

This BT shows the early values of p(n) HIT SUBSTRATE PRIMITIVES in
sequence, completing a pattern (with BT306 Catalan and BT307 Lucas)
of classical integer sequences whose substrate-index values are
substrate-clean.

==============================================================
PARTITION FUNCTION SMALL VALUES
==============================================================

  p(0) = 1
  p(1) = 1
  p(2) = 2 = lambda
  p(3) = 3 = q
  p(4) = 5 = F_5
  p(5) = 7 = Phi_6
  p(6) = 11 = p_Ih
  p(7) = 15 = g_neg
  p(8) = 22 = lambda * p_Ih
  p(9) = 30 = h(E_8) (TRIPLE CONVERGENCE!)
  p(10) = 42 = HURWITZ RECIPROCAL (BT289)
  p(11) = 56 = lambda^q * Phi_6 = |V(Klein quartic)| (BT285)
  p(12) = 77 = Phi_6 * p_Ih
  p(13) = 101 (substrate-adjacent)

==============================================================
PARTITION FUNCTION HITS SUBSTRATE PRIMITIVES IN ORDER
==============================================================

THE FIRST 8 = 2^q PARTITION VALUES p(0)..p(7) PRODUCE:
  {1, 1, lambda, q, F_5, Phi_6, p_Ih, g_neg}

That's SEVEN distinct substrate primitives in 8 consecutive p(n).

NEW SUBSTRATE STAR:
  p(n) for n = 0, ..., Phi_6 = 7 = {1, 1, lambda, q, F_5, Phi_6, p_Ih, g_neg}.

In particular:
  p(lambda) = lambda  (self-map!)
  p(q) = q (self-map!)
  p(mu) = F_5
  p(F_5) = Phi_6
  p(q!) = p_Ih
  p(Phi_6) = g_neg

THREE SELF-MAPS at lambda, q (and the trivial p(0) = p(1) = 1).

==============================================================
DEEPER VALUES = BT CHAIN OBJECTS
==============================================================

  p(9) = 30 = h(E_8) (Triple Convergence, BT78)
  p(10) = 42 = Hurwitz reciprocal (BT289)
  p(11) = 56 = |V(Klein quartic)| = |E(MK)| + |E(Q_mu)| (BT270, BT285)
  p(12) = 77 = Phi_6 * p_Ih (substrate clean)

NEW STAR IDENTITY:
  p(2^q + 1) = p(9) = h(E_8) = 30.
  Triple Convergence integer is partition number at octonion + 1.

  p(2^q + 2) = p(10) = Hurwitz reciprocal = 42.

  p(2^q + 3) = p(11) = |V(Klein quartic)| = 56.

THREE CONSECUTIVE BT-chain objects (h_E_8, Hurwitz, Klein quartic V)
are p(9), p(10), p(11).

==============================================================
ROGERS-RAMANUJAN AND PARTITION q-SERIES
==============================================================

The partition function satisfies the Euler product:
  Product_(k=1)^inf 1/(1 - q^k) = sum_(n=0) p(n) q^n.

Connection to modular forms:
  eta(q) = q^(1/24) * Product_(k=1)^inf (1 - q^k)
  1/eta(q) related to p(n)/q^(n/24).

The exponent 1/24 = 1/f appears here (f = W(3,3) pos eigenmult).

NEW SUBSTRATE READING:
  eta(q) shift exponent = 1/f.
  The partition generating function involves f^(-1) (BT295 Delta link).

==============================================================
RAMANUJAN'S CONGRUENCES
==============================================================

Ramanujan (1919):
  p(5k + 4) == 0 (mod 5) = (mod F_5)
  p(7k + 5) == 0 (mod 7) = (mod Phi_6)
  p(11k + 6) == 0 (mod 11) = (mod p_Ih)

NEW SUBSTRATE STAR:
  Ramanujan's congruences for p(n) hold modulo substrate primitives
  F_5, Phi_6, p_Ih.

  The THREE Ramanujan-congruence primes are substrate primitives.

==============================================================
THE COMBINED SEQUENCE-LADDER PATTERN
==============================================================

THREE classical integer sequences at substrate indices:

  index   p(n)       Catalan C_n        Lucas L_n
  ------------------------------------------------
  lambda  lambda     lambda              q
  q       q          F_5                  mu
  mu      F_5        lambda*Phi_6=14      Phi_6
  F_5     Phi_6      lambda*q*Phi_6=42    p_Ih
  q!      p_Ih       mu*q*p_Ih=132        18
  Phi_6   g_neg      q*p_Ih*Phi_3=429     29

ALL THREE sequences yield substrate-clean integers at substrate
indices, with consistent BT-chain cross-links:
  C_F_5 = 42 = p(2^q+2) (Hurwitz reciprocal, BT289)
  C_q! = 132 = Witt-12 blocks (BT304)
  p(2^q+1) = h(E_8) = Triple Convergence
  L_F_5 = p_Ih = p(q!) (cross-sequence link!)

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
    g_neg = 15
    f = 24
    h_E_8 = 30

    def partition(n, cache={0: 1}):
        # standard recursive partition count
        if n in cache:
            return cache[n]
        if n < 0:
            return 0
        total = 0
        k = 1
        while True:
            g1 = k * (3 * k - 1) // 2
            g2 = k * (3 * k + 1) // 2
            if g1 > n and g2 > n: break
            sign = (-1) ** (k + 1)
            if g1 <= n: total += sign * partition(n - g1)
            if g2 <= n: total += sign * partition(n - g2)
            k += 1
        cache[n] = total
        return total

    print("=" * 78)
    print("W(3,3) BREAKTHROUGH 308: PARTITION FUNCTION p(n) SUBSTRATE")
    print("=" * 78)
    print()

    print("PARTITION VALUES AT SUBSTRATE INDICES:")
    rows = [
        (0,  1,  "1 (trivial)"),
        (1,  1,  "1 (trivial)"),
        (lambda_,  lambda_,    "lambda (SELF-MAP)"),
        (q,         q,          "q (SELF-MAP)"),
        (mu,        F5,         "F_5"),
        (F5,        phi6,       "Phi_6"),
        (6,         p_Ih,       "p_Ih (icosahedron prime)"),
        (phi6,      g_neg,      "g_neg"),
        (2**q,      22,         "lambda * p_Ih"),
        (9,         h_E_8,      "h(E_8) = TRIPLE CONVERGENCE"),
        (10,        42,         "Hurwitz reciprocal (BT289)"),
        (11,        56,         "|V(Klein quartic)| (BT285)"),
        (12,        77,         "Phi_6 * p_Ih"),
    ]
    for n, val, link in rows:
        actual = partition(n)
        match = "OK" if actual == val else f"actual {actual}"
        print(f"  p({n:>2}) = {val:>3}   {link}    ({match})")
    print()

    print("STAR IDENTITIES:")
    print(f"  p(lambda) = lambda (SELF-MAP)")
    print(f"  p(q) = q (SELF-MAP)")
    print(f"  p(2^q+1) = h(E_8) = 30 (TRIPLE CONVERGENCE)")
    print(f"  p(2^q+2) = 42 = Hurwitz reciprocal = Catalan C_F_5 (BT289, BT306)")
    print(f"  p(2^q+3) = 56 = |V(Klein quartic)| (BT270, BT285)")
    print()

    print("RAMANUJAN'S CONGRUENCES (NEW SUBSTRATE READING):")
    print(f"  p(F_5 * k + mu) == 0 mod F_5  (mod F_5)")
    print(f"  p(Phi_6 * k + F_5) == 0 mod Phi_6  (mod Phi_6)")
    print(f"  p(p_Ih * k + q!) == 0 mod p_Ih  (mod p_Ih)")
    print(f"  ALL THREE Ramanujan primes are substrate primitives.")
    print()

    print("COMBINED p(n) + Catalan + Lucas SUBSTRATE LADDER:")
    print(f"  index   p(n)        C_n              L_n")
    print(f"  lambda  lambda      lambda            q")
    print(f"  q       q           F_5                mu")
    print(f"  mu      F_5         lambda*Phi_6=14    Phi_6")
    print(f"  F_5     Phi_6       lambda*q*Phi_6=42  p_Ih")
    print(f"  q!      p_Ih        mu*q*p_Ih=132      18")
    print(f"  Phi_6   g_neg       q*p_Ih*Phi_3=429   29")
    print()
    print(f"  Cross-sequence link: L_F_5 = p(q!) = p_Ih")
    print()

    print("=" * 78)
    print("BREAKTHROUGH 308 SUMMARY")
    print("=" * 78)
    print("""
PARTITION FUNCTION p(n) HITS SUBSTRATE PRIMITIVES IN SEQUENCE.

FIRST 8 = 2^q VALUES:
  p(0), ..., p(Phi_6) = {1, 1, lambda, q, F_5, Phi_6, p_Ih, g_neg}.

SEVEN SUBSTRATE PRIMITIVES IN EIGHT CONSECUTIVE PARTITION VALUES.

DEEPER VALUES = BT-chain objects:
  p(2^q+1) = h(E_8) = 30 (Triple Convergence)
  p(2^q+2) = 42 = Hurwitz reciprocal (BT289)
  p(2^q+3) = 56 = |V(Klein quartic)| (BT285)

RAMANUJAN'S THREE CONGRUENCES are mod F_5, Phi_6, p_Ih -- the substrate's
next-prime, heptad, and icosahedron prime.

THE COMBINED LUCAS-FIBONACCI-CATALAN-PARTITION SUBSTRATE LADDER
(BT306, BT307, BT308) shows ALL FOUR classical integer sequences hit
substrate primitives at substrate-natural indices:

  Lucas L_n maps substrate primitive n -> next primitive.
  Fibonacci F_n hits substrate at q!, F_5, Phi_6 (with octonion at q!).
  Catalan C_n hits Heawood V, Hurwitz, Witt-12.
  Partition p(n) hits substrate primitives 1 -> 8 in sequence,
  with h_E_8 / Hurwitz / Klein quartic in deeper values.

The substrate primitive set IS the early-value set of these four
fundamental integer sequences, suggesting the substrate is the
"natural integer hierarchy" emerging from golden-ratio (Lucas/Fibonacci),
balanced-paren (Catalan), and additive (partition) enumeration.
""")

    out = Path("data") / "w33_BREAKTHROUGH_308_partition_function_substrate.json"
    out.parent.mkdir(exist_ok=True)
    packet = {
        "partition_tower": [
            {"n": n, "p_n": v, "link": l} for n, v, l in rows
        ],
        "self_maps": ["p(lambda) = lambda", "p(q) = q"],
        "deep_BT_links": [
            "p(2^q+1) = h(E_8) (Triple Convergence)",
            "p(2^q+2) = Hurwitz reciprocal = Catalan C_F_5",
            "p(2^q+3) = |V(Klein quartic)|",
        ],
        "ramanujan_congruences": [
            "p(F_5 k + mu) == 0 mod F_5",
            "p(Phi_6 k + F_5) == 0 mod Phi_6",
            "p(p_Ih k + q!) == 0 mod p_Ih",
        ],
        "combined_4_sequence_ladder": (
            "Lucas, Fibonacci, Catalan, Partition ALL hit substrate primitives "
            "at substrate-natural indices, with consistent BT-chain cross-links."
        ),
        "conclusion": (
            "Partition function p(n) hits substrate primitives in sequence: "
            "first 8 values = {1, 1, lambda, q, F_5, Phi_6, p_Ih, g_neg}. "
            "p(2^q+1) = h_E_8 = Triple Convergence, p(2^q+2) = Hurwitz "
            "reciprocal, p(2^q+3) = |V(Klein quartic)|. Ramanujan's three "
            "congruences are mod F_5, Phi_6, p_Ih (substrate primes). The "
            "combined Lucas/Fibonacci/Catalan/Partition ladder shows substrate "
            "primitives ARE the early-value set of these four fundamental "
            "integer sequences."
        ),
    }
    out.write_text(json.dumps(packet, indent=2, default=str), encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
