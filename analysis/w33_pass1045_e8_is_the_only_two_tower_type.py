#!/usr/bin/env python3
"""Pass 1045: E8 is the ONLY type with two competing Springer towers -- and the
contextual fraction is the experiment that decides between them.

Two results, one census and one framing.

(1) THE COMPETITION IS PECULIAR TO E8.
Pass 1039 found that W(E8) has exactly one sibling tower: d=3/6 give
Shephard-Todd G32 over W(3,3), d=4 gives G31 over the doily.  That raised an
obvious question the pass did not answer -- is "exactly one sibling" a fact about
E8, or does every type have siblings?

By Springer, |C_W(regular w of order d)| = product of the degrees of W divisible
by d, so the census is pure arithmetic on the degree list.  Counting the d that
give a centraliser of rank >= 3 (a genuinely multi-dimensional complex reflection
group, not a torus-like remnant):

    E8   d = 3, 4, 6   ->  rank 4, 4, 4   ->  TWO distinct towers (3 and 6 coincide)
    E7   d = 3, 6      ->  rank 3, 3      ->  one tower
    E6   d = 3         ->  rank 3         ->  one tower
    F4   --                                ->  none
    D4   --                                ->  none
    H4   --                                ->  none

So E8 is the unique type in this list carrying two competing towers.  Everywhere
else the Springer construction is unambiguous, and the selection question this
corpus has been arguing about does not even arise.

That cuts both ways, honestly:
  * it makes E8 special in a way that has nothing to do with q = 3, and
  * it means the q = 2 / q = 3 competition is an E8 phenomenon, so resolving it
    resolves something about E8 rather than about generalised quadrangles.

(2) THE CONTEXTUAL FRACTION IS THE DECIDING EXPERIMENT.
Pass 1044 exhibited an explicit noncontextual model on the doily (contextual
fraction 0) and Pass 1042 showed W(3,3) admits none.  photonic_holonet.tex already
predicts CF = 1/10 for the q = 3 fabric and the demonstrator measures exactly this
quantity.  So the same number that selects between the two towers is the one the
experiment reports:

    measured CF = 0     ->  the substrate is the Gaussian/doily tower, which is
                            noncontextual, supports no magic, and cannot carry the
                            holonet architecture.  The q = 3 program is refuted.
    measured CF = 1/10  ->  the Eisenstein tower, as predicted.
    measured CF other   ->  neither tower; the substrate identification is wrong.

This upgrades contextuality from an internal discriminator to a FALSIFIER of the
whole substrate identification, with a numeric target and an existing protocol.

PRIOR ART -- cited, not reclaimed:
  * Springer, regular elements: |C| = product of degrees divisible by d.
  * Pass 1039 / 1039b -- the E8 tower census and the doily identification.
  * Pass 1042 / 1044 -- the ovoid counts and the explicit noncontextual model.
  * photonic_holonet.tex -- the CF = 1/10 prediction and demonstrator protocol.
    That number is ITS result; this pass only says what measuring it decides.
"""

from __future__ import annotations

import json
from math import prod
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass1045_e8_is_the_only_two_tower_type.json"

# Degrees of the finite reflection groups compared.
DEGREES = {
    "E8": [2, 8, 12, 14, 18, 20, 24, 30],
    "E7": [2, 6, 8, 10, 12, 14, 18],
    "E6": [2, 5, 6, 8, 9, 12],
    "F4": [2, 6, 8, 12],
    "D4": [2, 4, 4, 6],
    "H4": [2, 12, 20, 30],
}

MIN_RANK = 3   # rank >= 3: a genuinely multi-dimensional reflection group


def census(degs: list[int]) -> dict:
    members = []
    for d in range(3, max(degs) + 1):          # d = 2 is w = -1, the whole group
        s = [x for x in degs if x % d == 0]
        if len(s) >= MIN_RANK:
            members.append({"d": d, "rank": len(s), "order": prod(s)})
    # d and d' give the SAME tower when their centralisers coincide; detect by
    # identical (rank, order) with one dividing the other.
    towers = {}
    for m in members:
        towers.setdefault((m["rank"], m["order"]), []).append(m["d"])
    return {"members": members,
            "distinct_towers": len(towers),
            "tower_groups": [{"rank": k[0], "order": k[1], "d_values": v}
                             for k, v in sorted(towers.items())]}


def main() -> int:
    out = {"schema": "w33.pass1045.e8_only_two_tower_type.v1"}
    checks = {}
    table = {t: census(d) for t, d in DEGREES.items()}

    checks["E8_has_two_distinct_towers"] = table["E8"]["distinct_towers"] == 2
    checks["E8_towers_are_155520_and_46080"] = sorted(
        g["order"] for g in table["E8"]["tower_groups"]) == [46080, 155520]
    checks["d3_and_d6_are_the_same_E8_tower"] = any(
        set(g["d_values"]) == {3, 6} for g in table["E8"]["tower_groups"])
    checks["every_other_type_has_at_most_one"] = all(
        table[t]["distinct_towers"] <= 1 for t in table if t != "E8")
    checks["E8_is_the_unique_two_tower_type"] = (
        checks["E8_has_two_distinct_towers"]
        and checks["every_other_type_has_at_most_one"])

    decider = {
        "quantity": "contextual fraction (CF), measured by the existing demonstrator",
        "prediction_eisenstein_q3": "1/10",
        "prediction_gaussian_doily": "0 (explicit noncontextual model, Pass 1044)",
        "outcomes": {
            "CF = 0": "substrate is the noncontextual doily tower: no magic, the "
                      "holonet architecture cannot be carried, q=3 program refuted",
            "CF = 1/10": "Eisenstein tower as predicted",
            "CF = anything else": "neither tower; the substrate identification is wrong",
        },
        "status": "falsifier, not a fit -- the number is predicted before measurement",
        "prior_art": "photonic_holonet.tex owns the CF = 1/10 prediction and protocol",
    }

    out["status"] = "PASS" if all(checks.values()) else "FAIL"
    out["springer_census"] = table
    out["deciding_experiment"] = decider
    out["headline"] = (
        "E8 is the only reflection group in the compared list carrying TWO competing "
        "Springer towers (d=3/6 -> G32 order 155520 over W(3,3); d=4 -> G31 order "
        "46080 over the doily). E7 and E6 have one each; F4, D4, H4 have none. So the "
        "q=2 versus q=3 competition is an E8 phenomenon, and the contextual fraction "
        "-- 0 for the doily, 1/10 for W(3,3) -- is the experiment that decides it.")
    out["scope"] = (
        "A degree-list census plus a framing of an existing prediction. It does not "
        "verify transitivity of the derived subgroups outside E8, where that was "
        "computed in Pass 1039; for the other types only the rank/order census is "
        "done, which is what the two-tower claim needs.")
    out["checks"] = checks

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": out["status"], "checks": checks,
                      "distinct_towers": {t: table[t]["distinct_towers"]
                                          for t in table}}, sort_keys=True))
    return 0 if out["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
