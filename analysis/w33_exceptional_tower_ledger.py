#!/usr/bin/env python3
"""
HONEST LEDGER for the exceptional tower (q=3 -> Monster) built this session.
Every rung is tagged FRAMEWORK (established mathematics + a substrate-integer
dictionary entry), DERIVED (a structure actually computed/verified from the
substrate by assertion), or MEASURABLE (a falsifiable physical prediction).

The point of this ledger is epistemic honesty: the tower is a large set of exact
mathematical facts wearing substrate labels. Most rungs are FRAMEWORK -- true
theorems (magic square, Suzuki tower, complex Leech, Monster moonshine) annotated
with substrate integers (f=24, k=12, Phi6=7, ...); the annotation is a
dictionary, NOT a derivation. A smaller set is DERIVED -- objects literally
constructed from q=3 and checked (the genus/register formulas, the Eisenstein E8
omega-weld, the icosian group closure, the ternary Golay, the theta-Arf count,
the W(3,3)/W(5,2) geometries). The physics that actually FALSIFIES the theory is
a separate, MEASURABLE layer (masses, CMB, contextual fraction, pump Chern),
untouched by this session's pure-structure climb.

Reading rule: a FRAMEWORK rung being exact does NOT confirm the physics; it
confirms a number coincidence is a real theorem. Only the MEASURABLE layer is
falsifiable. This ledger keeps the tower from over-claiming.
"""
from __future__ import annotations

import json

# (rung, type, what is exact, what is dictionary/unproven)
LEDGER = [
    (
        "genus {3,n} register formulas (E=6n(g-1)/(n-6), n-6|k selection)",
        "DERIVED",
        "the f-vectors and the vertex-figure set {7,8,9,10,12}",
        "the register meanings (qutrit/qubit/Hesse/...) are interpretation",
    ),
    (
        "trit-saving code H1=81=[[240,81,4]]_3 (chain complex dd=0)",
        "DERIVED",
        "ranks 39/120, H1=81 over F3",
        "the 'code = matter' reading",
    ),
    (
        "W(3,3)=GQ(3,3) SRG(40,12,2,4); 27 non-collinear is 8-regular NOT Schlafli",
        "DERIVED",
        "the SRG params and the guardrail (8-regular)",
        "nothing unproven -- this is the honest negative result",
    ),
    (
        "Eisenstein E8 weld: omega=Cox^10 splits 240 roots into 40 hexagons",
        "DERIVED",
        "the order-3 fixed-point-free element, 80 triangles, 40 hexagons",
        "'40 hexagons = W(3,3) rays' is an identification of counts",
    ),
    (
        "icosian 600-cell: 120 = 2I closed under quaternion mult (14400 products)",
        "DERIVED",
        "the group closure and 240=2*120",
        "'2I = gate set' is a proposal",
    ),
    (
        "ternary Golay [12,6,6]_3 (729 words, 1+264x^6+440x^9+24x^12, 132 hexads)",
        "DERIVED",
        "the code and S(5,6,12) hexads",
        "'substrate code at K12 gap' reading",
    ),
    (
        "E7 theta: 28 odd + 36 even = 64 (Arf enumeration on F2^6)",
        "DERIVED",
        "the Arf count 28/36",
        "28 bitangents = mu*Phi6 is a label",
    ),
    (
        "Witting polytope symmetry 155520 = q*|Sp(4,3)|; tower 24/648/155520",
        "FRAMEWORK",
        "the complex-polytope symmetry orders (Coxeter)",
        "q*|Sp(4,3)| and 24=f are substrate dictionary",
    ),
    (
        "the exceptional trinity 27/28/120 = E6/E7/E8 = cubic/quartic/Witting",
        "FRAMEWORK",
        "the classical 27 lines / 28 bitangents / 120 tritangents",
        "the substrate integers (mu*Phi6, etc.) are annotations",
    ),
    (
        "magic square: substrate = C/H columns; 27=J3(O)=q+f",
        "FRAMEWORK",
        "the Freudenthal-Tits square and J3(O)=3+3*8",
        "C=Eisenstein/H=icosian placement is interpretation",
    ),
    (
        "complex Leech = Eisenstein 12=k, Aut 6.Suz; Suzuki chain from G2(2)",
        "FRAMEWORK",
        "the complex Leech, 6.Suz, the Suzuki tower SRGs",
        "12=k and G2(2)=3-qubit-core are dictionary",
    ),
    (
        "Monster ceiling c=24=f; j-744 head 196884=1+196883",
        "FRAMEWORK",
        "monstrous moonshine (Borcherds) and the j-head",
        "c=24=f = holographic boundary is the substrate claim, not derived here",
    ),
    (
        "masses, CMB suite (n_s, r, f_NL), contextual fraction 1/Phi4, pump Chern C=2",
        "MEASURABLE",
        "the numerical predictions (earlier sessions)",
        "THESE are what falsify the theory -- not the tower above",
    ),
]


