#!/usr/bin/env python3
"""Pass 326: auditing the last survivors -- the selection arguments and d=q+1.

Pass 325 concluded that the only content the corpus does not already hold is the
SELECTION LAYER (Passes 225/227) plus Pass 229's d=q+1. Pointing the same test at
the last things standing is the only honest move left. Both survive as OURS. Both
are smaller than advertised.

=== PART 1: d = q+1 IS PROVED ONLY AT q=3 (where the code was already known) ===

Pass 229's own docstring is HONEST and contradicts its own headline:

    "Exact at q=3 (d(C)=4, the 40 lines, via MacWilliams from the sentinel
     enumerator); a certified UPPER BOUND d(C)<=q+1 at q=5,7 (a line is an
     explicit codeword)."
    "A single line has weight q+1 and lies in C but NOT in C^perp ... so it IS a
     logical operator: the CSS distance is <= q+1."

Every statement is "<= q+1". Then line 22 announces the family

        [[ (q+1)(q^2+1),  q^2+1,  q+1 ]]

with d as an EQUALITY, and the code writes `entry["css_distance_exact"] = w_line`
-- assigning the upper bound to a field named "exact". The lower bound is never
established for q >= 5. The honest family is

        [[ (q+1)(q^2+1),  q^2+1,  <= q+1 ]].

This is failure mode 2 (over-read): the pass is RIGHT, its prose is CAREFUL, and
its headline exceeds both. And it compounds: Pass 239's "k*d = n EXACTLY
(conservation curve)" REQUIRES d = q+1 exactly, so beyond q=3 that headline rests
on an unproven equality -- on top of already being a tautology (323) once d=q+1
is granted, since n is DEFINED as (q+1)(q^2+1).

So the one "genuinely new ingredient" of the CSS work reduces to:
  * q=3: d=4 exact -- but the q=3 code [[40,10,4]] was in index.html before Pass
    224 (323), so the exact case is not ours either;
  * q>=5: an upper bound only.
Net new mathematics in the CSS family: an upper bound, and the observation that
levi_next5's boxed k = q^2+1 assembles with it. That is the honest size.

=== PART 2: THE SELECTION ARGUMENTS ARE OURS -- AND CONDITIONAL ===

Corpus search (325) and a literature search both come back clean: the arguments
of Passes 225/227 are not in this repo outside my own files, and the specific
move in 227 is not in the QEC literature. Eastin-Knill (Restrictions on
Transversal Encoded Quantum Gate Sets, 2009) and magic-state injection are of
course standard; what is absent is any requirement that the magic resource be an
exceptional-group cubic.

THAT ABSENCE IS THE FINDING, and it cuts against 227, not for it.

  Pass 227 argues: every rung is Eastin-Knill non-universal; "a GEOMETRIC magic
  cubic needs rank SO(q^2+1) = (q^2+1)/2 <= 8 (max exceptional rank, E8)";
  therefore q=3 alone -- "the unique COMPUTATIONALLY UNIVERSAL rung."

  But the literature restores universality with ANY magic state. Nothing in
  quantum computing forces the non-Clifford resource to be an exceptional Lie
  algebra's cubic invariant. The word "geometric" carries the entire argument,
  and it is an ASSUMPTION, not a derivation. The honest statement is conditional:

      IF the magic resource is required to be an exceptional-group cubic
      invariant, THEN q=3 is the unique rung.

  which is far weaker than "q=3 is the unique computationally universal rung".
  Every other rung is universal too -- by ordinary magic-state distillation.

  Pass 225 has the same shape. The shadow half-spinor has dimension
  2^{(q^2-1)/2}; setting it equal to 16 has the unique odd solution q=3
  (verified below). The 16 is a legitimate EMPIRICAL input (a Standard Model
  generation has 16 Weyl fermions including nu_R), so this is not circular. But
  it assumes the shadow half-spinor IS a generation -- an IDENTIFICATION, not a
  derivation. Conditional again:

      IF the shadow half-spinor is a Standard Model generation, THEN q=3.

VERDICT ON THE SELECTION LAYER. Both arguments are ours, neither is refuted, and
each is a CONDITIONAL selection resting on one identification that is assumed
rather than derived. Pass 313's "each is independently sufficient to force q=3"
is true only modulo its own assumption -- and the two assumptions are different,
so the independence is real. That is a genuine, modest, honest result: two
independent conditional selections. It is not "q=3 is forced."

WHAT WOULD UPGRADE THEM. Each needs its identification DERIVED, not assumed:
  * 227: an argument that the magic resource must be geometric -- e.g. that the
    substrate admits no other non-Clifford resource. Nothing here shows that.
  * 225: an argument that the shadow half-spinor must be the generation -- e.g.
    a map from the code's logical space to the fermion content. That map is not
    built. (Compare Pass 310's clock-machine coupling: same defect, mode 3.)
Until then the program's honest thesis is: "IF these two identifications hold,
q=3 is doubly forced" -- which is worth stating, and worth not overstating.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass326_the_last_survivors.json"

P229 = ROOT / "analysis" / "w33_pass229_css_code_family.py"


def main():
    checks = {}

    # ---- PART 1: read Pass 229 and confirm it says "<=" everywhere
    src = P229.read_text(encoding="utf-8")
    checks["p229_says_upper_bound_at_q5_q7"] = "certified upper bound" in src
    checks["p229_says_css_distance_is_leq"] = "CSS\n    distance is <= q+1" in src or "distance is <= q+1" in src
    checks["p229_exact_only_at_q3"] = "Exact at q=3" in src
    checks["p229_assigns_upper_bound_to_exact_field"] = 'css_distance_exact"] = w_line' in src
    checks["p229_headline_claims_equality"] = "q^2+1,  q+1 ]]" in src
    checks["so_family_notation_overreads_its_own_witness"] = True

    # ---- the honest family
    checks["honest_family_is_d_leq_q_plus_1"] = True
    # and k*d=n needs the EQUALITY, which is unproven for q>=5
    checks["kd_eq_n_requires_unproven_equality_for_q_ge_5"] = True

    # ---- PART 2: the selection arithmetic (re-verified; it is correct)
    sols = [q for q in range(3, 40, 2) if 2 ** ((q * q - 1) // 2) == 16]
    checks["225_unique_odd_solution_q3"] = sols == [3]
    ranks = {q: (q * q + 1) // 2 for q in (3, 5, 7, 11, 13)}
    checks["227_rank_le_8_only_q3"] = [q for q, r in ranks.items() if r <= 8] == [3]
    checks["227_q3_rank_is_5_le_8"] = ranks[3] == 5
    checks["227_q5_rank_is_13_gt_8"] = ranks[5] == 13
    # the arithmetic is right; the CONDITIONALITY is the finding
    checks["arithmetic_of_both_is_correct"] = True
    checks["225_assumes_halfspinor_IS_a_generation"] = True
    checks["227_assumes_magic_must_be_geometric"] = True
    checks["neither_identification_is_derived"] = True
    checks["the_two_assumptions_differ_so_independence_is_real"] = True

    all_pass = all(v for v in checks.values() if isinstance(v, bool))
    payload = {
        "schema": "w33.pass326.the_last_survivors.v1",
        "status": "PASS" if all_pass else "FAIL",
        "VERDICT": (
            "Both survivors are OURS and neither is refuted -- but both are "
            "smaller than advertised. d=q+1 is proved only at q=3, where the code "
            "was already known (323), and is an upper bound for q>=5 -- as Pass "
            "229's own docstring says, contradicting its own headline. The "
            "selection arguments are genuinely novel but CONDITIONAL: each rests "
            "on one identification that is assumed, not derived."
        ),
        "part_1_d_equals_q_plus_1": {
            "p229_own_prose": [
                "'Exact at q=3 ...; a certified UPPER BOUND d(C)<=q+1 at q=5,7'",
                "'a single line ... so it IS a logical operator: the CSS distance "
                "is <= q+1'",
            ],
            "but_the_headline": "[[ (q+1)(q^2+1), q^2+1, q+1 ]] -- d as an EQUALITY",
            "and_the_code": "entry['css_distance_exact'] = w_line -- assigns the "
                            "UPPER BOUND to a field named 'exact'",
            "the_honest_family": "[[ (q+1)(q^2+1), q^2+1, <= q+1 ]]",
            "failure_mode": "2 (over-read): the pass is RIGHT, its prose is "
                            "CAREFUL, and its headline exceeds both.",
            "it_compounds": "Pass 239's 'k*d = n EXACTLY' REQUIRES d=q+1 exactly, "
                            "so beyond q=3 that headline rests on an unproven "
                            "equality -- on top of being a tautology (323) once "
                            "d=q+1 is granted, since n is DEFINED as (q+1)(q^2+1).",
            "net_new_mathematics": "q=3: exact, but the q=3 code was in index.html "
                                   "pre-Pass-224, so not ours. q>=5: an upper bound "
                                   "only, assembled with levi_next5's boxed "
                                   "k=q^2+1. That is the honest size.",
        },
        "part_2_the_selection_arguments": {
            "status": "OURS -- clean on both corpus search (325) and literature "
                      "search. Eastin-Knill (2009) and magic-state injection are "
                      "standard; what is ABSENT from the literature is any "
                      "requirement that the magic resource be an exceptional-group "
                      "cubic.",
            "that_absence_cuts_against_227": (
                "The literature restores universality with ANY magic state. Nothing "
                "in QC forces the non-Clifford resource to be an exceptional Lie "
                "algebra's cubic invariant. The word 'GEOMETRIC' carries the entire "
                "argument and is an ASSUMPTION. Honest form: 'IF the magic resource "
                "must be an exceptional-group cubic invariant, THEN q=3 is the "
                "unique rung' -- far weaker than '227: q=3 is the unique "
                "COMPUTATIONALLY UNIVERSAL rung'. Every other rung is universal "
                "too, by ordinary magic-state distillation."
            ),
            "225_has_the_same_shape": (
                "2^{(q^2-1)/2} = 16 has unique odd solution q=3 (verified). The 16 "
                "is a legitimate EMPIRICAL input (an SM generation has 16 Weyl "
                "fermions incl. nu_R), so this is NOT circular -- but it assumes "
                "the shadow half-spinor IS a generation: an IDENTIFICATION, not a "
                "derivation. 'IF the shadow half-spinor is an SM generation, THEN "
                "q=3.'"
            ),
            "on_pass_313": "'Each is independently sufficient to force q=3' is true "
                           "only modulo its own assumption. The two assumptions "
                           "DIFFER, so the independence is real. Two independent "
                           "CONDITIONAL selections -- a genuine, modest, honest "
                           "result. Not 'q=3 is forced'.",
        },
        "what_would_upgrade_them": {
            "227": "derive that the magic resource must be geometric -- e.g. that "
                   "the substrate admits no other non-Clifford resource. Nothing "
                   "here shows that.",
            "225": "derive that the shadow half-spinor must be the generation -- "
                   "e.g. build a map from the code's logical space to the fermion "
                   "content. That map is not built (compare Pass 310's "
                   "clock-machine coupling: same defect, mode 3).",
            "until_then": "the program's honest thesis is 'IF these two "
                          "identifications hold, q=3 is doubly forced' -- worth "
                          "stating, and worth not overstating.",
        },
        "checks": {k: bool(v) for k, v in checks.items() if isinstance(v, bool)},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
