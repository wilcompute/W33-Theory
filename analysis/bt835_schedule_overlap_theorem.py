#!/usr/bin/env python3
"""
BT835 - The schedule-overlap theorem: switching measurement timetables.

The 36 complete measurement schedules (= regular spreads, BT817) form
the machine's timetable library.  Operational question: when the
controller switches schedules mid-run, how many contexts carry over?

BT813's double-six diagonal [1, 15, 20] says two distinct schedules
stand in one of exactly two relations.  Counting identity: each context
lies in 9 schedules, so for a fixed schedule S,
    sum_{S' != S} |S cap S'| = 10 x (9-1) = 80 = 15a + 20b,
with (a, b) the overlap sizes on the two relation classes.  BT835
computes the exact overlap spectrum and the switching cost.
"""
from __future__ import annotations

from itertools import combinations, product
from collections import Counter
import json

import numpy as np


def witting_rays():
    w = np.exp(2j * np.pi / 3.0)
    s3 = np.sqrt(3.0)
    rays = []
    for i in range(4):
        e = np.zeros(4, dtype=complex)
        e[i] = 1.0
        rays.append(e)
    for mu, nu in product(range(3), repeat=2):
        rays.append(np.array([0, 1, -(w**mu), w**nu]) / s3)
        rays.append(np.array([1, 0, -(w**mu), -(w**nu)]) / s3)
        rays.append(np.array([1, -(w**mu), 0, w**nu]) / s3)
        rays.append(np.array([1, w**mu, w**nu, 0]) / s3)
    return rays


def main():
    rays = witting_rays()
    n = 40
    orth = [[abs(np.vdot(rays[i], rays[j])) < 1e-9 for j in range(n)]
            for i in range(n)]
    contexts = [c for c in combinations(range(n), 4)
                if all(orth[i][j] for i, j in combinations(c, 2))]
    assert len(contexts) == 40
    ctx_of = [[ci for ci, c in enumerate(contexts) if r in c]
              for r in range(n)]

    schedules = []

    def cover(used, chosen):
        if len(chosen) == 10:
            schedules.append(frozenset(chosen))
            return
        r = min(set(range(n)) - used)
        for ci in ctx_of[r]:
            c = contexts[ci]
            if used & set(c):
                continue
            cover(used | set(c), chosen + [ci])

    cover(set(), [])
    assert len(schedules) == 36
    print(f"schedules: {len(schedules)} (= all regular spreads)")

    overlaps = Counter()
    for S, T in combinations(schedules, 2):
        overlaps[len(S & T)] += 1
    print(f"pairwise overlap spectrum |S cap T|: "
          f"{dict(sorted(overlaps.items()))}")

    # per-schedule relation census
    S0 = schedules[0]
    rel = Counter(len(S0 & T) for T in schedules if T != S0)
    print(f"one schedule vs the other 35: {dict(sorted(rel.items()))}")

    # identities
    total = sum(k * v for k, v in overlaps.items())
    assert total == 40 * (9 * 8 // 2)   # sum over contexts C(9,2)
    print(f"double count: sum |S cap T| over pairs = {total} "
          f"= 40 x C(9,2) = 1440")

    ks = sorted(k for k in rel)
    a, b = ks[0], ks[1]
    na, nb = rel[a], rel[b]
    assert a * na + b * nb == 80
    print(f"counting identity: {a}x{na} + {b}x{nb} = 80 "
          f"(each of 10 contexts shared with 8 others)")
    print(f"\nSCHEDULE-OVERLAP THEOREM: two distinct timetables share")
    print(f"EXACTLY {a} or {b} contexts ({na} and {nb} partners resp.);")
    print(f"relation classes = the double-six diagonal [1, {na}, {nb}]")
    print(f"of BT813.  Operational cost of a timetable switch: at least")
    print(f"{10 - b} of 10 contexts must be re-calibrated; the {nb}")
    print(f"'cheap' switches preserve {b} contexts each.")

    out = {
        "theorem": "BT835 schedule overlap",
        "overlap_spectrum": {str(k): v for k, v in sorted(overlaps.items())},
        "per_schedule": {str(k): v for k, v in sorted(rel.items())},
        "double_count": total,
        "bt813_match": "[1, %d, %d]" % (na, nb),
    }
    with open("data/bt835_schedule_overlap.json", "w") as fj:
        json.dump(out, fj, indent=2)
    print("\nwrote data/bt835_schedule_overlap.json")


if __name__ == "__main__":
    main()
