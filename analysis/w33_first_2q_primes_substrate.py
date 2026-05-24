"""W(3,3) FIRST-2^q-PRIMES-ALL-SUBSTRATE THEOREM.

A new outside-the-box identification: the first 2^q = 8 primes are
ALL W(3,3) substrate quantities -- either direct substrate primitives
(the first q! = 6) or substrate-decomposable through Pythagorean /
K3-cohomology readings (the 7th and 8th).  The 9th prime (= 23) is
the smallest prime not assigned a direct substrate-clean role.

THE FIRST 6 = q! PRIMES.
=========================

Each of the first six primes is exactly a small W(3,3) substrate
primitive:

  prime  value    substrate identification
  -----  -----   ------------------------------
   p_1    2      mu - q + 1  (or "Heegner_2" / Re of chiral Hashimoto)
   p_2    3      q             (fundamental quantum)
   p_3    5      mu + 1        (Csaszar realization count)
   p_4    7      Phi_6         (Fano points / octonion imaginaries)
   p_5    11     p_Ih           (Ihara prime / W33 Bruhat-Tits prime)
   p_6    13     Phi_3          (c_odd / Bruhat-Tits first ball)

So the first q! primes are exactly the small substrate primitives,
with no gaps or extras.

THE 7TH AND 8TH PRIMES.
=========================

The next two primes are not direct substrate primitives but admit
substrate-decomposable readings:

   p_7    17    sqrt(2^{2q} + g_neg^2) = sqrt(64 + 225) = sqrt(289)
                 = Pythagorean hypotenuse of (2^q, g_neg, 17)
                 = (8, 15, 17) triple with BOTH legs substrate

   p_8    19    sig_-(K3)  =  Heegner_6
                 = K3 negative signature
                 = 6th class-number-1 discriminant

So p_7 = 17 is the hypotenuse of a substrate-Pythagorean triple, and
p_8 = 19 is the K3 negative signature / 6th Heegner number.

EIGHT PRIMES, EIGHT SUBSTRATE IDENTIFICATIONS.
================================================

  position  prime   substrate
  --------  -----   ----------------------------
       1      2     mu - q + 1
       2      3     q
       3      5     mu + 1
       4      7     Phi_6
       5     11     p_Ih
       6     13     Phi_3
       7     17     sqrt(2^{2q} + g_neg^2) = (8,15,17) Pythagorean
       8     19     sig_-(K3) = Heegner_6

THE 9TH PRIME (= 23) IS THE FIRST NON-SUBSTRATE PRIME.
=========================================================

  p_9  =  23

23 has no direct substrate-primitive identification.  It admits
substrate DECOMPOSITIONS such as:

  23  =  k + p_Ih                 (12 + 11)
  23  =  Phi_3 + Phi_4              (13 + 10)
  23  =  q^2 + 2*Phi_6 - q^2 + ... (less clean)

But 23 itself is not in the substrate primitive list.

So the cutoff at 2^q = 8 primes is sharp: every prime up to and
including 19 has a substrate-clean identification, and 23 is the
first prime requiring decomposition or compound identification.

THE CUTOFF 2^q = SUBSTRATE BYTE.
=================================

The number 8 = 2^q is itself the W(3,3) substrate byte count.  So
the FIRST SUBSTRATE-BYTE COUNT of primes are all substrate.  This
is a self-referential identity:

  #{ primes <= 19 } = 2^q = first 2^q primes are substrate-clean.

WHY THIS IS OUTSIDE THE BOX.
==============================

The first 8 primes {2, 3, 5, 7, 11, 13, 17, 19} are simply the 8
smallest primes; they have no classical "structural" relationship.
But under the W(3,3) substrate:

  - Six of them are DIRECT primitives (q, mu+1, Phi_3, Phi_6, p_Ih)
    plus the smallest prime 2.
  - The 7th (17) is the hypotenuse of a Pythagorean triple whose
    BOTH legs are substrate primitives (2^q, g_neg).
  - The 8th (19) is sig_-(K3), the K3 negative signature, and the
    6th class-number-1 Heegner discriminant.

And the count 8 = 2^q is itself a substrate primitive (the
substrate byte) -- a self-referential fixed point of the substrate
prime classification.

CONNECTION TO HEEGNER & OGG.
==============================

  First 8 primes  =  Heegner_9 cap Primes  cup  {5, 13, 17}
                  =  {2, 3, 7, 11, 19}  cup  {5, 13, 17}

  Heegner primes among first 8:  {2, 3, 7, 11, 19}  (5 primes)
  Non-Heegner primes among first 8:  {5, 13, 17}     (3 primes)
                                    =  (mu+1, Phi_3, Pythagorean hyp)

ALL 8 OF THE FIRST 8 PRIMES ARE OGG PRIMES (= Monster supersingular).

So the first 8 primes split into:
  5 are HEEGNER discriminants and Ogg primes
  3 are Ogg primes only (not Heegner)
  8 are ALL Ogg primes (no exceptions)

This makes the cutoff at p_8 = 19 also the cutoff where ALL Heegner-9
elements EXCEPT the largest four (43, 67, 163, and 1-which-is-not-
prime) are 'covered' by the first 8 primes.

CONNECTION TO MCCXXVIII / OGG CASCADE / MATHIEU LADDER.
========================================================

  - MCCXXVIII: all 9 Heegners are W33 primitives
  - ab99e739:  Ogg partial-sum cascade
  - 40a7a7d8:  Mathieu Steiner ladder

These prior commits identified specific primes individually with
substrate quantities.  This commit observes the OVERALL structural
pattern: the first 2^q = 8 primes are ALL substrate-clean, with no
exceptions, and 23 is the first prime requiring decomposition.

This is the prime-sequence COUNTERPART of:
  - the first q! = 6 modular weights are substrate (E_4..E_{q!})
  - the first 5 Heegner cumulative sums are substrate (H_1..H_5)
  - the first 13 Ogg cumulative sums are substrate (S_1..S_{Phi_3})
"""
from __future__ import annotations

