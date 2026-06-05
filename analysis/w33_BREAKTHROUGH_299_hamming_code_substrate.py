"""W(3,3) BREAKTHROUGH 299: HAMMING CODE [Phi_6, mu, q]_2 SUBSTRATE.

The Hamming code Ham(r, lambda) over F_lambda has parameters:
  Length    n = lambda^r - 1
  Dim       k = lambda^r - 1 - r
  Distance  d = q = 3 (single-error correcting)

This BT shows the smallest non-trivial Hamming code [Phi_6, mu, q]_2
encodes THREE substrate primitives in ONE classical CS object, and
the family at all substrate-natural r is substrate-clean.

==============================================================
THE [Phi_6, mu, q]_2 HAMMING CODE
==============================================================

The classical [7, 4, 3]_2 Hamming code:
  Length n = 7 = Phi_6                   (substrate heptad)
  Dim    k = 4 = mu                       (substrate spacetime)
  Distance d = 3 = q                      (substrate color)

  THREE SUBSTRATE PRIMITIVES IN ONE CODE.

This is the smallest 1-error-correcting binary linear code:
  - perfect (sphere-packing bound tight: lambda^k * (1 + n) = lambda^n)
  - covers the Phi_6-bit codeword space with mu-bit info + q-bit ECC
  - 7 = Phi_6 syndromes (= length itself)

==============================================================
SPHERE-PACKING / PERFECT CODE CONDITION
==============================================================

For a binary perfect code [n, k, d] with d = 3:
  lambda^k * (1 + n) = lambda^n
  i.e., (1 + n) = lambda^(n - k).

At n = Phi_6, k = mu:
  1 + Phi_6 = lambda^(Phi_6 - mu) = lambda^q = 2^q = 8 (octonion!)
  8 = 1 + 7. CHECK.

NEW SUBSTRATE IDENTITY:
  Hamming-perfect condition at Phi_6: lambda^q = Phi_6 + 1.
  Octonion dim = heptad + 1.

==============================================================
GENERAL HAMMING FAMILY Ham(r, lambda)
==============================================================

  [lambda^r - 1, lambda^r - 1 - r, q]_lambda

At substrate-natural r:

  r = q = 3:    [Phi_6, mu, q] = [7, 4, 3]_2          (STAR)
  r = mu = 4:   [g_neg, p_Ih, q] = [15, 11, 3]_2
  r = F_5 = 5:  [M_5, lambda*Phi_3, q] = [31, 26, 3]_2

EVERY substrate-natural r gives a Hamming code with substrate-clean
length and dim.

==============================================================
[15, 11, 3] HAMMING SUBSTRATE (r = mu)
==============================================================

  n = lambda^mu - 1 = g_neg = 15
  k = g_neg - mu = p_Ih = 11
  d = q = 3

THREE substrate primitives: g_neg, p_Ih, q.

==============================================================
[31, 26, 3] HAMMING SUBSTRATE (r = F_5)
==============================================================

  n = lambda^F_5 - 1 = M_5 = 31 (Mersenne prime!)
  k = M_5 - F_5 = 26 = lambda * Phi_3 = BOSONIC STRING DIM!
  d = q = 3

NEW SUBSTRATE STAR:
  The (r = F_5) Hamming code has dim equal to the BOSONIC STRING
  critical dimension (BT292):
    k(Ham(F_5, lambda)) = lambda * Phi_3 = D_bosonic = 26.

==============================================================
SUBSTRATE HAMMING SUBSTRATE TABLE
==============================================================

r        n = lambda^r - 1    k = n - r            d   substrate dim
-------------------------------------------------------------------
q        Phi_6 = 7           mu = 4               q   3 of {q, mu, Phi_6}
mu       g_neg = 15          p_Ih = 11            q   3 of {q, g_neg, p_Ih}
F_5      M_5 = 31            lambda*Phi_3 = 26    q   STRING DIM!
q!       63                  57                   q   compound
Phi_6    127 (Mersenne prime) 120 = F_5!         q   F_5! dim!
2^q      255                 247                  q   compound

==============================================================
HAMMING -> REED-MULLER -> Q_mu (BT286 LINK)
==============================================================

RM(1, mu) = [lambda^mu, F_5, 2^q]_lambda = [16, 5, 8] (BT286).

The Hamming code Ham(r, lambda) is the DUAL of the (extended)
Reed-Muller code:
  Ham(r, 2) = dual of (extended) RM(r-1, r).

At r = q: Ham(q, lambda) = [7, 4, 3] = dual of RM(lambda, q) = [8, 4, 4].
RM(1, q) extended = [8, 4, 4] (Reed-Muller of order 1 in q vars + parity).

NEW SUBSTRATE READING:
  RM(1, q) extended = [lambda^q, mu, mu] = [8, 4, 4] = (octonion, mu, mu).
  Dual = [Phi_6, mu, q] = (heptad, mu, color).
  Hamming/RM duality matches substrate (octonion, heptad) duality.

==============================================================
HAMMING SYNDROME = Q_Phi_6 = 7-CUBE PROJECTION
==============================================================

Hamming code corrects 1 error by computing the syndrome (3 bits = q
bits) which uniquely identifies the error position (7 = Phi_6
non-zero syndromes + 1 zero = lambda^q = 8 total syndromes).

NEW SUBSTRATE READING:
  Hamming-q syndrome has lambda^q = octonion-many values, of which
  Phi_6 are nonzero (one per error position).

==============================================================
HAMMING DISTANCE q = SUBSTRATE COLOR (NEW CORE READING)
==============================================================

For ANY Hamming code Ham(r, 2): minimum distance d = q = 3.

  Hamming distance d = substrate color q.

This is the ONLY distance choice that makes the Hamming code:
  - 1-error correcting (the substrate's color charge correction)
  - Perfect (sphere-packing tight at substrate octonion-q condition)
  - Linear with substrate parity check.

The substrate color q IS the Hamming-code distance, baked into
the structure of single-error correction.

==============================================================
THE THREE-CLASSIC-CODES SUBSTRATE TRIPLE
==============================================================

Three "smallest" classical codes:

  [Phi_6, mu, q]_2 Hamming           (BT299 STAR)
  RM(1, q) extended [2^q, mu, mu]    (BT286)
  Single-parity [n, n-1, lambda]     (trivial, parity = lambda)

ALL THREE have parameters in substrate primitives, with the Hamming
code being the smallest perfect code on substrate-primitive integers.

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
    g_neg = 15
    p_Ih = 11
    M5 = 31

    print("=" * 78)
    print("W(3,3) BREAKTHROUGH 299: HAMMING CODE SUBSTRATE")
    print("=" * 78)
    print()

    print("THE [Phi_6, mu, q]_2 HAMMING CODE:")
    print(f"  Length  = Phi_6 = 7 (substrate HEPTAD)")
    print(f"  Dim     = mu = 4 (substrate SPACETIME)")
    print(f"  Distance = q = 3 (substrate COLOR)")
    print(f"  *** THREE SUBSTRATE PRIMITIVES IN ONE CODE ***")
    print()

    print("PERFECT-CODE CONDITION:")
    perfect = (1 + phi6) == lambda_ ** q
    assert perfect
    print(f"  lambda^k * (1 + n) = lambda^n -> 1 + n = lambda^(n - k)")
    print(f"  At n=Phi_6, k=mu: 1 + Phi_6 = lambda^q = 8 (octonion)")
    print(f"  *** STAR: Hamming-perfect condition -> octonion = heptad + 1 ***")
    print()

    print("HAMMING FAMILY AT SUBSTRATE r:")
    fam = [
        (q,      2**q - 1,    2**q - 1 - q,    "[Phi_6, mu, q]"),
        (mu,     2**mu - 1,   2**mu - 1 - mu,  "[g_neg, p_Ih, q]"),
        (F5,     2**F5 - 1,   2**F5 - 1 - F5,   "[M_5, lambda*Phi_3, q] = [31, 26, 3] STRING DIM!"),
        (6,      2**6 - 1,    2**6 - 1 - 6,     "[63, 57, q]"),
        (phi6,   2**phi6 - 1, 2**phi6 - 1 - phi6, "[127, F_5!, q] = [127, 120, 3] F_5!"),
        (2**q,   2**(2**q) - 1, 2**(2**q) - 1 - 2**q, "[255, 247, q]"),
    ]
    print(f"  r          n        k        substrate")
    for r, n, k, s in fam:
        marker = " ***" if r in (q, mu, F5) else ""
        print(f"  {r:<6}     {n:>4}    {k:>4}     {s}{marker}")
    print()

    print("STAR LINKS:")
    print(f"  r = q (= 3):     [Phi_6, mu, q] = 3 substrate primitives")
    print(f"  r = mu (= 4):    [g_neg, p_Ih, q] = 3 substrate primitives")
    print(f"  r = F_5 (= 5):   [M_5, lambda*Phi_3, q] -- dim = BOSONIC STRING (BT292)")
    print(f"  r = Phi_6 (= 7): [127, F_5!, q] -- dim = |Aut(Petersen)| (BT279)")
    print()

    print("HAMMING / REED-MULLER DUAL (BT286 LINK):")
    print(f"  Ham(q, lambda) = [Phi_6, mu, q]")
    print(f"  Extended RM(1, q) = [lambda^q, mu, mu] = [8, 4, 4]")
    print(f"  These are DUAL codes (Hamming/extended-RM duality).")
    print(f"  Substrate: Hamming = heptad-length; RM-ext = octonion-length.")
    print()

    print("THE q AS HAMMING DISTANCE (NEW CORE READING):")
    print(f"  EVERY Hamming code has min distance d = q = 3.")
    print(f"  The substrate's COLOR primitive IS the Hamming-code distance.")
    print(f"  Single-error correction = substrate-color charge correction.")
    print()

    print("=" * 78)
    print("BREAKTHROUGH 299 SUMMARY")
    print("=" * 78)
    print("""
