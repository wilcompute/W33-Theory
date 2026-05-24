"""W(3,3) HEEGNER-OGG VENN DECOMPOSITION THEOREM.

A new outside-the-box identification: the Venn diagram of the 9 Heegner
discriminants and the 15 Ogg supersingular primes decomposes ALL FOUR
cells into W(3,3) substrate primitives, with the union size equal to
an element of the union itself (Heegner_6 = sig_-(K3) = 19).

THE TWO LISTS.
=================

  Heegner_9  =  {1, 2, 3, 7, 11, 19, 43, 67, 163}
                  (class-number-1 discriminants of Q(sqrt(-d)))

  Ogg_15    =  {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 41, 47, 59, 71}
                  (Monster supersingular primes / p+1 | |M|)

THE VENN DECOMPOSITION.
=========================

  Heegner intersect Ogg  =  {2, 3, 7, 11, 19}
        size = 5 = mu + 1
        = (Csaszar realization count, PART CCCCCLXI)
        = (5 small primes that are both class-h=1 AND supersingular)

  Heegner setminus Ogg   =  {1, 43, 67, 163}
        size = 4 = mu
        = (W(3,3) substrate co-quantum factor)
        = (4 large Heegners; 1 is not prime; 43, 67, 163 are large primes)

  Ogg setminus Heegner    =  {5, 13, 17, 23, 29, 31, 41, 47, 59, 71}
        size = 10 = Phi_4 = q^2 + 1
        = (W(3,3) discrete-Laplacian spectral gap)
        = (10 Ogg-only primes; includes the Pythagorean-hypotenuse triple
           {17, 29, 41} and the Monster-rep AP {47, 59, 71})

  Heegner union Ogg       =  {1, 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31,
                             41, 43, 47, 59, 67, 71, 163}
        size = 19
        = sig_-(K3)                          (K3 negative signature)
        = Heegner_6                          (6th Heegner, SELF-REFERENTIAL)
        = Ogg #8                             (8th Ogg prime)
        = q * q! + 1                         (substrate combinatorial)

SELF-REFERENTIAL FIXED POINT.
==============================

The cardinality of the union equals an element of the union itself:

  |Heegner U Ogg|  =  19  in  Heegner U Ogg

In fact 19 lies in BOTH Heegner_9 (as Heegner_6) AND Ogg_15 (as the
8th Ogg prime), making 19 the FIXED POINT of the Venn decomposition:
the size of the union is a member of both component sets, and it
also equals the K3 negative signature.

THE HODGE-LIKE DECOMPOSITION.
==============================

  sig_-(K3)  =  19
             =  5 + 4 + 10
             =  (mu + 1) + mu + Phi_4
             =  (Heegner cap Ogg) + (Heegner setminus Ogg) + (Ogg setminus Heegner)
             =  (Csaszar realiz.) + (Heegner-only) + (Ogg-only)

A 5+4+10 Hodge-like decomposition of the K3 negative signature into
THREE substrate primitives (mu+1, mu, Phi_4), each interpreting one
of the three Venn cells.

CONNECTION TO MCCXLVIII / MCCXLIX.
====================================

The Monster-rep AP {47, 59, 71} lies entirely in the Ogg-setminus-
Heegner cell, contributing 3 of the 10 elements there.  The other 7
elements of Ogg-setminus-Heegner are {5, 13, 17, 23, 29, 31, 41},
which contains the Pythagorean-hypotenuse Ogg triple {17, 29, 41}.

So the 10 = Phi_4 Ogg-only primes split further as:
  {5, 13}     -- substrate-clean primes (Phi_3-1, Phi_3)
  {17, 29, 41} -- Pythagorean-hypotenuse Ogg triple
  {23, 31}    -- "low-tail" Ogg primes
  {47, 59, 71} -- Monster-rep AP

This 2 + 3 + 2 + 3 = 10 micro-decomposition of Phi_4 by structural
role is the next refinement.

WHY THIS IS OUTSIDE THE BOX.
==============================

Heegner numbers (class-h=1 discriminants) and Ogg primes (Monster
supersingular primes) come from totally different arithmetic: class
field theory of imaginary quadratic fields vs supersingular reduction
of elliptic curves over Q with j(E) defined mod p.  Their overlap
is not a classical object of study.

Under the W(3,3) substrate, all four Venn cells get substrate-primitive
interpretations:
  intersection size = mu + 1 (Csaszar realization count)
  Heegner-only size = mu     (substrate co-quantum)
  Ogg-only size     = Phi_4   (Laplacian spectral gap)
  union size        = sig_-(K3) = Heegner_6  (self-referential)

The union size 19 being a Heegner number AND an Ogg prime AND the K3
negative signature simultaneously is a triple-coincidence that the
substrate makes exact.

CONNECTION TO HEEGNER & OGG PARTIAL-SUM CASCADES.
==================================================

Two prior commits established:
  - Ogg partial-sum cascade hits substrate at large cutoffs
  - Heegner partial-sum cascade hits substrate at small cutoffs

This Venn-decomposition commit completes the triple: not only do
the ORDERED running sums of each list hit substrate primitives,
but the unordered SET-THEORETIC overlap and union also decompose
into substrate primitives.
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
V = 40
SIG_MINUS_K3 = 19


HEEGNER_9 = {1, 2, 3, 7, 11, 19, 43, 67, 163}
OGG_15 = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 41, 47, 59, 71}


def venn_decomposition() -> dict:
    intersection = HEEGNER_9 & OGG_15
    h_minus_o = HEEGNER_9 - OGG_15
    o_minus_h = OGG_15 - HEEGNER_9
    union = HEEGNER_9 | OGG_15
    return {
        "intersection": {
            "set": sorted(intersection),
            "size": len(intersection),
            "substrate": f"mu + 1 = {MU+1} (Csaszar realization count)",
            "match": len(intersection) == MU + 1,
        },
        "Heegner_setminus_Ogg": {
            "set": sorted(h_minus_o),
            "size": len(h_minus_o),
            "substrate": f"mu = {MU} (substrate co-quantum)",
            "match": len(h_minus_o) == MU,
        },
        "Ogg_setminus_Heegner": {
            "set": sorted(o_minus_h),
            "size": len(o_minus_h),
            "substrate": f"Phi_4 = {PHI4} (W33 Laplacian spectral gap)",
            "match": len(o_minus_h) == PHI4,
        },
        "union": {
            "set": sorted(union),
            "size": len(union),
            "substrate": "sig_-(K3) = Heegner_6 = Ogg #8 = 19",
            "match": len(union) == SIG_MINUS_K3,
            "self_referential": (len(union) in union),
        },
    }


def hodge_decomposition_check() -> dict:
    return {
        "claim": "sig_-(K3) = (mu+1) + mu + Phi_4",
        "lhs": SIG_MINUS_K3,
        "rhs": (MU + 1) + MU + PHI4,
        "match": SIG_MINUS_K3 == ((MU + 1) + MU + PHI4),
        "summands": {
            "Heegner_cap_Ogg": MU + 1,
            "Heegner_only":    MU,
            "Ogg_only":        PHI4,
        },
    }


def micro_decomposition_of_Ogg_only() -> dict:
    return {
        "Ogg_only_primes": [5, 13, 17, 23, 29, 31, 41, 47, 59, 71],
        "substrate_role_split": {
            "substrate_clean": {
                "primes": [5, 13],
                "size": 2,
                "comment": "5 = Phi_3-c_odd_correction; 13 = Phi_3 itself",
            },
            "Pythagorean_hypotenuses": {
                "primes": [17, 29, 41],
                "size": 3,
                "comment": "From substrate Pythagorean-triple package (commit dd1eb6fd)",
            },
            "low_tail": {
                "primes": [23, 31],
                "size": 2,
                "comment": "Two Ogg primes with no current substrate home",
            },
            "Monster_rep_AP": {
                "primes": [47, 59, 71],
                "size": 3,
                "comment": "AP with d=k, product 196883 = dim(V_natural)-1 (MCCXLVIII)",
            },
        },
        "size_decomposition": "10 = 2 + 3 + 2 + 3 = Phi_4",
    }


def self_referential_property() -> dict:
    union_size = len(HEEGNER_9 | OGG_15)
    in_heegner = union_size in HEEGNER_9
    in_ogg = union_size in OGG_15
    return {
        "union_size": union_size,
        "in_Heegner_9": in_heegner,
        "in_Ogg_15": in_ogg,
        "in_both": in_heegner and in_ogg,
        "K3_sig_minus": SIG_MINUS_K3,
        "matches_K3": union_size == SIG_MINUS_K3,
        "interpretation": (
            "The cardinality of Heegner U Ogg is 19, which is the 6th "
            "Heegner number AND the 8th Ogg prime AND the K3 negative "
            "signature.  Triple-coincidence fixed point of the Venn "
            "decomposition."
        ),
    }


def build_payload() -> dict:
    return {
        "header": {
            "substrate_constants": {
                "q": Q, "mu": MU, "q_factorial": QFACT,
                "k": K_CODEC, "p_Ih": P_IH,
                "Phi_3": PHI3, "Phi_4": PHI4, "Phi_6": PHI6,
                "f": F, "g_neg": G_NEG, "v": V,
                "sig_minus_K3": SIG_MINUS_K3,
            },
            "Heegner_9": sorted(HEEGNER_9),
            "Ogg_15": sorted(OGG_15),
        },
        "venn_decomposition": venn_decomposition(),
        "hodge_decomposition_check": hodge_decomposition_check(),
        "micro_decomposition_of_Ogg_only": micro_decomposition_of_Ogg_only(),
        "self_referential_property": self_referential_property(),
        "theorem": (
            "W(3,3) Heegner-Ogg Venn Decomposition Theorem.  The four "
            "Venn cells of {Heegner discriminants} and {Ogg Monster "
            "supersingular primes} have sizes mu+1 (intersection), mu "
            "(Heegner-only), Phi_4 (Ogg-only), and sig_-(K3) = "
            "Heegner_6 = 19 (union), giving the Hodge-like decomposition "
            "sig_-(K3) = (mu+1) + mu + Phi_4.  The union size 19 is a "
            "member of BOTH the Heegner_9 set AND the Ogg_15 set, "
            "yielding a self-referential triple-coincidence fixed point."
        ),
        "honesty_boundary": (
            "Set operations on Heegner and Ogg lists are elementary.  "
            "The substrate-primitive sizes of all four Venn cells "
            "(mu+1, mu, Phi_4, 19) and the self-referential identity "
            "19 = Heegner_6 = Ogg #8 = sig_-(K3) are the structural "
            "new content."
        ),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data") / "w33_heegner_ogg_venn_decomposition.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    print("=" * 78)
    print("W(3,3) HEEGNER-OGG VENN DECOMPOSITION THEOREM")
    print("=" * 78)

    v = payload["venn_decomposition"]
    print("\nVenn cells and substrate identifications:")
    print(f"  H cap O   = {v['intersection']['set']}, size {v['intersection']['size']} = {v['intersection']['substrate']}")
    print(f"  H \\ O     = {v['Heegner_setminus_Ogg']['set']}, size {v['Heegner_setminus_Ogg']['size']} = {v['Heegner_setminus_Ogg']['substrate']}")
    print(f"  O \\ H     = {v['Ogg_setminus_Heegner']['set']}, size {v['Ogg_setminus_Heegner']['size']} = {v['Ogg_setminus_Heegner']['substrate']}")
    print(f"  H cup O   = ..., size {v['union']['size']} = {v['union']['substrate']}")

    h = payload["hodge_decomposition_check"]
    print(f"\nHodge-like decomposition: sig_-(K3) = (mu+1) + mu + Phi_4")
    print(f"  {h['lhs']} = {(MU+1)} + {MU} + {PHI4} = {h['rhs']}: {h['match']}")

    sr = payload["self_referential_property"]
    print(f"\nSelf-referential fixed point:")
    print(f"  |H U O| = {sr['union_size']}")
    print(f"  in Heegner_9: {sr['in_Heegner_9']}, in Ogg_15: {sr['in_Ogg_15']}, in both: {sr['in_both']}")
    print(f"  matches sig_-(K3) = 19: {sr['matches_K3']}")

    m = payload["micro_decomposition_of_Ogg_only"]
    print(f"\nMicro-decomposition of the Phi_4 = 10 Ogg-only primes:")
    for role, info in m["substrate_role_split"].items():
        print(f"  {role:>25s}: {info['primes']} (size {info['size']})")
    print(f"  {m['size_decomposition']}")

    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