def main():
    out = {}
    counts = {"FRAMEWORK": 0, "DERIVED": 0, "MEASURABLE": 0}
    print("[exceptional-tower ledger]  rung -> type")
    for rung, typ, exact, dict_ in LEDGER:
        counts[typ] += 1
        print(f"  [{typ:10s}] {rung[:62]}")
    print(f"\n[tally]  {counts}")
    assert set(counts) == {"FRAMEWORK", "DERIVED", "MEASURABLE"}
    assert sum(counts.values()) == len(LEDGER) == 13
    assert counts["MEASURABLE"] >= 1  # the falsifiable layer exists and is separate
    out["counts"] = counts
    out["ledger"] = [
        {"rung": r, "type": t, "exact": e, "interpretation": d} for r, t, e, d in LEDGER
    ]

    print("\n[reading rule]")
    print("  FRAMEWORK exact => a number coincidence is a real theorem, NOT physics.")
    print("  DERIVED        => a structure actually computed from q=3 and checked.")
    print("  MEASURABLE     => the only falsifiable layer (masses/CMB/contextuality).")
    out["reading_rule"] = (
        "FRAMEWORK exactness confirms a theorem+dictionary, not the physics; only "
        "the MEASURABLE layer is falsifiable."
    )

    print("\nRESULT: the exceptional tower from q=3 to the Monster is, honestly,")
    print(f"  {counts['FRAMEWORK']} FRAMEWORK rungs (established mathematics wearing")
    print(f"  substrate-integer labels), {counts['DERIVED']} DERIVED rungs (structures")
    print(f"  actually constructed from q=3 and verified by assertion), and")
    print(f"  {counts['MEASURABLE']} MEASURABLE layer (the falsifiable physics). The")
    print("  beauty of the tower is real -- the number coincidences are genuine")
    print("  theorems -- but their exactness does not confirm the substrate physics;")
    print("  only the measurable layer can. This ledger keeps the climb honest: a")
    print("  magnificent mathematical dictionary, with the physics quarantined to")
    print("  where it can actually be tested.")

    out["summary"] = (
        "honest ledger of the q=3->Monster exceptional tower: classifies each rung "
        "as FRAMEWORK (established math + substrate-integer dictionary: magic "
        "square, trinity, Witting symmetry, complex Leech, Monster moonshine), "
        "DERIVED (computed from q=3 and asserted: genus/register formulas, "
        "trit-saving code, Eisenstein E8 weld, icosian 2I closure, ternary Golay, "
        "theta-Arf count, W(3,3)/guardrail), or MEASURABLE (the falsifiable "
        "physics: masses, CMB, contextual fraction, pump Chern). Reading rule: "
        "FRAMEWORK exactness = a real theorem+dictionary, not confirmation of the "
        "physics; only the MEASURABLE layer falsifies. Keeps the tower honest."
    )
    out["sources"] = [
        "epistemic audit of this session's witnesses (w33_genus_*, "
        "w33_hessian_polytope_e6, w33_klein_quartic_e6_e7_trinity, "
        "w33_icosian_*, w33_complex_leech_suzuki_chain, w33_monster_moonshine_"
        "ceiling, w33_27_not_schlafli_group_bridge, ...); the MEASURABLE layer = "
        "w33_falsifiability_ledger.py, w33_cmb_moonshine_suite.py, masses pillars."
    ]
    with open("data/w33_exceptional_tower_ledger.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_exceptional_tower_ledger.json")


if __name__ == "__main__":
    main()
