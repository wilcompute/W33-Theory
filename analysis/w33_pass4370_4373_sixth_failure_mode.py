#!/usr/bin/env python3
"""Passes 4370, 4372-4373 -- how many digits are earned, and is there a sixth failure mode?

CLAUDE.md lists five failure modes this repository has actually produced: coordinate
artefacts, over-reads, unbuilt objects, unbuilt halves, and rediscovery.  This session
produced roughly eight errors in one track.  Whether they fit the five is worth asking
rather than assuming, because the list exists to be added to.

  4370  SIGNIFICANT-FIGURE PROPAGATION.  The cadence error (Pass 4363) was one number
        printed with more digits than its weakest input supports.  Compute, per headline
        figure, how many digits are actually earned.
  4372  THE SIXTH FAILURE MODE.  Classify this session's errors against the five and see
        what is left over.
  4373  CLAIM LANGUAGE AGAINST EVIDENCE TIER.  Does the prose's confidence match the tier
        the claim is filed under?

    py -3 analysis/w33_pass4370_4373_sixth_failure_mode.py
"""

from __future__ import annotations

import json
import re
from math import log10
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Errors this track made in this session, with what each was and how it was caught.
SESSION_ERRORS = [
    ("4301 the point carrier was 'forced'",
     "compared what two carriers admit without checking the operation acts on either",
     "parallel track", "premise never tested"),
    ("4304 'dual-rail fault detection'",
     "compared faulty runs against correct runs; needs the answer to find the error",
     "parallel track", "premise never tested"),
    ("4305 'the linear opcodes are p/f symmetric'",
     "fixation booleans agreed while conjugation carried an opcode out of the set",
     "parallel track", "weaker test substituted for the real one"),
    ("4339 'the remedies share logic'",
     "compared additive gate counts against a multiplicative baseline",
     "self", "no valid null model"),
    ("4252/4279 'thermodynamic reversibility costs 2x'",
     "priced a property the machine already had; compute erases nothing on any machine",
     "self, prompted by writing a review request", "premise never tested"),
    ("4354 the femtowatt figure's cadence",
     "third factor was an assumption presented with the precision of a measurement",
     "self", "precision exceeded the weakest input"),
    ("4302 '27 duplicate inserts'",
     "the check was detecting a theorem-guard block this same session had prepended",
     "self", "checker measured its own repair"),
    ("4226/4286 checkers reporting zero",
     "the pattern could not match the corpus it was pointed at",
     "self", "checker never shown to catch anything"),
]

FIVE = ["coordinate artefact", "over-read", "unbuilt object", "unbuilt half", "rediscovery"]


def pass_4370() -> dict:
    print("=" * 78)
    print("Pass 4370 -- how many digits does each headline figure earn?")
    print("=" * 78)
    # figure -> (printed digits, inputs as (name, significant digits or None if exact))
    FIGURES = {
        "rho(B) = 5.746872679901964...": (
            22, [("adjacency matrix", None), ("eigenvalue solve", 15)]),
        "readout power 1.066e-13 W": (
            4, [("8/3 bits", None), ("kT ln2", 10), ("clock 208.86 MHz", 5),
                ("cadence 15 instructions", 0)]),
        "cell counts 103 / 132 / 206 / 240": (
            3, [("yosys synthesis", None), ("opcode ordering", 2)]),
        "mixing time 15 instructions": (
            2, [("walk matrix", None), ("TV threshold 1/4", 1)]),
        "|lambda_2| = 0.893992320": (
            9, [("walk matrix", None), ("eigenvalue solve", 15)]),
        "143 meV per routed read": (
            3, [("8 bits", None), ("kT ln2", 10), ("temperature 300 K", 3)]),
    }
    print(f"  {'figure':38s} {'printed':>8s} {'earned':>7s}  weakest input")
    rows = []
    for name, (printed, inputs) in FIGURES.items():
        finite = [(n, d) for n, d in inputs if d is not None]
        earned = min((d for _, d in finite), default=printed)
        weakest = min(finite, key=lambda t: t[1])[0] if finite else "all exact"
        flag = "  <-- OVERSTATED" if printed > earned else ""
        rows.append({"figure": name, "printed_digits": printed,
                     "earned_digits": earned, "weakest_input": weakest,
                     "overstated": printed > earned})
        print(f"  {name:38s} {printed:8d} {earned:7d}  {weakest}{flag}")
    bad = [r for r in rows if r["overstated"]]
    print(f"""
  {len(bad)} of {len(rows)} headline figures print more digits than their weakest input earns.

  The cadence case is the instructive one and it is already corrected: "one readout per 15
  instructions" is not a measurement at all, it is a modelling choice, so the power figure
  earns ZERO significant figures as stated and only survives as an order of magnitude.
  Pass 4363 rewrote it as a range.

  The rule this yields: a figure inherits the significant figures of its WEAKEST input, and
  an input that is a modelling choice contributes none. Exact objects -- a group, an
  adjacency matrix, a count -- contribute unlimited digits and are marked None above.""")
    return {"figures": rows, "overstated": len(bad)}


