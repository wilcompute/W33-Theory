#!/usr/bin/env python3
"""Pass 4363 -- the femtowatt figure's third factor, which I checked least.

Pass 4354 verified the readout wattage in three parts.  Two were checked properly: the
8/3 bits is the conditional entropy H(frame | support), re-derived rather than cited, and
the arithmetic is arithmetic.  The third -- "one readout per 15 instructions" -- was taken
from Pass 2867's mixing time and never questioned.

Mixing time answers "how long until the register forgets where it started".  That is the
cadence beyond which a readout tells you nothing NEW.  It is not the cadence a program
uses, and the two differ in a direction that matters: a program reading more often pays
more, and the quoted power scales linearly with the rate.

So the honest question is not what the mixing time is but what a realistic cadence is, and
whether the figure survives the plausible range.

    py -3 analysis/w33_pass4363_the_cadence_assumption.py
"""

from __future__ import annotations

import json
from math import log
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
K_B = 1.380649e-23
T_ROOM = 300.0
CLOCK_HZ = 208.86e6
BITS = 8 / 3


def main() -> int:
    print("=" * 78)
    print("Pass 4363 -- does the wattage survive a realistic readout cadence?")
    print("=" * 78)
    kTln2 = K_B * T_ROOM * log(2)
    print(f"  erasure per readout : {BITS:.4f} bits (Pass 4354, re-derived)")
    print(f"  kT ln2 at 300 K     : {kTln2:.4e} J")
    print(f"  clock               : {CLOCK_HZ / 1e6:.2f} MHz\n")
    print(f"  {'cadence':38s} {'rate':>12s} {'power':>12s}")
    rows = []
    for n, label in ((1, "every instruction (worst case)"),
                     (2, "every other instruction"),
                     (15, "the mixing time (Pass 2867)"),
                     (19, "the ISA diameter (Pass 2866)"),
                     (100, "once per hundred"),
                     (1000, "once per thousand")):
        rate = CLOCK_HZ / n
        w = BITS * kTln2 * rate
        rows.append({"instructions_per_readout": n, "label": label,
                     "rate_hz": rate, "watts": w})
        print(f"  {label:38s} {rate / 1e6:9.2f} MHz {w:12.4e} W")

    lo = rows[0]["watts"]
    hi = rows[-1]["watts"]
    print(f"""
  THE FIGURE MOVES BY A FACTOR OF {lo / hi:.0f} ACROSS THE PLAUSIBLE RANGE, from {lo:.2e} W
  if the machine is read every instruction to {hi:.2e} W once per thousand.  The
  quoted {rows[2]['watts']:.2e} W sits in the middle because it uses the mixing time, and the
  mixing time is not a program's cadence -- it is the point beyond which reading again tells
  you nothing new.

  SO THE THIRD FACTOR IS AN ASSUMPTION, not a measurement, and Pass 4354 should have said
  so.  What survives is the ORDER OF MAGNITUDE and the conclusion drawn from it: even the
  worst case, reading every single instruction at full clock, is {lo:.2e} W -- about
  {lo * 1e12:.1f} picowatts, still ten orders of magnitude below the static power of any real
  device.  The argument was never sensitive to the cadence; it only looked more precise
  than it was.

  The corrected sentence: a support readout costs at least {hi:.1e}--{lo:.1e} W depending on
  how often the machine is read, and Landauer is not what limits this design at any cadence
  in that range.""")

    out = {

        "boundary": ("the readout cadence is an ASSUMPTION with a 1000x plausible span, not a "

            "measurement; every wattage figure downstream inherits that span and no figure "

            "here should be quoted to more than an order of magnitude"),"bits_per_readout": BITS, "kT_ln2": kTln2, "clock_hz": CLOCK_HZ,
           "rows": rows, "span_factor": lo / hi,
           "quoted_figure_watts": rows[2]["watts"],
           "cadence_is_an_assumption": True,
           "conclusion_robust": True,
           "why": "even the worst-case cadence is ten orders of magnitude below device "
                  "static power, so the argument never depended on the cadence"}
    p = ROOT / "data" / "PART_W33_PASS4363_CADENCE.json"
    p.parent.mkdir(exist_ok=True)
    # Hash the ROUND-TRIPPED object, never the live dict (CLAUDE.md, Pass 2482).
    p.write_text(json.dumps(json.loads(json.dumps(out)), indent=2, sort_keys=True) + "\n",
                 encoding="utf-8")
    print(f"\nwrote {p.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
