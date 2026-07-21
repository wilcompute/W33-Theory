#!/usr/bin/env python3
"""Pass 530: the q = 3 integrality of characteristic polynomials does NOT
generalise -- a certificate for a result that was otherwise a note.

Pass 529 found that all six characteristic polynomials occurring at q = 3 have
RATIONAL INTEGER coefficients, and lie on six lattice points of the family
x^3 - 9a x - 27b.  The obvious question is whether that is structural.  It is
not, and this pass certifies the negative rather than leaving it in a session
note.

MEASURED.  Over sampled sections at q = 5, the number whose characteristic
polynomial has all coefficients in Z -- rather than properly in Z[zeta_5] --
is ZERO.  A single section with a non-rational coefficient settles it, and
there are no exceptions in the sample.

WHY IT MATTERS.  This is the fourth q = 3 regularity in one week to fail at
q = 5:

  * Pass 524: the valuation profile is a complete invariant at q = 3, not at
    q = 5 (34 profiles carry 52 trace vectors).
  * Pass 528: the image of the section space in charpoly space is six points at
    q = 3, large at q = 5 (220 samples give over a hundred).
  * Pass 529 / here: coefficients are rational integers at q = 3, never in the
    q = 5 sample.
  * And Pass 519's original refutation, where the factorial law's agreement
    locus contained every case that was cheap to test.

The standing lesson is now specific rather than general: q = 3 is small enough
that almost everything looks finite, integral and rigid there, and none of it
should be assumed to transfer.  The section space at q = 3 has 81 elements; at
q = 5 it has 5^12.

WHAT THIS DOES NOT SAY.  Nothing here explains the q = 3 integrality, and
nothing rules out a weaker q = 5 statement -- coefficients in the real subring,
say, or integrality after a Galois average.  Only the literal generalisation is
refused.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass530_q5_nonintegrality.json"


def _load(name, fn):
    s = importlib.util.spec_from_file_location(name, ROOT / "analysis" / fn)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


P511 = _load("p511", "w33_pass511_constant_orbit_theorem.py")
P527 = _load("p527", "w33_pass527_spectrum_deflation.py")


def part_A_q5(checks):
    """How many q = 5 sections have rational-integer charpolys?"""
    rational, total, witness = 0, 0, None
    for s in range(40):
        R, C, q, D, dcoef, rho = P511.setup(5, 80000 + s)
        E = P527.epoly(C, D, q)
        is_rat = all(all(x.denominator == 1 for x in E[k])
                     and not any(E[k][1:]) for k in range(2, q + 1))
        total += 1
        if is_rat:
            rational += 1
        elif witness is None:
            k = next(k for k in range(2, q + 1) if any(E[k][1:]))
            witness = {"seed": 80000 + s, "coefficient": f"e_{k}",
                       "has_nonzero_zeta_component": True}
    checks["q5_sections_sampled"] = total == 40
    checks["no_q5_section_has_a_rational_charpoly"] = rational == 0
    checks["an_explicit_witness_was_recorded"] = witness is not None
    return {"sections": total, "with_rational_charpoly": rational,
            "first_witness": witness,
            "verdict": (
                "ZERO of 40 sampled sections at q = 5 have all characteristic "
                "polynomial coefficients in Z; every one has a coefficient "
                "properly in Z[zeta_5].  A single such section settles the "
                "question, and an explicit one is recorded.  The q = 3 "
                "integrality is therefore NOT structural.")}


def part_B_pattern(checks):
    entries = {
        "Pass 519": (
            "the factorial law's agreement locus contained every case that "
            "was cheap to test; refuted at q = 3 by exhaustion"),
        "Pass 524": (
            "the valuation profile is a complete invariant at q = 3 (4 "
            "profiles, 4 trace vectors) but not at q = 5 (34 profiles carry "
            "52 vectors)"),
        "Pass 528": (
            "the image of the section space in charpoly space is six points "
            "at q = 3 and large at q = 5 (220 samples give over a hundred)"),
        "Pass 530": (
            "coefficients are rational integers at q = 3 and never so in the "
            "q = 5 sample"),
    }
    checks["four_instances_recorded"] = len(entries) == 4
    return {"instances": entries,
            "lesson": (
                "A measured pattern, not a proved one: q = 3 is small enough that "
                "almost everything looks finite, "
                "integral and rigid there.  Its section space has 81 elements; "
                "at q = 5 it has 5^12.  Four regularities in one week have "
                "held at q = 3 and failed at q = 5, so the working rule is "
                "that nothing observed only at q = 3 transfers until tested."),
            "scope": (
                "No mechanism is proved here.  This does not explain the q = 3 "
                "integrality, and does not "
                "rule out a WEAKER q = 5 statement -- coefficients in the real "
                "subring, or integrality after a Galois average.  Only the "
                "literal generalisation is refused.")}


def main_payload():
    checks = {}
    A = part_A_q5(checks)
    B = part_B_pattern(checks)
    status = "PASS" if all(checks.values()) else "FAIL"
    return {
        "schema": "w33.pass530.q5_nonintegrality.v1",
        "status": status,
        "headline": (
            "THE q = 3 INTEGRALITY DOES NOT GENERALISE.  All six "
            "characteristic polynomials at q = 3 have rational integer "
            "coefficients (Pass 529); at q = 5, ZERO of 40 sampled sections "
            "do -- every one has a coefficient properly in Z[zeta_5], and an "
            "explicit witness is recorded.  This is the fourth q = 3 "
            "regularity in one week to fail at q = 5, after the profile "
            "invariant (Pass 524), the finiteness of the charpoly image "
            "(Pass 528), and the factorial law's agreement locus (Pass 519).  "
            "The working rule is that nothing observed only at q = 3 transfers "
            "until tested: its section space has 81 elements against 5^12."),
        "part_A_q5_measurement": A,
        "part_B_the_pattern": B,
        "boundary": (
            "Not proved, measured.  Part A samples 40 sections at q = 5.  The claim refused is "
            "universal, so a single counterexample suffices and one is "
            "exhibited by seed; "
            "the sample size is not load-bearing.  "
            "Part B is an editorial summary of four previously certified "
            "results.  Nothing here explains the q = 3 integrality or rules "
            "out a weaker q = 5 statement."),
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
            raise SystemExit("Pass 530 certificate drift")
    else:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(text)
    print(json.dumps({"status": pl["status"],
                      "checks": sum(pl["checks"].values()),
                      "total": len(pl["checks"])}))
    return 0 if pl["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
