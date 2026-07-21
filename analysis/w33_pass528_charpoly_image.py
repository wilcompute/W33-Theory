#!/usr/bin/env python3
"""Pass 528: the image of the section space in charpoly space -- six
polynomials at q = 3, all with rational integer coefficients.

Everything in this arc reduced to one question (Pass 527): given charpoly(D),
compute v_lambda(tr D^m).  The trace-valuation vector is a FUNCTION of
charpoly(D) -- verified on 160 distinct characteristic polynomials at q = 5,
none mapping to two vectors -- so the whole problem is the composite

        section  -->  charpoly(D)  -->  (v_lambda(tr D^m))_m .

This pass computes the first arrow exhaustively at q = 3.

THE IMAGE.  Across all 81 sections exactly SIX characteristic polynomials
occur, and every coefficient is a rational integer:

        x^3,  x^3 - 9x,  x^3 - 18x,  x^3 - 27x,
        x^3 - 27x - 27,  x^3 - 36x - 81,

with multiplicities 1, 8, 24, 8, 24, 16 summing to 81.  Their valuation
profiles (v(e_2), v(e_3)) are (inf,inf), (4,inf), (4,inf), (6,inf), (6,6),
(4,8) -- recovering the four non-degenerate profiles of Pass 521 with the
counts 32 = 8 + 24, 8, 24, 16 exactly.  So the profile is a coarsening that
merges x^3 - 9x with x^3 - 18x, and those two happen to share a trace vector.

WHAT THAT SETTLES.  Since every power trace is determined recursively by the
charpoly, only six recurrences occur at q = 3.  The derivations of Passes
521-523 account for their measured m = 2..12 window.  The all-m minimum is
therefore reduced to six cases.  This witness's finite table cannot close the
noncancellation step; Pass 541 later does so from recurrence states modulo 9.

WHY IT DOES NOT IMMEDIATELY GIVE q = 5.  There the section space has 5^12
elements and the image is not enumerable; 220 sampled sections already produce
160 distinct charpolys, so the image is large rather than small.  The q = 3
phenomenon -- a tiny image making the law finite -- is a small-q accident, of
the same kind Pass 524 found for the profile invariant.  Recorded as such
rather than extrapolated.
"""
from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass528_charpoly_image.json"
INF = 10**8


def _load(name, fn):
    s = importlib.util.spec_from_file_location(name, ROOT / "analysis" / fn)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


P487 = _load("p487", "w33_pass487_scope_of_the_law_and_det_hunt.py")
P489 = _load("p489", "w33_pass489_frobenius_generality.py")
P504 = _load("p504", "w33_pass504_trDq_fitting_and_noncommutative.py")
P511 = _load("p511", "w33_pass511_constant_orbit_theorem.py")

matmul, trace, det_exact = P487.matmul, P504.trace, P487.det_exact
Cyc, LF, Heis = P487.Cyc, P489.LocalFrobenius, P489.Heis


