#!/usr/bin/env python3
"""Guard: warn when a sampling-based claim may rest on a degenerate sample.

This failure mode bit twice in one session, in opposite directions:

  * Pass 1010 "proved" rank <= #collision-classes on 6,703 of 6,703 samples.
    Every sample had n = k, i.e. all eigenvalue multiplicities 1, and for such an
    operator each branch operator has rational rank 1, which makes the bound
    automatic. The claim was a restatement of the sampling design, and W(3,3) --
    one collision class, rank 10 -- refuted it (Pass 1011).
  * The first attempt to break that bound built upper-triangular matrices with
    repeated diagonal entries and found 97% violations. Those matrices are
    DEFECTIVE: geometric multiplicities below algebraic ones, minimal polynomial
    not squarefree. The k-branch theory assumes a diagonalisable operator, so the
    violations refuted nothing.

Both are the same mistake: the sample was special with respect to the hypothesis
being tested, in a way that guaranteed the answer.

This guard greps a pass for the two constructions and, when it also claims a
bound or a general result, prints the caution. It WARNS, never blocks -- a
multiplicity-1 sample is perfectly legitimate when the claim is scoped to it.

Usage:  py -3 scripts/check_sample_degeneracy.py [files...]
        py -3 scripts/check_sample_degeneracy.py --staged
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MULT_ONE = re.compile(r"^\s*n\s*=\s*k\s*$|\bn\s*=\s*k\b(?!\w)", re.M)
UPPER_TRI = re.compile(r"for j in range\(\s*i\s*\+\s*1\s*,\s*n\s*\)", re.M)
REPEATED = re.compile(r"\[\s*c\s*\]\s*\*\s*m|mult\s*=\s*\[random", re.M)
GENERAL = re.compile(
    r"\b(never exceeds|always|bound|for every|for all|in every case|holds in "
    r"every|theorem)\b", re.I)
SCOPED = re.compile(
    r"(multiplicity[- ]one|multiplicities? (are |of )?1\b|diagonalis|"
    r"diagonaliz|defective|not proved|evidence, not)", re.I)


def scan(path: Path):
    try:
        s = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return []
    out = []
    general = bool(GENERAL.search(s))
    scoped = bool(SCOPED.search(s))
    # deliberately NOT suppressed by hedging: Pass 1010 hedged in its
    # boundary and still overstated in its headline, so the structural
    # risk is reported whenever the two co-occur.
    if MULT_ONE.search(s) and general:
        out.append((path.name, "multiplicity-one sample",
                    "the sample uses n = k, so every eigenvalue multiplicity is "
                    "1 and each branch operator has rational rank 1. Bounds of "
                    "the form rank <= (number of classes) are then automatic. "
                    "Scope the claim or sample with multiplicities > 1."))
    if UPPER_TRI.search(s) and REPEATED.search(s) and not scoped:
        out.append((path.name, "possibly defective sample",
                    "upper-triangular matrices with repeated diagonal entries "
                    "are generally NOT diagonalisable, so they violate the "
                    "k-branch hypothesis. Check prod_i (A - c_i I) == 0 before "
                    "drawing conclusions, or build symmetric matrices."))
    return out


def _staged():
    try:
        res = subprocess.run(["git", "diff", "--cached", "--name-only",
                              "--diff-filter=ACM"], cwd=ROOT,
                             capture_output=True, text=True, timeout=120).stdout
    except Exception:
        return []
    return [ROOT / ln for ln in res.splitlines() if ln.endswith(".py")]


def main(argv):
    args = [a for a in argv[1:] if a != "--staged"]
    targets = _staged() if "--staged" in argv[1:] else [Path(a) for a in args]
    findings = []
    for p in targets:
        if p.exists() and p.is_file():
            findings.extend(scan(p))
    print(f"[sample-degeneracy] files scanned: {len(targets)}; "
          f"cautions: {len(findings)}")
    for name, kind, why in findings:
        print(f"  {name} [{kind}]")
        print(f"    {why}")
    if findings:
        print()
        print("  A sample that is special with respect to the hypothesis can")
        print("  guarantee the answer. Pass 1010/1011 lost a theorem to exactly")
        print("  this, in both directions, within one session.")
    return 0  # advisory


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
