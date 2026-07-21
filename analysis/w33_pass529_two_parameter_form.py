#!/usr/bin/env python3
"""Pass 529: the six q = 3 characteristic polynomials are one two-parameter
family, and the arc's closing statement.

Pass 528 found that the 81 sections at q = 3 map onto exactly six
characteristic polynomials, all with rational integer coefficients.  They are
not six unrelated polynomials.

THE TWO-PARAMETER FORM.  Every one of them is

        x^3 - 9a x - 27b ,      (a, b) integers,

with (a,b) running over exactly {(0,0), (1,0), (2,0), (3,0), (3,1), (4,3)} and
multiplicities 1, 8, 24, 8, 24, 16.  So the image of the section space in
charpoly space is six lattice points, not six arbitrary polynomials: e_2 lies
in 9Z and e_3 in 27Z.  The measured q = 3 window is indexed by this pair of
small integers, while the all-m problem is reduced to their six recurrences.

THE DISCRIMINANTS.  For x^3 + px + q the discriminant is -4p^3 - 27q^2, which
here is 729(4a^3 - 27b^2) -- and 4a^3 - 27b^2 is, up to sign, the discriminant
of the reduced cubic x^3 - a x - b.  Its values across the six are
0, 4, 32, 108, 81, 13.  The last is prime and the family is not obviously
closed under anything; no pattern is asserted.

WHAT IS NOT DONE.  Why e_2 lies in 9Z and e_3 in 27Z is not proved here, only
observed exhaustively; the natural guess is that inverse closure plus the
Galois action forces rationality and the powers of 3 come from the ramification,
but that is a guess and this programme has retracted three of those in a week.
Whether the q = 5 image is small once quotiented by Sp(2,F_5) is untested.

THE CLOSING STATEMENT.  With Pass 527's deflation and Pass 528's image, the
whole arc reduces to one question -- given charpoly(D), compute
v_lambda(sum_j nu_j^m).  At q = 3 six lattice points reduce it to six exact
recurrences, but their all-m valuation minimum is still open; at q >= 5 even
the image is large and coefficient valuations do not suffice.  That is the
sentence the paper should end on, and this pass puts it there.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass529_two_parameter_form.json"

SIX = [
    ((0, 0), 1),
    ((-9, 0), 8),
    ((-18, 0), 24),
    ((-27, 0), 8),
    ((-27, 27), 24),
    ((-36, 81), 16),
]


def part_A_family(checks):
    rows, ok = {}, True
    ab = []
    for (e2, e3), mult in SIX:
        if e2 % 9 or e3 % 27:
            ok = False
            continue
        a, b = -e2 // 9, e3 // 27
        ab.append((a, b))
        disc = -4 * e2**3 - 27 * e3**2
        rows[f"x^3{e2:+d}x{-e3:+d}"] = {
            "e2": e2,
            "e3": e3,
            "sections": mult,
            "a": a,
            "b": b,
            "discriminant": disc,
            "disc_over_729": disc // 729,
            "four_a_cubed_minus_27_b_squared": 4 * a**3 - 27 * b**2,
        }
    checks["all_six_have_the_two_parameter_form"] = ok
    checks["e2_in_9Z_and_e3_in_27Z"] = all(
        e2 % 9 == 0 and e3 % 27 == 0 for (e2, e3), _ in SIX
    )
    checks["multiplicities_sum_to_81"] = sum(m for _, m in SIX) == 81
    checks["disc_is_729_times_4a3_minus_27b2"] = all(
        r["discriminant"] == 729 * r["four_a_cubed_minus_27_b_squared"]
        for r in rows.values()
    )
    return {
        "rows": rows,
        "ab_pairs": sorted(ab),
        "form": "x^3 - 9a x - 27b",
        "reading": (
            "The image of the section space in charpoly space is six "
            "LATTICE POINTS, not six arbitrary polynomials: e_2 lies in "
            "9Z and e_3 in 27Z.  They index the measured q = 3 window and "
            "reduce the all-m problem to six recurrences.  The discriminant "
            "is 729(4a^3 - 27b^2), "
            "and 4a^3 - 27b^2 is up to sign the discriminant of the "
            "reduced cubic x^3 - a x - b; its six values are 0, 4, 32, "
            "108, 81, 13.  The last is prime and no pattern is asserted."
        ),
        "not_proved": (
            "Why e_2 lies in 9Z and e_3 in 27Z is OBSERVED exhaustively, "
            "not proved.  The natural guess -- inverse closure plus the "
            "Galois action forcing rationality, with the powers of 3 from "
            "the ramification -- is a guess, and this programme has "
            "retracted three of those in a week."
        ),
    }


def part_B_closing(checks):
    tex = (ROOT / "papers" / "heisenberg_weyl_determinant_law.tex").read_text(
        encoding="utf-8", errors="ignore"
    )
    checks["closing_section_present"] = "sec:closing" in tex
    checks["closing_states_the_localization"] = "charpoly" in tex.lower()
    return {
        "statement": (
            "Given charpoly(D), compute v_lambda(sum_j nu_j^m).  At q = 3 six "
            "lattice points (a,b) in {(0,0),(1,0),(2,0),(3,0),(3,1),(4,3)} under "
            "x^3 - 9a x - 27b reduce the problem to six recurrences; the all-m "
            "valuation minimum remains open.  At q >= 5, coefficient "
            "valuations demonstrably do not suffice -- 34 valuation profiles carry "
            "52 distinct trace vectors."
        ),
        "why_it_is_the_right_ending": (
            "Passes 510-528 produced an orbit decomposition, a sieve, a closed "
            "form, a transfer matrix and a covariance theorem.  Pass 527 "
            "showed the transfer matrix carries exactly the information the "
            "block already carried, and Pass 528 showed the orbit machinery "
            "computes a six-row table.  What survives as a QUESTION is one "
            "sentence, and a reader is better served by it than by the "
            "machinery that led there."
        ),
    }


def main_payload():
    checks = {}
    A = part_A_family(checks)
    B = part_B_closing(checks)
    status = "PASS" if all(checks.values()) else "FAIL"
    return {
        "schema": "w33.pass529.two_parameter_form.v1",
        "status": status,
        "headline": (
            "THE SIX q = 3 CHARACTERISTIC POLYNOMIALS ARE ONE TWO-PARAMETER "
            "FAMILY: x^3 - 9a x - 27b with (a,b) in {(0,0), (1,0), (2,0), "
            "(3,0), (3,1), (4,3)} and multiplicities 1, 8, 24, 8, 24, 16.  So "
            "the image of the section space in charpoly space is six lattice "
            "points -- e_2 in 9Z, e_3 in 27Z -- indexing the measured q = 3 "
            "window and reducing the all-m problem to six recurrences.  The "
            "discriminant is "
            "729(4a^3 - 27b^2), with 4a^3 - 27b^2 taking the values 0, 4, 32, "
            "108, 81, 13.  Why the coefficients are so constrained is observed "
            "exhaustively, NOT proved."
        ),
        "part_A_two_parameter_family": A,
        "part_B_closing_statement": B,
        "boundary": (
            "Part A is arithmetic on the six polynomials Pass 528 proved "
            "exhaustively; it adds a parametrisation and asserts no mechanism "
            "for it.  Part B checks that the paper carries the closing "
            "statement and is otherwise editorial."
        ),
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
            raise SystemExit("Pass 529 certificate drift")
    else:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(text)
    print(
        json.dumps(
            {
                "status": pl["status"],
                "checks": sum(pl["checks"].values()),
                "total": len(pl["checks"]),
            }
        )
    )
    return 0 if pl["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
