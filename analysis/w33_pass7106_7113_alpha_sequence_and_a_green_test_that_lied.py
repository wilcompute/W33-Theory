"""Passes 7106-7113 -- the alpha(W(3,q)) sequence, a literature check, and a green test
that certified a false theorem in its own name.

  7106  alpha(W(3,3)) = 7 and alpha(W(3,5)) = 18, exact, three independent ways.
  7107  The literature check BEFORE claiming: both are published.  So is q=7.
  7108  Tallini's bound q^2-q+1, and where it is and is not attained.
  7109  The interpolation (q+4)(q-1)/2 -- what it is, and what it is NOT.
  7110  Why my alpha(W(3,7)) job was rediscovery, and why I let it run anyway.
  7111  The corpus contradiction: five different values for one integer.
  7112  A PASSING TEST NAMED FOR A FALSE THEOREM.
  7113  Scope.

    py -3 analysis/w33_pass7106_7113_alpha_sequence_and_a_green_test_that_lied.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# q -> (points, q^2+1, Tallini q^2-q+1, alpha, provenance)
TABLE = [
    (2, 15, 5, None, 5, "ovoid exists (q even); alpha = q^2+1"),
    (3, 40, 10, 7, 7, "computed here, exact, three ways"),
    (5, 156, 26, 21, 18, "computed here; MATCHES Cimrakova-Fack 2005 Table 1"),
    (7, 400, 50, 43, 33, "Cimrakova-Fack 2005 Table 1, unique up to equivalence"),
]


def main() -> int:
    print("=" * 78)
    print("Passes 7106-7113 -- alpha(W(3,q)), the literature, and a lying green test")
    print("=" * 78)

    print("\n  PASS 7106-7108 -- the sequence, with provenance on every row\n")
    print(f"    {'q':>2s} {'points':>7s} {'q^2+1':>6s} {'Tallini':>8s} {'alpha':>6s}  provenance")
    for q, pts, ov, tal, a, prov in TABLE:
        t = "-" if tal is None else str(tal)
        print(f"    {q:2d} {pts:7d} {ov:6d} {t:>8s} {a:6d}  {prov}")
    print("""
    alpha(W(3,3)) = 7 IS ESTABLISHED THREE INDEPENDENT WAYS: an ILP witness of size 7
    verified pairwise non-collinear by hand; the ILP forced to size 8 returning INFEASIBLE;
    and an exhaustive branch-and-bound over all forty points, now running inside the test
    suite. alpha(W(3,5)) = 18 is established two ways here.

    TALLINI'S BOUND is |O'| <= q^2 + 1 - q for q odd. It is ATTAINED at q = 3 (7 = 7) and
    MISSED at q = 5 (18 < 21) and q = 7 (33 < 43), with the gap widening. The Hoffman ratio
    bound q^2+1 is attained only for q EVEN, where ovoids exist -- W(3,q) has no ovoid for
    q odd (Thas), which is exactly why the odd rows fall short.""")

    print("\n  PASS 7107, 7110 -- the literature check, run BEFORE the claim\n")
    print("""    I COMPUTED alpha(W(3,5)) = 18 AND THEN WENT LOOKING FOR IT. Cimrakova and Fack,
    "Searching for maximal partial ovoids and spreads in generalized quadrangles", Bull.
    Belg. Math. Soc. 12 (2005) 697-705, Table 1, gives exactly:

        W(5):  156 points, bound 21, largest partial ovoid 18, two inequivalent
        W(7):  400 points, bound 43, largest partial ovoid 33, ONE up to equivalence

    So 18 is a confirmation, not a discovery -- and my background job computing q=7 is
    recomputing a value published twenty-one years ago. That is this repo's failure mode
    five, rediscovery, and the only reason it did not become a claim is that the search for
    the RESULT happened before the write-up rather than after.

    I LET THE q=7 JOB RUN ANYWAY, for a reason that is not sentiment: 33 is now a POSITIVE
    CONTROL. If my pipeline returns 33 it is validated on a case with a published answer,
    which is what earns the right to believe it at q=9 where there is no published answer.""")

    print("\n  PASS 7109 -- the interpolation, stated as an interpolation\n")
    for q in (3, 5, 7, 9, 11):
        print(f"    q={q:2d}:  (q+4)(q-1)/2 = {(q + 4) * (q - 1) // 2:3d}"
              f"     Tallini = {q * q - q + 1:3d}")
    print("""
    (q+4)(q-1)/2 REPRODUCES 7, 18 AND 33 EXACTLY. It also has three free coefficients
    fitted to three data points, so it has ZERO degrees of freedom and is not evidence of
    anything whatsoever. Any quadratic through three points does this; the content is not
    that it fits, it is that it PREDICTS 52 at q=9 where this repo's local searches
    plateau at 51.

    THAT IS THE ONLY REASON TO WRITE IT DOWN: it is falsifiable next week rather than
    decorative. A 52-point partial ovoid confirms it and beats the repo's best; a proof
    that 51 is optimal kills it. Both outcomes are worth more than another search
    returning 51.""")

    print("\n  PASS 7111 -- five values for one integer\n")
    print(f"    {'asserted':>10s}  where")
    for val, where in (
            ("7", "all of analysis/ -- correct"),
            ("10", "exploration/PART_CCCLI, tests/, manuscripts/parts/ -- the Hoffman "
                   "BOUND mistaken for the value"),
            ("4", "PART_CCCXIII_LOVASZ_THETA_BRIDGE.md -- a greedy result taken as maximum"),
            ("<= 40", "trivially true, harmless"),
            ("< 10", "true, and the sharp statement given q odd")):
        print(f"    {val:>10s}  {where}")
    print("""
    THE VALUE 10 IS THE INTERESTING ERROR. It is q^2+1, the ovoid size and the Hoffman
    bound -- so every file asserting it is implicitly asserting that W(3,3) HAS an ovoid,
    which Thas ruled out. One file, exploration/w33_ovoid_spread_bridge.py, had already
    caught and retracted exactly this. The others had not.""")

    print("\n  PASS 7112 -- the green test that certified a false theorem\n")
    print("""    tests/test_extremal_combinatorics_computation.py contained:

        def test_independence_number_equals_10(self, basic_counts):
            \"\"\"alpha(W(3,3)) = 10 exactly. ...
            An ovoid ... provides alpha >= 10.\"\"\"
            ...
            # Greedy finds at least 7; Hoffman bound proves alpha <= 10
            assert len(ovoid) >= 7

    THE NAME AND DOCSTRING ASSERT 10. THE BODY ASSERTS 7. It passed for as long as it
    existed, because the only executable claim in it is true and the false claim is in the
    part Python does not run.

    THIS IS WHERE THE CORPUS'S 10 CAME FROM. A test name is the most citable thing in a
    repository -- it is what a grep returns and it carries the authority of a green suite.
    Every checkable guard in this repo would pass this file: the arithmetic is sound, the
    scope matches the evidence, nothing is rediscovered, and the assertion is correct. Only
    reading the sentence against the assertion catches it.

    NOW FIXED: renamed to test_independence_number_equals_7, docstring corrected with the
    reason the bound is not attained, and the body replaced by an exhaustive branch-and-
    bound asserting best == 7 and best < 10. It passes.

    THE GENERAL LESSON, and it is a new failure mode for CLAUDE.md: A TEST'S NAME IS AN
    UNTESTED ASSERTION. Everything else in a test file is executed and therefore checked;
    the name and the docstring are the only parts that can be false while the suite is
    green, and they are exactly the parts that get cited.""")

    print("\n  PASS 7113 -- scope\n")
    print("""    ESTABLISHED: alpha(W(3,3)) = 7 and alpha(W(3,5)) = 18, exactly, and 18 agrees
    with the published value. NOT NEW: both, plus q=7 = 33, are in Cimrakova-Fack 2005.
    FIXED: three files and one test that asserted 10 or 4.

    NOT ESTABLISHED: that (q+4)(q-1)/2 is anything but an interpolation. NOT DONE:
    alpha(W(3,9)), where the prediction is 52 and the repo's searches reach 51 -- running,
    no result claimed either way.""")

    out = {
        "boundary": (
            "alpha(W(3,3)) = 7 and alpha(W(3,5)) = 18 are EXACT and verified multiple ways; "
            "both, and alpha(W(3,7)) = 33, are PUBLISHED (Cimrakova-Fack 2005 Table 1) and "
            "are therefore confirmations, not discoveries. The closed form (q+4)(q-1)/2 is "
            "an interpolation through three points with zero degrees of freedom and is NOT "
            "evidence; its only value is the falsifiable prediction 52 at q=9. No claim is "
            "made about alpha(W(3,9))"),
        "pass_7106_7108": {
            "table": [{"q": q, "points": pts, "hoffman_q2_plus_1": ov,
                       "tallini_q2_minus_q_plus_1": tal, "alpha": a, "provenance": prov}
                      for q, pts, ov, tal, a, prov in TABLE],
            "alpha_w33_verified_three_ways": [
                "ILP witness of size 7, pairwise non-collinearity checked directly",
                "ILP forced to size 8 returns INFEASIBLE",
                "exhaustive branch and bound over all 40 points, in the test suite"],
            "tallini_attained_at": [3], "tallini_missed_at": [5, 7],
            "why_hoffman_missed_for_odd_q": "W(3,q) has no ovoid for q odd (Thas)"},
        "pass_7107_7110": {
            "citation": ("M. Cimrakova and V. Fack, Searching for maximal partial ovoids "
                         "and spreads in generalized quadrangles, Bull. Belg. Math. Soc. "
                         "Simon Stevin 12 (2005) 697-705, Table 1"),
            "published_values": {"W(5)": 18, "W(7)": 33},
            "inequivalent_optima": {"W(5)": 2, "W(7)": 1},
            "status_of_my_q7_job": "REDISCOVERY, repurposed as a positive control",
            "why_it_was_caught": "the search for the result preceded the write-up"},
        "pass_7109": {
            "interpolation": "(q+4)(q-1)/2",
            "reproduces": {"3": 7, "5": 18, "7": 33},
            "degrees_of_freedom": 0,
            "evidential_status": "NONE -- three coefficients fitted to three points",
            "sole_value": "the falsifiable prediction alpha(W(3,9)) = 52",
            "repo_local_search_plateau_at_q9": 51},
        "pass_7111_7112": {
            "corpus_values_found": {"7": "correct", "10": "Hoffman bound as value",
                                    "4": "greedy result as maximum"},
            "why_10_is_the_serious_one": (
                "10 = q^2+1 is the ovoid size, so asserting it asserts an ovoid exists, "
                "which Thas ruled out for q odd"),
            "the_green_test": {
                "file": "tests/test_extremal_combinatorics_computation.py",
                "was": "test_independence_number_equals_10, body asserting len(ovoid) >= 7",
                "why_it_passed": "the false claim lived in the name and docstring, which "
                                 "Python does not execute",
                "now": "test_independence_number_equals_7, exhaustive branch and bound "
                       "asserting best == 7 and best < 10",
                "new_failure_mode": ("A TEST'S NAME IS AN UNTESTED ASSERTION -- the name "
                                     "and docstring are the only parts of a test that can "
                                     "be false while the suite is green, and they are the "
                                     "parts that get cited")},
        },
        "pass_7113": {"not_done": ["alpha(W(3,9)) -- running, prediction 52, plateau 51",
                                   "any proof that (q+4)(q-1)/2 is more than a fit"]},
    }
    fp = ROOT / "data" / "PART_W33_PASS7106_7113_ALPHA_SEQUENCE.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
