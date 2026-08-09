#!/usr/bin/env python3
"""Passes 4419-4420 -- the look-elsewhere audit applied to the whole board, and F7.

Pass 4411b measured how crowded the neutrino window was: of 372 integers reachable by
simple expressions in this geometry's standard constants, 55 landed inside the 59-120 meV
window the prediction had to hit.  That made "101 = Phi_4^2 + 1" uninformative at the
precision the scoreboard claimed.

The obvious follow-up is that the SAME test applies to every integer-valued row, and it is
a much sharper instrument than re-checking bounds one at a time -- a bound check asks
whether a prediction is still alive, while this asks whether it ever said anything.

  4419  The audit, row by row.  For each prediction: how many comparably simple expressions
        land inside the window that prediction had to hit?  A row where the answer is 1 is
        a real prediction.  A row where it is 50 is a coincidence with good marketing.

  4420  F7 in detail, because Pass 4412 identified it as the tightest live tension and it
        is the row where the look-elsewhere count is smallest.

    py -3 analysis/w33_pass4419_4420_look_elsewhere_board.py
"""

from __future__ import annotations

import itertools
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402

CONSTANTS = {"q": 3, "v": 40, "k": 12, "lambda": 2, "mu": 4, "Phi_3": 13, "Phi_4": 10,
             "Phi_6": 7, "f": 24, "g": 15, "27": 27, "36": 36, "45": 45, "81": 81,
             "160": 160, "51840": 51840, "25920": 25920, "240": 240, "120": 120}


def reachable(limit: int) -> dict[int, tuple[int, str]]:
    """Integer -> (minimum cost, cheapest expression) over a closed, cost-ranked grammar.

    THE FIRST VERSION OF THIS FUNCTION WAS SATURATED AND THEREFORE VACUOUS.  It asked only
    "is this integer reachable", with 19 constants and 18 operation forms, and reached 72 of
    the 87 integers in the Higgs window -- 83%.  A test that hits five sixths of every window
    cannot rank anything, and worse, it did not reach 125 at all, because the prediction's
    own expression (mu+1)^q needs the DERIVED constant 5 = mu + 1 which the flat grammar
    never built.  Failing to reach the very number under audit is the clearest possible
    signal that the instrument was wrong.

    Cost is the number of constant tokens plus the number of operations, so a cheaper
    expression is a shorter description.  Grammar is applied twice, so derived constants
    like mu + 1 are available to later steps at their own cost -- which is what makes the
    prediction expressible and the comparison fair.
    """
    base = {v: (1, k) for k, v in
            sorted(CONSTANTS.items(), key=lambda kv: kv[1])}
    seen: dict[int, tuple[int, str]] = dict(base)
    for _round in range(2):
        cur = list(seen.items())
        for a, (ca, fa) in cur:
            for form, val, extra in ((f"{fa}^2", a * a, 1), (f"{fa}^3", a ** 3, 1),
                                     (f"2*{fa}", 2 * a, 1), (f"3*{fa}", 3 * a, 1),
                                     (f"{fa}+1", a + 1, 1), (f"{fa}-1", a - 1, 1)):
                if 0 < val <= limit and (val not in seen or seen[val][0] > ca + extra):
                    seen[val] = (ca + extra, form)
        cur = list(seen.items())
        for (a, (ca, fa)), (b, (cb, fb)) in itertools.permutations(cur, 2):
            if ca + cb + 1 > 5:
                continue
            for form, val in ((f"{fa}+{fb}", a + b), (f"{fa}-{fb}", a - b),
                              (f"{fa}*{fb}", a * b)):
                if 0 < val <= limit and (val not in seen or seen[val][0] > ca + cb + 1):
                    seen[val] = (ca + cb + 1, form)
    return seen


# (row, quantity, predicted, window the prediction had to hit, why that window, unit)
ROWS = [
    ("F7", "Higgs mass", 125, (114, 200),
     "LEP direct limit below, perturbative-unitarity above", "GeV"),
    ("F16", "Sigma m_nu", 101, (59, 120),
     "normal-ordering oscillation floor below, Planck 2018 above", "meV"),
    ("F10", "WIMP mass", 2143, (10, 100000),
     "the mass range direct detection was ever sensitive to", "GeV"),
    ("F12", "heavy scalar", 3215, (1500, 10000),
     "LHC exclusion below, FCC reach above", "GeV"),
]