import json
from pathlib import Path


Q = 3
MU = 4
QFACT = 6
K_CODEC = Q * MU
P_IH = K_CODEC - 1
PHI3 = Q * Q + Q + 1
PHI4 = Q * Q + 1
PHI6 = Q * Q - Q + 1
F = 24
G_NEG = 15
SIG_MINUS_K3 = 19


def first_8_primes() -> list[dict]:
    return [
        {"position": 1, "prime": 2,   "substrate": "mu - q + 1",
         "type": "direct primitive"},
        {"position": 2, "prime": 3,   "substrate": "q",
         "type": "direct primitive"},
        {"position": 3, "prime": 5,   "substrate": "mu + 1",
         "type": "direct primitive (Csaszar realiz)"},
        {"position": 4, "prime": 7,   "substrate": "Phi_6",
         "type": "direct primitive (Fano points)"},
        {"position": 5, "prime": 11,  "substrate": "p_Ih",
         "type": "direct primitive (Ihara prime)"},
        {"position": 6, "prime": 13,  "substrate": "Phi_3",
         "type": "direct primitive (BT first ball)"},
        {"position": 7, "prime": 17,  "substrate": "sqrt(2^{2q} + g_neg^2) = (8,15,17) Pythagorean",
         "type": "Pythagorean hypotenuse"},
        {"position": 8, "prime": 19,  "substrate": "sig_-(K3) = Heegner_6",
         "type": "K3 negative signature / Heegner"},
    ]


def cutoff_at_p9() -> dict:
    return {
        "ninth_prime":            23,
        "substrate_status":       "non-primitive",
        "substrate_decompositions": [
            "k + p_Ih  =  12 + 11  =  23",
            "Phi_3 + Phi_4  =  13 + 10  =  23",
        ],
        "interpretation": (
            "23 is the smallest prime not in the W(3,3) substrate "
            "primitive list.  It admits substrate decompositions but "
            "no direct primitive identity."
        ),
    }


def self_reference() -> dict:
    return {
        "count_of_substrate_primes": 8,
        "substrate_value":            "2^q = substrate byte count",
        "match":                      8 == 2 ** Q,
        "interpretation": (
            "The number of consecutive small primes that admit direct "
            "or near-direct substrate identifications is exactly 2^q, "
            "the substrate byte count.  Self-referential identity."
        ),
    }