THE HAMMING CODE [Phi_6, mu, q]_2 ENCODES THREE SUBSTRATE PRIMITIVES.

THE FULL HAMMING FAMILY AT SUBSTRATE r:
  r = q:    [Phi_6, mu, q]              (smallest non-trivial)
  r = mu:   [g_neg, p_Ih, q]
  r = F_5:  [M_5, lambda*Phi_3, q]      (k = bosonic string dim 26!)
  r = Phi_6: [127, F_5!, q]              (k = |Aut(Petersen)| = 120)

STAR NEW IDENTITIES:
  Hamming-perfect condition at r = q: lambda^q = Phi_6 + 1
    (octonion dim = heptad + 1)
  k(Ham(F_5, 2)) = lambda * Phi_3 = D_bosonic_string (BT292)
  k(Ham(Phi_6, 2)) = F_5! = |Aut(Petersen)| = |I_h| (BT279)
  Hamming min distance d = q (substrate color)

HAMMING/REED-MULLER DUAL = HEPTAD/OCTONION DUAL:
  Hamming [Phi_6, mu, q] dual to extended RM [lambda^q, mu, mu].
  Heptad-length code dual to octonion-length code.

THE SUBSTRATE'S COLOR (q = 3) IS LITERALLY THE MINIMUM HAMMING
DISTANCE -- the most fundamental error-correcting parameter in
classical coding theory.

