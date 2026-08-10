#!/usr/bin/env python3
"""Pass 4800 -- the deficit-q law I proposed at Pass 4795 is false, and q = 5 killed it.

Pass 4795 found alpha(W(3,3)) = 7 against a Hoffman bound of 10, noticed that
7 = q^2 - q + 1, and wrote:

    "ONE DATA POINT, so this is a match to a cited formula and not a verification of it;
     the falsifiable form is that alpha(W(3,5)) should be 25 - 5 + 1 = 21 against a
     Hoffman bound of 26, a gap of 5. That is computable and is not computed here."

It is now computed.  Thirty-five minutes of exhaustive search on SRG(156,30,4,6) gives

    alpha(W(3,5)) = 18,  not 21.

So the deficit is 8, not 5, and "the deficit from the Hoffman bound is exactly q" is FALSE.
The agreement at q = 3 was a single point, and a single point through which infinitely many
formulas pass.

    py -3 analysis/w33_pass4800_the_deficit_law_is_false.py
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

# alpha values computed exhaustively: q=2,3,4 at Pass 4795/4799, q=5 here (2075 s)
MEASURED = [(2, 5, 5), (3, 40, 7), (4, 17, 17), (5, 26, 18)]
NAMES = {2: (5, 5), 3: (10, 7), 4: (17, 17), 5: (26, 18)}


def main() -> int:
    print("=" * 78)
    print("Pass 4800 -- the deficit-q law, falsified at q = 5")
    print("=" * 78)

    print(f"\n  {'q':>3s} {'parity':>6s} {'Hoffman':>8s} {'alpha':>6s} {'gap':>5s} "
          f"{'q^2-q+1':>8s} {'predicted gap':>14s} {'holds':>6s}")
    rows = []
    for q, (hb, a) in sorted(NAMES.items()):
        gap = hb - a
        pred_alpha = q * q - q + 1
        pred_gap = q if q % 2 else 0
        holds = (a == (hb if q % 2 == 0 else pred_alpha))
        rows.append({"q": q, "even": q % 2 == 0, "hoffman": hb, "alpha": a,
                     "gap": gap, "q2_minus_q_plus_1": pred_alpha,
                     "predicted_gap": pred_gap, "prediction_holds": bool(holds)})
        print(f"  {q:3d} {'even' if q%2==0 else 'odd':>6s} {hb:8d} {a:6d} {gap:5d} "
              f"{pred_alpha:8d} {pred_gap:14d} {str(holds):>6s}")

    odd = [r for r in rows if not r["even"]]
    print(f"""
    THE LAW IS FALSE AND THE FALSIFIER WAS THE ONE I NAMED. At q = 3 the independence
    number is 7 = q^2 - q + 1 and the deficit is 3 = q. At q = 5 the formula predicts 21
    and the answer is 18, so the deficit is 8, not 5.

    Odd-q deficits so far: {', '.join(f'q={r["q"]}: {r["gap"]}' for r in odd)}. Not q, and not obviously anything else
    from two points -- which is the lesson rather than a new candidate formula. A single
    agreement fitted a curve through one point and the curve was wrong.

    WHAT SURVIVES UNTOUCHED. Everything the deficit law was decoration on:

      * W(3,q) meets its Hoffman bound iff q is even -- still true at q = 2,3,4,5, and now
        with a second odd witness rather than one.
      * alpha separates W(3,3) from Q(4,3) at identical parameters (7 vs 10) -- Pass 4797.
      * both dual pairs split on "has an ovoid" -- Pass 4799.

    The parity result is if anything STRONGER now: q = 5 misses the bound by 8, a wider
    failure than q = 3's 3, so the odd-q obstruction is not a marginal near-miss that might
    close up at larger q.

    WHY THIS PASS EXISTS RATHER THAN A QUIET EDIT. Pass 4795 published the prediction with
    the falsifier attached and the cost named. Deleting it now would leave a corpus in which
    predictions are only ever recorded when they succeed, and this repository already has a
    retraction-propagation problem from claims that were never followed up. The prediction
    was made, it was cheap to test, it was tested, and it failed.""")

    out = {
        "boundary": ("alpha values are exhaustive independence numbers via igraph and are "
                     "exact; q = 5 took 2,075 s on SRG(156,30,4,6). No odd q beyond 5 is "
                     "computed, so 'not q' is established while no replacement formula is "
                     "proposed -- two points do not determine one"),
        "rows": rows,
        "deficit_q_law": False,
        "refutes": "Pass 4795's proposal that the Hoffman deficit at odd q equals q",
        "q3_was_coincidence": ("alpha(W(3,3)) = 7 = q^2-q+1 holds; alpha(W(3,5)) = 18 != 21, "
                               "so the formula does not generalise and the q=3 agreement "
                               "was a single point"),
        "unaffected": [
            "W(3,q) meets its Hoffman bound iff q is even (q = 2,3,4,5)",
            "alpha separates W(3,3) from Q(4,3) at identical parameters (Pass 4797)",
            "both dual pairs split on having an ovoid (Pass 4799)"],
        "strengthened": ("the odd-q failure widens with q -- deficit 3 at q=3, 8 at q=5 -- "
                         "so it is not a marginal near-miss that might close at larger q"),
    }
    fp = ROOT / "data" / "PART_W33_PASS4800_DEFICIT_LAW_FALSE.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