def part_A_image(checks):
    """Exhaustive image of the section space in charpoly space, q = 3."""
    p_ = 3
    R, C = LF(p_, 1), Cyc(p_, 1)
    H = Heis(R, C)
    q = H.q
    F = H.block(H.full_sec(tuple(R.zero for _ in H.pairs)))
    seen, nsec = {}, 0
    for offs in itertools.product(R.elems, repeat=len(H.pairs)):
        nsec += 1
        B = H.block(H.full_sec(offs))
        D = [[C.sub(B[i][j], F[i][j]) for j in range(q)] for i in range(q)]
        D2 = matmul(D, D, C)
        e2 = tuple(-x // 2 for x in trace(D2, C))
        e3 = det_exact(D, C)
        seen[(e2, e3)] = seen.get((e2, e3), 0) + 1
    rows, rational = {}, True
    for (e2, e3), cnt in sorted(seen.items(), key=lambda x: -x[1]):
        if any(e2[1:]) or any(e3[1:]):
            rational = False
        ve2 = INF if not any(e2) else C.vlam(e2)
        ve3 = INF if not any(e3) else C.vlam(e3)
        rows[f"x^3+({e2[0]})x-({e3[0]})"] = {
            "e2": e2[0],
            "e3": e3[0],
            "sections": cnt,
            "v_e2": None if ve2 >= INF else ve2,
            "v_e3": None if ve3 >= INF else ve3,
        }
    checks["section_space_enumerated"] = nsec == 81
    checks["exactly_six_charpolys_occur"] = len(seen) == 6
    checks["all_coefficients_are_rational_integers"] = rational
    checks["multiplicities_sum_to_81"] = sum(seen.values()) == 81
    return {
        "sections": nsec,
        "distinct_charpolys": len(seen),
        "rows": rows,
        "reading": (
            "Exactly six characteristic polynomials occur at q = 3, all "
            "with rational integer coefficients: x^3, x^3 - 9x, "
            "x^3 - 18x, x^3 - 27x, x^3 - 27x - 27, x^3 - 36x - 81, with "
            "multiplicities 1, 8, 24, 8, 24, 16.  Their valuation profiles "
            "recover the four non-degenerate profiles of Pass 521 with the "
            "counts 32 = 8 + 24, 8, 24, 16 -- so the profile invariant is "
            "a coarsening that merges x^3 - 9x with x^3 - 18x, and those "
            "two happen to share a trace vector."
        ),
    }


def part_B_lookup(checks):
    """Six charpolys reproduce the measured m = 2..12 q = 3 window."""
    p_ = 3
    R, C = LF(p_, 1), Cyc(p_, 1)
    H = Heis(R, C)
    q = H.q
    F = H.block(H.full_sec(tuple(R.zero for _ in H.pairs)))
    table, ok = {}, True
    for offs in itertools.product(R.elems, repeat=len(H.pairs)):
        B = H.block(H.full_sec(offs))
        D = [[C.sub(B[i][j], F[i][j]) for j in range(q)] for i in range(q)]
        D2 = matmul(D, D, C)
        e2 = tuple(-x // 2 for x in trace(D2, C))
        e3 = det_exact(D, C)
        Dm = [[C.rat(1) if i == j else C.zero() for j in range(q)] for i in range(q)]
        vec = []
        for m in range(1, 13):
            Dm = matmul(Dm, D, C)
            t = trace(Dm, C)
            vec.append(None if not any(t) else C.vlam(t))
        key = f"x^3+({e2[0]})x-({e3[0]})"
        if key in table and table[key] != vec:
            ok = False
        table[key] = vec
    # m = 1 is all-None: tr D = 0 for every section (e_1 = 0, Pass 473), so
    # that column has no finite entry to minimise over.
    mins = []
    for i in range(12):
        col = [v[i] for v in table.values() if v[i] is not None]
        mins.append(min(col) if col else None)
    fit = [2 * ((i + 1) + ((i + 1) % 2)) for i in range(12)]
    checks["charpoly_determines_the_trace_vector"] = ok
    checks["minimum_over_the_six_reproduces_measured_q3_window"] = mins[1:] == fit[1:]
    return {
        "table": table,
        "minimum_per_m": mins,
        "law_2m_plus_2odd": fit,
        "reading": (
            "Each of the six charpolys determines its trace vector, and "
            "the minimum over the six reproduces 2(m + [m odd]) for "
            "m = 2..12.  Thus the measured q = 3 window is a six-row "
            "table.  For all m these same polynomials give six exact "
            "recurrences.  This witness does not prove their all-m minimum; "
            "Pass 541 later closes it by exact modular recurrences."
        ),
    }


def part_C_no_extrapolation(checks):
    """The small image is a q = 3 accident."""
    seen = set()
    for s in range(220):
        R, C, q, D, dcoef, rho = P511.setup(5, 80000 + s)
        A = [[C.rat(1) if i == j else C.zero() for j in range(q)] for i in range(q)]
        tr = []
        for k in range(1, q + 1):
            A = matmul(A, D, C)
            tr.append(tuple(trace(A, C)))
        seen.add(tuple(tr))
    checks["q5_image_is_large"] = len(seen) > 100
    return {
        "q5_sections_sampled": 220,
        "distinct_charpoly_data": len(seen),
        "reading": (
            "At q = 5 the section space has 5^12 elements and 220 samples "
            "already give this many distinct characteristic polynomials, "
            "so the image is large rather than small.  The q = 3 "
            "phenomenon -- a tiny image making the law a finite table -- "
            "is a small-q accident, of the same kind Pass 524 found for "
            "the profile invariant.  It is recorded, not extrapolated."
        ),
    }


def main_payload():
    checks = {}
    A = part_A_image(checks)
    B = part_B_lookup(checks)
    Cc = part_C_no_extrapolation(checks)
    status = "PASS" if all(checks.values()) else "FAIL"
    return {
        "schema": "w33.pass528.charpoly_image.v1",
        "status": status,
        "headline": (
            "EXACTLY SIX CHARACTERISTIC POLYNOMIALS OCCUR AT q = 3, ALL WITH "
            "RATIONAL INTEGER COEFFICIENTS: x^3, x^3 - 9x, x^3 - 18x, "
            "x^3 - 27x, x^3 - 27x - 27, x^3 - 36x - 81, with multiplicities "
            "1, 8, 24, 8, 24, 16 over the complete 81-section space.  Since "
            "the trace-valuation vector is a function of charpoly(D) "
            "(Pass 527), the measured m = 2..12 q = 3 law is a six-row table, "
            "whose minimum reproduces 2(m + [m odd]) on that window.  The "
            "profile invariant of Pass 521 is the coarsening that merges "
            "x^3 - 9x with x^3 - 18x.  At q = 5 the image is large -- 220 "
            "samples give over a hundred distinct charpolys -- so the "
            "six-recurrence reduction is a small-q phenomenon.  This finite "
            "check is not promoted here; Pass 541 later supplies the all-m proof."
        ),
        "part_A_the_image": A,
        "part_B_six_row_lookup": B,
        "part_C_not_extrapolated": Cc,
        "boundary": (
            "Part A is exhaustive over the complete q = 3 section space.  "
            "Part B is exact only for m = 1..12; the six charpolys define "
            "all-m recurrences but do not themselves prove the all-m valuation "
            "minimum; Pass 541 later does.  Part C samples 220 sections at "
            "q = 5 and establishes only that the image is large, which is all "
            "that is needed to refuse the extrapolation.  Nothing here says "
            "what governs q = 5."
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
            raise SystemExit("Pass 528 certificate drift")
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
