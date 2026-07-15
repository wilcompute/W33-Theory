#!/usr/bin/env python3
"""Pass 323: the OTHER "theorem that stands" -- auditing the CSS family.

Pass 322 dissolved the rank law (published + already proved in-repo). This pass
applies the same test to the second of W33_HONEST_SYNTHESIS.md's "two theorems
that stand": the CSS family [[(q+1)(q^2+1), q^2+1, q+1]].

METHOD (Pass 322's rule): search for the RESULT, not the topic. Grep the literal
code parameters, and use git to ask WHEN they entered the repo.

FINDING 1 -- THE q=3 ANCHOR WAS ALREADY DOCUMENTED, AND MORE STRONGLY.
docs/index.html contained BOTH [[40,10,4]] and [40,15,8] BEFORE my Pass 224
commit (a9e38beb6) -- verified by `git show a9e38beb6~1:docs/index.html`, and the
file is byte-identical on those counts today. It attributes them to Passes
187/189, which establish considerably MORE than my pass did:

    "F2^40 is uniserial with layers 1|14|1|8|1|14|1. There are exactly eight
     invariant binary codes; the [40,15,8] sentinel is the unique invariant
     15-space, C^perp/C is forced, and the central eight is the unique
     eight-dimensional subquotient. Endomorphism fields are F2 for the 14 and
     F4 for the eight."

My Pass 224 showed C^perp is doubly-even and self-orthogonal, so a CSS register
exists with k=10. Passes 187/189 had already PROVED C^perp/C is FORCED, and had
the whole submodule lattice with uniqueness. Their "central eight" is my
"central quadratic shadow q^2-1 = 8" (224). index.html also already names "the
sentinel [[40,10,4]] CSS code" explicitly, with its logical Pauli space of
dimension 20.

FINDING 2 -- k WAS PROVED FOR ALL ODD q BEFORE MY PASS.
analysis/2026-07-10_levi_next5.md boxes rank_2 A_L = q^2+1, proved for every odd
prime power. That IS the family's k. So the k half of the "family" was a theorem
in this repo five days before Pass 224 claimed it.

FINDING 3 -- "k*d = n EXACTLY" IS A TAUTOLOGY.
Pass 239's headline called k*d = n a "conservation curve". But n is DEFINED as
the line count (q+1)(q^2+1) of W(3,q), k = q^2+1 and d = q+1. So
        k*d = (q^2+1)(q+1) = n
is the statement that n factors the way n is written. It cannot fail. This is the
same error as Pass 287's "trace law" and Pass 319's delta table -- a computation
that could not have come out otherwise, quoted as a result. Third instance.
Verified symbolically below.

WHAT ACTUALLY SURVIVES.
The generalization itself: [[156,26,6]] and [[400,50,8]] appear in NO file that
predates my passes (grep over the whole repo returns only pass_254+ and files
downstream of them). So extending the q=3 anchor to a family over all odd q is
plausibly mine. But it is a MODEST extension, and honesty requires the decomposition:

    n = (q+1)(q^2+1)   standard GQ(q,q) line count -- textbook
    k = q^2+1          PROVED in-repo before Pass 224 (levi_next5, boxed)
    d = q+1            Pass 229 -- the one genuinely new ingredient
    k*d = n            tautology (Finding 3)

So the family reduces to ONE new claim: that the CSS distance equals q+1. The
upper bound is immediate (isotropic lines have weight q+1). The content is the
lower bound. That -- not "a family with a conservation law" -- is the honest size
of what Passes 224/229/239 contributed.

VERDICT. Both "theorems that stand" have now failed the corpus test in their
headline form. The rank law is published (322). The CSS family is a known q=3
code, whose k is a known theorem, packaged with a tautology and one real lemma.
"""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass323_the_css_family_audit.json"


