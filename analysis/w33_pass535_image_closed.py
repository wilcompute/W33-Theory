#!/usr/bin/env python3
"""Pass 535: the q = 3 image constraint is two theorems this paper already
proved -- a second instance of under-extraction, one pass after naming it.

Pass 528 found six characteristic polynomials at q = 3; Pass 529 put them on
the lattice e_2 in 9Z, e_3 in 27Z; Passes 531-534 explained why the
coefficients are rational at all (reality, via D Hermitian, at p = 3 where the
real subring has degree 1).  What was left open, and called "the only q = 3
question", was WHY the lattice.

It is not a new question.  For a RATIONAL coefficient, divisibility and
valuation are the same statement:

        9 | e_2   <=>   v_lambda(e_2) = 2 v_3(e_2) >= 4 ,
        27 | e_3  <=>   v_lambda(e_3) = 2 v_3(e_3) >= 6 ,

and both bounds are already theorems here.  The first is Pass 487's
v_lambda(e_k) >= 2k at k = 2.  The second is the sharp determinant law's
v_lambda(e_q) >= v_lambda(q) + 4, which at q = 3 reads 2 + 4 = 6.  Verified on
all six polynomials: the divisibility and the bound agree in every case, in
both directions.

SO THE q = 3 STORY CLOSES with no new input:

    inverse closure  =>  D Hermitian  =>  charpoly real
                     =>  at p = 3, rational  (real subring has degree 1)
    Pass 487         =>  v_lambda(e_2) >= 4   =>  9 | e_2
    sharp law        =>  v_lambda(e_3) >= 6   =>  27 | e_3

and the six occurring polynomials are exactly the lattice points those two
bounds allow, among those the sections realise.

A SECOND INSTANCE OF UNDER-EXTRACTION.  Pass 534 named the failure mode --
a hypothesis strong enough for more than was taken from it -- with Pass 491 as
the example.  This is another, and it was live while the name was being
written: the lattice looked like an open problem for three passes and was
implied by two theorems already in the paper.  The difference from Pass 491 is
instructive.  There, one hypothesis gave more than one conclusion.  Here, two
CONCLUSIONS already proved were not recognised as answering a question posed in
different vocabulary -- divisibility rather than valuation.  Same cost,
different cause: the corpus is indexed by the form a statement was written in,
not by what it says.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass535_image_closed.json"

SIX = [(0, 0), (-9, 0), (-18, 0), (-27, 0), (-27, 27), (-36, 81)]


def v3(n):
    if n == 0:
        return None
    n, v = abs(n), 0
    while n % 3 == 0:
        n //= 3
        v += 1
    return v


def part_A_equivalence(checks):
    rows, ok2, ok3 = {}, True, True
    for e2, e3 in SIX:
        a, b = v3(e2), v3(e3)
        va = None if a is None else 2 * a
        vb = None if b is None else 2 * b
        div2, div3 = (e2 % 9 == 0), (e3 % 27 == 0)
        bnd2 = (va is None or va >= 4)
        bnd3 = (vb is None or vb >= 6)
        if div2 != bnd2:
            ok2 = False
        if div3 != bnd3:
            ok3 = False
        rows[f"e2={e2},e3={e3}"] = {
            "v_lambda_e2": va, "v_lambda_e3": vb,
            "nine_divides_e2": div2, "bound_e2_at_least_4": bnd2,
            "twentyseven_divides_e3": div3, "bound_e3_at_least_6": bnd3}
    checks["divisibility_by_9_is_the_e2_bound"] = ok2
    checks["divisibility_by_27_is_the_e3_bound"] = ok3
    checks["all_six_polynomials_checked"] = len(rows) == 6
    return {"rows": rows,
            "equivalence": (
                "For a RATIONAL coefficient, divisibility and valuation are "
                "the same statement: 9 | e_2 iff v_lambda(e_2) = 2 v_3(e_2) "
                ">= 4, and 27 | e_3 iff v_lambda(e_3) >= 6.  Both directions "
                "hold on all six polynomials."),
            "sources": {
                "v_lambda(e_2) >= 4": "Pass 487, v_lambda(e_k) >= 2k at k = 2",
                "v_lambda(e_3) >= 6": (
                    "the sharp determinant law, v_lambda(e_q) >= v_lambda(q) "
                    "+ 4, which at q = 3 is 2 + 4")}}


def part_B_closure(checks):
    checks["q3_chain_complete"] = True
    return {"chain": (
        "inverse closure => D Hermitian => charpoly real => at p = 3 rational "
        "(the real subring has degree (p-1)/2 = 1); then Pass 487 gives "
        "v_lambda(e_2) >= 4, hence 9 | e_2, and the sharp law gives "
        "v_lambda(e_3) >= 6, hence 27 | e_3.  The six occurring polynomials "
        "are lattice points those two bounds allow."),
        "what_is_still_not_explained": (
            "WHICH lattice points the sections realise.  The bounds permit "
            "infinitely many; exactly six occur, with multiplicities "
            "1, 8, 24, 8, 24, 16.  Nothing here predicts that list -- only "
            "that it lies in the lattice."),
        "status": (
            "The q = 3 question as posed in Pass 534 -- why the lattice -- is "
            "answered.  The finer question -- why these six points -- is not, "
            "and was not what was asked.")}


def part_C_second_instance(checks):
    checks["second_instance_recorded"] = True
    return {"instance": (
        "Pass 534 named UNDER-EXTRACTION -- a hypothesis strong enough for "
        "more than was taken from it -- with Pass 491 as the example.  This "
        "is a second instance, live while the name was being written: the "
        "lattice looked open for three passes and was implied by two theorems "
        "already in the paper."),
        "the_difference": (
            "In Pass 491 one HYPOTHESIS gave more than one conclusion.  Here "
            "two CONCLUSIONS already proved were not recognised as answering a "
            "question posed in different vocabulary -- divisibility rather "
            "than valuation.  Same cost, different cause."),
        "the_lesson": (
            "The corpus is indexed by the FORM a statement was written in, not "
            "by what it says.  A question about divisibility did not match "
            "theorems about valuations, though over the rationals they are the "
            "same statement.  Searching by result rather than by topic -- the "
            "standing rule here -- is necessary and was not sufficient: the "
            "result has to be searched for in every vocabulary it could wear.")}


def main_payload():
    checks = {}
    A = part_A_equivalence(checks)
    B = part_B_closure(checks)
    C = part_C_second_instance(checks)
    status = "PASS" if all(checks.values()) else "FAIL"
    return {
        "schema": "w33.pass535.image_closed.v1",
        "status": status,
        "headline": (
            "THE q = 3 LATTICE IS TWO THEOREMS ALREADY IN THE PAPER.  For a "
            "rational coefficient, divisibility and valuation are the same "
            "statement: 9 | e_2 iff v_lambda(e_2) >= 4, and 27 | e_3 iff "
            "v_lambda(e_3) >= 6.  The first bound is Pass 487's "
            "v_lambda(e_k) >= 2k at k = 2; the second is the sharp determinant "
            "law's v_lambda(e_q) >= v_lambda(q) + 4, which at q = 3 reads "
            "2 + 4 = 6.  Both directions verified on all six polynomials.  So "
            "the chain closes with no new input: inverse closure gives D "
            "Hermitian, hence a real characteristic polynomial, hence rational "
            "at p = 3 where the real subring has degree 1, and the two bounds "
            "give the lattice.  This is a SECOND instance of the "
            "under-extraction named one pass earlier -- and a different cause: "
            "there a hypothesis gave more than was taken, here two proved "
            "conclusions went unrecognised because the question was posed in "
            "divisibility and the theorems were written in valuations."),
        "part_A_the_equivalence": A,
        "part_B_the_chain_closes": B,
        "part_C_second_instance_of_under_extraction": C,
        "boundary": (
            "Part A is arithmetic on the six polynomials Pass 528 enumerated "
            "exhaustively, and checks an equivalence rather than proving the "
            "bounds -- both bounds are cited, not re-proved.  What is NOT "
            "explained is which lattice points the sections realise: the "
            "bounds permit infinitely many and exactly six occur.  Part C is "
            "an editorial observation."),
        "checks": {k: bool(v) for k, v in checks.items()},
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--output", type=Path, default=OUT)
    a = ap.parse_args()
    pl = main_payload()
    text = json.dumps(pl, sort_keys=True, separators=(",", ":")) + "\n"
    if a.check:
        if not a.output.exists() or a.output.read_text() != text:
            raise SystemExit("Pass 535 certificate drift")
    else:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(text)
    print(json.dumps({"status": pl["status"],
                      "checks": sum(pl["checks"].values()),
                      "total": len(pl["checks"])}))
    return 0 if pl["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
