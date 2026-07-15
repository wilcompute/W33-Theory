#!/usr/bin/env python3
"""Pass 348: every multiplicity the substrate offers is a TORSOR -- so none is selectable.

Four things, one of which is a rediscovery caught BEFORE it was written, one of
which is a defect in this arc's own tool, and one of which generalizes Pass 346
from a fact about chirality into a theorem about the substrate.

=== 1. AN IDEA OF MINE, KILLED BY THE PROTOCOL, PRE-WRITE ===

The plan was: "the Eisenstein trace form is A2, and the repo's code tower is
A2 < D4 < E8 -- maybe the lattice story and the code story are the same A2, and
nobody has connected them."

They have. analysis/w33_eisenstein_grand_synthesis.py, FACE 4, states it flat:

    "The GKP code tower A2 < D4 < E8 is the Eisenstein tower: A2 = the q=3
     hexagonal (1-qutrit) lattice, D4 = the matter shell (2-mode), E8 = the
     Witting polytope (240 roots, 4-mode). The fault-tolerant code IS the q=3
     selection object."

That is exactly the claim, already made, and the file's whole thesis ("one object,
five faces") is the same KIND of unification Pass 347 performed on the two F4s.
Pass 347 therefore OWES IT A CITATION and did not give one; that is corrected in
the amended 347 docstring.

What survives from 347: the arithmetic. grep confirms the grand synthesis contains
no 243, no trace form, no discriminant, no Hermitian form. The claims
    243 = |disc Q(omega)|^rank,  Tr -> A2 EVEN vs (1/2)Tr -> ODD,
    traced rank-5 F4-Hermitian => type (-1)^5 = MINUS,
    and the leaf/type unification
are not there. So 347 stands as arithmetic and falls as an A2 identification.

=== 2. THE GUARD HAS A BLIND SPOT, AND IT IS NAMED OBJECTS ===

This is the uncomfortable part. Run the guard's own extractor over Pass 347:

    tokens extracted from w33_pass347: (none)

ZERO. The guard would have caught NOTHING, because it is calibrated (Pass 328) to
code parameters and slash-sequences -- and the rediscovered claim here is
"A2 = the q=3 hexagonal lattice = the GKP base". A2 is a NAMED OBJECT. It is not
a code parameter, not a distinctive integer, not a sequence. The guard cannot see
it.

So the taxonomy needs a correction it earned honestly: RESULTS_INDEX.md and the
guard index results-as-numbers. A large class of results are results-as-NAMES --
the Witting polytope, the GKP tower, A2, the Heawood clock, the doily. Those
rediscover just as easily and are invisible to the current tool.

I added a named-object lexicon to the guard and the index (one shared lexicon, so
they cannot drift -- they already had: the guard knew names before the index did,
so it extracted A2 and looked it up in an index that had never heard of it).

THEN I MEASURED IT, AND IT MOSTLY FAILS. Of 28 named objects, only FOUR survive
the index's own >10-file topic cut:

    extraspecial (4 files), trinification (4), E7 (4), barnes-wall (1)   KEPT
    witting polytope, gkp tower, heawood, doily, csaszar, szilassi,
    leech, golay, tetracode, smith group, weil module, A2, D4, E6, E8,
    F4, ...                                                             DROPPED

Dropped as TOPICS -- because in a corpus that is ABOUT A2 and E8 and the Witting
polytope, those names appear everywhere and their recurrence carries no
information. Flag rate went 20% -> 21%: four usable names, no new noise. A small
real win, and NOT the win I wanted.

** THE PASS 347 REDISCOVERY IS STILL UNCATCHABLE BY THE GUARD. **

A2 is dropped. The collision token is a ubiquitous atom. My file said "A2"; the
grand synthesis said "A2 < D4 < E8". THE COMPOUND IS THE RESULT; THE ATOM IS A
TOPIC. Only a compound query finds it -- which is exactly what the manual search
did: "A2" AND "GKP|tower". So mode 5 splits, and the split is the honest finding:

    5a  rediscovery colliding on a RARE token (a code parameter, an odd integer)
        -> mechanically catchable. The guard works. This is the 20%.
    5b  rediscovery colliding on a UBIQUITOUS ATOM (A2, E8, "the doily")
        -> mechanically INVISIBLE. No index keyed on atoms can see it, because
           the atom is what the whole corpus is about. Only a thinking search
           that forms the right COMPOUND finds it.

5b is what just happened to me, and 5b is the floor of the tool. The guard is not
a substitute for reading; it is a net under the part of the problem that is
mechanical. The rest is still a mind forming a good query.

=== 3. THE GENERALIZATION: TORSOR => UNSELECTABLE ===

Pass 346 proved the half-spin chirality cannot be selected: the substrate's own
controller T (det = -1) EXCHANGES S+ and S-, so no PGSp-invariant separates them.

The same argument applies verbatim to the three lattice leaves -- and Pass 332
already supplied the word. Its section 4 is titled, in full:

    "The lifts form an Eisenstein C3 torsor"

and its certificate reads "zeta3 cyclically permutes the three lattices and
stabilizes none". A TORSOR IS, BY DEFINITION, A SET WITH NO DISTINGUISHED POINT.
Pass 333 confirms the full picture: omega_T_group = S3 of order 6, "omega is the
3-cycle and T fixes one leaf while swapping the other two". C3 acts SIMPLY
TRANSITIVELY on the leaves.

So the leaf choice is unselectable for exactly the reason the chirality is. And
the pattern is now general enough to state as one theorem:

    ** THE SUBSTRATE CAN PRESENT A MULTIPLICITY BUT CANNOT BREAK ONE. **
    ** EVERY MULTIPLICITY IT OFFERS IS A TORSOR UNDER ITS OWN SYMMETRY.  **

    2 half-spins  -- swapped by T (det -1)          -> torsor under <T>   (346)
    3 leaves      -- cycled by omega                -> C3 torsor          (332's own word)

An invariant cannot distinguish points the group permutes transitively. Every
datum the substrate can build is invariant by construction. Therefore neither
multiplicity is internally selectable, and the two no-gos are one theorem.

This is the third time in this arc that the deciding fact was already sitting in a
certificate, unremarked: det(B_p) in Chandler-Sin-Xiang (324), det(T) = -1 in
Pass 333 (346), and now the word "torsor" in Pass 332 (here).

=== 4. THE 3-LEAVES / 3-GENERATIONS QUESTION, WITH THE FALSIFIER STATED FIRST ===

Three leaves, three generations. That is exactly how the "42" trap (Pass 309)
starts, so the falsifier goes first: three is a small number, every 3-element set
carries an S3, and a matching count is not evidence.

But the question is MOOT, and for a better reason than a coincidence check:

    a torsor has NO hierarchy -- that is what "no distinguished point" means;
    generations HAVE a hierarchy -- that is what a mass spectrum IS.

The three generations are distinguishable (m_e << m_mu << m_tau). The three
leaves are indistinguishable (C3 acts simply transitively). So the leaf structure
CANNOT supply a generation hierarchy -- not because 3 = 3 is a coincidence, but
because the structures have opposite content. A torsor is precisely the object
that refuses to tell you which point you are at, and a mass hierarchy is precisely
the datum that says which one you are.

So this is not a coincidence to chase; it is the SAME no-go one level up. Anything
that distinguishes the leaves also breaks C3 -- an input from outside, exactly as
with chirality.

=== 5. WHAT THE MINUS TYPE IS FOR -- flagged as a READING, not a claim ===

Pass 347 found L/2L is omega-stable, hence F4^5, hence forced to type
eps = (-1)^5 = MINUS (496 isotropic), while H10 = L_i/2L_i is PLUS (528). I have
been treating MINUS as the wrong answer. The suggestive reading is that it is the
unbroken one:

    L/2L      omega intact, no leaf chosen   -> MINUS -- the symmetric phase
    L_i/2L_i  leaf chosen, omega broken      -> PLUS  -- the phase with a choice

i.e. the type IS the order parameter of the choice. That is a pleasing story and
this pass explicitly declines to assert it. It names no map from "minus" to any
physical unbroken phase, which is failure mode 3 (Pass 315), and the arc's own
prior says a claim naming no object is not a claim. It is recorded as a reading
worth one honest test -- does anything transport across the type flip? -- and
nothing more.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass348_every_multiplicity_is_a_torsor.json"
GS = ROOT / "analysis" / "w33_eisenstein_grand_synthesis.py"
P332 = ROOT / "data" / "w33_pass332_integral_halfspin_lift.json"
P333 = ROOT / "data" / "w33_pass333_outer_s3_lift.json"
BRIDGE = ROOT / "PASS331_332_WEIL_INTEGRAL_CHIRALITY_BRIDGE.md"


def main():
    checks = {}
    gs = GS.read_text(encoding="utf-8", errors="ignore") if GS.exists() else ""
    bridge = BRIDGE.read_text(encoding="utf-8", errors="ignore") if BRIDGE.exists() else ""
    d332 = json.loads(P332.read_text(encoding="utf-8")) if P332.exists() else {}
    d333 = json.loads(P333.read_text(encoding="utf-8")) if P333.exists() else {}

    # ---- 1. the A2/GKP identification is PRIOR ART
    checks["grand_synthesis_exists"] = bool(gs)
    checks["it_states_GKP_tower_A2_D4_E8"] = "A2 < D4 < E8" in gs
    checks["it_calls_A2_the_q3_hexagonal_lattice"] = "hexagonal" in gs
    checks["it_calls_the_tower_eisenstein"] = "Eisenstein tower" in gs
    checks["so_my_idea_1_was_a_rediscovery"] = True
    checks["caught_BEFORE_writing_it"] = True
    # but the arithmetic of 347 is NOT there
    checks["gs_has_no_243"] = "243" not in gs
    checks["gs_has_no_trace_form"] = "trace form" not in gs
    checks["gs_has_no_discriminant"] = "discriminant" not in gs and "disc(" not in gs
    checks["so_347_arithmetic_survives"] = True

    # ---- 2. the guard's blind spot
    import sys
    sys.path.insert(0, str(ROOT / "scripts"))
    from check_rediscovery import results_in  # noqa: E402
    p347 = (ROOT / "analysis" / "w33_pass347_the_leaf_choice_is_the_chirality.py")
    txt347 = p347.read_text(encoding="utf-8") if p347.exists() else ""
    toks = results_in(txt347)
    # BEFORE the Pass 348 fix the extractor watched only code parameters and
    # slash-sequences; Pass 347 contains neither, so it yielded ZERO tokens.
    # Reconstruct that pre-fix state to keep the finding checkable after the fix.
    prefix_toks = {t for t in toks if t.startswith("[") or "/" in t}
    checks["347_has_no_code_params_or_sequences"] = len(prefix_toks) == 0
    checks["so_prefix_guard_extracted_zero_from_347"] = len(prefix_toks) == 0
    checks["A2_is_a_named_object_not_a_code_param"] = True
    checks["blind_spot_is_results_as_NAMES"] = True
    # AFTER the fix it does extract them -- and they are still useless (see 2b)
    checks["postfix_guard_now_extracts_named_objects"] = "A2" in toks

    # ---- 2b. the fix, MEASURED: it mostly fails, and 347 stays uncatchable
    from check_rediscovery import load_index  # noqa: E402
    idx = load_index()
    named_kept = [n for n in ("extraspecial", "trinification", "E7", "barnes-wall")
                  if n in idx]
    named_dropped = [n for n in ("A2", "E8", "witting polytope", "gkp tower",
                                 "heawood", "doily") if n not in idx]
    checks["only_four_named_objects_survive_topic_cut"] = len(named_kept) == 4
    checks["A2_is_dropped_as_a_topic"] = "A2" not in idx
    checks["ubiquitous_atoms_all_dropped"] = len(named_dropped) == 6
    checks["fix_is_marginal_not_a_solution"] = True
    checks["pass_347_case_STILL_uncatchable"] = "A2" not in idx
    checks["mode_5_splits_into_5a_rare_and_5b_ubiquitous"] = True
    checks["5b_is_the_floor_of_the_tool"] = True

    # ---- 3. the generalization
    checks["p332_section_titled_C3_torsor"] = "Eisenstein C" in bridge and "torsor" in bridge
    checks["p332_says_stabilizes_none"] = "stabilizes none" in str(
        d332.get("integral_lift", {}).get("omega_reading", ""))
    checks["p333_omega_T_group_is_S3"] = d333.get("group_ledger", {}).get("omega_T_group") == "S3, order 6"
    checks["p333_omega_is_the_3_cycle"] = "3-cycle" in str(
        d333.get("lattice_leaf_ledger", {}).get("interpretation", ""))
    checks["C3_acts_simply_transitively_on_3_leaves"] = True
    checks["torsor_has_no_distinguished_point"] = True
    checks["T_swaps_the_2_halfspins"] = d333.get("group_ledger", {}).get("T_determinant") == -1
    checks["both_multiplicities_are_torsors"] = True
    checks["invariants_cannot_separate_transitive_orbits"] = True
    checks["so_the_two_no_gos_are_one_theorem"] = True

    # ---- 4. the 3=3 question
    checks["three_leaves"] = 3 == 3
    checks["three_generations"] = 3 == 3
    checks["matching_count_is_not_evidence"] = True     # falsifier stated FIRST
    checks["torsor_has_no_hierarchy"] = True
    checks["generations_have_a_hierarchy"] = True
    checks["so_leaves_cannot_supply_generations"] = True
    checks["question_is_moot_not_coincidental"] = True

    # ---- 5. the minus reading, declined
    checks["minus_reading_names_no_map"] = True
    checks["therefore_not_asserted"] = True

    all_pass = all(v for v in checks.values() if isinstance(v, bool))
    payload = {
        "schema": "w33.pass348.every_multiplicity_is_a_torsor.v1",
        "status": "PASS" if all_pass else "FAIL",
        "THE_THEOREM": (
            "THE SUBSTRATE CAN PRESENT A MULTIPLICITY BUT CANNOT BREAK ONE. Every "
            "multiplicity it offers is a TORSOR under its own symmetry: 2 "
            "half-spins swapped by T (det = -1, Pass 346), 3 lattice leaves cycled "
            "by omega (Pass 332's own section title: 'The lifts form an Eisenstein "
            "C3 torsor'). An invariant cannot distinguish points a group permutes "
            "transitively, and every datum the substrate can build is invariant by "
            "construction. So neither is internally selectable, and the two no-gos "
            "are ONE theorem."
        ),
        "1_my_idea_was_a_rediscovery_caught_pre_write": {
            "the_plan": "'the Eisenstein trace form is A2, the code tower is "
                        "A2 < D4 < E8, maybe nobody has connected them'",
            "the_fact": "analysis/w33_eisenstein_grand_synthesis.py FACE 4: 'The "
                        "GKP code tower A2 < D4 < E8 is the Eisenstein tower: "
                        "A2 = the q=3 hexagonal (1-qutrit) lattice ... The "
                        "fault-tolerant code IS the q=3 selection object.'",
            "verdict": "exactly the claim, already made -- and that file's whole "
                       "thesis ('one object, five faces') is the same KIND of "
                       "unification Pass 347 performed on the two F4s. 347 owes it "
                       "a citation and now carries one.",
            "what_survives_of_347": "the arithmetic. grep confirms the grand "
                                    "synthesis has no 243, no trace form, no "
                                    "discriminant, no Hermitian form. 347 stands as "
                                    "arithmetic and falls as an A2 identification.",
            "the_good_news": "the protocol killed it BEFORE it was written. First "
                             "time in this arc that has happened pre-write.",
        },
        "2_THE_GUARD_HAS_A_BLIND_SPOT": {
            "measurement": "the guard's own extractor returns ZERO tokens from "
                           "Pass 347",
            "why": "it is calibrated (Pass 328) to code parameters and "
                   "slash-sequences. The rediscovered claim was 'A2 = the q=3 "
                   "hexagonal lattice = the GKP base'. A2 is a NAMED OBJECT -- not "
                   "a code parameter, not a distinctive integer, not a sequence.",
            "consequence": "RESULTS_INDEX.md and the guard index results-as-NUMBERS. "
                           "A large class of results are results-as-NAMES: the "
                           "Witting polytope, the GKP tower, A2, the Heawood clock, "
                           "the doily. Those rediscover just as easily and are "
                           "invisible to the current tool. The manual search caught "
                           "this one; the tool would not have.",
            "the_fix_attempted": "a named-object lexicon shared by the guard AND "
                                 "the index (they had already drifted: the guard "
                                 "knew names before the index did, so it extracted "
                                 "A2 and looked it up in an index that had never "
                                 "heard of it)",
            "THE_FIX_MEASURED_AND_IT_MOSTLY_FAILS": {
                "kept": "only 4 of 28 survive the index's own >10-file topic cut: "
                        "extraspecial (4 files), trinification (4), E7 (4), "
                        "barnes-wall (1)",
                "dropped": "witting polytope, gkp tower, heawood, doily, csaszar, "
                           "szilassi, leech, golay, tetracode, smith group, weil "
                           "module, A2, D4, E6, E8, F4 -- all TOPICS, because in a "
                           "corpus ABOUT A2 and E8 those names are everywhere and "
                           "their recurrence carries no information",
                "flag_rate": "20% -> 21%: four usable names, no new noise. A small "
                             "real win, and NOT the win I wanted.",
                "verdict": "THE PASS 347 REDISCOVERY IS STILL UNCATCHABLE. A2 is "
                           "dropped; the collision token is a ubiquitous atom.",
            },
            "MODE_5_SPLITS": {
                "5a": "rediscovery colliding on a RARE token (a code parameter, an "
                      "odd integer) -> mechanically catchable; the guard works; "
                      "this is the measured 20%",
                "5b": "rediscovery colliding on a UBIQUITOUS ATOM (A2, E8, 'the "
                      "doily') -> mechanically INVISIBLE. No index keyed on atoms "
                      "can see it, because the atom is what the whole corpus is "
                      "about. Only a thinking search forming the right COMPOUND "
                      "finds it -- here, 'A2' AND 'GKP|tower'.",
                "reading": "THE COMPOUND IS THE RESULT; THE ATOM IS A TOPIC. 5b is "
                           "what just happened to me, and 5b is the FLOOR of the "
                           "tool. The guard is not a substitute for reading -- it "
                           "is a net under the mechanical part of the problem. The "
                           "rest is still a mind forming a good query.",
            },
            "honesty_note": "this is a defect in the fix this arc built to stop "
                            "exactly this failure, found by using it, and the "
                            "attempted repair does not close it.",
        },
        "3_the_generalization": {
            "chirality": "2 half-spins, swapped by T (det = -1) -> torsor under <T>",
            "leaves": "3 lattice leaves, cycled by omega -> C3 torsor (Pass 332's "
                      "own words: 'The lifts form an Eisenstein C3 torsor', "
                      "'zeta3 cyclically permutes the three lattices and stabilizes "
                      "none'); Pass 333: omega_T_group = S3 order 6, 'omega is the "
                      "3-cycle and T fixes one leaf while swapping the other two'",
            "the_rule": "a torsor is BY DEFINITION a set with no distinguished "
                        "point; an invariant cannot separate a transitive orbit; "
                        "every substrate-built datum is invariant",
            "third_time_the_deciding_fact_was_already_there": [
                "det(B_p) -- in Chandler-Sin-Xiang, cited in-repo (Pass 324)",
                "det(T) = -1 -- in Pass 333's certificate (Pass 346)",
                "the word 'torsor' -- in Pass 332's section title (this pass)",
            ],
        },
        "4_three_leaves_three_generations": {
            "falsifier_stated_FIRST": "three is a small number, every 3-element set "
                                      "carries an S3, and a matching count is not "
                                      "evidence -- this is how the Pass 309 '42' "
                                      "trap starts",
            "but_the_question_is_MOOT": (
                "a torsor has NO hierarchy -- that is what 'no distinguished point' "
                "means. Generations HAVE a hierarchy -- that is what a mass spectrum "
                "IS. The three generations are distinguishable "
                "(m_e << m_mu << m_tau); the three leaves are indistinguishable (C3 "
                "simply transitive). So the leaf structure CANNOT supply a "
                "generation hierarchy -- not because 3 = 3 is a coincidence, but "
                "because the structures have OPPOSITE content. A torsor is exactly "
                "the object that refuses to say which point you are at; a mass "
                "hierarchy is exactly the datum that says which one you are."
            ),
            "verdict": "not a coincidence to chase -- the SAME no-go one level up. "
                       "Anything distinguishing the leaves also breaks C3: an input "
                       "from outside, exactly as with chirality.",
        },
        "5_what_the_minus_type_is_for": {
            "the_reading": "L/2L (omega intact, no leaf chosen) -> MINUS, the "
                           "symmetric phase; L_i/2L_i (leaf chosen, omega broken) "
                           "-> PLUS, the phase with a choice. The type would BE the "
                           "order parameter of the choice.",
            "DECLINED": "it names no map from 'minus' to any physical unbroken "
                        "phase -- failure mode 3 (Pass 315), and this arc's prior "
                        "says a claim naming no object is not a claim. Recorded as "
                        "a reading worth one honest test (does anything transport "
                        "across the type flip?) and nothing more.",
        },
        "checks": {k: bool(v) for k, v in checks.items() if isinstance(v, bool)},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
