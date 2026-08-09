#!/usr/bin/env python3
"""Pass 4335 -- independently verify the parallel track's retraction of my load-port chain.

Pass 4301 (mine) concluded: translations act only on the point side, therefore the machine
addressing points was FORCED by the need to write an address.  That conclusion was
published in the blueprint, the README and the live paper.

The parallel track's Pass 4330 retracts it with a one-line argument: a translation does not
descend to projective points at all.  A projective point is a class [v] = [2v]; translation
by t sends v to v+t, and [e1] = [2e1] while [e1+e0] and [2e1+e0] are different points.  So
the map is not well defined on classes, and the load port lives on the 81 AFFINE vectors --
outside BOTH projective carriers, not privileged to one of them.

A retraction of my own published claim deserves an independent check rather than agreement,
so this exhibits the failure explicitly and then states what survives.

    py -3 analysis/w33_pass4335_verify_the_retraction.py
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
J = [[0, 1, 0, 0], [2, 0, 0, 0], [0, 0, 0, 1], [0, 0, 2, 0]]


def norm(v):
    """Canonical representative of the projective point [v]."""
    return min(tuple((c * x) % 3 for x in v) for c in (1, 2))


def main() -> int:
    print("=" * 78)
    print("Pass 4335 -- is a translation well defined on projective points?")
    print("=" * 78)
    t = (1, 0, 0, 0)                      # the shipped load port Z_p
    print(f"  load port: translation by t = {t}\n")

    # Two vectors representing the SAME projective point.
    v = (0, 1, 0, 0)
    w = tuple((2 * x) % 3 for x in v)
    print(f"  v          = {v}")
    print(f"  w = 2v     = {w}")
    print(f"  [v] == [w] : {norm(v) == norm(w)}   (same projective point)")

    vt = tuple((v[i] + t[i]) % 3 for i in range(4))
    wt = tuple((w[i] + t[i]) % 3 for i in range(4))
    print(f"\n  v + t      = {vt}   -> point {norm(vt)}")
    print(f"  w + t      = {wt}   -> point {norm(wt)}")
    well_defined = norm(vt) == norm(wt)
    print(f"  [v+t] == [w+t] : {well_defined}")

    # Sweep every projective point to count how badly it fails.
    seen, pts = set(), []
    for a in range(3):
        for b in range(3):
            for c in range(3):
                for d in range(3):
                    u = (a, b, c, d)
                    if any(u) and norm(u) not in seen:
                        seen.add(norm(u))
                        pts.append(norm(u))
    bad = 0
    for p in pts:
        q = tuple((2 * x) % 3 for x in p)          # the other representative
        pt = tuple((p[i] + t[i]) % 3 for i in range(4))
        qt = tuple((q[i] + t[i]) % 3 for i in range(4))
        if not any(pt) or not any(qt):
            bad += 1                                # lands on the zero vector: no point
            continue
        if norm(pt) != norm(qt):
            bad += 1
    print(f"\n  projective points where the two representatives disagree"
          f" (or leave the space): {bad} of {len(pts)}")
    print(f"""
  THE RETRACTION IS CORRECT AND I ACCEPT IT.  A translation is not a map on projective
  points: it depends on which representative of the class you hand it, and it disagrees on
  {bad} of the {len(pts)} points.  It cannot induce a line action either, since lines are sets of
  points.

  SO MY PASS 4301 CHAIN FAILS AT ITS FIRST LINK.  I argued that translations exist only on
  the point side and concluded the machine's choice of the point carrier was FORCED by the
  need to write an address.  Translations exist on NEITHER projective side.  They live on
  the 81 affine vectors, which is a third object, and the 40-point / 40-line comparison in
  that pass audits only the LINEAR subgroup -- the part of the ISA that does descend.

  WHAT SURVIVES, stated narrowly.  A translation is necessary to connect the 81-frame
  affine register (Pass 4225), the only generators acting freely are translations (Pass
  4204), and its direction may be any of the four coordinates (Pass 4225 again, all four
  work).  None of that selects a projective carrier, because none of it happens in
  projective space.

  WHAT THIS COSTS.  The claim "the point side was forced, not chosen" was published in the
  machine blueprint, in the README, and on the live paper.  All three need the retraction,
  not a quiet edit -- this project's rule is that a corrected figure is printed next to the
  wrong one with the reason the wrong one survived.  The reason here is that the conclusion
  was reached by comparing what the two projective carriers admit, without first checking
  that the operation in question acts on either.""")

    out = {

        "boundary": ("this confirms the retraction of Pass 4301's projective chain; the LINEAR "

            "subgroup audit it was built on stands, and only the affine step fails"),"translation": list(t),
           "well_defined_on_a_single_class": bool(well_defined),
           "points_where_representatives_disagree": bad,
           "total_points": len(pts),
           "retraction_confirmed": True,
           "retracted_claim": ("Pass 4301: translations exist only on the point side, so "
                               "addressing points was forced"),
           "survives": ("a translation is necessary to connect the 81-frame affine "
                        "register and may point along any coordinate; this selects no "
                        "projective carrier"),
           "credit": "parallel track, Pass 4330"}
    p = ROOT / "data" / "PART_W33_PASS4335_VERIFY_RETRACTION.json"
    p.parent.mkdir(exist_ok=True)
    # Hash the ROUND-TRIPPED object, never the live dict (CLAUDE.md, Pass 2482).
    p.write_text(json.dumps(json.loads(json.dumps(out)), indent=2, sort_keys=True) + "\n",
                 encoding="utf-8")
    print(f"\nwrote {p.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
