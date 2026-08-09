#!/usr/bin/env python3
"""Pass 4367 -- the flag-incidence comparator, and its exact single-fault boundary.

CREDIT.  The Codex track reserved this as their Pass 4331 -- "intrinsic flag-incidence
comparator and exact single-fault detection boundary" -- and identified why my Pass 4304
was not one: 4304 compared each faulty trajectory with its CORRECT trajectory, which is a
golden-run sensitivity test.  It needs the right answer to detect a wrong one, so it cannot
run on hardware.  Their framing and their name for the object are used here.  It is built
in this track only because it did not land across four reservation blocks and
analysis/PASS4364_QUERY_TO_CODEX_ON_4331.md said I would.

THE IDEA, which is theirs.  A flag is an incident point-line pair.  There are 1600 pairs
and only 160 flags, so the incidence relation is a heavy constraint the state must satisfy
at all times.  A machine that holds a flag can check its own validity -- is this point on
this line? -- with no reference trajectory, no duplicate hardware, and no golden run.  What
it detects is any fault that carries the state off the incidence relation; what it misses
is any fault that maps one valid flag to another.

That boundary is exact and computable, and computing it is the point: a detector whose
miss set is unknown is not a detector.

    py -3 analysis/w33_pass4367_flag_incidence_comparator.py
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
J = [[0, 1, 0, 0], [2, 0, 0, 0], [0, 0, 0, 1], [0, 0, 2, 0]]
ID4 = tuple(tuple(1 if i == j else 0 for j in range(4)) for i in range(4))
LIN = {"F_p": ((0, 2, 0, 0), (1, 0, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)),
       "CX_pf": ((1, 0, 0, 0), (0, 1, 0, 2), (1, 0, 1, 0), (0, 0, 0, 1)),
       "CX_fp": ((1, 0, 1, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 2, 0, 1))}
ISA = ["F_p", "CX_pf", "CX_fp"]


def mv(A, v):
    return tuple(sum(A[i][k] * v[k] for k in range(4)) % 3 for i in range(4))


def norm(v):
    return min(tuple((c * x) % 3 for x in v) for c in (1, 2))


def geometry():
    seen, pts = set(), []
    for a in range(3):
        for b in range(3):
            for c in range(3):
                for d in range(3):
                    v = (a, b, c, d)
                    if any(v) and norm(v) not in seen:
                        seen.add(norm(v))
                        pts.append(norm(v))
    pidx = {p: i for i, p in enumerate(pts)}

    def form(u, v):
        return sum(u[i] * J[i][j] * v[j] for i in range(4) for j in range(4)) % 3

    lines = set()
    for i in range(40):
        for j in range(i + 1, 40):
            if form(pts[i], pts[j]):
                continue
            span = set()
            for c1 in range(3):
                for c2 in range(3):
                    w = tuple((c1 * pts[i][t] + c2 * pts[j][t]) % 3 for t in range(4))
                    if any(w):
                        span.add(norm(w))
            if len(span) == 4:
                lines.add(frozenset(span))
    lines = sorted(lines, key=lambda s: sorted(s))
    return pts, pidx, lines


def main() -> int:
    print("=" * 78)
    print("Pass 4367 -- the flag-incidence comparator (Codex track's Pass 4331 framing)")
    print("=" * 78)
    pts, pidx, lines = geometry()
    lidx = {L: i for i, L in enumerate(lines)}
    incident = np.zeros((40, 40), dtype=bool)
    for li, L in enumerate(lines):
        for p in L:
            incident[pidx[p], li] = True
    flags = [(p, l) for p in range(40) for l in range(40) if incident[p, l]]
    print(f"  (point, line) pairs      : {40 * 40}")
    print(f"  of those, INCIDENT flags : {len(flags)}")
    print(f"  the constraint rejects   : {40 * 40 - len(flags)} of {40 * 40} "
          f"({100 * (1 - len(flags) / 1600):.1f}%)")
    print("""
  So a state that is supposed to be a flag can be checked against the geometry alone.
  No golden run, no duplicated datapath -- just 'is this point on this line?'.
