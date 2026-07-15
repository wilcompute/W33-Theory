#!/usr/bin/env python3
"""Pass 313: is Pass 308 decorative?  Yes -- 225 and 227 each already force q=3.

Pass 308 presented the TBM-field containment as "a third selection argument for
characteristic 3", joining Pass 225 (the half-spinor equals one generation only
at q=3) and Pass 227 (the shadow rank fits an exceptional group only at q=3).
It hedged that it selects a family (3^odd) rather than a point.  This witness
asks the sharper question the hedge invites: does it add ANY constraint?

IT DOES NOT.

    225 alone:  2^{(q^2-1)/2} = 16  <=>  q^2 = 9  <=>  q = 3.   Unique.
    227 alone:  (q^2+1)/2 <= 8      <=>  q^2 <= 15 <=>  q = 3.   Unique (odd q).
    308 alone:  sf(q) = 3           <=>  q = 3, 27, 243, ...     A family.

Each of 225 and 227 is independently SUFFICIENT.  The intersection of all three
is {3}; the intersection of 225 and 227 alone is also {3}.  Removing 308 changes
nothing.  So 308 is DECORATIVE: it is consistent with q=3 but carries no
selective power, and quoting it as "a third selection argument" overstates it in
exactly the way Pass 311 catalogued -- a true statement read wider than it is.

WHAT 308 DOES STILL SHOW.  That the TBM field is not reached by q=5, 7, 11, or by
any even q, or by q=9 and 81 (even Frobenius degree).  That is a real fact about
the field ladder.  It just is not a selection principle, because the two genuine
ones already collapse the space to a point before it is consulted.
"""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass313_selection_audit.json"


def sf(n):
    o = 1
    for p, e in sp.factorint(int(n)).items():
        if e % 2:
            o *= p
    return int(o)


def main():
    checks = {}
    odd_pp = [q for q in range(3, 400) if len(sp.factorint(q)) == 1 and q % 2 == 1]

    s225 = [q for q in odd_pp if 2 ** ((q * q - 1) // 2) == 16]
    s227 = [q for q in odd_pp if (q * q + 1) // 2 <= 8]
    s308 = [q for q in odd_pp if sf(q) == 3]

    checks["225_selects_only_3"] = s225 == [3]
    checks["227_selects_only_3"] = s227 == [3]
    checks["308_selects_a_family"] = len(s308) > 1 and 3 in s308 and 27 in s308

    inter_all = sorted(set(s225) & set(s227) & set(s308))
    inter_225_227 = sorted(set(s225) & set(s227))
    checks["all_three_intersect_at_3"] = inter_all == [3]
    checks["225_and_227_alone_already_give_3"] = inter_225_227 == [3]
    checks["308_ADDS_NOTHING"] = inter_all == inter_225_227
    checks["308_is_decorative"] = inter_all == inter_225_227

    # q=27 is the discriminating case: passes 308, fails both real selectors
    spin27 = 2 ** ((27 * 27 - 1) // 2)
    rank27 = (27 * 27 + 1) // 2
    checks["q27_passes_308"] = sf(27) == 3
    checks["q27_fails_225"] = spin27 != 16
    checks["q27_fails_227"] = rank27 > 8

    table = {}
    for q in odd_pp[:12]:
        table[str(q)] = {
            "225_spinor_is_16": bool(2 ** ((q * q - 1) // 2) == 16),
            "227_rank_le_8": bool((q * q + 1) // 2 <= 8),
            "308_TBM_field": bool(sf(q) == 3),
        }

    all_pass = all(v for v in checks.values() if isinstance(v, bool))
    payload = {
        "schema": "w33.pass313.selection_audit.v1",
        "status": "PASS" if all_pass else "FAIL",
        "VERDICT": (
            "Pass 308 is DECORATIVE. Each of Pass 225 (2^{(q^2-1)/2} = 16 <=> "
            "q = 3) and Pass 227 ((q^2+1)/2 <= 8 <=> q = 3 for odd q) is "
            "INDEPENDENTLY SUFFICIENT to force q = 3. Pass 308 selects the family "
            "{3, 27, 243, ...}, and the intersection of all three ({3}) equals "
            "the intersection of 225 and 227 alone ({3}). Removing 308 changes "
            "nothing, so calling it 'a third selection argument' overstates it."
        ),
        "selectors": {
            "225 spinor selection": {"condition": "2^{(q^2-1)/2} = 16",
                                     "selects": s225, "sufficient_alone": True},
            "227 exceptional rank": {"condition": "(q^2+1)/2 <= 8",
                                     "selects": s227, "sufficient_alone": True},
            "308 TBM field": {"condition": "sf(q) = 3",
                              "selects": s308[:5], "sufficient_alone": False},
        },
        "intersections": {
            "all_three": inter_all,
            "225_and_227_only": inter_225_227,
            "308_contributes": inter_all != inter_225_227,
        },
        "the_discriminating_case": {
            "q": 27,
            "passes_308": True,
            "fails_225": f"half-spinor = 2^364, not 16",
            "fails_227": f"rank SO(730) = {rank27} >> 8",
            "meaning": "q=27 is exactly where 308 and the real selectors "
                       "disagree, and the real selectors win",
        },
        "per_q": table,
        "what_308_does_still_show": (
            "That the TBM field is NOT reached by q = 5, 7, 11, by any even q, or "
            "by q = 9 and 81 (even Frobenius degree). That is a real fact about "
            "the field ladder. It simply is not a SELECTION principle, because "
            "the two genuine ones collapse the space to a point before it is "
            "consulted."
        ),
        "the_pattern_this_confirms": (
            "Pass 311 catalogued two failure modes: coordinate artefacts, and "
            "correct results over-stated. This is the second kind, caught one "
            "round later on my own pass -- 308's arithmetic is right, its framing "
            "as 'a third selection argument' is not. The prior 311 recommended "
            "(treat any claim whose scope exceeds its proof as an over-read) "
            "flags it immediately, which is the point of having the prior."
        ),
        "checks": {k: bool(v) for k, v in checks.items() if isinstance(v, bool)},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
