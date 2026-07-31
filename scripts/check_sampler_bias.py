#!/usr/bin/env python3
"""Flag files that generalise from a DETERMINISTIC enumeration order.

WHY THIS EXISTS (measured, Pass 1428).  Pass 1411 concluded that the stabilisers
of exact covers are "diagonal" -- that none fixes a frame.  The evidence was six
covers.  All six came from ONE depth-first search, and a DFS visits solutions in
an order determined by the problem encoding, not by any notion of typicality.
Re-running the same search across twelve RANDOMISED orders immediately produced
`C2`-stabilised covers fixing twelve frames each, refuting the conclusion:

    one DFS order      C4, C2xC2, C4xC2        0 fixed frames    (6 covers)
    randomised orders  + C2                   12 fixed frames    (24 covers)

The mathematics was right and the sampling was wrong, which is the harder failure
to notice: every individual computation checked out.

WHAT IT FLAGS.  Files that (a) enumerate solutions, (b) truncate to the first few,
and (c) never randomise.  That is a CANDIDATE pattern, not a defect -- plenty of
files truncate only for display, and plenty enumerate exhaustively so order is
irrelevant.  The measured population over analysis/ and scripts/ is ~152 files,
far too many to be all wrong; the point is to make the question askable at the
moment someone writes "sampled ... therefore".

The sharpest sub-signal is (d): a generalising word near the truncation.

Run:  py -3 scripts/check_sampler_bias.py [files...]   (default: analysis/, scripts/)
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

RE_ENUM = re.compile(
    r"\bdef solve\b|\bbacktrack\b|exact.?cover|Algorithm X|dancing links"
    r"|itertools\.(?:permutations|combinations)\b", re.I)
RE_TRUNC = re.compile(r"\[:\s*\d+\]|len\(\w+\)\s*>=\s*\d+|\bbreak\b", re.I)
RE_RAND = re.compile(r"\brandom\.|\bshuffle\b|\bseed\b|\brng\b", re.I)
# the tell that a truncated sample is being turned into a general statement
RE_GENERALISE = re.compile(
    r"(?i)\b(sampled|every|all |always|never|uniformly|in general|therefore"
    r"|so a |conclude)\b")

# WHAT KIND OF CONCLUSION IS BEING DRAWN (refined, Pass 1431, by reading the
# flagged files instead of trusting the flag).
#
# The heuristic flagged `w33_pass1417_exact_cover_orbit_frontier.py`, the
# parallel track's own cover census. Reading it: its enumeration IS
# order-deterministic, but it computes the full PSp(4,3)-orbit of each of its
# sixteen covers and PROVES they are pairwise distinct, then sums orbit sizes
# for a LOWER BOUND. That is valid no matter how the sixteen were found -- an
# exhibited object stays exhibited.
#
# My Pass 1411 did the opposite: it took a sample and asserted a UNIVERSAL
# property ("cover stabilisers are diagonal"). Same flag, opposite verdicts.
#
# So the flag only bites when the conclusion quantifies over everything. A file
# whose claim is a bound, an existence statement, or an exhibited orbit census
# is downgraded.
RE_BOUND_CLAIM = re.compile(
    r"(?i)\b(at least|lower bound|there exist|exhibit|distinct .*orbits"
    r"|orbit size|G_orbit|>=)\b")


def scan(paths: list[Path]) -> list[tuple[Path, bool]]:
    out = []
    for p in paths:
        try:
            t = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if RE_ENUM.search(t) and RE_TRUNC.search(t) and not RE_RAND.search(t):
            generalises = bool(RE_GENERALISE.search(t))
            # a bound / existence claim survives a biased sample; a universal
            # claim does not
            if RE_BOUND_CLAIM.search(t):
                generalises = False
            out.append((p, generalises))
    return out


def main(argv: list[str]) -> int:
    if argv:
        paths = [Path(a) for a in argv if Path(a).suffix == ".py"]
    else:
        paths = sorted(list((ROOT / "analysis").glob("*.py"))
                       + list((ROOT / "scripts").glob("*.py")))
    hits = scan(paths)
    strong = [p for p, g in hits if g]
    print("=" * 74)
    print("[sampler bias] enumerate + truncate + no randomisation")
    print("=" * 74)
    print(f"scanned {len(paths)} files")
    print(f"  deterministic-order samplers      : {len(hits)}")
    print(f"  ...claiming something UNIVERSAL   : {len(strong)}   <- read these")
    print(f"  (bound/existence claims are excluded: a lower bound from exhibited")
    print(f"   objects survives a biased sample; a universal property does not)")
    for p in strong[:30]:
        print(f"    {p.relative_to(ROOT)}")
    print("\n  CANDIDATES, not defects. Truncating for display is fine; so is an")
    print("  exhaustive search, where order cannot matter. What is NOT fine is")
    print("  'the sampled X all have property P, therefore X has property P'")
    print("  when the sample came from one search order. Randomise, then claim.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
