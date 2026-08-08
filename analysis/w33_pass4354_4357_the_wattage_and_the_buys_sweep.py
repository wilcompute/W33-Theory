#!/usr/bin/env python3
"""Passes 4354, 4357 -- re-examine the wattage, then look for the same error shape.

Pass 4353 found that "thermodynamic reversibility costs 2.00x the cells" was an over-read:
every machine computes at zero Landauer cost already, and what the closure buys is
time-symmetry of the RANDOM-INSTRUCTION walk, not a reduction in dissipation.

Pass 4337 produced a wattage from the same Landauer framing.  If the framing was wrong for
the reversibility claim it may be wrong here, and the honest move is to apply the same
scrutiny to my own number rather than wait for someone else to.

  4354  IS THE 107 FEMTOWATT FIGURE SOUND?  It prices readout at 8/3 bits x kT ln2 x clock.
        Check each factor: is 8/3 bits actually ERASED, is the clock the right rate, and is
        the resulting number describing anything a device would do?
  4357  THE "X BUYS Y" SWEEP.  The reversibility error had a shape -- a cost priced against
        a property nobody verified the purchase delivers.  Sweep the manuscripts for cost
        claims and check each names what is bought AND that the thing bought was measured.

    py -3 analysis/w33_pass4354_4357_the_wattage_and_the_buys_sweep.py
"""

from __future__ import annotations

import json
import re
from math import log
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
ID4 = tuple(tuple(1 if i == j else 0 for j in range(4)) for i in range(4))
TV = [(a, b, c, d) for a in range(3) for b in range(3)
      for c in range(3) for d in range(3)]
K_B = 1.380649e-23
CLOCK_HZ = 208.86e6
T_ROOM = 300.0


def mv(A, v):
    return tuple(sum(A[i][k] * v[k] for k in range(4)) % 3 for i in range(4))


def pass_4354() -> dict:
    print("=" * 78)
    print("Pass 4354 -- is the 107 femtowatt readout figure sound?")
    print("=" * 78)
    kTln2 = K_B * T_ROOM * log(2)
    print("  The figure was: 8/3 bits x kT ln2 x clock / 15, giving ~1.07e-13 W.")
    print("  Three factors, checked one at a time.\n")

    # FACTOR 1: is 8/3 bits actually erased?
    # A support readout reports which coordinates are non-zero.  That is a function of the
    # frame, so the map frame -> support is NOT injective: the information lost is the
    # conditional entropy of the frame given its support.
    supp = {}
    for x in TV:
        s = tuple(1 if c else 0 for c in x)
        supp.setdefault(s, []).append(x)
    n = len(TV)
    H_cond = 0.0
    for s, xs in supp.items():
        p = len(xs) / n
        H_cond += p * (log(len(xs), 2) if len(xs) > 1 else 0.0)
    print(f"  FACTOR 1 -- what a support readout discards")
    print(f"    distinct support patterns          : {len(supp)}")
    print(f"    H(frame | support), in bits        : {H_cond:.6f}")
    print(f"    the quoted 8/3                     : {8 / 3:.6f}")
    print(f"    agree: {abs(H_cond - 8 / 3) < 1e-9}")
    print(f"""
    So 8/3 IS the conditional entropy discarded by a support-only observation, and that is
    a genuine erasure: the readout keeps the support and forgets which of the {max(len(v) for v in supp.values())} frames
    sharing it you had.  Unlike the compute claim of Pass 4353, this one survives -- the
    map is not injective, so information really is destroyed.""")

    # FACTOR 2: the rate.
    print(f"\n  FACTOR 2 -- the rate")
    print(f"    the clock is {CLOCK_HZ / 1e6:.2f} MHz, but readouts do not happen every cycle.")
    print(f"    Pass 2867's mixing time says one readout per 15 instructions is the")
    print(f"    fastest cadence that is not wasteful, so the rate is clock/15 = "
          f"{CLOCK_HZ / 15 / 1e6:.2f} MHz.")
    w = (8 / 3) * kTln2 * CLOCK_HZ / 15
    print(f"    {8 / 3:.4f} bits x {kTln2:.4e} J x {CLOCK_HZ / 15:.4e} Hz = {w:.4e} W")

    # FACTOR 3: what does the number describe?
    print(f"""
  FACTOR 3 -- what the number describes, and this is where the caution belongs.
    {w:.3e} W is the LANDAUER FLOOR for the erasure a support readout performs at that
    cadence.  It is a lower bound on the heat any physical implementation must dump, not an
    estimate of what one would dump.  Real detectors dissipate many orders of magnitude
    more, so the figure cannot be used to size a power budget.

  THE VERDICT DIFFERS FROM PASS 4353's, and the difference is the point.  The reversibility
  claim failed because the thing being priced -- erasure during compute -- does not happen
  at all.  This claim survives because the erasure DOES happen and is exactly quantified:
  a support readout is a non-injective map, {H_cond:.4f} bits go, and Landauer applies.

  What both share is a scope requirement.  The correct sentence is "a support readout costs
  at least {w:.2e} W at this cadence", never "the machine consumes {w:.2e} W".""")
    return {"kT_ln2": kTln2, "conditional_entropy_bits": H_cond,
            "matches_8_over_3": bool(abs(H_cond - 8 / 3) < 1e-9),
            "readout_watts_floor": w, "is_a_floor_not_an_estimate": True,
            "survives_scrutiny": True,
            "differs_from_4353_because": "the erasure is real; the map frame->support is "
                                         "not injective"}