def main() -> int:
    print("=" * 78)
    print("Passes 4419-4420 -- how much did each row ever say?")
    print("=" * 78)

    ex = reachable(200000)
    print(f"\n  integers with a cost-ranked expression: {len(ex)}\n")
    print(f"  {'row':5s} {'quantity':14s} {'pred':>6s} {'cheapest form':>16s} {'cost':>5s} "
          f"{'saturation':>11s} {'cheaper in window':>18s}  verdict")
    rows_out = []
    for tag, name, pred, (lo, hi), why, unit in ROWS:
        window = {v: ex[v] for v in range(lo, hi + 1) if v in ex}
        sat = len(window) / (hi - lo + 1)
        if pred not in ex:
            print(f"  {tag:5s} {name:14s} {pred:6d} {'NOT REACHABLE':>16s}")
            rows_out.append({"row": tag, "quantity": name, "predicted": pred,
                             "reachable": False, "saturation": round(sat, 4)})
            continue
        cost, form = ex[pred]
        cheaper = sum(1 for v, (c, _) in window.items() if c < cost and v != pred)
        equal = sum(1 for v, (c, _) in window.items() if c == cost and v != pred)
        # Informative if very few values in the window have a description this short.
        verdict = ("informative" if cheaper + equal <= 2 else
                   "weak" if cheaper + equal <= 10 else "uninformative")
        rows_out.append({"row": tag, "quantity": name, "predicted": pred, "unit": unit,
                         "window": [lo, hi], "window_rationale": why,
                         "reachable": True, "cost": cost, "cheapest_form": form,
                         "saturation": round(sat, 4), "cheaper_in_window": cheaper,
                         "equally_cheap_in_window": equal, "verdict": verdict})
        print(f"  {tag:5s} {name:14s} {pred:6d} {form[:16]:>16s} {cost:5d} "
              f"{sat:10.1%} {f'{cheaper} / {equal} equal':>18s}  {verdict}")

    print(f"""
  THE INSTRUMENT HAD TO BE REBUILT MID-PASS, AND SAYING WHY IS THE MOST USEFUL PART.

  The first version asked only "is this integer reachable at all". With 19 constants and 18
  operation forms it reached 72 of the 87 integers in the Higgs window -- 83 per cent
  saturation -- so it ranked nothing. And it did not reach 125, because (mu+1)^q needs the
  DERIVED constant 5 = mu + 1, which a flat grammar never builds. An audit that cannot
  express the claim it is auditing is not a weak audit, it is the wrong one.

  The rebuilt version ranks by DESCRIPTION LENGTH: how short is the cheapest expression for
  the predicted value, and how many values in the same window are describable at least as
  cheaply. That question does not saturate, because cost is bounded below.

  WHAT IT LIMITS. The grammar and the cost function are both judgements, so the absolute
  costs mean little. All rows are scored identically, so the RANKING between them is the
  part to trust -- and the ranking is what the scoreboard needs, since it currently gives
  every row the same implied weight.""")

    # ---- Pass 4420 ---------------------------------------------------------
    pred, meas, err = 125.0, 125.20, 0.11
    sigma_now = abs(meas - pred) / err
    hl_err = 0.05
    sigma_hl = abs(meas - pred) / hl_err
    print(f"""
  PASS 4420 -- F7 in detail

    prediction        m_H = (mu+1)^q = 5^3 = {pred:.0f} GeV exactly, with no error bar
    world average     {meas:.2f} +/- {err:.2f} GeV
    tension now       {sigma_now:.1f} sigma
    HL-LHC projected  +/- {hl_err:.2f} GeV -> {sigma_hl:.1f} sigma if the central value holds

    THIS IS THE ROW TO WATCH, BUT NOT BECAUSE THE AUDIT ABOVE FAVOURS IT.

    Every integer row scored UNINFORMATIVE, F7 included: 125 = (mu+1)^3 costs 3, and 10
    other values in its window are cheaper with 42 more equally cheap. So the description
    length says nothing special about 125 and I am not claiming it does.

    What makes F7 the row to watch is different and simpler -- it is the only one with a
    live, model-independent tension: no cosmology, no dark-sector assumption, just a mass. At
    {sigma_now:.1f} sigma it is not yet evidence against anything -- one-in-fourteen happens -- but the
    error bar is projected to halve, and a prediction with NO error bar of its own cannot
    absorb that. If the central value holds, this row falsifies at HL-LHC.

    AND THE HONEST CAVEAT, WHICH CUTS AGAINST THE PREDICTION RATHER THAN FOR IT. "125 GeV"
    is not a scheme-independent statement: the pole mass, the MS-bar mass and the measured
    resonance position differ at the sub-GeV level, and the prediction does not say which
    one it means. A prediction that does not specify its scheme cannot be {sigma_now:.1f} sigma from
    anything. Fixing that is a one-line addition to the row and it should be made before
    the HL-LHC number arrives, not after.""")

    out = {
        "boundary": ("the expression grammar is a judgement and the absolute counts depend "
                     "on it; only the RANKING between rows is robust, since all rows use "
                     "the same grammar. Windows are stated with their rationale and are "
                     "also judgements. Nothing here is derived from the geometry"),
        "reachable_integers": len(ex),
        "instrument_rebuilt": ("v1 asked only reachability, saturated at 83% in the Higgs "
                               "window, and could not express (mu+1)^q at all; v2 ranks by "
                               "description length, which does not saturate"),
        "rows": rows_out,
        "pass_4420_F7": {
            "predicted_GeV": pred, "measured_GeV": meas, "error_GeV": err,
            "tension_sigma": round(sigma_now, 3),
            "hl_lhc_projected_error_GeV": hl_err,
            "tension_sigma_if_central_holds": round(sigma_hl, 3),
            "unresolved": ("the prediction does not state a renormalisation scheme; pole, "
                           "MS-bar and resonance-position masses differ at the sub-GeV "
                           "level, which is larger than the quoted tension"),
        },
    }
    p = ROOT / "data" / "PART_W33_PASS4419_4420_LOOK_ELSEWHERE_BOARD.json"
    p.parent.mkdir(exist_ok=True)
    p.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {p.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