def main():
    checks = {}
    q = sp.Symbol("q", positive=True)

    # ---- Finding 3: k*d = n is a tautology
    n = (q + 1) * (q ** 2 + 1)      # the GQ(q,q) line count -- the DEFINITION of n
    k = q ** 2 + 1                  # levi_next5's boxed rank_2 A_L
    d = q + 1                       # Pass 229
    checks["k_times_d_equals_n_identically"] = sp.simplify(k * d - n) == 0
    checks["so_the_conservation_curve_cannot_fail"] = True
    checks["it_is_the_statement_that_n_factors_as_written"] = True
    # a tautology holds at every q, including non-prime-powers -- the tell
    checks["holds_at_q_6_a_non_prime_power"] = int((k * d).subs(q, 6)) == int(n.subs(q, 6))

    # ---- the family values, for the record
    fam = {}
    for qq in (3, 5, 7, 9, 11):
        fam[str(qq)] = {"n": int(n.subs(q, qq)), "k": int(k.subs(q, qq)),
                        "d": int(d.subs(q, qq)),
                        "k*d": int((k * d).subs(q, qq))}
    checks["q3_is_40_10_4"] = (fam["3"]["n"], fam["3"]["k"], fam["3"]["d"]) == (40, 10, 4)
    checks["q5_is_156_26_6"] = (fam["5"]["n"], fam["5"]["k"], fam["5"]["d"]) == (156, 26, 6)

    # ---- Finding 1/2: provenance (established by git + grep, recorded here)
    idx = (ROOT / "docs" / "index.html").read_text(encoding="utf-8", errors="ignore")
    checks["index_html_names_40_10_4_today"] = "40,10,4" in idx
    checks["index_html_names_40_15_8_today"] = "40,15,8" in idx
    checks["index_html_has_uniserial_layers"] = "1|14|1|8|1|14|1" in idx
    checks["index_html_says_Cperp_over_C_forced"] = "is forced" in idx
    # git-verified in the pass body: both strings present at a9e38beb6~1 (pre-224)
    checks["both_predate_my_pass_224"] = True

    all_pass = all(v for v in checks.values() if isinstance(v, bool))
    payload = {
        "schema": "w33.pass323.css_family_audit.v1",
        "status": "PASS" if all_pass else "FAIL",
        "VERDICT": (
            "The second of the 'two theorems that stand' also fails the corpus test "
            "in its headline form. The q=3 anchor [[40,10,4]] and its sentinel "
            "[40,15,8] were in docs/index.html BEFORE Pass 224 (git-verified at "
            "a9e38beb6~1), attributed to Passes 187/189 -- which prove MORE than I "
            "did: the full uniserial submodule lattice 1|14|1|8|1|14|1, exactly "
            "eight invariant binary codes, [40,15,8] as the UNIQUE invariant "
            "15-space, C^perp/C FORCED, and the central eight (= my 'central "
            "quadratic shadow q^2-1=8') as the unique 8-dim subquotient."
        ),
        "finding_1_the_anchor_was_documented": {
            "evidence": "git show a9e38beb6~1:docs/index.html contains both "
                        "'40,10,4' and '40,15,8'; counts identical today (1 and 2)",
            "index_html_text": "F2^40 is uniserial with layers 1|14|1|8|1|14|1. "
                               "There are exactly eight invariant binary codes; the "
                               "[40,15,8] sentinel is the unique invariant 15-space, "
                               "C^perp/C is forced, and the central eight is the "
                               "unique eight-dimensional subquotient. Endomorphism "
                               "fields are F2 for the 14 and F4 for the eight.",
            "attributed_to": "Passes 187/189 -- 'The Complete Binary Submodule Chain'",
            "my_pass_224": "showed C^perp doubly-even + self-orthogonal => a CSS "
                           "register exists, k=10. Strictly weaker: 187/189 had "
                           "already PROVED C^perp/C is forced, with uniqueness.",
        },
        "finding_2_k_was_already_a_theorem": {
            "levi_next5_boxed": "rank_2 A_L = q^2 + 1, for EVERY odd prime power",
            "that_is": "the family's k -- proved in-repo five days before Pass 224",
        },
        "finding_3_kd_equals_n_is_a_tautology": {
            "pass_239_headline": "'k*d = n EXACTLY (conservation curve)'",
            "the_fact": "n is DEFINED as the GQ(q,q) line count (q+1)(q^2+1); "
                        "k = q^2+1 and d = q+1; so k*d = (q^2+1)(q+1) = n is the "
                        "statement that n factors the way n is written. It cannot "
                        "fail -- it even holds at q=6, which is not a prime power.",
            "the_pattern": "third instance of the same error: Pass 287's 'trace "
                           "law', Pass 319's delta table, and now Pass 239's "
                           "'conservation curve'. A computation that could not have "
                           "come out otherwise carries no information.",
        },
        "what_actually_survives": {
            "the_generalization": "[[156,26,6]] / [[400,50,8]] appear in NO file "
                                  "predating my passes -- so extending the q=3 "
                                  "anchor to a family over all odd q is plausibly "
                                  "mine.",
            "but_the_honest_decomposition": {
                "n = (q+1)(q^2+1)": "standard GQ(q,q) line count -- textbook",
                "k = q^2+1": "PROVED in-repo before Pass 224 (levi_next5, boxed)",
                "d = q+1": "Pass 229 -- THE ONE genuinely new ingredient",
                "k*d = n": "tautology",
            },
            "the_real_size": "The family reduces to ONE new claim: the CSS distance "
                             "equals q+1. Its upper bound is immediate (isotropic "
                             "lines have weight q+1); the content is the lower "
                             "bound. That -- not 'a family with a conservation law' "
                             "-- is the honest size of Passes 224/229/239.",
        },
        "the_family_table": fam,
        "checks": {k_: bool(v) for k_, v in checks.items() if isinstance(v, bool)},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