def pass_4357() -> dict:
    print()
    print("=" * 78)
    print("Pass 4357 -- the 'X buys Y' sweep: cost claims whose Y was never measured")
    print("=" * 78)
    print("""  The Pass 4353 error had a shape: a cost priced against a property nobody had
  checked the purchase delivers.  "Reversibility costs 2.00x" -- but the machine was
  already reversible in the sense implied, so the 2.00x bought something else.

  Look for the shape: a sentence pairing a price with a benefit.\n""")
    COST = re.compile(r"\b(costs?|prices?d?|buys?|pays?|worth)\b", re.I)
    NUM = re.compile(r"\d")
    # A benefit is verified if the passage names a measurement, a pass, or a certificate.
    EVIDENCE = ("measured", "pass ", "verified", "certificate", "synthesis", "simulated",
                "proved", "exact", "computed", "\\S\\ref", "table")
    rows = []
    for f in sorted(ROOT.glob("*.tex")):
        lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
        for i, ln in enumerate(lines):
            if not COST.search(ln) or not NUM.search(ln):
                continue
            w = " ".join(lines[max(0, i - 4):i + 5]).lower()
            backed = any(e in w for e in EVIDENCE)
            rows.append((f.name, i + 1, backed, ln.strip()[:66]))
    unbacked = [r for r in rows if not r[2]]
    print(f"  cost/benefit sentences found : {len(rows)}")
    print(f"  with nearby evidence         : {len(rows) - len(unbacked)}")
    print(f"  WITHOUT                      : {len(unbacked)}")
    for f, ln, _, txt in unbacked[:12]:
        print(f"    {f[:34]:34s} {ln:6d}  {txt}")
    print(f"""
  {len(unbacked)} sentence(s) pair a number with a cost or benefit and name no measurement
  nearby.  This is a triage list and the classifier is loose -- "costs" appears in ordinary
  prose -- but the shape it looks for is the one that produced a published error, and a
  cost claim with no evidence within four lines is where that error hides.

  The general rule worth extracting, since this is the second sweep built from one mistake:
  before writing "X costs N", check that X is a thing the machine does not already have.
  The reversibility claim failed that test and the readout wattage of Pass 4354 passes it.""")
    return {"claims": len(rows), "unbacked": len(unbacked),
            "sample": [{"file": f, "line": ln, "text": t} for f, ln, _, t in unbacked[:20]]}


def main() -> int:
    out = {"pass_4354_wattage": pass_4354(), "pass_4357_buys_sweep": pass_4357()}
    p = ROOT / "data" / "PART_W33_PASS4354_4357_WATTAGE_AND_BUYS.json"
    p.parent.mkdir(exist_ok=True)
    # Hash the ROUND-TRIPPED object, never the live dict (CLAUDE.md, Pass 2482).
    p.write_text(json.dumps(json.loads(json.dumps(out)), indent=2, sort_keys=True) + "\n",
                 encoding="utf-8")
    print(f"\nwrote {p.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