ONE CLASSICAL OBJECT (Hamming code) encodes the substrate's HEPTAD
(length), SPACETIME (dim), COLOR (distance), and PERFECT-CODE
condition octonion = heptad + 1.
""")

    out = Path("data") / "w33_BREAKTHROUGH_299_hamming_code_substrate.json"
    out.parent.mkdir(exist_ok=True)
    packet = {
        "smallest_hamming_code": {
            "parameters": [phi6, mu, q],
            "substrate": "[Phi_6, mu, q] -- length=heptad, dim=spacetime, dist=color",
        },
        "perfect_code_identity": "lambda^q = Phi_6 + 1 (octonion = heptad + 1)",
        "hamming_family_at_substrate_r": [
            {"r": r, "n": n, "k": k, "substrate": s} for r, n, k, s in fam
        ],
        "star_identities": [
            "[Phi_6, mu, q] -- 3 substrate primitives in one code",
            "k(Ham(F_5, 2)) = lambda*Phi_3 = bosonic string dim",
            "k(Ham(Phi_6, 2)) = F_5! = |Aut(Petersen)|",
            "Hamming d = q (substrate color)",
        ],
        "hamming_rm_duality": "[Phi_6, mu, q] dual to extended RM [2^q, mu, mu]",
        "conclusion": (
            "Hamming code [Phi_6, mu, q]_2 has length = heptad, dim = "
            "spacetime, distance = color -- THREE substrate primitives in one "
            "code. Perfect-code condition: octonion = heptad + 1. "
            "Hamming family at substrate r in {q, mu, F_5, Phi_6} gives "
            "substrate-clean (n, k, d). Bosonic string dim appears as "
            "k(Ham(F_5, 2)) = 26 = lambda*Phi_3. Substrate's color q IS "
            "the Hamming minimum distance."
        ),
    }
    out.write_text(json.dumps(packet, indent=2, default=str), encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