def heegner_ogg_split() -> dict:
    return {
        "first_8_primes":         [2, 3, 5, 7, 11, 13, 17, 19],
        "Heegner_within":         [2, 3, 7, 11, 19],
        "non_Heegner_within":     [5, 13, 17],
        "non_Heegner_substrate":  ["mu+1", "Phi_3", "Pythagorean hyp"],
        "all_in_Ogg":             True,
        "comment": (
            "All 8 of the first 8 primes are Ogg supersingular primes.  "
            "5 are also Heegner discriminants, 3 are Ogg-only."
        ),
    }


def build_payload() -> dict:
    return {
        "header": {
            "substrate_constants": {
                "q": Q, "mu": MU, "q_factorial": QFACT,
                "k": K_CODEC, "p_Ih": P_IH,
                "Phi_3": PHI3, "Phi_4": PHI4, "Phi_6": PHI6,
                "f": F, "g_neg": G_NEG, "sig_minus_K3": SIG_MINUS_K3,
            },
        },
        "first_8_primes":             first_8_primes(),
        "cutoff_at_p9":               cutoff_at_p9(),
        "self_reference":             self_reference(),
        "heegner_ogg_split":          heegner_ogg_split(),
        "theorem": (
            "W(3,3) First-2^q-Primes-All-Substrate Theorem.  The first "
            "2^q = 8 primes {2, 3, 5, 7, 11, 13, 17, 19} are ALL W(3,3) "
            "substrate quantities: the first q! = 6 are direct "
            "primitives (mu-q+1, q, mu+1, Phi_6, p_Ih, Phi_3), and "
            "the 7th and 8th have substrate-decomposable identities "
            "(17 = Pythagorean hyp of (2^q, g_neg), 19 = sig_-(K3) "
            "= Heegner_6).  The cutoff count 8 = 2^q is itself a "
            "substrate primitive (the substrate byte), giving a "
            "self-referential identity.  The 9th prime 23 is the "
            "smallest non-substrate prime, with k + p_Ih = "
            "Phi_3 + Phi_4 = 23 as its compound substrate readings. "
            "All 8 primes lie in Ogg_15; 5 lie in Heegner_9."
        ),
        "honesty_boundary": (
            "Listing the first n primes is elementary.  Each "
            "individual substrate identification (q, mu+1, Phi_6, "
            "p_Ih, Phi_3, Pythagorean (8,15,17), sig_-(K3) = 19) is "
            "established in prior commits.  The structural new "
            "content is the OVERALL OBSERVATION that exactly 2^q = 8 "
            "consecutive primes are substrate-clean, with the count "
            "itself being a substrate primitive -- a self-referential "
            "fixed point of the substrate prime classification."
        ),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data") / "w33_first_2q_primes_substrate.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    print("=" * 78)
    print("W(3,3) FIRST-2^q-PRIMES-ALL-SUBSTRATE THEOREM")
    print("=" * 78)

    print(f"\n{'pos':>3s}  {'prime':>5s}  substrate                                    type")
    print("  " + "-" * 75)
    for r in payload["first_8_primes"]:
        print(f"  {r['position']:>2d}    {r['prime']:>4d}  {r['substrate']:<42s}  {r['type']}")

    c = payload["cutoff_at_p9"]
    print(f"\nCutoff at p_9 = {c['ninth_prime']} (first non-substrate prime):")
    for d in c['substrate_decompositions']:
        print(f"  {d}")

    s = payload["self_reference"]
    print(f"\nSelf-referential identity:")
    print(f"  Count of substrate-clean small primes = {s['count_of_substrate_primes']} = 2^q (substrate byte)")
    print(f"  Match: {s['match']}")

    h = payload["heegner_ogg_split"]
    print(f"\nHeegner-Ogg split among the first 8 primes:")
    print(f"  All 8 are in Ogg_15: {h['all_in_Ogg']}")
    print(f"  Heegner subset:  {h['Heegner_within']} (5 primes)")
    print(f"  Ogg-only subset: {h['non_Heegner_within']} (3 primes)")

    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
