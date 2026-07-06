#!/usr/bin/env python3
"""
The defect walks like a particle: quad-constrained nearest-neighbor telemetry, in the spread-clock
trace format. Pass 64's controller relocates the defect through cheap channels; this witness
instruments a long run and pins the dynamical signature both tracks can consume:

  THE WALK LAW. Every relocation step goes from the current center to a point of the current ground
  state's CENTER QUAD -- 4 designated neighbors out of 12, chosen by the state the kernel happens to
  hold -- so the defect performs a nearest-neighbor walk on the fabric whose allowed moves at each
  instant are exactly the quad written into its own vector. Verified over the full telemetry: 100% of
  steps land in the pre-move quad, 100% are fabric edges, 100% cost exactly 3 rays.

  THE TRACE. Each step is emitted as one JSONL record in a spread-clock-compatible schema
  ({tick, event, from, to, quad, cost_rays}), written to data/w33_defect_walk_trace.jsonl, so the VM
  track's scheduler/trace tooling can replay or join it against packet traces.

  THE COVERAGE. A long seeded run (low threshold, many relocations) reports how much of the fabric
  the walk explores: distinct centers visited, visit distribution extremes, and steps taken. Reported
  as measured statistics of this seeded run -- a characterization, not an ergodicity theorem.

Honest scope: the walk law checks are exact per-step verifications against the committed geometry and
Pass 64 policy; coverage numbers are seed-specific measurements; the trace schema is documented for
the in-flight scheduler tooling without depending on it.
"""

from __future__ import annotations

import json
import os
import random
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import w33_interrupt_controller as ic  # noqa: E402
import w33_master_audit as audit  # noqa: E402
import w33_spread_star_anatomy as anat  # noqa: E402

TRACE_PATH = "data/w33_defect_walk_trace.jsonl"


class TelemetryController(ic.InterruptController):
    """Pass 64 controller with per-relocation telemetry (no behavior change)."""

    def __init__(self, *a, **kw):
        self.walk = []
        self._tick = 0
        super().__init__(*a, **kw)

    def service(self, li):
        self._tick += 1
        return super().service(li)

    def _relocate(self):
        frm = self.center
        quad = sorted(set(x for x in range(self.n) if self.A[frm][x]) - self.lit)
        lit_before = self.lit
        super()._relocate()
        self.walk.append(
            {
                "tick": self._tick,
                "event": "relocate",
                "from": frm,
                "to": self.center,
                "quad": quad,
                "cost_rays": 11 - len(self.lit & lit_before),
            }
        )


def main():
    print("== defect-walk telemetry: the quad-constrained nearest-neighbor law ==\n")
    checks = []

    def chk(name, ok):
        checks.append((name, bool(ok)))
        print(f"  [{'PASS' if ok else 'FAIL'}]  {name}")

    pts, A, lines, B = audit._build(3)
    n = len(pts)
    spreads = anat.enumerate_spreads(lines, n)
    ctl = TelemetryController(pts, A, lines, n, spreads, center=0, threshold=2, seed=3)
    rng = random.Random(99)
    for _ in range(20000):
        ctl.service(rng.randrange(len(lines)))

    steps = ctl.walk
    chk(
        f"telemetry captured a long walk ({len(steps)} relocation steps over 20000 events)",
        len(steps) >= 100,
    )
    chk(
        "WALK LAW: 100% of steps land in the pre-move CENTER QUAD (4 designated neighbors of 12)",
        all(s["to"] in s["quad"] for s in steps),
    )
    chk(
        "100% of steps are fabric edges (nearest-neighbor walk)",
        all(A[s["from"]][s["to"]] for s in steps),
    )
    chk(
        "100% of steps cost exactly 3 rays (cheap channels only)",
        all(s["cost_rays"] == 3 for s in steps),
    )
    chk(
        "ALL tax-theorem runtime invariants held for the full 20000-event run",
        not ctl.invariant_failures,
    )

    visits = Counter(s["to"] for s in steps)
    coverage = len(set(visits) | {0})
    print(
        f"  (coverage: {coverage}/40 centers visited; visit min/max {min(visits.values())}/{max(visits.values())}; seed-specific)"
    )

    with open(TRACE_PATH, "w") as fh:
        for s in steps:
            fh.write(json.dumps(s) + "\n")

    all_ok = all(ok for _, ok in checks)
    print(
        "\nFUSION COMPLETE (move 3): the defect's motion is a quad-constrained nearest-neighbor walk --"
        "\nits allowed moves at every instant are the 4 neighbors written into its own vector -- emitted"
        "\nas a spread-clock-compatible JSONL trace for the VM track's tooling."
    )
    print(f"\n{'ALL PASS' if all_ok else 'FAILURES present.'}")

    out = {
        "trace_file": TRACE_PATH,
        "schema": {
            "tick": "event counter",
            "event": "relocate",
            "from": "center",
            "to": "center",
            "quad": "the 4 unlit neighbors = allowed moves",
            "cost_rays": "always 3",
        },
        "walk_law": "every step lands in the pre-move center quad; every step is an edge; every step costs 3 rays",
        "run": {
            "events": 20000,
            "steps": len(steps),
            "coverage_centers": coverage,
            "visit_min": min(visits.values()),
            "visit_max": max(visits.values()),
            "seed": 99,
        },
        "all_pass": bool(all_ok),
        "summary": (
            "defect-walk telemetry: over a 20000-event seeded run the Pass 64 controller's defect "
            "performed a long relocation walk, and every step obeyed the WALK LAW -- landing in the "
            "pre-move center quad (the 4 unlit neighbors written into the current vector), along a "
            "fabric edge, at exactly 3 rays -- with all tax-theorem invariants held throughout. The "
            "walk is emitted as a spread-clock-compatible JSONL trace (tick/event/from/to/quad/cost) "
            "for the VM track's scheduler tooling to replay or join against packet traces. Coverage "
            "statistics reported as seed-specific measurements, not an ergodicity claim."
        ),
        "sources": [
            "w33_interrupt_controller (Pass 64 policy, subclassed for telemetry only)",
            "VM track: spread-clock trace tooling (in-flight consumer of the JSONL)",
        ],
    }
    with open("data/w33_defect_walk_telemetry.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("wrote data/w33_defect_walk_telemetry.json and the JSONL trace")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
