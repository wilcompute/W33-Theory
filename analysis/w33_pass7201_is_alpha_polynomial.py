"""Pass 7201 -- is alpha(W(3,q)) a polynomial in q at all?

WHY THE QUESTION IS NOT IDLE. Everyone attacking this -- me included, this week -- reaches
for a closed form. But the best PUBLISHED construction for W(3,q), q an odd square with
p != 3 (Ceria-De Beule-Pavese-Smaldore 2022, Table 1), has size

    (q^{3/2} + 3q - q^{1/2} + 3) / 3

which is not a polynomial in q, and applies only on an arithmetic subfamily. If alpha itself
is not polynomial, then every closed form fitted to a handful of values is a coincidence, and
the failure of constructions to generalise is explained rather than merely lamented.

THE SHARP TENSION IN THE DATA. alpha = 7, 18, 33 at q = 3, 5, 7 is certain. At q=9 the value
is 51 or 52, and the two choices behave completely differently:

    52  ->  third difference 0 (exactly quadratic), AND the deficit from Tallini's
            q^2-q+1 is exactly C(q-2,2): 0, 3, 10, 21
    51  ->  third difference -1 (no quadratic), AND the deficit sequence 0, 3, 10, 22
            has second differences 4, 5 -- no clean form either

So 52 makes TWO independent framings clean at once and 51 makes both messy. Against that:
four independent LNS runs plateau at 51, and a certified basin of radius 9 excludes every
52-set that agrees with a known 51-set in 42 or more points.

This script states the tension exactly and computes what each hypothesis PREDICTS at q=11 and
q=13, where runs are in progress. It resolves nothing on its own and does not pretend to.

    py -3 analysis/w33_pass7201_is_alpha_polynomial.py
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

KNOWN = {3: 7, 5: 18, 7: 33}


def lagrange(pts, x):
    tot = Fraction(0)
    for i, (xi, yi) in enumerate(pts):
        term = Fraction(yi)
        for j, (xj, _) in enumerate(pts):
            if i != j:
                term *= Fraction(x - xj, xi - xj)
        tot += term
    return tot


def diffs(seq):
    out = [list(seq)]
    while len(out[-1]) > 1:
        cur = out[-1]
        out.append([cur[i + 1] - cur[i] for i in range(len(cur) - 1)])
    return out


def main() -> int:
    print("=" * 78)
    print("Pass 7201 -- is alpha(W(3,q)) polynomial in q?")
    print("=" * 78)

    for a9 in (51, 52):
        seq = [7, 18, 33, a9]
        d = diffs(seq)
        tall = [q * q - q + 1 for q in (3, 5, 7, 9)]
        defic = [t - a for t, a in zip(tall, seq)]
        dd = diffs(defic)
        print(f"\n  HYPOTHESIS alpha(W(3,9)) = {a9}\n")
        print(f"    alpha           {seq}")
        print(f"    1st differences {d[1]}")
        print(f"    2nd differences {d[2]}")
        print(f"    3rd difference  {d[3]}   "
              f"{'-> EXACTLY QUADRATIC' if d[3] == [0] else '-> not quadratic'}")
        print(f"    Tallini q^2-q+1 {tall}")
        print(f"    deficit         {defic}")
        print(f"    deficit 2nd dif {dd[2]}   "
              f"{'-> deficit is C(q-2,2)' if dd[2] == [4, 4] else '-> no clean deficit form'}")
        pts = list(zip((3, 5, 7, 9), seq))
        p11, p13 = lagrange(pts, 11), lagrange(pts, 13)
        print(f"    cubic through all four predicts:  q=11 -> {p11}   q=13 -> {p13}")

    print("\n  WHAT THE TWO HYPOTHESES PREDICT, side by side\n")
    print(f"    {'model':34s} {'q=9':>6s} {'q=11':>7s} {'q=13':>7s}")
    quad = lambda q: (q + 4) * (q - 1) // 2
    print(f"    {'(q+4)(q-1)/2  [needs alpha(9)=52]':34s} "
          f"{quad(9):6d} {quad(11):7d} {quad(13):7d}")
    c51 = list(zip((3, 5, 7, 9), [7, 18, 33, 51]))
    print(f"    {'cubic through 7,18,33,51':34s} {51:6d} "
          f"{str(lagrange(c51, 11)):>7s} {str(lagrange(c51, 13)):>7s}")
    print(f"    {'Tallini upper bound q^2-q+1':34s} {73:6d} {111:7d} {157:7d}")

    print("""
  THE NON-POLYNOMIAL POSSIBILITY, which nothing here rules out. The published
  construction for this family is (q^{3/2}+3q-q^{1/2}+3)/3 and carries a q^{1/2}, so the
  natural closed forms in this area are NOT polynomial. And they are arithmetic-conditional:
  that construction requires q an odd square with p != 3, which is exactly why q=9 = 3^2 is
  EXCLUDED from it and why the published lower bound at q=9 is only 2q+1 = 19.

  IF alpha DEPENDS ON THE ARITHMETIC OF q -- q mod 3, q a square, q prime -- then fitting a
  polynomial through q = 3, 5, 7, 9 mixes incompatible cases and every such fit, including
  mine from earlier this week, is meaningless. q=11 (prime, non-square) and q=13 (prime,
  non-square) are being computed and will discriminate: both are the SAME arithmetic type as
  5, 7 and 11, whereas 9 is the odd one out as the only square in the list.

  THAT LAST OBSERVATION IS THE USEFUL ONE. q = 3, 5, 7, 11, 13 are prime; q = 9 is not. If
  alpha is arithmetic-conditional, q=9 is precisely the value one should NOT use to fit a
  formula -- and it is the only value I used that is not certain.""")

    out = {
        "boundary": ("this pass RESOLVES NOTHING. It states the 51-vs-52 tension exactly and "
                     "records what each hypothesis predicts at q=11 and q=13. The "
                     "non-polynomial possibility is not ruled out and no formula is asserted"),
        "certain_values": KNOWN,
        "uncertain": {"q": 9, "candidates": [51, 52],
                      "evidence_for_51": ["four independent LNS plateaus",
                                          "certified basin radius 9"],
                      "evidence_for_52": ["makes the sequence exactly quadratic",
                                          "makes the Tallini deficit exactly C(q-2,2)"]},
        "hypotheses": {
            "alpha9_52": {"third_difference": 0, "deficit": [0, 3, 10, 21],
                          "deficit_form": "C(q-2,2)",
                          "predicts": {"q=11": 75, "q=13": 102}},
            "alpha9_51": {"third_difference": -1, "deficit": [0, 3, 10, 22],
                          "deficit_form": "none clean",
                          "predicts": {"q=11": str(lagrange(c51, 11)),
                                       "q=13": str(lagrange(c51, 13))}}},
        "non_polynomial_possibility": {
            "published_construction": "(q^{3/2}+3q-q^{1/2}+3)/3, carries q^{1/2}",
            "arithmetic_condition": "requires q odd square with p != 3",
            "consequence_for_q9": ("q=9=3^2 is EXCLUDED, which is why the published lower "
                                   "bound at q=9 is only 2q+1 = 19"),
            "the_useful_observation": ("q = 3,5,7,11,13 are prime and q=9 is not; if alpha is "
                                       "arithmetic-conditional then q=9 is exactly the value "
                                       "one should not fit a formula through -- and it is the "
                                       "only uncertain one")},
        "not_done": ["alpha(W(3,9))", "alpha(W(3,11))", "alpha(W(3,13))",
                     "any proof that alpha is or is not polynomial"],
    }
    fp = ROOT / "data" / "PART_W33_PASS7201_IS_ALPHA_POLYNOMIAL.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