""")

    def act_p(M, p):
        return pidx[norm(mv(M, pts[p]))]

    def act_l(M, l):
        return lidx[frozenset(norm(mv(M, q)) for q in lines[l])]

    # A fault model on the STATE, which is what a detector sees: corrupt the point
    # register, the line register, or both, and ask whether incidence still holds.
    rng = np.random.default_rng(4367)
    caught = Counter()
    trials = 0
    for (p, l) in flags:
        for newp in range(40):                       # single-register point fault
            if newp == p:
                continue
            trials += 1
            caught["point fault detected" if not incident[newp, l]
                   else "point fault MISSED"] += 1
        for newl in range(40):                       # single-register line fault
            if newl == l:
                continue
            trials += 1
            caught["line fault detected" if not incident[p, newl]
                   else "line fault MISSED"] += 1
    print(f"  {'outcome':28s} {'count':>9s} {'rate':>8s}")
    for k in ("point fault detected", "point fault MISSED",
              "line fault detected", "line fault MISSED"):
        n = caught[k]
        base = caught["point fault detected"] + caught["point fault MISSED"] \
            if "point" in k else caught["line fault detected"] + caught["line fault MISSED"]
        print(f"  {k:28s} {n:9d} {100 * n / base:7.2f}%")

    det = caught["point fault detected"] + caught["line fault detected"]
    miss = caught["point fault MISSED"] + caught["line fault MISSED"]
    print(f"\n  overall single-register fault detection: {100 * det / (det + miss):.2f}%")

    # THE MISS SET, exactly.  A point fault is missed iff the new point is also on the
    # same line -- there are 4 points per line, so 3 wrong points survive the check.
    per_line = Counter(len([p for p in range(40) if incident[p, l]]) for l in range(40))
    per_point = Counter(len([l for l in range(40) if incident[p, l]]) for p in range(40))
    print(f"\n  points per line : {dict(per_line)}")
    print(f"  lines per point : {dict(per_point)}")
    k_line = list(per_line)[0]
    k_point = list(per_point)[0]
    print(f"""
  THE MISS SET IS EXACT AND SMALL.  A corrupted point survives the check exactly when it
  still lies on the held line, and each line carries {k_line} points -- so {k_line - 1} of the {39} wrong
  points are missed, {100 * (k_line - 1) / 39:.1f}%.  A corrupted line survives when it still passes through
  the held point, and each point lies on {k_point} lines, so {k_point - 1} of {39} are missed,
  {100 * (k_point - 1) / 39:.1f}%.

  That is the whole detection boundary, and it needs no simulation to state: the comparator
  catches every single-register fault except the {k_line - 1} that land on the same line or the
  {k_point - 1} that land on the same point through it.  Both numbers come from the quadrangle's
  own parameters, not from a fault campaign.

  WHY THIS IS A REAL DETECTOR AND PASS 4304 WAS NOT.  This test runs on the machine's own
  state at any instant.  Pass 4304 compared a faulty run against the correct run, which
  presupposes the correct run -- available in a simulation and never on hardware.  The
  Codex track named that distinction and it is the difference between a sensitivity study
  and an error detector.

  WHAT IT DOES NOT DO.  It does not detect a fault that moves the flag to another valid
  flag, which includes every fault expressible as a group element -- and the machine's own
  opcodes are group elements.  So this catches corruption, not incorrect computation.  A
  wrong-but-legal instruction is invisible to it, and no amount of incidence checking will
  change that.""")

    out = {

        "boundary": ("measured on W(3,3) only, for SINGLE-register faults, against a comparator "

            "that uses nothing but the incidence relation; multi-register faults and "

            "correlated faults are not covered and were not simulated"),"pairs": 1600, "flags": len(flags),
           "constraint_rejects_fraction": 1 - len(flags) / 1600,
           "points_per_line": k_line, "lines_per_point": k_point,
           "point_fault_miss_rate": (k_line - 1) / 39,
           "line_fault_miss_rate": (k_point - 1) / 39,
           "overall_detection": det / (det + miss),
           "trials": trials,
           "credit": "Codex track Pass 4331 reservation: framing and name",
           "detects": "any single-register corruption leaving the incidence relation",
           "misses": "faults mapping one valid flag to another, including every group "
                     "element, so incorrect computation is invisible to it"}
    p = ROOT / "data" / "PART_W33_PASS4367_FLAG_INCIDENCE_COMPARATOR.json"
    p.parent.mkdir(exist_ok=True)
    # Hash the ROUND-TRIPPED object, never the live dict (CLAUDE.md, Pass 2482).
    p.write_text(json.dumps(json.loads(json.dumps(out)), indent=2, sort_keys=True) + "\n",
                 encoding="utf-8")
    print(f"\nwrote {p.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
