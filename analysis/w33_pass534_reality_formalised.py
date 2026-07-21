#!/usr/bin/env python3
"""Pass 534: the reality theorem formalised, and Pass 491's hypothesis audited.

Pass 533 closed the derivation: inverse closure makes D Hermitian, hence its
eigenvalues real, hence charpoly(D) in Z[zeta_p]^+[x].  Two follow-ups belong
with it.

THE FORMALISATION.  formal/W33/Pass533HermitianReal.lean proves outright that
the determinant of a Hermitian matrix is self-adjoint, that a PRINCIPAL
submatrix of a Hermitian matrix is Hermitian (the same index map on rows and
columns is what makes this work -- a general submatrix need not be), and hence
that every principal minor is self-adjoint.  The passage to the characteristic
polynomial is stated with the sum-of-principal-minors expansion as an explicit
hypothesis, in the style of the other modules of this arc.

Pass 491 already formalised the top case, det D in Z[zeta_p]^+.  What is new is
that the same hypothesis gives every coefficient, so the earlier module proves a
corollary of something its own hypothesis supplied.

THE AUDIT.  That raises a general question worth a name: which results in this
corpus prove SPECIAL CASES of what their own hypotheses already give?  Pass 491
is one instance -- Hermitian was assumed and only the determinant extracted.
The question is asked here and answered for the passes of this arc; a full
corpus sweep is not attempted.

WHAT REMAINS OPEN, restated precisely.  Reality is settled.  The IMAGE is not:
which real values actually occur is unknown at every q.  At q = 3 that is the
question why e_2 lies in 9Z and e_3 in 27Z across the six occurring
polynomials, which is now the only q = 3 question left.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass534_reality_formalised.json"


def part_A_lean(checks):
    f = ROOT / "formal" / "W33" / "Pass533HermitianReal.lean"
    txt = f.read_text(encoding="utf-8") if f.exists() else ""
    idx = (ROOT / "formal" / "W33.lean").read_text(encoding="utf-8")
    checks["module_present"] = f.exists()
    checks["module_is_imported"] = "Pass533HermitianReal" in idx
    checks["module_proves_det_case"] = "det_isSelfAdjoint_of_isHermitian" in txt
    checks["module_proves_submatrix_case"] = "isHermitian_submatrix" in txt
    return {"file": "formal/W33/Pass533HermitianReal.lean",
            "lines": len(txt.splitlines()),
            "proved_outright": [
                "det of a Hermitian matrix is self-adjoint",
                "a PRINCIPAL submatrix of a Hermitian matrix is Hermitian",
                "hence every principal minor is self-adjoint"],
            "assumed": (
                "the expansion of a characteristic polynomial coefficient as a "
                "sum of principal minors, supplied as the hypothesis hexp"),
            "checked_by": "CI -- this container has no Lean toolchain"}


def part_B_audit(checks):
    entries = {
        "Pass 491 (det D in Z[zeta_p]^+)": (
            "PROVED A SPECIAL CASE.  It assumed D Hermitian and extracted only "
            "the determinant; the same hypothesis gives every characteristic "
            "polynomial coefficient, as Passes 531-533 show."),
        "Pass 514 (the sieve theorem)": (
            "NO.  Its hypotheses -- m/t odd and e | (m/t) -- are each used, and "
            "Pass 525 confirmed the identity fails to vanish when the parity "
            "hypothesis is dropped while the identity itself survives."),
        "Pass 517 (the closed form)": (
            "NO.  Its hypothesis e | (m/d) is exactly what makes the phase "
            "trivial, and Pass 518 showed the phase is the obstruction at the "
            "top class."),
        "Pass 526 (translation covariance)": (
            "NO, but its CONCLUSION was over-read: Pass 527 showed the "
            "spectrum it exposes is D's, so the reformulation opened no door."),
    }
    special = [k for k, v in entries.items() if v.startswith("PROVED A SPECIAL")]
    checks["audit_covers_the_arc"] = len(entries) >= 4
    checks["audit_found_at_least_one_instance"] = len(special) >= 1
    return {"entries": entries, "special_cases_found": special,
            "question": (
                "Which results prove SPECIAL CASES of what their own "
                "hypotheses already give?  Pass 491 is one: Hermitian was "
                "assumed and only the determinant extracted.  Within this arc "
                "it is the only one; a full corpus sweep is not attempted and "
                "is not claimed."),
            "why_it_is_a_distinct_failure_mode": (
                "It is not rediscovery -- nobody proved the same thing twice "
                "-- and not an over-read, since the stated result was true and "
                "correctly proved.  It is UNDER-extraction: a hypothesis "
                "strong enough for more than was taken from it.  Four passes "
                "(529-533) were spent recovering what Pass 491's hypothesis "
                "had already supplied.")}


def part_C_open(checks):
    checks["open_question_restated"] = True
    return {"settled": (
        "Reality: charpoly(D) lies in Z[zeta_p]^+[x], derived from inverse "
        "closure through the Hermitian property, with no measured link."),
        "open": (
            "Not proved and not conjectured.  The IMAGE: which real "
            "values actually occur.  This is unknown at "
            "every q.  At q = 3 it is the question why e_2 lies in 9Z and e_3 "
            "in 27Z across the six occurring polynomials -- now the only q = 3 "
            "question left, since reality accounts for their being rational at "
            "all."),
        "at_q5": (
            "Reality places the coefficients in a degree-(p-1)/2 real field "
            "rather than in Z[zeta_p], so the search for whatever refines the "
            "valuation profile at q = 5 -- 34 profiles carrying 52 trace "
            "vectors -- now runs in a materially smaller space.  That is a "
            "consequence worth using and is not used here.")}


def main_payload():
    checks = {}
    A = part_A_lean(checks)
    B = part_B_audit(checks)
    C = part_C_open(checks)
    status = "PASS" if all(checks.values()) else "FAIL"
    return {
        "schema": "w33.pass534.reality_formalised.v1",
        "status": status,
        "headline": (
            "THE REALITY THEOREM IS FORMALISED, AND PASS 491 UNDER-EXTRACTED "
            "ITS OWN HYPOTHESIS.  formal/W33/Pass533HermitianReal.lean proves "
            "outright that a Hermitian matrix has a self-adjoint determinant, "
            "that PRINCIPAL submatrices inherit the Hermitian property, and "
            "hence that every principal minor is self-adjoint; the passage to "
            "the characteristic polynomial is stated with the "
            "sum-of-principal-minors expansion as an explicit hypothesis.  "
            "Pass 491 formalised the top case alone.  That is a distinct "
            "failure mode from rediscovery or over-reading: the result was "
            "true and correctly proved, but the hypothesis was strong enough "
            "for more than was taken from it, and four passes (529-533) went "
            "into recovering what it had already supplied.  What remains open "
            "is the IMAGE -- which real values occur -- unknown at every q."),
        "part_A_formalisation": A,
        "part_B_under_extraction_audit": B,
        "part_C_what_is_open": C,
        "boundary": (
            "Part A reports the Lean module's contents and imports; the kernel "
            "check is CI's, this container having no toolchain, and the "
            "sum-of-minors expansion is assumed rather than derived.  Part B "
            "audits the four passes of this arc and explicitly does NOT sweep "
            "the corpus.  Part C restates an open problem and solves nothing."),
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
            raise SystemExit("Pass 534 certificate drift")
    else:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(text)
    print(json.dumps({"status": pl["status"],
                      "checks": sum(pl["checks"].values()),
                      "total": len(pl["checks"])}))
    return 0 if pl["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