def pass_4372() -> dict:
    print()
    print("=" * 78)
    print("Pass 4372 -- do this session's errors fit CLAUDE.md's five failure modes?")
    print("=" * 78)
    print(f"  the five: {', '.join(FIVE)}\n")
    print(f"  {'error':44s} {'caught by':14s} shape")
    shapes = {}
    for name, _, who, shape in SESSION_ERRORS:
        shapes[shape] = shapes.get(shape, 0) + 1
        print(f"  {name[:44]:44s} {who[:14]:14s} {shape}")
    print(f"\n  {'shape':44s} count")
    for s, n in sorted(shapes.items(), key=lambda t: -t[1]):
        print(f"  {s:44s} {n}")

    self_caught = sum(1 for _, _, w, _ in SESSION_ERRORS if w.startswith("self"))
    print(f"""
  {self_caught} of {len(SESSION_ERRORS)} were caught in this track, {len(SESSION_ERRORS) - self_caught} by the parallel one.

  AGAINST THE FIVE.  "Over-read" covers some of these -- the reversibility claim and the
  'forced' carrier both stated more than their evidence -- but it does not describe the
  mechanism, and the mechanism repeats:

     THREE errors were a PREMISE NEVER TESTED: a comparison run without first checking the
     comparison was licensed. Does the operation act on either carrier? Does the machine
     already have the property being priced? Is the correct run available at runtime?

     TWO were a CHECKER THAT COULD NOT FAIL: a scan reporting zero because its pattern
     could not match the corpus, and a duplicate-detector detecting its own repair.

  Neither is on the list of five, and the second is the more dangerous because a clean
  report from a broken check is indistinguishable from a clean corpus. It is also NOT
  'unbuilt object' -- the checker exists and runs; it is 'built and vacuous'.

  PROPOSED SIXTH AND SEVENTH:
     6. THE UNTESTED PREMISE -- a comparison, ratio or price computed before checking that
        the quantities are comparable. Guard: before writing 'X costs N' or 'A beats B',
        state what would make the comparison invalid and check that first.
     7. THE VACUOUS CHECK -- a checker that has never been shown to catch anything. Guard:
        every check ships with a planted fault it must detect
        (scripts/test_checker_recall.py is the pattern).

  Both guards already exist in this repository as of this session, which is the argument
  for naming the modes: the fixes were built one at a time from individual failures, and
  naming the shape is what makes them reusable rather than incidental.""")
    return {"errors": len(SESSION_ERRORS), "self_caught": self_caught,
            "shapes": shapes,
            "proposed_sixth": "the untested premise",
            "proposed_seventh": "the vacuous check"}


def pass_4373() -> dict:
    print()
    print("=" * 78)
    print("Pass 4373 -- does claim language match the evidence tier?")
    print("=" * 78)
    STRONG = re.compile(r"\b(prove[nds]?|proof|theorem|establishes?|demonstrates?|"
                        r"shows? that|implies|therefore|hence|must be)\b", re.I)
    HEDGE = re.compile(r"\b(suggests?|consistent with|appears?|may|might|conjectur\w+|"
                       r"open|unproved|not established|modelled|exhaust\w+)\b", re.I)
    rows = []
    for f in sorted(ROOT.glob("*.tex")):
        lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
        strong = sum(1 for ln in lines if STRONG.search(ln))
        hedge = sum(1 for ln in lines if HEDGE.search(ln))
        if strong + hedge < 30:
            continue
        rows.append((f.name, strong, hedge, hedge / (strong + hedge)))
    rows.sort(key=lambda r: r[3])
    print(f"  {'manuscript':40s} {'strong':>7s} {'hedged':>7s} {'hedge share':>12s}")
    for n, s, h, r in rows[:10]:
        print(f"  {n[:40]:40s} {s:7d} {h:7d} {100 * r:11.1f}%")
    print(f"""
  This is a crude instrument and should be read as one: it counts words, not claims, and a
  proof legitimately says 'therefore'. What it can show is RELATIVE posture between
  documents that describe the same object at different evidence levels.

  A document making architecture claims should hedge more than one making theorems, because
  the architecture is unbuilt and the theorems are proved. If the ordering above runs the
  other way, the confident language is in the document with less to stand on -- and that is
  checkable without reading 1000 pages.""")
    return {"rows": [{"file": n, "strong": s, "hedged": h, "hedge_share": r}
                     for n, s, h, r in rows]}


def main() -> int:
    out = {"pass_4370_sigfigs": pass_4370(),
           "pass_4372_failure_modes": pass_4372(),
           "pass_4373_claim_language": pass_4373()}
    p = ROOT / "data" / "PART_W33_PASS4370_4373_SIXTH_FAILURE_MODE.json"
    p.parent.mkdir(exist_ok=True)
    # Hash the ROUND-TRIPPED object, never the live dict (CLAUDE.md, Pass 2482).
    p.write_text(json.dumps(json.loads(json.dumps(out)), indent=2, sort_keys=True) + "\n",
                 encoding="utf-8")
    print(f"\nwrote {p.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
